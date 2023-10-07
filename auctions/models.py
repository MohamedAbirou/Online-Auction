from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_listings')
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bid on {self.listing.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.listing.title}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    watchlist = models.ManyToManyField(Listing, blank=True)

    def __str__(self):
        return self.user.username