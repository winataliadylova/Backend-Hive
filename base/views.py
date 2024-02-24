from rest_framework import generics, permissions 
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Car, Provider
from .serializers import ProviderSerializer, CarSerializer 

# Create your views here.

def home(request):
    content = {'customers' : customers}
    return render(request, 'base/homepage.html', content)

def customer(request, pk):
    customer = None
    for i in customers:
        if i['id'] == int(pk):
            customer = i
            
    context = {'customer' : customer}
    return render(request, 'base/customer.html', context)


# REST API
class ProviderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows provider to be viewed or edited.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    
class CarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows car to be viewed or edited.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
