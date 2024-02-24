from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomerForm
from .models import Customer

from rest_framework import generics, permissions 
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Car, Provider
from .serializers import ProviderSerializer, CarSerializer 

# Create your views here.

def home(request):
    customers = Customer.objects.all()
    content = {'customers' : customers}
    return render(request, 'base/homepage.html', content)

def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    context = {'customer' : customer}
    return render(request, 'base/customer.html', context)


def createCustomer(request):
    form = CustomerForm()
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'forms': form}
    return render(request, 'base/customer_form.html', context)

def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'forms':form}
    return render(request, 'base/customer_form.html', context)

def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': customer})
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
