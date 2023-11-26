from django.contrib import admin

# Register your models here.
from records.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'id', 'Salary', 'Ddesignation', 'Address')
