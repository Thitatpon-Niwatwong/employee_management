from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=100) 

class Position(models.Model):
    name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

class Employee(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    is_manager = models.BooleanField(default=False) 
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='employee_images/', null=True, blank=True)


class Department(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='managed_departments')
