from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('student/', views.student, name='student'),
    path('instructor/', views.instructor, name='instructor'),
    path('admin/', views.admin, name='admin')
]