from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.models import Product, Category, Review
from .serializers import (ProductSerializer, CategorySerializer, ReviewSerializer,
                          ProductValidateSerializer, CategoryValidateSerializer, ReviewValidateSerializer)
from rest_framework import status
from django.db.models import Avg
from django.http import HttpRequest


@api_view(['GET', 'POST'])
def products_list_api_view(request):
    if request.method == 'GET':
        products_list = Product.objects.all()
        data = ProductSerializer(products_list, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')
        product = Product.objects.create(title=title, description=description,
                                         price=price, category_id=category_id)
        return Response(status=status.HTTP_201_CREATED, data={'product_id': product.id})


@api_view(['GET'])
def products_reviews_api_view(request: HttpRequest):
    products_list = Product.objects.all()
    data = []
    for product in products_list:
        reviews = Review.objects.filter(product=product).values('text', 'stars')
        average_rating = reviews.aggregate(Avg('stars'))['stars__avg']
        if average_rating is not None:
            average_rating = round(average_rating, 1)
        serialized_product = ProductSerializer(product).data
        serialized_product['average_rating'] = average_rating
        serialized_product['reviews'] = list(reviews)
        data.append(serialized_product)

    return Response(data=data)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product_detail = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error_message': 'Product does not'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductSerializer(product_detail).data
        return Response(data=data)
    elif request.method == 'PUT':
        product_detail.title = request.data.get('title')
        product_detail.description = request.data.get('description')
        product_detail.price = request.data.get('price')
        product_detail.category_id = request.data.get('category_id')
        product_detail.save()
        return Response(status=status.HTTP_201_CREATED, data={'product_id': product_detail.id})
    else:
        product_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def categories_list_api_view(request):
    if request.method == 'GET':
        categories_list = Category.objects.all()
        data = []
        for category in categories_list:
            category_data = CategorySerializer(category).data
            category_data['products_count'] = category.product_set.count()
            data.append(category_data)
        return Response(data=data)
    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})
        name = request.data.get('name')
        category = Category.objects.create(name=name)
        return Response(status=status.HTTP_201_CREATED, data={'category_id': category.id})


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category_detail = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error_message': 'Category does not'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategorySerializer(category_detail).data
        return Response(data=data)
    elif request.method == 'PUT':
        category_detail.name = request.data.get('name')
        category_detail.save()
        return Response(status=status.HTTP_201_CREATED, data={'category_id': category_detail.id})
    else:
        category_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def reviews_list_api_view(request):
    if request.method == 'GET':
        reviews_list = Review.objects.all()
        data = ReviewSerializer(reviews_list, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})
        text = request.data.get('text')
        product_id = request.data.get('product_id')
        stars = request.data.get('stars')
        review = Review(text=text, product_id=product_id, stars=stars)
        review.save()
        return Response(status=status.HTTP_201_CREATED, data={'review_id': review.id})


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review_detail = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error_message': 'Review does not'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(review_detail).data
        return Response(data=data)
    elif request.method == 'PUT':
        review_detail.text = request.data.get('text')
        review_detail.product_id = request.data.get('product_id')
        review_detail.stars = request.data.get('stars')
        review_detail.save()
        return Response(status=status.HTTP_201_CREATED, data={'review_id': review_detail.id})
    else:
        review_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
