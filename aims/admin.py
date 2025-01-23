from django.contrib import admin
from .models import InappropriateReason, Evaluation, Summarization, Extraction, EssayCriteria, EssayRange

# Uitls
class ShortContent:
     def short_content(self, obj):
         return f"{obj.content[:50]}..." if len(obj.content) > 30 else obj.content

# Register your models here.
@admin.register(Extraction)
class ExtractionAdmin(admin.ModelAdmin, ShortContent):
    list_display = ('document', 'short_content')

@admin.register(InappropriateReason)
class Inappropriate_ReasonAdmin(admin.ModelAdmin, ShortContent):
    list_display = ('document', 'short_content')

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin, ShortContent):
    list_display = ('document', 'short_content')

@admin.register(EssayCriteria)
class EssayCriteriaAdmin(admin.ModelAdmin, ShortContent):
    list_display = ('short_content',)

@admin.register(EssayRange)
class EssayRangeAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

@admin.register(Summarization)
class SummarizationAdmin(admin.ModelAdmin, ShortContent):
    list_display = ('document', 'short_content', 'short_question')

    def short_question(self, obj):
        return f"{obj.question[:50]}..." if len(obj.question) > 30 else obj.question