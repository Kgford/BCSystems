from django.shortcuts import render
import datetime
from datetime import date
import time
from datetime import timedelta
from io import BytesIO
import io
import sys
import ast
import os
from os.path import exists
import socket
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from collections import OrderedDict
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.utils.timezone import make_aware
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views import View
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import AnonymousUser
from django.utils.html import format_html
from functions import sub_functions
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from BCSystems.overhead import TimeCode, Security,Email,Costing,DateCode,Greetings,StringThings
from test_executive.models import Specifications,JobData,TabularData,TraceData,Workstation,TestStatus,TestLogs,TestFixture,SpecAttachments,SpecDrawings,TestData
from BCSystems.settings import LOGIN_REDIRECT_URL	
from BCSystems.settings import DATA_DIR
import BCSystems.overhead
import html2text
import base64   
from openpyxl import Workbook   
from openpyxl import load_workbook  
#from fpdf import FPDF
#from urllib.request import urlopen


            

def index(request):
    template_name = "index.html"
    success_url = reverse_lazy('test_exec:test_exec')
    return redirect('test_exec:test_exec')



def update_offset(request): # for future addons
    # request should be ajax and method should be POST.
    print('request.method=',request.method)
    print(request.is_ajax)
    if request.is_ajax and request.method == "POST":
        try:
            print('we are here in post')
            part_number = request.POST['part_number']
            print('part_number',part_number)
            workstation = request.POST['workstation']
            print('workstation ',workstation )
            pc = request.POST['pc']
            print('pc ',pc )
            offset_val = request.POST['offset_val']
            print('offset_val ',offset_val )
            offset = request.POST['offset']
            print('offset',offset )
            active_user = request.POST['active_user']
            print('pc ',pc )
            this_spec=Specifications.objects.filter(partnumber=part_number).last() # Check if this job exists on the new database
            if this_spec:
                if Workstation.objects.select_related().filter(spec=this_spec).filter(workstationname=workstation,computername=pc,operator=active_user).exists():
                    if offset=='1':
                        Workstation.objects.filter(spec=this_spec).filter(workstationname=workstation,computername=pc,operator=active_user).update(offset1=offset_val)
                    elif offset=='2':
                        Workstation.objects.filter(spec=this_spec).filter(workstationname=workstation,computername=pc,operator=active_user).update(offset2=offset_val)
                    elif offset=='3':
                        Workstation.objects.filter(spec=this_spec).filter(workstationname=workstation,computername=pc,operator=active_user).update(offset3=offset_val)
                    elif offset=='4':
                        Workstation.objects.filter(spec=this_spec).filter(workstationname=workstation,computername=pc,operator=active_user).update(offset4=offset_val)
                    elif offset=='5':
                        Workstation.objects.filter(spec=this_spec).update(offset5=offset_val)
                   
                    print('data updated good')
                    return JsonResponse({"all good": "all good"}, status=200)
                else:
                    if offset=='1':
                        Workstation.objects.create(spec=this_spec,workstationname=workstation,computername=pc,operator=active_user,offset1=offset_val)
                    elif offset=='2':
                        Workstation.objects.create(spec=this_spec,workstationname=workstation,computername=pc,operator=active_user,offset1=offset_val)
                    elif offset=='3':
                        Workstation.objects.create(spec=this_spec,workstationname=workstation,computername=pc,operator=active_user,offset1=offset_val)
                    elif offset=='4':
                        Workstation.objects.create(spec=this_spec,workstationname=workstation,computername=pc,operator=active_user,offset1=offset_val)
                    elif offset=='5':
                        Workstation.objects.create(spec=this_spec,workstationname=workstation,computername=pc,operator=active_user,offset1=offset_val)
                    print('model created')
                    return JsonResponse({"all good": "all good"}, status=200)
            print('no spec')
            return JsonResponse({"all good": "no spec"}, status=200)
        except BaseException as e: 
            print('Error ate typical update ',e)
                
     # some error occured
    return JsonResponse({"error": ""}, status=400)

class TestExec(View):
    template_name = "email_view.html"
    success_url = reverse_lazy('test_exec:test_exec')
    #Note: email pics are stored here: https://imagekit.io/dashboard
    #Image location: https://ik.imagekit.io/gaxflngb5tpt/Email/image.jpg
    def get(self, request, *args, **kwargs):
        try:
            #~~~~~~~~~~~~~ Time ~~~~~~~~~~~~~~~~~
            days=2 # end_date is today + 2 
            time_code = TimeCode(days)
            today = datetime.datetime.today()
            current_time=today.time()
            this_date=today.date()
            today = make_aware(today)
            today_str=today.strftime('%Y-%m-%d')
            #~~~~~~~~~~~~~ Time ~~~~~~~~~~~~~~~~~
            #print('today =', today)
            print('we are here in GET')
            active_ticket=1
            active_user_name = request.user.get_full_name()
            active_user_firstname = request.user.get_short_name()
            active_user = request.user
            pc=socket.gethostname()
            workstation=os.getlogin()
            pc=socket.gethostname()
            if pc=='INN-AUTOCON':
                debug = True
            else:
                debug = False
            special_config=-1
            debug_pass = True;debug_fail = False;switch=False;test1='Insertion Loss';test2='Return Loss';test3='Isolation'; test4='Amp Balance';test5='Phase Balance'
            vna_type='8753E'
            address=16
            
            
            job_data=[]
            part_number = request.GET.get('part_number', -1)
            print('part_number=',part_number)
            job_number = request.GET.get('job_number', -1)
            
               
            print('job_number=',job_number)
            job_status = request.GET.get('job_status', -1)
            if job_status==-1 and job_number==-1:
                job_status='load job'
            
            
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"test_executive/test_exec.html",{'part_number':part_number,'job_number':job_number})
        
    
    def post(self, request, *args, **kwargs):
        try:
            #~~~~~~~~~~~~~ Time ~~~~~~~~~~~~~~~~~
            #print('today =', today)
            active_ticket=1
            active_user_name = request.user.get_full_name()
            active_user_firstname = request.user.get_short_name()
            active_user = request.user
            network_access=sub_functions.check_network_folder(SERVER_DATA_DIR)
            e2_access=sub_functions.check_E2_connection()
            test_access=sub_functions.check_TEST_connection()
            test_access=True # Function not working yet
            print('network_access=',network_access,' SERVER_DATA_DIR=',SERVER_DATA_DIR)
            print('e2_access=',e2_access,' test_access=',test_access)
            pc=socket.gethostname()
            workstation=os.getlogin()
            print('pc=',pc)
            print('workstation=',workstation)
            print('active_user=',active_user)
            #~~~~~~~~~~~~~ Time ~~~~~~~~~~~~~~~~~
            days=4 # end_date is today + 2 
            time_code = TimeCode(days)
            today = datetime.datetime.today()
            today = make_aware(today)
            this_date=today.date()
            today_str=today.strftime('%Y-%m-%d')
            year = time_code.this_year()
            month_num = time_code.this_month()
            month_string = time_code.month_string()
            last_day=time_code.month_length()
            #print('last_day=',last_day)
            #print('month_num=',month_num)
            day = time_code.this_day()
            minute = time_code.this_minute()
            sec = time_code.this_sec()
            week = time_code.week()
            week = int(week)-1
            resume=False
            job_number = request.POST.get('_job_number', -1)
            part_number = request.POST.get('_part_number', -1)
            if job_number !=-1 and part_number==-1:
                return redirect(f"{reverse('test_exec:test_exec')}?job_number=" + str(job_number))
            if job_number ==-1 and part_number!=-1:
                return redirect(f"{reverse('test_exec:test_exec')}?part_number=" + str(part_number))
           
            
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"test_executive/test_exec.html",{'part_number':part_number,'job_number':job_number})
