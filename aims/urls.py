from django.urls import path
from . import views

urlpatterns = [
    path('extractions/<int:document_id>/', views.ExtractionView.as_view()),
    path('summarizations/<int:document_id>/', views.SummarizationView.as_view()),
    path('reasons/<int:document_id>/', views.DocumentPassFailView.as_view()),
    path('evaluations/<int:document_id>/', views.EvaluationView.as_view()),
]