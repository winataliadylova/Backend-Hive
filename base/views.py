from rest_framework import generics, permissions 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import connection
from .models import *
from .serializers import *
import json

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
    
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


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
    
### API for provider login
@api_view(['POST'])
def provider_login (request):
    email = request.data['email']
    password = request.data['password']
    
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM provider WHERE email = %s AND password = %s', [email, password])
        provider = dictfetchall(cursor)
    
    if not provider :
        # return unauthorized if customer not found
        return Response(None, 401)
    else :
        return Response(ProviderSerializer(provider[0]).data)
    

### API for approval user masih error csrf token
@api_view(['POST'])
# @csrf_exempt
def admin_approval_user (request):
    admin = request.data['admin']
    id = request.data['id']
    user = request.data['user']
    status = request.data['status']
    
    with connection.cursor() as cursor:
        if user == "cust":
            cursor.execute('UPDATE public.customer SET status = %s, approved_by = %s WHERE id = %s', [status, admin, id])
            cursor.execute('SELECT * FROM customer WHERE id = %s', [id])
            user = dictfetchall(cursor)
        else:
            cursor.execute('SELECT * FROM provider WHERE id = %s', [id])
            user = dictfetchall(cursor)
        
        return Response(user)

### API for customer filter + search car
@api_view(['POST'])
def customer_check_order_schedule (request):
    start_date = request.data['start_date']
    end_date = request.data['end_date']
    province = request.data['province'].lower()
    city = request.data['city'].lower()
    start_price = request.data['start_price']
    end_price = request.data['end_price']
    car_type = request.data['car_type']
    start_year = request.data['start_year']
    end_year = request.data['end_year']
    seat = request.data['seat']
    transmission = request.data['transmission']
    fuel = request.data['fuel']
    
    query = "SELECT * FROM public.car WHERE isdelete = %s AND provider_id IN (SELECT id FROM provider WHERE LOWER(province) = %s AND LOWER(city) = %s) AND id NOT IN (SELECT car_id FROM public.order WHERE status < %s AND (start_datetime BETWEEN %s AND %s OR end_datetime BETWEEN %s AND %s))"
    
    variable = ['0', province, city, '4',start_date, end_date, start_date, end_date]
    
    if start_price is not None:
        temp = " AND price BETWEEN %s AND %s"
        query = query + temp
        variable.append(start_price)
        variable.append(end_price)
        
    if car_type is not None:
        temp = " AND car_type IN ("
        for item in car_type:
            if car_type.index(item) == len(car_type) - 1:
                print(item, end='')
                temp = temp + "%s)"
            else:
                print(item, end=', ')
                temp = temp + "%s,"
                print(temp)
            variable.append(item)
        query = query + temp
        print(query)
        print(variable)
        
    if start_year is not None:
        temp = " AND year BETWEEN %s AND %s"
        query = query + temp
        variable.append(start_year)
        variable.append(end_year)
        
    if seat is not None:
        temp = " AND seat IN ("
        for item in seat:
            if seat.index(item) == len(seat) - 1:
                print(item, end='')
                temp = temp + "%s)"
            else:
                print(item, end=', ')
                temp = temp + "%s,"
                print(temp)
            variable.append(item)
        query = query + temp
        print(query)
        print(variable)
        
    if transmission is not None:
        temp = " AND transmission IN ("
        for item in transmission:
            if transmission.index(item) == len(transmission) - 1:
                print(item, end='')
                temp = temp + "%s)"
            else:
                print(item, end=', ')
                temp = temp + "%s,"
                print(temp)
            variable.append(item)
        query = query + temp
        print(query)
        print(variable)
        
    if fuel is not None:
        temp = " AND fuel IN ("
        for item in fuel:
            if fuel.index(item) == len(fuel) - 1:
                print(item, end='')
                temp = temp + "%s)"
            else:
                print(item, end=', ')
                temp = temp + "%s,"
                print(temp)
            variable.append(item)
        query = query + temp
        print(query)
        print(variable)
    
    with connection.cursor() as cursor:
        cursor.execute(query, variable)
        order = dictfetchall(cursor)
        
        return Response(order)
    
### API for customer_dropdown_location
@api_view(['GET'])
def customer_dropdown_location (request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT DISTINCT CONCAT(city, %s ,province) AS location FROM provider ', [', '])
        location = json.loads(json.dumps(cursor.fetchall()))
        location = [item for sublist in location for item in sublist]
        return Response(location)
    
def test_notif(request):
    return render(request, 'notif_index.html')
