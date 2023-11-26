from django.db import models


# Create your models here.

# class Excel(models.Model):
#     file = models.FileField(verbose_name="Excel File",upload_to="excel")


class Employee(models.Model):
    Name = models.CharField(max_length=20)
    Salary = models.PositiveBigIntegerField()
    Ddesignation = models.CharField(max_length=15)
    Address = models.TextField()


    def __str__(self):
        return self.Name
