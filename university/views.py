from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def student(request):
    return HttpResponse("student page")

def instructor(request):
    return HttpResponse("instructor page")