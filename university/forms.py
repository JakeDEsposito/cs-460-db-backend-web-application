from django import forms

USER_TYPE=[
    ('student', 'Student'),
    ('instructor', 'Instructor'),
    ('admin', 'Admin')
]

SEMESTERS = (
    (1, 'Fall'),
    (2, 'Spring')
)

YEARS = (
    (2019, '2019'),
    (2020, '2020'),
    (2021, '2021'),
    (2022, '2022'),
    (2023, '2023')
)

TYPE = (
    (0, 'Course Sec. & # of Students'),
    (1, 'List of Students')
)

ADMIN_QUERY_OPTIONS = (
    (1, 'Professor Sort'),
    (2, 'Salary Stats'),
    (3, 'Instructor Preformance')
)

PROFESSOR_SORT_CHOICES = (
    ('name', 'Name'),
    ('dept_name', 'Department'),
    ('salary', 'Salary')
)

DIRECTION = (
    ('ASC', 'Ascending Order'),
    ('DESC', 'Descending Order')
)

class LoginForm(forms.Form):
    userType = forms.CharField(label='Select User Type', widget=forms.RadioSelect(choices = USER_TYPE))
    userID = forms.CharField(label='ID #', min_length=5, max_length=8)
    
class studentForm(forms.Form):
    yearVal = forms.ChoiceField(choices = YEARS, label = "Select Year")
    semesterVal = forms.ChoiceField(choices = SEMESTERS, label = "Select Semester")

class instructorForm(forms.Form):
    typeVal = forms.ChoiceField(widget = forms.RadioSelect, choices = TYPE, label = "Select Query Type")
    yearVal = forms.ChoiceField(choices = YEARS, label = "Select Year")
    semesterVal = forms.ChoiceField(choices = SEMESTERS, label = "Select Semester")
    
class adminQuerySelect(forms.Form):
    queryChoice = forms.ChoiceField(widget = forms.RadioSelect, choices = ADMIN_QUERY_OPTIONS, label = "Select Query Option")
    
class adminForm1(forms.Form):
    sortType = forms.ChoiceField(choices = PROFESSOR_SORT_CHOICES, label = "Sort By")
    directionSelect = forms.ChoiceField(choices = DIRECTION, label = "Order")
    
class adminForm3(forms.Form):
    profName = forms.CharField(label = "Professor's Name", max_length = 16, min_length = 2)
    yearVal = forms.ChoiceField(choices = YEARS, label = "Select Year")
    semesterVal = forms.ChoiceField(choices = SEMESTERS, label = "Select Semester")
