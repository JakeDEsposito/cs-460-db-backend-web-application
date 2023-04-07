from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import forms

# Create your views here.
from . import forms

def index(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            if formCheck(data):
                request.session['userType'] = data['userType']
                request.session['userID'] = data['userID']
                
                # localType = request.session.get('userID')
                # localID = request.session.get('userID')
                
                errorMsg = 'Done'
                return render(request, 'main/loginForm.html', {'form': form, 'errorMsg': errorMsg})
            errorMsg = 'ERROR: Invalid Login. Please Try Again.'
            return render(request, 'main/loginForm.html', {'form': form, 'errorMsg': errorMsg})
    else:
        form = forms.LoginForm()
        request.session['userType'] = ''
        request.session['userID'] = ''
        errorMsg = ''
        return render(request, 'main/loginForm.html', {'form': form})
    
def instructor(request):
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
    return HttpResponse("admin/admin.html");

def formCheck(formData):
    if formData['userID'].isnumeric(): 
        return True
    return False