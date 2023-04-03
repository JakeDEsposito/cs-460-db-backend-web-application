from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def index(request):
    template = loader.get_template('main/loginForm.html');
    context = {};
    
    return HttpResponse(template.render(context, request));