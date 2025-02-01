from django.contrib import admin
from common.admin import CommonAdmin
from .models import Essay, EssayCriteria, EssayRange

# Register your models here.
@admin.register(Essay)
class EssayAdmin(CommonAdmin):
    pass

@admin.register(EssayCriteria)
class EssayCriteriaAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

@admin.register(EssayRange)
class EssayRangeAdmin(admin.ModelAdmin):
    list_display = ('__str__',)