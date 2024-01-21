from django.db import models

# Create your models here.
class Student(models.Model):
    # id = models.AutoField() This field is automatically created by django. It's like a primary key and counter [1,2,3,4,...]
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    # image = models.ImageField()
    # file = models.FileField()

class Car(models.Model):
    car_name = models.CharField(max_length=500)
    speed = models.IntegerField(default=40)
    # when we create objects for this in django shell and then read it using <name_of_object>.objects.all() it will return us a queryset like this: 
    # <QuerySet [<Car: Car object (1)>, <Car: Car object (2)>, <Car: Car object (3)>, <Car: Car object (4)>, <Car: Car object (5)>]>
    # Its hard to read and not able to show data so we will define a function to return field related to the class so when we enter the above command then it will show that field.

    def __str__(self) -> str:
        return self.car_name
    # The above function will give query set like: <QuerySet [<Car: >, <Car: Nexon>, <Car: Thar>, <Car: Jeep>, <Car: i20>]>



    

