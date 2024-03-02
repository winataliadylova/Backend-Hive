from rest_framework import generics, permissions 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from .models import *
from .serializers import *

# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    
class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class CarFilesViewSet(viewsets.ModelViewSet):
    queryset = CarFile.objects.all()
    serializer_class = CarFileSerializer

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

class WithdrawalViewSet(viewsets.ModelViewSet):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer

class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


### Helper function
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


### API for check user email is exists or not
@api_view(['POST'])
def is_email_exists(request, **kwargs):
    email = request.data['email']
    user_type = kwargs['user']

    with connection.cursor() as cursor:
        if (user_type == 'providers') :
            cursor.execute('SELECT COUNT(*) FROM provider WHERE email = %s', [email])            
        elif (user_type == 'customers') : 
            cursor.execute('SELECT COUNT(*) FROM customer WHERE email = %s', [email])
        else :
            cursor.execute('SELECT COUNT(*) FROM admin WHERE email = %s', [email])
            
        result = dictfetchall(cursor)
        email_count = result[0].get('count')
        print(email_count)
        
    if (email_count == 0) :
        return Response(False)
    else :
        return Response(True)

### API for customer login
@api_view(['POST'])
def customer_login (request):
    email = request.data['email']
    password = request.data['password']
    
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM customer WHERE email = %s AND password = %s', [email, password])
        customer = dictfetchall(cursor)
        cursor.execute('SELECT * FROM provider WHERE email = %s', [email])
        provider = dictfetchall(cursor)
    
    if not customer :
        # return unauthorized if customer not found
        return Response(None, 401)
    else :
        # return the customer data, can be null for provider 
        return Response({
            "customer": CustomerSerializer(customer[0]).data,
            "provider": ProviderSerializer(provider[0]).data if provider else None
        })
