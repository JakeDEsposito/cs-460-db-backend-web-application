from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from . import forms
from . import models
from django.db import connection

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

        data = request.POST

        typeVal = data['typeVal']
        yearVal = data['yearVal']
        semesterVal = data['semesterVal']

        semester = '01' if semesterVal == 0 else '02'

        if typeVal == "0":
            # Create the list of course sections and the number of students enrolled in each section that the professor taught in a given semester
            with connection.cursor() as cursor:
                cursor.execute("SELECT Teaches.sec_id, COUNT(Takes.student_id) FROM Teaches JOIN Takes ON Teaches.course_id = Takes.course_id AND Teaches.sec_id = Takes.sec_id WHERE teacher_id = {} AND Teaches.semester = {} AND Teaches.year = {} GROUP BY Teaches.course_id, Teaches.sec_id".format(request.session.get('userID'), semester, yearVal))
                results = cursor.fetchall()
        else:
            # Create the list of students enrolled in a course section taught by the professor in a given semester
            with connection.cursor() as cursor:
                cursor.execute("SELECT Teaches.sec_id, (SELECT name FROM Student WHERE Student.student_id = Takes.student_id) FROM Teaches JOIN Takes ON Teaches.sec_id = Takes.sec_id WHERE teacher_id = {} AND Teaches.semester = {} AND Teaches.year = {}".format(request.session.get('userID'), semester, yearVal))
                results = cursor.fetchall()

        # FIXME: Here for testing! Remove for final release!
        print(results)

        courseSearch = forms.instructorForm(request.POST)
        errorMsg = 'POST'
        return render(request, 'instructor/instructor.html', {'lookupForm': courseSearch, 'errorMsg': errorMsg, "rows": results, "typeVal": typeVal})
    else:
        courseSearch = forms.instructorForm()
        errorMsg = 'GET'
        #return render(request, 'main/noUser.html')
        return render(request, 'instructor/instructor.html', {'lookupForm': courseSearch, 'errorMsg': errorMsg})
        
def student(request):
    if (request.session['userType'] != "student"): return render(request, 'main/noUser.html')
    if request.method == "POST":
        courseSearch = forms.studentForm(request.POST)
        data = request.POST
        print(data)
        yearSearch = int(data['yearVal'])
        semesterSearch = int(data['semesterVal'])
        
        with connection.cursor() as cursor:
            cursor.execute("select section.course_id, course.title, section.sec_id, course.dept_name from section join course on (section.course_id = course.course_id) where year={} and semester={};".format(yearSearch, semesterSearch))
            results = cursor.fetchall()
            print(results)
        
        rows = len(results)
        if(rows == 0):
            return render(request, 'student/student.html', {'lookupForm': courseSearch, 'errorMsg': 'No results found'})
        else:
            return render(request, 'student/student.html', {'lookupForm': courseSearch, 'testVal': 1, 'results': results})
    else:
        courseSearch = forms.studentForm()
        errorMsg = 'GET'
        return render(request, 'student/student.html', {'lookupForm': courseSearch, 'errorMsg': errorMsg})

def admin(request):
    if (request.session['userType'] != "admin"): return render(request, 'main/noUser.html')
    if request.method == 'POST':
        form = forms.adminQuerySelect(request.POST)
        if form.is_valid():
            redirectVal = int(form.cleaned_data['queryChoice'])
            return getAdminSubpage(redirectVal)
    else:
        return render(request, 'admin/admin.html', {'adminChooseQuery': forms.adminQuerySelect()})

def roster(request):
    if (request.session['userType'] != "admin"): return render(request, 'main/noUser.html')
    if request.method == "POST":
        form = forms.adminForm1(request.POST)
        data = request.POST
        sortType = data['sortType']
        sortOrder = data['directionSelect']
        
        if (sortOrder == "DESC"):
            sortType = '-' + sortType
        
        results = models.Instructor.objects.all().order_by(sortType).values()
        return render(request, 'admin/F1.html', {'adminSortSelect': form, 'testVal': 1, 'results': results})
        
    else:
        form = forms.adminForm1()
        return render(request, 'admin/F1.html', {'adminSortSelect': form})

def salary(request):
    if (request.session['userType'] != "admin"): return render(request, 'main/noUser.html')

    with connection.cursor() as cursor:
        cursor.execute("SELECT dept_name, MIN(salary), MAX(salary), AVG(salary) FROM instructor WHERE dept_name IS NOT NULL GROUP BY dept_name")
        instructors = cursor.fetchall()
        
    return render(request, 'admin/F2.html', { "rows": instructors})
    
def preformance(request):
    if (request.session['userType'] != "admin"): return render(request, 'main/noUser.html')
    if request.method == "POST":
        form = forms.adminForm3(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if (isName(data['profName'])):
                
                name = data['profName']
                year = int(data['yearVal'])
                sem = int(data['semesterVal'])
                
                with connection.cursor() as cursor:
                    cursor.execute('select instructor.name, instructor.funding, instructor.papers_published, count(student_id) as numStudentsTaught, count(distinct teaches.course_id, teaches.sec_id, teaches.semester, teaches.year) as numCourses from takes right join teaches on (teaches.course_id, teaches.sec_id, teaches.year, teaches.semester) = (takes.course_id, takes.sec_id, takes.year, takes.semester) right join instructor on (teaches.teacher_id) = (instructor.id) where instructor.name = \'{}\' AND teaches.year = {} AND teaches.semester = {} GROUP BY instructor.name, instructor.funding, instructor.papers_published;'.format(name, year, sem))
                    rowData = cursor.fetchall()
                rowCount = len(rowData)
                
                if (rowCount != 0):
                    return render(request, 'admin/F3.html', {'adminPrefForm': forms.adminForm3(request.POST), 'testVal': 1, 'results': rowData})
                else:
                    return render(request, 'admin/F3.html', {'adminPrefForm': forms.adminForm3(request.POST), 'errorMsg': 'Error: No Valid Entries'})
            else:
                error = 'Invalid Name. Please try again'
                return render(request, 'admin/F3.html', {'adminPrefForm': forms.adminForm3(request.POST), 'errorMsg': error})
    else:
        form = forms.adminForm3()
        error = ''
        return render(request, 'admin/F3.html', {'adminPrefForm': form, 'errorMsg': error})


# Functions for Views

def formCheck(formData):
    if formData['userID'].isnumeric(): 
        return True
    return False

def queryLogin(uType, uID):
    if (uType == 'student'):
        queryData = models.Student.objects.filter(student_id = uID)
    elif (uType == 'instructor'):
        queryData = models.Instructor.objects.filter(id = uID)
    else:
        queryData = models.Admin.objects.filter(adminid = uID)
    for r in queryData:
        print(r)
    print(queryData.count())
    return (queryData.count() > 0)

def login(uType):
    if (uType == 'student'):
        return redirect("student")
    elif (uType == 'instructor'):
        return redirect("instructor")
    else:
        return redirect("admin")
    
def getAdminSubpage(queryNum):
    if queryNum == 1:
        return redirect("roster")
    elif queryNum == 2:
        return redirect("salary")
    else:
        return redirect("preformance")
    
def isName(name):
    return (name.isalpha())