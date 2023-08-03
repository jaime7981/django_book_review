from django.views.generic import RedirectView
from django.urls import path
from . import views as books

urlpatterns = [
    path('', RedirectView.as_view(url='/books/main/')),
    path('main/', books.main, name = 'main'),
]