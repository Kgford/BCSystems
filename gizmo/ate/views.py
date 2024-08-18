import sys
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core import serializers
from .forms import AteForm
from datetime import date
from django.urls import reverse, reverse_lazy
from ate.models import Specifications, Trace, Testdata, Workstation, Effeciency
from django.views import View
import datetime

class AteView(View):
    form_class = AteForm
    template_name = "ate_page.html"
    success_url = reverse_lazy('ate:ate_page')
    
    def get(self, *args, **kwargs):
        form = self.form_class()
        part_list = []
        job_list = []
        part=-1
        job=-1
        log=-1
        led1=0
        led2=0
        led3=0
        led4=0
        logdata = "this is a test"
        try:
            print("in GET")
            part_list = Specifications.objects.order_by('part_number').values_list('part_number', flat=True).distinct()
            job_list = Specifications.objects.order_by('job_number').values_list('job_number', flat=True).distinct()
               
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"ate/index.html",{"form": form,  "part_list":part_list,"part":part, "job_list":job_list, "job":job, "log":log})

    def post(self, request, *args, **kwargs):
        try: 
            part_list = []
            job_list = []
            job=-1
            log=-1
            part=-1
            print("in POST2")
            print('request =',request)
            part = request.POST.get('_part', -1)
            print('part = ',part)
            job = request.POST.get('_job', -1)
            print('job = ',job)
            log = logdata
			
			#Get generic Lists
            part_list = Specifications.objects.order_by('part_number').values_list('part_number', flat=True).distinct()
            job_list = Specifications.objects.order_by('job_number').values_list('job_number', flat=True).distinct()
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        return render (self.request,"ate/index.html",{"form": form,  "part_list":part_list,"part":part, "job_list":job_list, "job":job, "log":log})
