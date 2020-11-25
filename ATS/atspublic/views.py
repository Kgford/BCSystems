from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from datetime import date
from django.urls import reverse, reverse_lazy
from django.views import View
import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
class PublicView(View):
    template_name = "index.html"
    success_url = reverse_lazy('index')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        return render (self.request,"index.html",{"inventory": inv})
    
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        print('inv_list',inv)
        return render (self.request,"index.html",{"inventory": inv})
		   
class WorkstationView(View):
    template_name = "racks.html"
    success_url = reverse_lazy('workstations:racks')
	
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        return render (self.request,"racks.html",{"inventory": inv})
		
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        print('inv_list',inv)
        return render (self.request,"index.html",{"inventory": inv})
