from .models import *
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

class ProviderSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     print(validated_data)
    #     with connection.cursor() as cursor:
    #         cursor.execute('CALL insert_user_provider(%s, %s)', [validated_data['email'], validated_data['password']])
    #         return self
    
    class Meta:
        model = Provider
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
class CarFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarFile
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(read_only=True)
    queryset = Car.objects.prefetch_related('car_files')
    car_files = CarFileSerializer(queryset, many=True, read_only=True)
    
    provider_id = serializers.PrimaryKeyRelatedField(
        queryset=Provider.objects.all(), source='provider', write_only=True)
    
    class Meta:
        model = Car
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

class OrderSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    
    car_id = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all(), source='car', write_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    car_id = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all(), source='car', write_only=True)
    
    class Meta:
        model = Wishlist
        fields = '__all__'

class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

class ChatRoomSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    provider = ProviderSerializer(read_only=True)
    queryset = Chat.objects.prefetch_related('chat')
    chats = ChatSerializer(queryset, many=True, read_only=True)

    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True)
    provider_id = serializers.PrimaryKeyRelatedField(
        queryset=Provider.objects.all(), source='provider', write_only=True)

    class Meta:
        model = ChatRoom
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
