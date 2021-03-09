from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    image = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True, related_name="category")
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    price = models.IntegerField()
    closeChecker = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ManyToManyField(User, blank=True, related_name="watched_list")

class Bids(models.Model):
    listingId = models.IntegerField()
    amount = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
