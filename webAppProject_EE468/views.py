from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from . import forms

def index(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            if formCheck(data):
                errorMsg = 'Done'
                return render(request, 'main/loginForm.html', {'form': form, 'errorMsg': errorMsg})
            errorMsg = 'ERROR: Invalid Login. Please Try Again.'
            return render(request, 'main/loginForm.html', {'form': form, 'errorMsg': errorMsg})
    else:
        form = forms.LoginForm()
        errorMsg = ''
        return render(request, 'main/loginForm.html', {'form': form})
        
def formCheck(formData):
    if formData['userID'].isnumeric(): 
        return True
    return False