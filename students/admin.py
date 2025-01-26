from django.contrib import admin
from .models import Student, Department, Applicant, ApplicantType

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'department', 'phone')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department',)

@admin.register(ApplicantType)
class ApplicantTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Applicant)
class ApplicantsAdmin(admin.ModelAdmin):
    list_display = ('student', 'application_type', 'active')