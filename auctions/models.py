from email.policy import default
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, default= 0)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="Lister", null=True)
    description = models.TextField(default="")
    image = models.URLField(blank=True, default="https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="1", blank=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    current_bid = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="Winner", null=True)


    def __str__(self):
        return f"{self.title} for {self.price}$"

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT, null=True)
    bid = models.DecimalField(max_digits=6, decimal_places=2)


class Comments(models.Model):
    pass

