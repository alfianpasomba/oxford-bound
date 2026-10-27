from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-vocabulary/', views.add_vocabulary, name='add_vocabulary'),
    path('submit-challenge/', views.submit_challenge, name='submit_challenge'),
]