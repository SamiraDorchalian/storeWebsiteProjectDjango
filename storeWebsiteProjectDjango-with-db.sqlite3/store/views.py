from itertools import count
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Category, Product
from .serializers import ProductSerializer, CategorySerializer

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').all()
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, pk):
        product = get_object_or_404(
            Product.objects.select_related('category'), 
            pk=pk,
        )
        if product.order_items.count() > 0:
            return Response({'error': 'There is some order including this product. Please remove them first.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductList(ListCreateAPIView):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.select_related('category').all()
    
#     def get_serializer_context(self):
#         return {'request': self.request}

# class ProductList(ListCreateAPIView):
#     def get_serializer_class(self):
#         return ProductSerializer
    
#     def get_queryset(self):
#         return Product.objects.select_related('category').all()
    
#     def get_serializer_context(self):
#         return {'request': self.request}

# class ProductList(APIView):
#     def get(self, request):
#         product_queryset = Product.objects.select_related('category').all()
#         serializer = ProductSerializer(
#             product_queryset, 
#             many=True, 
#             context={'request': request}
#         )
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         product_queryset = Product.objects.select_related('category').all()
#         serializer = ProductSerializer(
#             product_queryset, 
#             many=True, 
#             context={'request': request}
#         )
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.select_related('category').all()

#     # def get(self, request, pk):
#     #     product = get_object_or_404(
#     #         Product.objects.select_related('category'), 
#     #         pk=pk,
#     #     )
#     #     serializer = ProductSerializer(product, context={'request': request})
#     #     return Response(serializer.data)
    
#     # def put(self, request, pk):
#     #     product = get_object_or_404(
#     #         Product.objects.select_related('category'), 
#     #         pk=pk,
#     #     )
#     #     serializer = ProductSerializer(product, data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data)
    
#     def delete(self, request, pk):
#         product = get_object_or_404(
#             Product.objects.select_related('category'), 
#             pk=pk,
#         )
#         if product.order_items.count() > 0:
#             return Response({'error': 'There is some order including this product. Please remove them first.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, pk):
#     product = get_object_or_404(
#         Product.objects.select_related('category'), 
#         pk=pk
#     )
#     if request.method == 'GET':
#         serializer = ProductSerializer(product, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.order_items.count() > 0:
#             return Response({'error': 'There is some order including this product. Please remove them first.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('products').all()

    def delete(seld, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'There is some products relating this category. Please remove them first.'})
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class CategoryList(ListCreateAPIView):
#     serializer_class = CategorySerializer
#     queryset = Category.objects.prefetch_related('products').all()

# class CategoryList(ListCreateAPIView):
#     def get_serializer_class(self):
#         return CategorySerializer
#     def get_queryset(self):
#         return Category.objects.prefetch_related('products').all()

# class CategoryList(APIView):
#     def get(self, request):
#         categories_queryset = Category.objects.prefetch_related('products').all()
#         serializer = CategorySerializer(categories_queryset, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET','POST'])
# def category_list(request):
#     if request.method == 'GET':
#         categories_queryset = Category.objects.annotate(
#             products_count=Count('products')
#         ).all()
#         serializer = CategorySerializer(categories_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class CategoryDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = CategorySerializer
#     queryset = Category.objects.prefetch_related('products')

#     # def get(self, request, pk):
#     #     category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
#     #     serializer = CategorySerializer(category)
#     #     return Response(serializer.data)
    
#     # def put(self, request, pk):
#     #     category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
#     #     serializer = CategorySerializer(category, data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data)
    
#     def delete(seld, request, pk):
#         category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
#         if category.products.count() > 0:
#             return Response({'error': 'There is some products relating this category. Please remove them first.'})
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'PUT', 'DELETE'])
# def category_detail(request, pk):
#     category = get_object_or_404(Category.objects.annotate(products_count=Count('products')), pk=pk)
#     if request.method == 'GET':
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CategorySerializer(category, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if category.products.count() > 0:
#             return Response({'error': 'There is some products relating this category. Please remove them first.'})
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

