from rest_framework import generics, permissions 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import connection
from django.db.models import Subquery, OuterRef, Q
from .models import *
from .serializers import *
import json
from datetime import datetime, date
import requests
import decimal
from django.utils.crypto import get_random_string
import locale

# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    
class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    
    def get_queryset(self):
        queryset = Car.objects.all()
        provider = self.request.query_params.get('provider_id')
        if provider is not None:
            queryset = queryset.filter(provider_id = provider)
        return queryset

class CarFilesViewSet(viewsets.ModelViewSet):
    queryset = CarFile.objects.all()
    serializer_class = CarFileSerializer

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        queryset = Order.objects.select_related('car').all()
        customer = self.request.query_params.get('customer_id')
        if customer is not None:
            queryset = queryset.filter(customer_id = customer)
        
        provider = self.request.query_params.get('provider_id')
        if provider is not None:
            queryset = queryset.filter(car__provider = provider)
        return queryset.order_by('-created_datetime')
    
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    
    def get_queryset(self):
        queryset = Wishlist.objects.all()
        customer = self.request.query_params.get('customer_id')
        if customer is not None:
            queryset = queryset.filter(customer_id = customer)
        return queryset
    
class ChatRoomViewSet(viewsets.ModelViewSet):
    serializer_class = ChatRoomSerializer
    
    def get_queryset(self):
        queryset = ChatRoom.objects.all()
        customer = self.request.query_params.get('customer_id')
        if customer is not None:
            queryset = queryset.filter(customer_id = customer)
            return queryset
        
        provider = self.request.query_params.get('provider_id')
        if provider is not None:
            queryset = queryset.filter(provider_id = provider)
        return queryset
        
class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    
    def get_queryset(self):
        queryset = Chat.objects.all()
        
        room = self.request.query_params.get('chat_room_id')
        if room is not None:
            queryset = queryset.filter(chat_room_id = room)
        return queryset
    
class BalanceHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = BalanceHistorySerializer
    
    def get_queryset(self):
        queryset = BalanceHistory.objects.all()
        
        provider = self.request.query_params.get('provider_id')
        if provider is not None:
            queryset = queryset.filter(provider_id = provider)
        return queryset.order_by('-transaction_datetime')
    
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        queryset = Notification.objects.all()
        customer = self.request.query_params.get('customer_id')
        if customer is not None:
            queryset = queryset.filter(customer_id = customer)
        
        provider = self.request.query_params.get('provider_id')
        if provider is not None:
            queryset = queryset.filter(provider_id = provider)
        return queryset.order_by('-created_datetime')

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
    # start_price = request.data['start_price']
    # end_price = request.data['end_price']
    # car_type = request.data['car_type']
    # start_year = request.data['start_year']
    # end_year = request.data['end_year']
    # seat = request.data['seat']
    # transmission = request.data['transmission']
    # fuel = request.data['fuel']
    
    query = "SELECT * FROM public.car WHERE isdelete = %s AND status = %s AND provider_id IN (SELECT id FROM provider WHERE LOWER(province) = %s AND LOWER(city) = %s) AND id NOT IN (SELECT car_id FROM public.order WHERE status < %s AND (start_datetime BETWEEN %s AND %s OR end_datetime BETWEEN %s AND %s))"
    
    variable = ['0', '1', province, city, '5', start_date, end_date, start_date, end_date]
    
    # if start_price is not None:
    #     temp = " AND price BETWEEN %s AND %s"
    #     query = query + temp
    #     variable.append(start_price)
    #     variable.append(end_price)
        
    # if car_type is not None:
    #     temp = " AND car_type IN ("
    #     for item in car_type:
    #         if car_type.index(item) == len(car_type) - 1:
    #             print(item, end='')
    #             temp = temp + "%s)"
    #         else:
    #             print(item, end=', ')
    #             temp = temp + "%s,"
    #             print(temp)
    #         variable.append(item)
    #     query = query + temp
    #     print(query)
    #     print(variable)
        
    # if start_year is not None:
    #     temp = " AND year BETWEEN %s AND %s"
    #     query = query + temp
    #     variable.append(start_year)
    #     variable.append(end_year)
        
    # if seat is not None:
    #     temp = " AND seat IN ("
    #     for item in seat:
    #         if seat.index(item) == len(seat) - 1:
    #             print(item, end='')
    #             temp = temp + "%s)"
    #         else:
    #             print(item, end=', ')
    #             temp = temp + "%s,"
    #             print(temp)
    #         variable.append(item)
    #     query = query + temp
    #     print(query)
    #     print(variable)
        
    # if transmission is not None:
    #     temp = " AND transmission IN ("
    #     for item in transmission:
    #         if transmission.index(item) == len(transmission) - 1:
    #             print(item, end='')
    #             temp = temp + "%s)"
    #         else:
    #             print(item, end=', ')
    #             temp = temp + "%s,"
    #             print(temp)
    #         variable.append(item)
    #     query = query + temp
    #     print(query)
    #     print(variable)
        
    # if fuel is not None:
    #     temp = " AND fuel IN ("
    #     for item in fuel:
    #         if fuel.index(item) == len(fuel) - 1:
    #             print(item, end='')
    #             temp = temp + "%s)"
    #         else:
    #             print(item, end=', ')
    #             temp = temp + "%s,"
    #             print(temp)
    #         variable.append(item)m
    #     query = query + temp
    #     print(query)
    #     print(variable)
    
    with connection.cursor() as cursor:
        cursor.execute(query, variable)
        cars = dictfetchall(cursor)
        
        for car in cars:
            try:
                cf = CarFile.objects.filter(car_id=car.get('id'))
            except CarFile.DoesNotExist:
                cf = None
                
            if cf is not None:
                serializer = CarFileSerializer(cf, many=True)
                car['car_files'] = serializer.data
            else:
                car['car_files'] = []
                        
    return Response(cars)
    
### API for customer_dropdown_location
@api_view(['GET'])
def customer_dropdown_location (request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT DISTINCT CONCAT(city, %s ,province) AS location FROM provider ', [', '])
        location = json.loads(json.dumps(cursor.fetchall()))
        location = [item for sublist in location for item in sublist]
        return Response(location)

### API for rating order and calc rating in car
@api_view(['POST'])
def rate_order(request):
    id = request.data['id']
    rating = request.data['rating']
    order = Order.objects.get(id=id)
    order.rating = rating
    order.save()
    print('order', order)
    
    car = Car.objects.get(id=order.car.id)
    car.rating = (car.rating * car.order_count + rating) / (car.order_count + 1)
    car.order_count += 1
    car.save()
    print('car', car)
    return Response(OrderSerializer(Order.objects.get(id=id)).data)
    
def test_notif(request, room_name):
    return render(request, 'notif_index.html', {
        'room_name': room_name
    })

def room(request, room_name):
    return render(request, 'chat/chatroom.html', {
        'room_name' : room_name
    })

### Dummy endpoint for quasar upload
@api_view(['POST'])
def image_upload(request):
    return Response(status=201)

### API to check if room already exists and create if not exists
@api_view(['GET'])
def get_or_create_room(request):
    customer = request.query_params.get('customer_id')
    provider = request.query_params.get('provider_id')
    
    try:
        room = ChatRoom.objects.get(customer_id = customer, provider_id = provider)
        return Response(ChatRoomSerializer(room).data)
    except ChatRoom.DoesNotExist:
        room = ChatRoom(customer_id = customer, provider_id = provider)
        room.save()
        return Response(ChatRoomSerializer(room).data, status = 201)

@api_view(['GET'])
def get_time(request):
    return Response(datetime.now())

@api_view(['POST'])
def complete_order(request, **kwargs):
    id = kwargs['id']
    provider_id = request.data['provider_id']
    order = Order.objects.get(id = id)
    order.status = '4'
    order.save()
    
    provider = Provider.objects.get(id = provider_id)
    provider.balance = provider.balance + decimal.Decimal(order.base_price)
    provider.save()
    
    balance_history = BalanceHistory(provider_id = provider, amount = order.base_price, is_income = True)
    balance_history.save()
    
    payments = Payment.objects.filter(order_id = id)
    first_payment = payments[0]
    first_payment.deposit_return_time = datetime.now()
    first_payment.save()
    
    return Response()

@api_view(['POST'])
def cancel_order(request, **kwargs):
    id = kwargs['id']
    order = Order.objects.get(id = id)
    order.status = '5'
    order.save()
    
    payments = Payment.objects.filter(order_id = id)
    first_payment = payments[0]
    first_payment.deposit_return_time = datetime.now()
    first_payment.save()
    
    return Response()

@api_view(['GET'])
def get_bank_list(request):
    url = 'https://api-rekening.lfourr.com/listBank'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data)

@api_view(['GET'])
def get_bank_account(request):
    bankCode = request.query_params.get('bank_code')
    accountNumber = request.query_params.get('acc_number')
    
    url = 'https://api-rekening.lfourr.com/getBankAccount'
    params = {
        'bankCode': bankCode,
        'accountNumber': accountNumber
    }
    response = requests.get(url, params = params)
    data = response.json()
    return JsonResponse(data)

@api_view(['POST'])
def withdraw(request):
    provider_id = request.data['provider_id']
    amount = request.data['amount']
    
    provider = Provider.objects.all().get(id = provider_id)
    provider.balance = provider.balance - decimal.Decimal(amount)
    print('balance', provider.balance)
    provider.save()
    
    balance_history = BalanceHistory(provider_id = provider, amount = amount, is_income = False)
    balance_history.save()
    
    return Response()

@api_view(['POST'])
def read_chat(request, **kwargs):
    room_id = kwargs['id']
    user_type = kwargs['user']
    
    if (user_type == 'provider'):
        Chat.objects.filter(chat_room_id = room_id).filter(provider_id__isnull = False).update(is_read=True)
    else:
        Chat.objects.filter(chat_room_id = room_id).filter(customer_id__isnull = False).update(is_read=True)
        
    return Response()

@api_view(['POST'])
def initiate_payment(request):
    order_id = request.data['order_id']
    amount = request.data['amount']
    invoice_no = get_random_string(10).upper()
    # print(invoice_no)
    
    while Payment.objects.filter(invoice_no = invoice_no).exists():
        invoice_no = get_random_string(10).upper() 
    
    url = 'https://app.sandbox.midtrans.com/snap/v1/transactions'
    headers = {
        'Authorization': 'Basic U0ItTWlkLXNlcnZlci0xamI1RmlEcUwtanVCZU1LX2hoWkFqaDk6',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        'transaction_details': {
            'order_id': invoice_no,
            'gross_amount': amount
        }, 
        'credit_card': {
            'secure': True
        }
    }
    # print('request', json.dumps(data))
    response = requests.post(url, headers = headers, data = json.dumps(data))
    # print('response', response.json())
    token  = response.json()['token']
    order = Order.objects.get(id = order_id)
    payment = Payment(order_id = order, invoice_no = invoice_no, amount = amount, token = token, status = 'IN')
    payment.save()
    
    return Response(PaymentSerializer(payment).data, status = 201)

@api_view(['POST'])
def callback_payment(request):
    invoice_no = request.data['order_id']
    ref_no = request.data['transaction_id']
    payment_method = request.data['payment_type']
    approval_code = request.data.get('approval_code')
    
    payment = Payment.objects.get(invoice_no = invoice_no)
    payment.status = 'PA'
    payment.payment_method = payment_method
    payment.reference_number = ref_no
    payment.approval_code = approval_code
    payment.save()
    
    order = Order.objects.get(id = payment.order_id.id)
    order.status = '1'
    order.save()
    
    currDate = date.today()
    month = currDate.month
    strDate = currDate.strftime("%d %b %Y")
    
    if (month == 5):
        strDate = strDate.replace("May", "Mei")
    elif (month == 8):
        strDate = strDate.replace("Aug", "Agt")
    
    message = 'Pembayaranmu untuk sewa mobil {car} pada {date} telah diterima.'
    message = message.replace('{car}', order.car.brand).replace('{date}', strDate)
    notif = Notification(isread = '0', provider_id = order.car.provider, customer_id = order.customer_id, 
                         title = 'Pembayaran diterima', message = message)
    notif.save()
    

    return Response()
