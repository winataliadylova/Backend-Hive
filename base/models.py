from django.db import models

# Create your models here.

class Admin(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
   
    class Meta:
        db_table = "admin"
        managed = False
   
    def admin(self):
        return Admin
 
class Customer(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=200)
    name = models.CharField(null=True, max_length=200)
    password = models.CharField(max_length=200)
    id_card = models.CharField(null=True, max_length=200)
    license_card = models.CharField(null=True, max_length=200)
    phone_number = models.CharField(null=True, max_length=200)
    status = models.CharField(null=True, max_length=200)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    approved_by = models.ForeignKey(Admin, related_name="customers", on_delete=models.SET_NULL, null=True, db_column="approved_by")
    approved_datetime = models.DateTimeField(null=True)
   
    class Meta:
        db_table = "customer"
        managed = False
   
    def customer(self):
        return Customer
 
class Provider(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    trading_name = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=150,null=True, blank=True)
    city = models.CharField(max_length=50,null=True, blank=True)
    province = models.CharField(max_length=50,null=True, blank=True)
    bank_account_number = models.CharField(max_length=50,null=True, blank=True)
    bank_account_name = models.CharField(max_length=50,null=True, blank=True)
    id_card = models.CharField(max_length=50,null=True, blank=True)
    phone_number = models.CharField(max_length=20,null=True, blank=True)
    status = models.CharField(max_length=15,null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=0, default=0, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    approved_datetime = models.DateTimeField(null=True)
    approved_by = models.ForeignKey(Admin, related_name="providers", on_delete=models.SET_NULL, null=True, db_column="approved_by")
    updated_datetime = models.DateTimeField(auto_now=True)
   
    class Meta:
        db_table = "provider"
        managed = False
   
    def provider(self):
        return Provider
 
class Car(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    provider = models.ForeignKey(Provider, related_name="cars", on_delete=models.CASCADE, db_column="provider_id") #when Provider deleted all children will be deleted
    brand = models.CharField(max_length=20)
    car_type = models.CharField(max_length=20)
    year = models.CharField(max_length=4)
    color = models.CharField(max_length=20)
    seat = models.PositiveIntegerField()
    vehicle_no = models.CharField(max_length=15)
    transmission = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=6, decimal_places=0)
    deposit = models.DecimalField(max_digits=6, decimal_places=0, null=True)
    description = models.TextField(null=True)
    status = models.CharField(max_length=15, null=True, default="A")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(Admin, related_name="cars", on_delete=models.SET_NULL, null=True, db_column="updated_by")

    class Meta:
        db_table = "car"
        managed = False
           
    def car(self):
        return Car
    
# one car have one or many car file
class CarFile(models.Model):
    id = models.BigAutoField(primary_key=True)
    car_id = models.ForeignKey(Car, related_name="car_files", on_delete=models.CASCADE, db_column="car_id") #when car deleted all children will be deleted
    file_path = models.CharField(max_length=200)
    file_type = models.CharField(max_length=5)
    created_datetime = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        db_table = "car_file"
        managed = False
           
    def car_file(self):
        return CarFile
 
class ChatRoom(models.Model):
    id = models.BigAutoField(primary_key=True)
    provider = models.ForeignKey(Provider, related_name="chat_rooms", on_delete=models.SET_NULL, null=True, db_column="provider_id")
    customer = models.ForeignKey(Customer, related_name="chat_rooms", on_delete=models.SET_NULL, null=True, db_column="customer_id")

    class Meta:
        db_table = "chat_room"
        managed = False

    def chat_room(self):
        return ChatRoom
   
class Chat(models.Model):
    id = models.BigAutoField(primary_key=True)
    chat_room_id = models.ForeignKey(ChatRoom, related_name="chats", on_delete=models.CASCADE, db_column="chat_room_id")
    message = models.TextField()
    file_path = models.CharField(max_length=200, null=True)
    is_read = models.BooleanField(default=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        db_table = "chat"
        managed = False
   
    def chat(self):
        return Chat
 
class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    car = models.ForeignKey(Car, related_name="orders", on_delete=models.SET_NULL, null=True, db_column="car_id")
    customer = models.ForeignKey(Customer, related_name="orders", on_delete=models.SET_NULL, null=True, db_column="customer_id")
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    pickup_location = models.CharField(max_length=100)
    return_location = models.CharField(max_length=100)
    status = models.CharField(max_length=15)
    transport_fee = models.DecimalField(max_digits=6, decimal_places=0, default=0)
    damage_fee = models.DecimalField(max_digits=6, decimal_places=0, default=0)
    late_fee = models.DecimalField(max_digits=6, decimal_places=0, default=0)
    review = models.TextField(null=True, blank=True)
    rating = models.PositiveIntegerField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
   
    class Meta:
        db_table = "order"
        managed = False
   
    def order(self):
        return Order
   
class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, related_name="payments", on_delete=models.SET_NULL, null=True, db_column="order_id")
    invoice_no = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=6, decimal_places=0, null=True)
    transaction_datetime = models.DateTimeField(auto_now_add=True)
    deposit_return_time = models.DateTimeField(null=True)
    refund_datetime = models.DateTimeField(null=True)
    status = models.CharField(max_length=15, default="IN")
   
    class Meta:
        db_table = "payment"
        managed = False
   
    def payment(self):
        return Payment
   
class Report(models.Model):
    id = models.BigAutoField(primary_key=True)
    car_id = models.ForeignKey(Car, related_name="reports", on_delete=models.CASCADE, db_column="car_id")
    customer_id = models.ForeignKey(Customer, related_name="reports", on_delete=models.SET_NULL, null=True, db_column="customer_id")
    reason = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        db_table = "report"
        managed = False
   
    def report(self):
        return Report
   
class Wishlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    car = models.ForeignKey(Car, related_name="wishlists", on_delete=models.CASCADE, db_column="car_id")
    customer_id = models.ForeignKey(Customer, related_name="wishlists", on_delete=models.CASCADE, db_column="customer_id")
    start_date = models.DateField()
    end_date = models.DateField()
   
    class Meta:
        db_table = "wishlist"
        managed = False
   
    def wishlist(self):
        return Wishlist
   
class Withdrawal(models.Model):
    id = models.BigAutoField(primary_key=True)
    provider_id = models.ForeignKey(Provider, related_name="withdrawals", on_delete=models.CASCADE, db_column="provider_id")
    amount = models.DecimalField(max_digits=6, decimal_places=0)
    withdraw_datetime = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        db_table = "withdrawal"
        managed = False
   
    def withdrawal(self):
        return Withdrawal