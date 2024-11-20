from django.db import models

from catalogue.models import Product


class Comment(models.Model):
    RATING_CHOICES = (
        (1, "Bad"),
        (2, "Not Bad"),
        (3, "OK"),
        (4, "Good"),
        (5, "Very Good")
    )
    title = models.CharField(max_length=48)
    description = models.TextField(blank=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    is_recommended = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=5)

    def __str__(self):
        return self.title
