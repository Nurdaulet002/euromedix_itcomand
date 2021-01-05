from django.shortcuts import render, redirect
# Create your views here.


def identifyRole(request):
    if(request.user.role.title == 'doctor'):
        return redirect('doctorPanel:index')
    elif(request.user.role.title == 'registration'):
        return redirect('registrationPanel:index')
