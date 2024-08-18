from django import forms
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
#from .forms import InventoryForm
from retail.models import Retail_BOM, Retail_Inventory, Retail_Invoice
from datetime import date
from django.urls import reverse, reverse_lazy
from django.views import View
import datetime
from django.contrib.auth.decorators import login_required

def index(request):
    template_name = "index.html"
    success_url = reverse_lazy('retail:dashboard')
    contSuccess = 0
    return render (request,"retail/index.html")


class RetailView(View):
    #form_class = RetailForm
    template_name = "index.html"
    success_url = reverse_lazy('retail:dashboard')
    contSuccess = 0
    
    def get(self, *args, **kwargs):
        #form = self.form_class()
        try:
            BOM = Retail_BOM.objects.all()
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"retail/index.html",{})
        	   	
    def post(self, request, *args, **kwargs):
        return render (self.request,"retail/index.html,{}")



def ViewName(request):
    client_name = request.session['client']

