from django.urls import path
from .views import DocumentCreateView


urlpatterns = [
    path('', DocumentCreateView.as_view(), name='document-create'),
]
