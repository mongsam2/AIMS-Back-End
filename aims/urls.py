from django.urls import path
from . import views

urlpatterns = [
    path('extraction/<int:document_id>/', views.ExtractionView.as_view()),
    path('summarization/<int:document_id>/', views.SummarizationView.as_view()),
    path('reason/<int:document_id>/', views.ReasonView.as_view()),
    path('evaluation/<int:document_id>/', views.EvaluationView.as_view()),
]