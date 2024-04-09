from .models import Product, Category
from rest_framework import serializers
from .models import Review


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, min_length=2)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    category_id = serializers.IntegerField()


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, min_length=3)


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=300)
    product_id = serializers.IntegerField()
    stars = serializers.FloatField()
