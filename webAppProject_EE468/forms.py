from django import forms

USER_TYPE=[
    ('student', 'Student'),
    ('instructor', 'Instructor'),
    ('admin', 'Admin')
]

class LoginForm(forms.Form):
    userType = forms.CharField(label='Select User Type: ', widget=forms.RadioSelect(choices = USER_TYPE))
    userID = forms.CharField(label='ID #', min_length=5, max_length=8)
    
    