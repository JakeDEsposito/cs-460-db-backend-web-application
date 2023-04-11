#--Admin can do the following: 
# 
# F1. Roster: Create a list of professors sorted by one of the following 
#             criteria chosen by the admin: 
#               (1) by name (2) by dept, or (3) by salary. 
#F2. Salary: Create a table of min/max/average salaries by dept.
#F3. Performance: Given a professor's name, an academic year, 
#                 and a semester, show the following for the professor: the total 
#                 number of course sections taught during the semester,
#                 the total number of students taught, the total dollar amount 
#                 of funding the professor has secured, and the total number 
#                 of papers the professor has published. 
# --#

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def admin(request):
    return render(request, 'admin.html')

def F1(request):
    return render(request, 'F1.html')

def F2(request):
    return render(request, 'F2.html')

def F3(request):
    return render(request, 'F3.html')
