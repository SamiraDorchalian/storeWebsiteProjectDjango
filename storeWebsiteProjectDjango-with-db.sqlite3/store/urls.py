from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

from . import views

# router = SimpleRouter()
# router = DefaultRouter()
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('comments', views.CommentViewSet, basename='product-comments')

urlpatterns = router.urls + products_router.urls

# urlpatterns = [
#     path('', include(router.urls))
# ]

# urlpatterns = [
#     # path('products/', views.product_list, name='product-list'),
#     path('products/', views.ProductList.as_view(), name='product-list'),
#     # path('products/<int:pk>/', views.product_detail, name='product-detail'),
#     path('products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
#     # path('categories/', views.category_list, name='category-list'),
#     path('categories/', views.CategoryList.as_view(), name='category-list'),
#     # path('categories/<int:pk>/', views.category_detail, name='category-detail'),
#     path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
# ]
