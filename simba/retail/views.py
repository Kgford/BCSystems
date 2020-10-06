from django.shortcuts import render

def ViewName(request):
    client_name = request.session['client']
