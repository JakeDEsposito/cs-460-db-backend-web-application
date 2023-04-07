from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from . import forms

# Create your views here.
def index(request):
    if request.method == "POST":
        courseSearch = forms.offeredCourses(request.POST)
        errorMsg = 'POST'
        return render(request, 'student/student.html', {'lookupForm': courseSearch, 'errorMsg': errorMsg})
    else:
        courseSearch = forms.offeredCourses()
        errorMsg = 'GET'
        #return render(request, 'main/noUser.html')
        return render(request, 'student/student.html', {'lookupForm': courseSearch, 'errorMsg': errorMsg})