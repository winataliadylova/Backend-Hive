from django.urls import include, path
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from . import views

router = routers.DefaultRouter()
router.register(r'providers', views.ProviderViewSet)
router.register(r'cars', views.CarViewSet)

urlpatterns = [
    path('', views.home, name="home"),
    path('customer_list/<str:pk>/', views.customer, name="customer"),

    path('create-customer/', views.createCustomer, name="create-customer"),
    path('update-customer/<str:pk>/', views.updateCustomer, name="update-customer"),
    
    path('delete-customer/<str:pk>/', views.deleteCustomer, name="delete-customer")
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace="rest_framework")),
    path('schema/', get_schema_view()),
]

urlpatterns += router.urls
