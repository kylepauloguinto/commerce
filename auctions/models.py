from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watchlist = models.ManyToManyField(
        "Listing", blank=True, related_name="user_watch"
    )

class Category(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    image = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    price = models.IntegerField()
    closeChecker = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.id}"

class Bids(models.Model):
    listingId = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingId")
    amount = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    date = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['-amount']

class Comments(models.Model):
    commentListingId = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commentListingId")
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentUser")
    commentTitle = models.CharField(max_length=64)
    commentDescription = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['-date']