from django.contrib import admin
from .models import Student, Department, Applicants

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'phone')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department',)

@admin.register(Applicants)
class ApplicantsAdmin(admin.ModelAdmin):
    list_display = ('student', 'application_type', 'active')