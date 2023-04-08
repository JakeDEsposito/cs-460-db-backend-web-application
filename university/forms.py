from django import forms

USER_TYPE=[
    ('student', 'Student'),
    ('instructor', 'Instructor'),
    ('admin', 'Admin')
]

SEMESTERS = (
    (0, 'Fall'),
    (1, 'Spring')
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

class LoginForm(forms.Form):
    userType = forms.CharField(label='Select User Type', widget=forms.RadioSelect(choices = USER_TYPE))
    userID = forms.CharField(label='ID #', min_length=5, max_length=8)
    
class studentForm(forms.Form):
    yearVal = forms.ChoiceField(choices = YEARS, label = "Select Year")
    semesterVal = forms.ChoiceField(choices = SEMESTERS, label = "Select Semester")

class instructorForm(forms.Form):
    typeVal = forms.ChoiceField(widget = forms.RadioSelect, choices = TYPE, label = "Select query type")
    yearVal = forms.ChoiceField(choices = YEARS, label = "Select Year")
    semesterVal = forms.ChoiceField(choices = SEMESTERS, label = "Select Semester")