from django import forms

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

class offeredCourses(forms.Form):
    yearVal = forms.ChoiceField(choices = YEARS, label = "Select Year")
    semesterVal = forms.ChoiceField(choices = SEMESTERS, label = "Select Semester")