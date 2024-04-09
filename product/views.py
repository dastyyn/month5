from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from product.models import Product, Category, Review
from .serializers import (ProductSerializer, CategorySerializer, ReviewSerializer,
                          ProductValidateSerializer, CategoryValidateSerializer, ReviewValidateSerializer)


class ProductsListAPIView(APIView):
    def get(self, request):
        products_list = Product.objects.all()
        data = ProductSerializer(products_list, many=True).data
        return Response(data=data)

    def post(self, request):
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})

        product = serializer.save()
        return Response(status=status.HTTP_201_CREATED, data={'product_id': product.id})


class ProductsReviewsAPIView(APIView):
    def get(self, request):
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


class ProductDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return None

    def get(self, request, id):
        product_detail = self.get_object(id)
        if not product_detail:
            return Response(data={'error_message': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)

        data = ProductSerializer(product_detail).data
        return Response(data=data)

    def put(self, request, id):
        product_detail = self.get_object(id)
        if not product_detail:
            return Response(data={'error_message': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductValidateSerializer(product_detail, data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})

        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data={'product_id': product_detail.id})

    def delete(self, request, id):
        product_detail = self.get_object(id)
        if not product_detail:
            return Response(data={'error_message': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)

        product_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoriesListAPIView(APIView):
    def get(self, request):
        categories_list = Category.objects.all()
        data = []
        for category in categories_list:
            category_data = CategorySerializer(category).data
            category_data['products_count'] = category.product_set.count()
            data.append(category_data)
        return Response(data=data)

    def post(self, request):
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})

        category = serializer.save()
        return Response(status=status.HTTP_201_CREATED, data={'category_id': category.id})


class CategoryDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            return None

    def get(self, request, id):
        category_detail = self.get_object(id)
        if not category_detail:
            return Response(data={'error_message': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)

        data = CategorySerializer(category_detail).data
        return Response(data=data)

    def put(self, request, id):
        category_detail = self.get_object(id)
        if not category_detail:
            return Response(data={'error_message': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoryValidateSerializer(category_detail, data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})

        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data={'category_id': category_detail.id})

    def delete(self, request, id):
        category_detail = self.get_object(id)
        if not category_detail:
            return Response(data={'error_message': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)

        category_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewsListAPIView(APIView):
    def get(self, request):
        reviews_list = Review.objects.all()
        data = ReviewSerializer(reviews_list, many=True).data
        return Response(data=data)

    def post(self, request):
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})

        review = serializer.save()
        return Response(status=status.HTTP_201_CREATED, data={'review_id': review.id})


class ReviewDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Review.objects.get(id=id)
        except Review.DoesNotExist:
            return None

    def get(self, request, id):
        review_detail = self.get_object(id)
        if not review_detail:
            return Response(data={'error_message': 'Review does not exist'}, status=status.HTTP_404_NOT_FOUND)

        data = ReviewSerializer(review_detail).data
        return Response(data=data)

    def put(self, request, id):
        review_detail = self.get_object(id)
        if not review_detail:
            return Response(data={'error_message': 'Review does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewValidateSerializer(review_detail, data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})

        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data={'review_id': review_detail.id})

    def delete(self, request, id):
        review_detail = self.get_object(id)
        if not review_detail:
            return Response(data={'error_message': 'Review does not exist'}, status=status.HTTP_404_NOT_FOUND)

        review_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
