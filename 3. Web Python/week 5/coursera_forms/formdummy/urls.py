from django.urls import path

from . import views

urlpatterns = [
    path('', views.MarshView.as_view()),
]
