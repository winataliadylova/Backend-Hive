from django.db import models

# Create your models here.

class Admin(models.Model):
    # admin_id = models.BigAutoField(primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    created = models.DateTimeField("created", auto_now_add=True)
    updated = models.DateTimeField("updated", auto_now=True)
    
    def admin(self):
        return Admin

class Customer(models.Model):
    # customer_id = models.BigAutoField(primary_key=True)
    email = models.CharField("email", max_length=200)
    name = models.CharField("name", max_length=200)
    password = models.CharField("password", max_length=200)
    idCard = models.CharField("idCard", max_length=200)
    licenceCard = models.CharField("licenseCard", max_length=200)
    phoneNumber = models.CharField("phoneNumber", max_length=200)
    status = models.CharField("status", max_length=200)
    created = models.DateTimeField("created", auto_now_add=True)
    updated = models.DateTimeField("updated", auto_now=True)
    #approvedBy
    #approvedDate
    
    def customer(self):
        return Customer

class Provider(models.Model):
    # provider_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    trading_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    bank_account_number = models.CharField(max_length=50)
    bank_account_name = models.CharField(max_length=50)
    id_card = models.CharField(max_length=50)
    phoneNumber = models.CharField("phoneNumber", max_length=20)
    status = models.CharField("status", max_length=15)
    balance = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    approved_datetime = models.DateTimeField(null=True, blank=True)
    # approved_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null = True)
    updated_datetime = models.DateTimeField(auto_now=True)
    
    def provider(self):
        return Provider

class Car(models.Model):
    # car_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='car_id')
    provider_id = models.ForeignKey(Provider, on_delete=models.CASCADE) #when Provider deleted all children will be deleted
    brand = models.CharField(max_length=20)
    year = models.CharField(max_length=4)
    color = models.CharField(max_length=20)
    seat = models.PositiveIntegerField()
    vehicle_no = models.CharField(max_length=15)
    trasmission = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=6, decimal_places=0)
    deposit = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=15, null=True, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    # updated_by
    
    def car(self):
        return Car
# one car have one or many car file
class CarFile(models.Model):
    # car_file_id = models.BigAutoField(primary_key=True)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE) #when car deleted all children will be deleted
    file_path = models.CharField(max_length=200)
    file_type = models.CharField(max_length=5)
    created_datetime = models.DateTimeField(auto_now_add=True)
    
    def car_file(self):
        return CarFile

class ChatRoom(models.Model):
    # chat_room_id = models.BigAutoField(primary_key=True)
    provider_id = models.ForeignKey(Provider, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    def chat_room(self):
        return ChatRoom
    
class Chat(models.Model):
    # chat_id = models.BigAutoField(primary_key=True)
    chat_room_id = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message = models.TextField()
    file_path = models.CharField(max_length=200)
    created = models.DateTimeField("created", auto_now_add=True)
    
    def chat(self):
        return Chat

class Order(models.Model):
    # order_id = models.BigAutoField(primary_key=True)
    car_id = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    pickup_location = models.CharField(max_length=100)
    return_location = models.CharField(max_length=100)
    status = models.CharField(max_length=15)
    transport_fee = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)
    damage_fee = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)
    late_fee = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    rating = models.PositiveIntegerField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    
    def order(self):
        return Order
    
class Payment(models.Model):
    # payment_id = models.BigAutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    invoice_no = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)
    transaction_datetime = models.DateTimeField()
    deposit_return_time = models.DateTimeField(null=True, blank=True)
    refund_datetime = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15)
    
    def payment(self):
        return Payment
    
class Report(models.Model):
    # report_id = models.BigAutoField(primary_key=True)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    reason = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    
    def report(self):
        return Report
    
class Wishlist(models.Model):
    # wishlist_id = models.BigAutoField(primary_key=True)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def wishlist(self):
        return Wishlist
    
class Withdrawal(models.Model):
    # withdrawal_id = models.BigAutoField(primary_key=True)
    provider_id = models.ForeignKey(Provider, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=0)
    withdraw_datetime = models.DateTimeField()
    
    def withdrawal(self):
        return Withdrawal