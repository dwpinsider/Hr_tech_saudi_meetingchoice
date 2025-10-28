from django.urls import path
from . import views

urlpatterns = [
    path('', views.delegate_meeting_register, name='delegate_meeting_register'),
    path('', views.delegate_meeting_register, name='delegate_meeting_finish'),
]
