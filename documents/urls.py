from django.urls import path
from .views import DocumentCreateView, DocumentListView, StudentRecordsView, StudentRecordsDetailView


urlpatterns = [
    path('', DocumentCreateView.as_view()),
    path('student-records/<int:record_id>/', StudentRecordsDetailView.as_view()),
    path('<str:student_id>/<str:document_type>/', DocumentListView.as_view()),
    path('student-records/', StudentRecordsView.as_view()),
]
