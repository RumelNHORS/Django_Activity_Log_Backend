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
    product_name = serializers.SerializerMethodField()
    product_owner = serializers.SerializerMethodField()

    class Meta:
        model = ActivityLog
        fields = '__all__'

    def get_product_name(self, obj):
        """Extract product name from the changes field."""
        if obj.model_name == "Product":
            return obj.changes.get('fields', {}).get('name', None)
        return None

    def get_product_owner(self, obj):
        """Fetch product owner if model is Product"""
        if obj.model_name == "Product":
            product_id = obj.changes.get('fields', {}).get('id')
            if product_id:
                try:
                    product = Product.objects.get(id=product_id)
                    return product.user.username
                except Product.DoesNotExist:
                    return None
        return None

