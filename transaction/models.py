from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce


class Transaction(models.Model):
    CHARGE = 1
    PURCHASE = 2
    TRANSFER_RECEIVER = 3
    TRANSFER_SENDER = 4

    TRANSACTION_TYPE_CHOICES = (
        (CHARGE, "Charge"),
        (PURCHASE, "Purchase"),
        (TRANSFER_RECEIVER, "Transfer receiver"),
        (TRANSFER_SENDER, "Transfer sender")
    )

    user = models.ForeignKey(User, related_name="transactions", on_delete=models.RESTRICT)
    transaction_type = models.SmallIntegerField(choices=TRANSACTION_TYPE_CHOICES, default=CHARGE)
    amount = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.get_transaction_type_display()} - {self.amount}"

    @classmethod
    def get_report(cls):
        positive_transactions = Sum(
            "transactions__amount",
            filter=Q(transactions__transaction_type__in=[cls.CHARGE, cls.TRANSFER_RECEIVER]))

        negative_transactions = Sum(
            "transactions__amount",
            filter=Q(transactions__transaction_type__in=[cls.PURCHASE, cls.TRANSFER_SENDER])
        )

        users = User.objects.annotate(
            transactions_count=Count("transactions__id"),
            balance=Coalesce(positive_transactions, 0) - Coalesce(negative_transactions, 0)
        )
        return users

    @classmethod
    def total_balance(cls, user):
        query_set = cls.get_report()
        return query_set.aggregate(Sum("balance"))

    @classmethod
    def user_balance(cls, user):
        positive_transactions = Sum(
            "amount",
            filter=Q(transaction_type__in=[Transaction.CHARGE, Transaction.TRANSFER_RECEIVER]))
        negative_transactions = Sum(
            "amount",
            filter=Q(transaction_type__in=[Transaction.PURCHASE, Transaction.TRANSFER_SENDER])
        )

        user_balance = user.transactions.all().aggregate(
            balance=Coalesce(positive_transactions, 0) - Coalesce(negative_transactions, 0)
        )
        return user_balance.get("balance", 0)


class UserBalance(models.Model):
    user = models.ForeignKey(User, related_name="balance_record", on_delete=models.RESTRICT)
    balance = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.balance}"

    @classmethod
    def user_balance_recorder(cls, user):
        user_balance = Transaction.balance(user=user)
        instance = cls.objects.create(user=user, balance=user_balance)
        return instance

    @classmethod
    def all_users_balance_recorder(cls):
        for user in User.objects.all():
            cls.user_balance_recorder(user=user)


class TransferTransaction(models.Model):
    sent_transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT, related_name="sent_transfer")
    received_transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT, related_name="received_archive")
    created_time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def transfer(cls, sender, receiver, amount):
        if Transaction.user_balance(sender) < amount:
            return "Transaction not Allowed, Insufficient balance"

        with transaction.atomic():
            sender_transaction = Transaction.objects.create(
                user=sender, transaction_type=Transaction.TRANSFER_SENDER, amount=amount
            )
            receiver_transaction = Transaction.objects.create(
                user=receiver, transaction_type=Transaction.TRANSFER_RECEIVER, amount=amount
            )
            instance = cls.objects.create(
                sent_transaction=sender_transaction,
                received_transaction=receiver_transaction
            )
        return instance


class UserScore(models.Model):
    score = models.PositiveSmallIntegerField(default=0)

    class Meta:
        permissions = [
            ("has_score_permission", "Has Score Permission")
        ]


class TransactionArchive(models.Model):
    pass
