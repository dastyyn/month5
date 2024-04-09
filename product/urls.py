from django.contrib import admin
from django.urls import path
from product import views

urlpatterns = [
    path('', views.ProductsListAPIView.as_view()),
    path('reviews/', views.ProductsReviewsAPIView.as_view()),
    path('<int:id>/', views.ProductDetailAPIView.as_view()),

    path('categories/', views.CategoriesListAPIView.as_view()),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view()),

    path('reviews_list/', views.ReviewsListAPIView.as_view()),
    path('reviews/<int:id>/', views.ReviewDetailAPIView.as_view()),
]
