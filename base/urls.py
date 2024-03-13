from django.urls import include, path
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from . import views

router = routers.DefaultRouter()
router.register(r'customers', views.CustomerViewSet)
router.register(r'providers', views.ProviderViewSet)
router.register(r'cars', views.CarViewSet)
router.register(r'car-files', views.CarFilesViewSet)
router.register(r'admins', views.AdminViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'wishlists', views.WishlistViewSet)
router.register(r'withdrawals', views.PaymentViewSet)
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
    path('notif', views.test_notif, name='test_notif')
]

urlpatterns += router.urls
