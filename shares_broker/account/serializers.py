from collections import OrderedDict
from rest_framework_json_api import serializers
from rest_framework import status
from rest_framework.exceptions import APIException

from .models import Profile, Shares, Order, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), many=False)
    class Meta:
        model = Profile
        fields = (
            'user',
            'ucurrency',
            'balance',
        )


class SharesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shares
        fields = (
            'name',
            'ticker',
            'logo',
            'currency',
            'no_of_shares',
            'c',
            'h',
            'l',
            'd',
        )


class OrderSerializer(serializers.ModelSerializer):

    customer = serializers.PrimaryKeyRelatedField(queryset = Profile.objects.all(), many=False)
    shares = serializers.PrimaryKeyRelatedField(queryset = Shares.objects.all(), many=False)
    
    class Meta:
        model = Order
        fields = (
            'customer',
            'shares',
            'price',
            'quantity',
            'date_order',
        )

    def validate(self, res: OrderedDict):
        '''
        Used to validate Share stock levels
        '''
        item = res.get("share")
        quantity = res.get("quantity")
        # if not item.check_stock(quantity):
        #     raise NotEnoughStockException
        # return res