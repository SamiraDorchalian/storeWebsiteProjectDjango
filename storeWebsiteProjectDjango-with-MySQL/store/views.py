from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view()
def product_list(request):
    return Response('Hello')

@api_view()
def product_detail(request, pk):
    return Response(pk)