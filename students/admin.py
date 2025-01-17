from django.contrib import admin
from .models import Student, Department

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'phone')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department',)