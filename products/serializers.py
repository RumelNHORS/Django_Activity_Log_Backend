from rest_framework import serializers
from .models import Product, ActivityLog
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        

class ActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField() 
    product = serializers.StringRelatedField()
    product_owner = serializers.CharField(source='product.user.username', read_only=True)


    class Meta:
        model = ActivityLog
        fields = '__all__'
