from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.models import Product, Category, Review
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from rest_framework import status


@api_view(['GET'])
def products_list_api_view(request):
    products_list = Product.objects.all()
    data = ProductSerializer(products_list, many=True).data
    return Response(data=data)


@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product_detail = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error_message': 'Product does not'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ProductSerializer(product_detail).data
    return Response(data=data)


@api_view(['GET'])
def categories_list_api_view(request):
    categories_list = Category.objects.all()
    data = CategorySerializer(categories_list, many=True).data
    return Response(data=data)


@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category_detail = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error_message': 'Category does not'},
                        status=status.HTTP_404_NOT_FOUND)
    data = CategorySerializer(category_detail).data
    return Response(data=data)


@api_view(['GET'])
def reviews_list_api_view(request):
    reviews_list = Review.objects.all()
    data = ReviewSerializer(reviews_list, many=True).data
    return Response(data=data)


@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review_detail = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error_message': 'Review does not'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ReviewSerializer(review_detail).data
    return Response(data=data)
