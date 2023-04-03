from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template

# Create your views here.
def index(request):
    template = get_template('student/student.html')
    context = { "test_data": "test data" }

    return HttpResponse(template.render(context, request))