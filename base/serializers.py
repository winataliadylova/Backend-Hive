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
        queryset=Provider.objects.all(), source='provider', write_only=True, required=False)
    
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
        
class PaymentSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Payment
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    queryset = Order.objects.prefetch_related('payments')
    payments = PaymentSerializer(queryset, many=True, read_only=True)
    
    car_id = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all(), source='car', write_only=True, required=False)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True, required=False)

    class Meta:
        model = Order
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
    # sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=UserProfile.objects.all())
    # receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=UserProfile.objects.all())
    
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

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
