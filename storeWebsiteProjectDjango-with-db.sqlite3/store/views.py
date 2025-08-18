from django.shortcuts import render
from django.http import HttpResponse

from .models import Product

def show_data(request):
    Product.objects.all()

    return render(request, 'hello.html')
