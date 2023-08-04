from django.urls import path
from . import views as views

urlpatterns = [
    path('main/', views.main, name='main'),
]
