from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from . import forms
from . import models

# localType = request.session.get('userType')
# localID = request.session.get('userID')

def index(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if formCheck(data):
                uID = data['userID']
                uType = data['userType']
                
                if queryLogin(uType, uID):
                    request.session['userType'] = uType
                    request.session['userID'] = uID
                    return login(uType)
                
                errorMsg = 'ERROR: Invalid Login. Please Try Again.'
                return render(request, 'main/loginForm.html', {'form': form, 'errorMsg': errorMsg})
           
            errorMsg = 'ERROR: Invalid Syntax. Please Try Again.'
            return render(request, 'main/loginForm.html', {'form': form, 'errorMsg': errorMsg})
    else:
        form = forms.LoginForm()
        request.session['userType'] = ''
        request.session['userID'] = ''
        errorMsg = ''
        return render(request, 'main/loginForm.html', {'form': form})
    
def instructor(request):
    if (request.session['userType'] != "instructor"): return render(request, 'main/noUser.html')
    if request.method == "POST":
        courseSearch = forms.instructorForm(request.POST)
        errorMsg = 'POST'
        return render(request, 'instructor/instructor.html', {'lookupForm': courseSearch, 'errorMsg': errorMsg})
    else:
        courseSearch = forms.instructorForm()
        errorMsg = 'GET'
        #return render(request, 'main/noUser.html')
        return render(request, 'instructor/instructor.html', {'lookupForm': courseSearch, 'errorMsg': errorMsg})
        
def student(request):
    if (request.session['userType'] != "student"): return render(request, 'main/noUser.html')
    if request.method == "POST":
        courseSearch = forms.studentForm(request.POST)
        errorMsg = 'POST'
        return render(request, 'student/student.html', {'lookupForm': courseSearch, 'errorMsg': errorMsg})
    else:
        courseSearch = forms.studentForm()
        errorMsg = 'GET'
        #return render(request, 'main/noUser.html')
        return render(request, 'student/student.html', {'lookupForm': courseSearch, 'errorMsg': errorMsg})

def admin(request):
    return render(request, 'admin/admin.html')

# Functions for Views

def formCheck(formData):
    if formData['userID'].isnumeric(): 
        return True
    return False

def queryLogin(uType, uID):
    queryCount = 0
    if (uType == 'student'):
        queryData = models.Student.objects.filter(student_id = uID)
        queryCount = queryData.count()
    elif (uType == 'instructor'):
        queryData = models.Instructor.objects.filter(id = uID)
        queryCount = queryData.count()
    else:
        queryData #Need Admin Table
    for r in queryData:
        print(r)
    print(queryCount)
    return (queryCount > 0)

def login(uType):
    if (uType == 'student'):
        return redirect("student")
    elif (uType == 'instructor'):
        return redirect("instructor")
    else:
        return redirect("admin")