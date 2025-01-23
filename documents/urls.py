from django.urls import path
from . import views


urlpatterns = [
    path('', views.DocumentCreateView.as_view()),
    path('student-records/<int:record_id>/', views.StudentRecordDetailView.as_view()),
    path('student-records/', views.StudentRecordsView.as_view()),
    path('essays/', views.EssaysView.as_view()),
    path('essays/<int:essay_id>/', views.EssayDetailView.as_view()),
    path('essays/<int:essay_id>/criteria/', views.EssayCriteriaView.as_view()),
    path('<str:student_id>/<str:document_type>/', views.DocumentListView.as_view()),
]
