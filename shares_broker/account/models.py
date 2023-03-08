from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    balance = models.FloatField(default=1000.00, blank=True)

    #this method to generate profile when user is created
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    #this method to update profile when user is updated
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return  self.user.username


class Shares(models.Model):
    name = models.CharField(max_length=100, null=True)
    ticker = models.CharField(max_length=50, null=True)
    logo = models.CharField(max_length=250, null=True, blank=True)
    currency = models.CharField(max_length=50, null=True, blank=True)
    no_of_shares = models.IntegerField(default=100, blank=True)
    # price = models.DecimalField(max_digits=7, decimal_places=2, default=1.0)
    # image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.ticker

class Order(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    shares = models.ForeignKey(Shares, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    price = models.FloatField(default=1.0)
    date_order = models.DateTimeField(auto_now_add=True)
    # complete = models.BooleanField(default=False, null=True, blank=False)
    # transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total = self.price * self.quantity
        return total

# class OrderItem(models.Model):
#     shares = models.ForeignKey(Shares, on_delete=models.SET_NULL, null=True, blank=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
#     quantity = models.IntegerField(default=0, null=True, blank=True)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.shares.ticker

#     @property
#     def get_total(self):
#         total = self.shares.price * self.quantity
#         return total