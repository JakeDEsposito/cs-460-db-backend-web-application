from django.urls import path, include
from university import views

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('student/', views.student, name='student'),
    path('instructor/', views.instructor.as_view(), name='instructor'),
    path('admin/', views.admin, name='admin'),
    
    path('admin/roster', views.roster, name='roster'),
    path('admin/salary', views.salary, name='salary'),
    path('admin/preformance', views.preformance, name='preformance'),
    
    path('instructor/sectionEnrolled', views.sectionEnrolled, name='sectionEnrolled'),
    path('instructor/sectionStudents', views.sectionStudents, name='sectionStudents')
]