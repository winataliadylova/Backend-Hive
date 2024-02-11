from django.db import models

# Create your models here.

class Customer(models.Model):
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
    
    def Customer(self):
        return Customer
    

# class Car(models.Model):

#     #carId 
#     #providerId
#     brand = models.CharField(max_length=200)
#     year = models.CharField(max_length=200)
#     color = models.CharField(max_length=200)
#     seat = models.CharField(max_length=200)
#     vehicleNo = models.CharField(max_length=200)
#     transmission = models.CharField(max_length=200)
#     price = models.CharField(max_length=200)
#     deposit = models.CharField(max_length=200)
#     description = models.CharField(max_length=200)
#     status = models.CharField(max_length=200)
#     created = models.CharField(max_length=200)
#     updated = models.CharField(max_length=200)
#     #updatedBy
    
#     def __str__(self):
#         return self.name

