from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('customer_list/<str:pk>/', views.customer, name="customer"),

    path('create-customer/', views.createCustomer, name="create-customer"),
    path('update-customer/<str:pk>/', views.updateCustomer, name="update-customer"),
    
    path('delete-customer/<str:pk>/', views.deleteCustomer, name="delete-customer")
]

