from django.urls import path
from .views import DocumentCreateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', DocumentCreateView.as_view(), name='document-create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
