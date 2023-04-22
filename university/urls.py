from django.urls import path, include
from university import views

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('student/', views.student.as_view(), name='student'),
    path('instructor/', views.instructor.as_view(), name='instructor'),
    path('admin/', views.admin.as_view(), name='admin'),
    
    path('admin/roster', views.roster.as_view(), name='roster'),
    path('admin/salary', views.salary.as_view(), name='salary'),
    path('admin/preformance', views.preformance.as_view(), name='preformance'),
    
    path('instructor/sectionEnrolled', views.sectionEnrolled.as_view(), name='sectionEnrolled'),
    path('instructor/sectionStudents', views.sectionStudents.as_view(), name='sectionStudents')
]