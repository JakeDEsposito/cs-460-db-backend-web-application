from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from . import forms
from . import models
from django.db import connection
from django.views.generic import TemplateView

# localType = request.session.get('userType')
# localID = request.session.get('userID')

class index(TemplateView):
    def get(self, request, **kwargs):
        form = forms.LoginForm()
        request.session['userType'] = ''
        request.session['userID'] = ''
        request.session['courseList'] = ''
        errorMsg = ''
        return render(request, 'main/loginForm.html', {'form': form})
    
    def post(self, request):
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

# Instructor Functions
class instructor(TemplateView):
    def get(self, request, **kwargs):
        if (request.session['userType'] != "instructor"): return render(request, 'main/noUser.html')

        typeForm = forms.instructorForm()
        return render(request, 'instructor/instructor.html', {'lookupForm': typeForm})
    def post(self, request):
        if (request.session['userType'] != "instructor"): return render(request, 'main/noUser.html')
        form = forms.instructorForm(request.POST)
        data = request.POST
        if (form.is_valid()):
            queryChoice = int(data['typeVal'])
            return getInstructorSubpage(queryChoice)

class sectionStudents(TemplateView):
    def get(self, request, **kwargs):
        if (request.session['userType'] != "instructor"): return render(request, 'main/noUser.html')
        form = forms.instructorQuery2()
        
        # Dynamically get courses taught by the instructor logged in, don't account for year or semester
        with connection.cursor() as cursor:
            cursor.execute('select distinct concat(course_id, "-", sec_id) as course from teaches where teacher_id = \'{}\';'.format(request.session.get('userID')))
            courseList = cursor.fetchall()
        newCourseList = []
        for course in courseList:
            index = courseList.index(course)
            newCourseList.append((courseList[index][0], courseList[index][0]))
        
        request.session['courseList'] = newCourseList
        form.fields['classVal'].choices = newCourseList
        return render(request, 'instructor/F5.html', {'lookupForm':form})
    
    def post(self, request):
        if (request.session['userType'] != "instructor"): return render(request, 'main/noUser.html')
        form = forms.instructorQuery2(request.POST)
        form.fields['classVal'].choices = request.session.get('courseList')
        data = request.POST
        courseSec = data['classVal']
        year = int(data['yearVal'])
        semester = int(data['semesterVal'])
        
        # Decompose combined course/section from search
        course = courseSec[0:courseSec.find("-")]
        sec = courseSec[courseSec.find("-")+1:len(courseSec)]
        
        with connection.cursor() as cursor:
            cursor.execute('select name, student.student_id from takes join student on (takes.student_id)=(student.student_id) where course_id = \'{}\' AND sec_id = \'{}\' AND semester = {} AND year = {};'.format(course, sec, semester, year))
            results = cursor.fetchall()
        rows = len(results)
        
        if (rows == 0):
            return render(request, 'instructor/F5.html', {'lookupForm':form, 'errorMsg': "Error: No such course/section exists in the specified year/semester."})
        else:
            fullCourse = courseSec + " - " + str(forms.SEMESTERS[semester-1][1]) + ", " + str(year)
            return render(request, 'instructor/F5.html', {'lookupForm':form, 'testVal': 1, 'rows': results, 'courseSection': fullCourse})
    
class sectionEnrolled(TemplateView):
    def post(self, request):
        if (request.session['userType'] != "instructor"): return render(request, 'main/noUser.html')
        courseSearch = forms.instructorQuery1(request.POST)
        data = request.POST
        year = data['yearVal']
        semester = data['semesterVal']
        
        with connection.cursor() as cursor:
            cursor.execute('select teaches.course_id, teaches.sec_id, count(student_id) from teaches join takes on (teaches.course_id, teaches.sec_id, teaches.year, teaches.semester) = (takes.course_id, takes.sec_id, takes.year, takes.semester) where teacher_id = \'{}\' AND teaches.year = {} AND teaches.semester = {} GROUP BY teaches.course_id, teaches.sec_id;'.format(request.session.get('userID'), year, semester))
            results = cursor.fetchall()
            
        rows = len(results)
        if (rows == 0):
            return render(request, 'instructor/F4.html', {'lookupForm': courseSearch, 'testVal': 0, 'errorMsg': "Error: No results found"})
        else:
            return render(request, 'instructor/F4.html', {'lookupForm': courseSearch, 'testVal': 1, 'rows': results})
    def get(self, request, **kwargs):
        if (request.session['userType'] != "instructor"): return render(request, 'main/noUser.html')
        form = forms.instructorQuery1()
        return render(request, 'instructor/F4.html', {'lookupForm': form})

# Student Functions
class student(TemplateView):
    def post(self, request):
        if (request.session['userType'] != "student"): return render(request, 'main/noUser.html')
        courseSearch = forms.studentForm(request.POST)
        data = request.POST
        yearSearch = int(data['yearVal'])
        semesterSearch = int(data['semesterVal'])
        
        with connection.cursor() as cursor:
            cursor.execute("select section.course_id, course.title, section.sec_id, course.dept_name from section join course on (section.course_id = course.course_id) where year={} and semester={};".format(yearSearch, semesterSearch))
            results = cursor.fetchall()
        
        rows = len(results)
        if(rows == 0):
            return render(request, 'student/student.html', {'lookupForm': courseSearch, 'errorMsg': 'No results found'})
        else:
            return render(request, 'student/student.html', {'lookupForm': courseSearch, 'testVal': 1, 'results': results})
    def get(self, request, **kwargs):
        if (request.session['userType'] != "student"): return render(request, 'main/noUser.html')
        courseSearch = forms.studentForm()
        errorMsg = ''
        return render(request, 'student/student.html', {'lookupForm': courseSearch, 'errorMsg': errorMsg})

# Admin Functions
class admin(TemplateView):
    def post(self, request):
        if (request.session['userType'] != "admin"): return render(request, 'main/noUser.html')
        form = forms.adminQuerySelect(request.POST)
        if form.is_valid():
            redirectVal = int(form.cleaned_data['queryChoice'])
            return getAdminSubpage(redirectVal)
    def get(self, request, **kwargs):
        if (request.session['userType'] != "admin"): return render(request, 'main/noUser.html')
        return render(request, 'admin/admin.html', {'adminChooseQuery': forms.adminQuerySelect()})

class roster(TemplateView):
    def post(self, request):
        if (request.session['userType'] != "admin"): return render(request, 'main/noUser.html')
        form = forms.adminForm1(request.POST)
        data = request.POST
        sortType = data['sortType']
        sortOrder = data['directionSelect']
        
        if (sortOrder == "DESC"):
            sortType = '-' + sortType
        
        results = models.Instructor.objects.all().order_by(sortType).values()
        return render(request, 'admin/F1.html', {'adminSortSelect': form, 'testVal': 1, 'results': results})
        
    def get(self, request, **kwargs):
        if (request.session['userType'] != "admin"): return render(request, 'main/noUser.html')
        form = forms.adminForm1()
        return render(request, 'admin/F1.html', {'adminSortSelect': form})

class salary(TemplateView):
    def get(self, request):
        if (request.session['userType'] != "admin"): return render(request, 'main/noUser.html')

        with connection.cursor() as cursor:
            cursor.execute("SELECT dept_name, MIN(salary), MAX(salary), AVG(salary) FROM instructor WHERE dept_name IS NOT NULL GROUP BY dept_name")
            instructors = cursor.fetchall()
            
        return render(request, 'admin/F2.html', { "rows": instructors})
    
class preformance(TemplateView):
    def post(self, request):
        if (request.session['userType'] != "admin"): return render(request, 'main/noUser.html')
        form = forms.adminForm3(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if (isName(data['profName'])):
                
                name = data['profName']
                year = int(data['yearVal'])
                sem = int(data['semesterVal'])
                
                with connection.cursor() as cursor:
                    cursor.execute('select name, round(sum(funding_per_award), 0) as funding, papers, numStudent, numSections from (select name as name, avg(amount) as funding_per_award, count(distinct paper.paper_id) as papers, count(distinct student_id) as numStudent, count(distinct teaches.course_id, teaches.sec_id, teaches.semester, teaches.year) as numSections from takes right join teaches on (teaches.course_id, teaches.sec_id, teaches.year, teaches.semester) = (takes.course_id, takes.sec_id, takes.year, takes.semester) right join instructor on (teaches.teacher_id) = (instructor.id) join funding_awardee on (funding_awardee.instructor_id) = (instructor.ID) join paper_author on (paper_author.instructor_id = instructor.id) join funding on (funding.funding_id) = (funding_awardee.funding_id) join paper on (paper.paper_id) = (paper_author.paper_id) where instructor.name = \'{}\' and teaches.year = {} AND teaches.semester = {} GROUP BY name, funding.funding_id) as partial_form GROUP BY name, papers, numStudent, numSections;'.format(name, year, sem))
                    rowData = cursor.fetchall()
                rowCount = len(rowData)
                
                if (rowCount != 0):
                    return render(request, 'admin/F3.html', {'adminPrefForm': forms.adminForm3(request.POST), 'testVal': 1, 'results': rowData})
                else:
                    return render(request, 'admin/F3.html', {'adminPrefForm': forms.adminForm3(request.POST), 'errorMsg': 'Error: No Valid Entries'})
            else:
                error = 'Invalid Name. Please try again'
                return render(request, 'admin/F3.html', {'adminPrefForm': forms.adminForm3(request.POST), 'errorMsg': error})
    def get(self, request, **kwargs):
        if (request.session['userType'] != "admin"): return render(request, 'main/noUser.html')
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
    
def getInstructorSubpage(formChoice):
    if (formChoice == 0):
        return redirect("sectionEnrolled")
    else:
        return redirect("sectionStudents")
    
def isName(name):
    return (name.isalpha())