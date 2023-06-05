from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# from utils.model_abstracts import Model
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    TitleSlugDescriptionModel
)


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    ucurrency = models.CharField(max_length=50, null=False, blank=False, default='GBP')
    balance = models.FloatField(default=50000.00, blank=True)

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
    c = models.FloatField(null=True, blank=True, default=100.0)
    h = models.FloatField(null=True, blank=True, default=100.0)
    l = models.FloatField(null=True, blank=True, default=100.0)
    d = models.FloatField(null=True, blank=True, default=1.0)
    

    def __str__(self):
        return self.ticker

    def manage_stock(self, qty):
        #used to reduce Share stock
        self.no_of_shares = self.no_of_shares - int(qty)
        # self.stock = new_stock
        self.save()


    def check_stock(self, qty):
        #used to check if order quantity exceeds stock levels
        if int(qty) > self.no_of_shares:
            return False
        return True

    def place_order(self, share, user, qty):
        #used to place an order
        if self.check_stock(qty):
            order = Order.objects.create(
                item=self, 
                quantity=qty, 
                user=user)
            self.manage_stock(qty)
            return order
        else:
            return None

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
