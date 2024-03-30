from django.urls import include, path
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from . import views

router = routers.DefaultRouter()
router.register(r'customers', views.CustomerViewSet)
router.register(r'providers', views.ProviderViewSet)
router.register(r'cars', views.CarViewSet, basename='Car')
router.register(r'car-files', views.CarFilesViewSet, basename='CarFile')
router.register(r'admins', views.AdminViewSet)
router.register(r'orders', views.OrderViewSet, basename='Order')
router.register(r'payments', views.PaymentViewSet)
router.register(r'wishlists', views.WishlistViewSet, basename='Wishlist')
router.register(r'withdrawals', views.WithdrawalViewSet)
router.register(r'chat-rooms', views.ChatRoomViewSet)
router.register(r'chats', views.ChatViewSet)
router.register(r'reports', views.ReportViewSet)
router.register(r'notifications', views.NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace="rest_framework")),
    path('schema/', get_schema_view()),
    path('<str:user>/check-email', views.is_email_exists),
    
    path('admin/user-approval', views.admin_approval_user),
    
    path('customer/login', views.customer_login),
    path('customer/check-schedule', views.customer_check_order_schedule),
    path('customer/dropdown-location', views.customer_dropdown_location),
    path('notif/<str:room_name>/', views.test_notif, name='test_notif'),

    path('provider/login', views.provider_login),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('orders/rate', views.rate_order),
    path('img/upload', views.image_upload)
]

urlpatterns += router.urls
