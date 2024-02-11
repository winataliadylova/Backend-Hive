from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

customers = [
    {'id': 1, 'name':'Daniel'},
    {'id': 2, 'name':'Winata'},
    {'id': 3, 'name':'Yohanes'},
]


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
