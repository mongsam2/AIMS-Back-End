from django.urls import path
from .views import AplicantsListView

urlpatterns = [
    path('', AplicantsListView.as_view(), name='applicants-list'),
]