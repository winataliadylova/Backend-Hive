from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('customer_list/<str:pk>/', views.customer, name="customer"),
]

