from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views

# router = DefaultRouter()
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('comments', views.CommentViewSet, basename='product-comment')

urlpatterns = router.urls + products_router.urls
