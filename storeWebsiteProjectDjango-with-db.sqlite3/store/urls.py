from django.urls import path

from . import views


urlpatterns = [
    # path('products/', views.product_list, name='product-list'),
    path('products/', views.ProductList.as_view(), name='product-list'),
    # path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    # path('categories/', views.category_list, name='category-list'),
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    # path('categories/<int:pk>/', views.category_detail, name='category-detail'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
]
