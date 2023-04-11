from django.urls import path, include;
from . import views;

urlpatterns = [
    path('', views.admin, name='admin'),
    path('F1', views.F1, name='F1'),
    path('F2', views.F2, name='F2'),
    path('F3', views.F3, name='F3'),


]
