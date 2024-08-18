from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .forms import ModelsForm
from datetime import date
from django.urls import reverse,  reverse_lazy
from django.urls import reverse
from django.views import View
from equipment.models import Model
from ATS.overhead import TimeCode, Security,Email,Costing,DateCode,Greetings,StringThings
from vendor.models import Vendor
from datetime import date, datetime
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import datetime
model_id = 0


class UserLogin(View):
    template_name = "user_login.html"
    success_url = reverse_lazy('equipment:login')
        
    def get(self, *args, **kwargs):
        try:
            operator = str(self.request.user.get_short_name())
        
        except IOError as e:
           print('error = ',e) 
        return render(request, 'equipments/user_login.html', {})
 
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    redirect_to = resolve_url(LOGIN_REDIRECT_URL)
                    print('redirect =',LOGIN_REDIRECT_URL)
                    return render(request,'equipment/index.html')
                else:
                    return render(request, 'equipment/user_login.html', {'message':'Login Failed!!'})
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
            return render(request, 'equipment/user_login.html', {'message':'Login Failed!!'})
        else:
            return render(request, 'equipment/user_login.html', {})

class EquipmentView(View):
    form_class = ModelsForm
    template_name = "index.html"
    success_url = reverse_lazy('equipment:equipment')
    contSuccess = 0
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        
        try:
            models = Model.objects.all()
            vendor_list = Vendor.objects.order_by('name').values_list('name', flat=True).distinct()
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create Lists~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            security=Security(request,'Sales')
            sales_users=security.get_dept_users()
            sales_costing=security.get_costing_users()
            security=Security(request,'Engineering')
            eng_users=security.get_dept_users()
            eng_costing=security.get_costing_users()
            #print('eng_costing=',eng_costing)
            security=Security(request,'Test')
            test_users=security.get_dept_users()
            test_costing=security.get_costing_users()
            security=Security(request,'Stock')
            stock_users=security.get_dept_users()
            stock_costing=security.get_costing_users()
            security=Security(request,'Software')
            software_users=security.get_dept_users()
            software_costing=security.get_costing_users()
            security=Security(request,'Administrator')
            administrators=security.get_dept_users()
            admin_costing=security.get_costing_users()
            security=Security(request,'Design')
            design_users=security.get_dept_users()
            design_costing=security.get_costing_users()
            security=Security(request,'Manufacturing')
            manufacturing_users=security.get_dept_users()
            manuf_costing=security.get_costing_users()
            security=Security(request,'Quality')
            qa_users=security.get_dept_users()
            qa_costing=security.get_costing_users()
            security=Security(request,'Purchasing')
            purchasing_users=security.get_dept_users()
            Purchasing_costing=security.get_costing_users()
            security=Security(request,'Human Resources')
            hr_users=security.get_dept_users()
            hr_costing=security.get_costing_users()
            accounting_users=security.get_accounting_users()
            accounting_costing=security.get_costing_users()
            security=Security(request,'Senior Management')
            executives=security.get_dept_users()
            dept_managers=security.get_dept_Manager_list()
            dept_supervisors=security.get_dept_Supervisor_list()
            all_users=security.get_ticket_user_names()
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create Lists~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~active~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            active_user = security.get_active_user()
            active_user_name = security.get_active_user_name()
            active_user_firstname = security.get_active_user_firstname()
            security=Security(request,self.request.user.get_full_name())
            active_user_group = security.get_user_group() 
            security=Security(request,'Senior Management')    
            active_group=security.get_active_group()
            #print ("active_group ", active_group)
            active_manager=security.get_active_manager()
            active_executive=security.get_executive_manager()
            active_administrator=security.get_active_administrator()
            active_department_manager=security.get_dept_Manager()
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~active~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
           
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Assign Lists~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if active_executive or active_administrator:
                active_users=all_users #Manager/Admin can see all users
                assigned_list=all_users #Manager/Admin  can assign any user
                initiate_list=all_users#Manager/Admin  can change initiator
                active_costing_users=sales_costing
            elif active_department_manager and  'Sales' in active_group:
                active_users=all_users #Manager/Admin can see all users
                assigned_list=all_users #Manager/Admin  can assign any user
                initiate_list=all_users#Manager/Admin  can change initiator
                active_costing_users=sales_costing
            elif active_department_manager:
                active_users=all_users #Manager/Admin can see all users
                assigned_list=all_users #Manager/Admin  can assign any user
                initiate_list=all_users#Manager/Admin  can change initiator
                active_costing_users=get_active_costing_users(active_group,sales_costing,eng_costing,test_costing,stock_costing,software_costing,admin_costing,manuf_costing,design_costing,qa_costing,Purchasing_costing,hr_costing)
            elif 'Sales' in active_group:
                print('in sales')
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users #Sales gets to assign everyone
                initiate_list=all_users #active user is the only initiator
                active_costing_users=sales_costing
            elif 'Engineering' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=eng_costing
            elif 'Test' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=test_costing
            elif 'Stock' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=stock_costing
            elif 'Software' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=software_costing
            elif 'Administrator' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=admin_costing
            elif 'Manufacturing' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=manuf_costing
            elif 'Design' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=manuf_costing
            elif 'Quality' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=qa_costing
            elif 'Purchasing' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=Purchasing_costing
            elif 'Human Resources' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=hr_costing
            else:
                active_users=security.get_active_users() #users in your department
                assigned_list=active_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=[]
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"equipment/index.html",{"form": form, "models": models, 'vendor_list':vendor_list, "index_type":"EQUIPMENT",
                                                            'active_user':active_user,'active_user_name':active_user_name,'active_user_firstname':active_user_firstname,'active_user_group':active_user_group,'active_manager':active_manager,
                                                            'active_executive':active_executive,'active_administrator':active_administrator})
	   	
    def post(self, request, *args, **kwargs):
        form = self.form_class()
        search = request.POST.get('search', -1)
        vendor_list = Vendor.objects.order_by('name').values_list('name', flat=True).distinct()
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create Lists~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        security=Security(request,'Sales')
        sales_users=security.get_dept_users()
        sales_costing=security.get_costing_users()
        security=Security(request,'Engineering')
        eng_users=security.get_dept_users()
        eng_costing=security.get_costing_users()
        #print('eng_costing=',eng_costing)
        security=Security(request,'Test')
        test_users=security.get_dept_users()
        test_costing=security.get_costing_users()
        security=Security(request,'Stock')
        stock_users=security.get_dept_users()
        stock_costing=security.get_costing_users()
        security=Security(request,'Software')
        software_users=security.get_dept_users()
        software_costing=security.get_costing_users()
        security=Security(request,'Administrator')
        administrators=security.get_dept_users()
        admin_costing=security.get_costing_users()
        security=Security(request,'Design')
        design_users=security.get_dept_users()
        design_costing=security.get_costing_users()
        security=Security(request,'Manufacturing')
        manufacturing_users=security.get_dept_users()
        manuf_costing=security.get_costing_users()
        security=Security(request,'Quality')
        qa_users=security.get_dept_users()
        qa_costing=security.get_costing_users()
        security=Security(request,'Purchasing')
        purchasing_users=security.get_dept_users()
        Purchasing_costing=security.get_costing_users()
        security=Security(request,'Human Resources')
        hr_users=security.get_dept_users()
        hr_costing=security.get_costing_users()
        accounting_users=security.get_accounting_users()
        accounting_costing=security.get_costing_users()
        security=Security(request,'Senior Management')
        executives=security.get_dept_users()
        dept_managers=security.get_dept_Manager_list()
        dept_supervisors=security.get_dept_Supervisor_list()
        all_users=security.get_ticket_user_names()
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create Lists~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~active~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        active_user = security.get_active_user()
        active_user_name = security.get_active_user_name()
        active_user_firstname = security.get_active_user_firstname()
        security=Security(request,self.request.user.get_full_name())
        active_user_group = security.get_user_group() 
        security=Security(request,'Senior Management')    
        active_group=security.get_active_group()
        #print ("active_group ", active_group)
        active_manager=security.get_active_manager()
        active_executive=security.get_executive_manager()
        active_administrator=security.get_active_administrator()
        active_department_manager=security.get_dept_Manager()
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~active~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Assign Lists~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if active_executive or active_administrator:
            active_users=all_users #Manager/Admin can see all users
            assigned_list=all_users #Manager/Admin  can assign any user
            initiate_list=all_users#Manager/Admin  can change initiator
            active_costing_users=sales_costing
        elif active_department_manager and  'Sales' in active_group:
            active_users=all_users #Manager/Admin can see all users
            assigned_list=all_users #Manager/Admin  can assign any user
            initiate_list=all_users#Manager/Admin  can change initiator
            active_costing_users=sales_costing
        elif active_department_manager:
            active_users=all_users #Manager/Admin can see all users
            assigned_list=all_users #Manager/Admin  can assign any user
            initiate_list=all_users#Manager/Admin  can change initiator
            active_costing_users=get_active_costing_users(active_group,sales_costing,eng_costing,test_costing,stock_costing,software_costing,admin_costing,manuf_costing,design_costing,qa_costing,Purchasing_costing,hr_costing)
        elif 'Sales' in active_group:
            print('in sales')
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users #Sales gets to assign everyone
            initiate_list=all_users #active user is the only initiator
            active_costing_users=sales_costing
        elif 'Engineering' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=eng_costing
        elif 'Test' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=test_costing
        elif 'Stock' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=stock_costing
        elif 'Software' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=software_costing
        elif 'Administrator' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=admin_costing
        elif 'Manufacturing' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=manuf_costing
        elif 'Design' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=manuf_costing
        elif 'Quality' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=qa_costing
        elif 'Purchasing' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=Purchasing_costing
        elif 'Human Resources' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=hr_costing
        else:
            active_users=security.get_active_users() #users in your department
            assigned_list=active_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=[]
        print('search =',search)
        success = True
        if not search ==-1:
            models = Model.objects.filter(description__icontains=search) | Model.objects.filter(category__icontains=search) | Model.objects.filter(band__icontains=search) | Model.objects.filter(vendor__icontains=search) | Model.objects.filter(model__icontains=search) | Model.objects.filter(status__contains=search).all()
            if not models:
                models = Model.objects.all()
        else:
            models = Model.objects.all()

        return render (self.request,"equipment/index.html",{"form": form, "models": models, 'vendor_list':vendor_list, "index_type":"EQUIPMENT",
                                                            'active_user':active_user,'active_user_name':active_user_name,'active_user_firstname':active_user_firstname,'active_user_group':active_user_group,'active_manager':active_manager,
                                                            'active_executive':active_executive,'active_administrator':active_administrator})

class ModelView(View):
    form_class = ModelsForm
    template_name = "model.html"
    success_url = reverse_lazy('equipment:newmodel')
   
    def get(self, *args, **kwargs):
        form = self.form_class()
        try:
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create Lists~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            security=Security(request,'Sales')
            sales_users=security.get_dept_users()
            sales_costing=security.get_costing_users()
            security=Security(request,'Engineering')
            eng_users=security.get_dept_users()
            eng_costing=security.get_costing_users()
            #print('eng_costing=',eng_costing)
            security=Security(request,'Test')
            test_users=security.get_dept_users()
            test_costing=security.get_costing_users()
            security=Security(request,'Stock')
            stock_users=security.get_dept_users()
            stock_costing=security.get_costing_users()
            security=Security(request,'Software')
            software_users=security.get_dept_users()
            software_costing=security.get_costing_users()
            security=Security(request,'Administrator')
            administrators=security.get_dept_users()
            admin_costing=security.get_costing_users()
            security=Security(request,'Design')
            design_users=security.get_dept_users()
            design_costing=security.get_costing_users()
            security=Security(request,'Manufacturing')
            manufacturing_users=security.get_dept_users()
            manuf_costing=security.get_costing_users()
            security=Security(request,'Quality')
            qa_users=security.get_dept_users()
            qa_costing=security.get_costing_users()
            security=Security(request,'Purchasing')
            purchasing_users=security.get_dept_users()
            Purchasing_costing=security.get_costing_users()
            security=Security(request,'Human Resources')
            hr_users=security.get_dept_users()
            hr_costing=security.get_costing_users()
            accounting_users=security.get_accounting_users()
            accounting_costing=security.get_costing_users()
            security=Security(request,'Senior Management')
            executives=security.get_dept_users()
            dept_managers=security.get_dept_Manager_list()
            dept_supervisors=security.get_dept_Supervisor_list()
            all_users=security.get_ticket_user_names()
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create Lists~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~active~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            active_user = security.get_active_user()
            active_user_name = security.get_active_user_name()
            active_user_firstname = security.get_active_user_firstname()
            security=Security(request,self.request.user.get_full_name())
            active_user_group = security.get_user_group() 
            security=Security(request,'Senior Management')    
            active_group=security.get_active_group()
            #print ("active_group ", active_group)
            active_manager=security.get_active_manager()
            active_executive=security.get_executive_manager()
            active_administrator=security.get_active_administrator()
            active_department_manager=security.get_dept_Manager()
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~active~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
           
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Assign Lists~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if active_executive or active_administrator:
                active_users=all_users #Manager/Admin can see all users
                assigned_list=all_users #Manager/Admin  can assign any user
                initiate_list=all_users#Manager/Admin  can change initiator
                active_costing_users=sales_costing
            elif active_department_manager and  'Sales' in active_group:
                active_users=all_users #Manager/Admin can see all users
                assigned_list=all_users #Manager/Admin  can assign any user
                initiate_list=all_users#Manager/Admin  can change initiator
                active_costing_users=sales_costing
            elif active_department_manager:
                active_users=all_users #Manager/Admin can see all users
                assigned_list=all_users #Manager/Admin  can assign any user
                initiate_list=all_users#Manager/Admin  can change initiator
                active_costing_users=get_active_costing_users(active_group,sales_costing,eng_costing,test_costing,stock_costing,software_costing,admin_costing,manuf_costing,design_costing,qa_costing,Purchasing_costing,hr_costing)
            elif 'Sales' in active_group:
                print('in sales')
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users #Sales gets to assign everyone
                initiate_list=all_users #active user is the only initiator
                active_costing_users=sales_costing
            elif 'Engineering' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=eng_costing
            elif 'Test' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=test_costing
            elif 'Stock' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=stock_costing
            elif 'Software' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=software_costing
            elif 'Administrator' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=admin_costing
            elif 'Manufacturing' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=manuf_costing
            elif 'Design' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=manuf_costing
            elif 'Quality' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=qa_costing
            elif 'Purchasing' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=Purchasing_costing
            elif 'Human Resources' in active_group:
                active_users=security.get_active_users() #users in your department
                assigned_list=all_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=hr_costing
            else:
                active_users=security.get_active_users() #users in your department
                assigned_list=active_users
                initiate_list=[] #active user is the only initiator
                active_costing_users=[]
            model_id = self.request.GET.get('model_id', -1)
            print('model_id=',model_id)
            mod=-1
            form=-1
            uploaded_file_url=-1
            if model_id !=-1:
                mod = Model.objects.filter(id=model_id).all()
                mod = mod[0]
                uploaded_file_url=mod.image
                print('uploaded_file_url=',uploaded_file_url)
               
            models = Model.objects.all()
            vendor_list = Vendor.objects.order_by('name').values_list('name', flat=True).distinct()
            
            print(models)
            print(mod)
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"equipment/model.html",{"form": form, "models": models, "mod": mod, 'vendor_list':vendor_list, 'uploaded_file_url':uploaded_file_url,  "index_type":"EQUIPMENT",
                                                            'active_user':active_user,'active_user_name':active_user_name,'active_user_firstname':active_user_firstname,'active_user_group':active_user_group,'active_manager':active_manager,
                                                            'active_executive':active_executive,'active_administrator':active_administrator})
        
    def post(self, *args, **kwargs):
        timestamp = date.today()
        band = self.request.POST.get('_band',-1)
        category = self.request.POST.get('_category',-1)
        description = self.request.POST.get('_desc',-1)
        model = self.request.POST.get('_model',-1)
        vendor= self.request.POST.get('_vendor',-1)
        active = True
        image = self.request.POST.get('fileupload',-1)
        print('image=',image)
        comments = self.request.POST.get('_comments',-1)
        model_id = self.request.POST.get('m_id',-1)
        save = self.request.POST.get('_save',-1)
        print('save=',save)
        update = self.request.POST.get('_update',-1)
        print('update=',update)
        delete = self.request.POST.get('_delete',-1)
        print('delete=',delete)
        models = Model.objects.all()
        vendor_list = Vendor.objects.order_by('name').values_list('name', flat=True).distinct()
        mod=-1
        form=-1
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create Lists~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        security=Security(request,'Sales')
        sales_users=security.get_dept_users()
        sales_costing=security.get_costing_users()
        security=Security(request,'Engineering')
        eng_users=security.get_dept_users()
        eng_costing=security.get_costing_users()
        #print('eng_costing=',eng_costing)
        security=Security(request,'Test')
        test_users=security.get_dept_users()
        test_costing=security.get_costing_users()
        security=Security(request,'Stock')
        stock_users=security.get_dept_users()
        stock_costing=security.get_costing_users()
        security=Security(request,'Software')
        software_users=security.get_dept_users()
        software_costing=security.get_costing_users()
        security=Security(request,'Administrator')
        administrators=security.get_dept_users()
        admin_costing=security.get_costing_users()
        security=Security(request,'Design')
        design_users=security.get_dept_users()
        design_costing=security.get_costing_users()
        security=Security(request,'Manufacturing')
        manufacturing_users=security.get_dept_users()
        manuf_costing=security.get_costing_users()
        security=Security(request,'Quality')
        qa_users=security.get_dept_users()
        qa_costing=security.get_costing_users()
        security=Security(request,'Purchasing')
        purchasing_users=security.get_dept_users()
        Purchasing_costing=security.get_costing_users()
        security=Security(request,'Human Resources')
        hr_users=security.get_dept_users()
        hr_costing=security.get_costing_users()
        accounting_users=security.get_accounting_users()
        accounting_costing=security.get_costing_users()
        security=Security(request,'Senior Management')
        executives=security.get_dept_users()
        dept_managers=security.get_dept_Manager_list()
        dept_supervisors=security.get_dept_Supervisor_list()
        all_users=security.get_ticket_user_names()
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create Lists~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~active~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        active_user = security.get_active_user()
        active_user_name = security.get_active_user_name()
        active_user_firstname = security.get_active_user_firstname()
        security=Security(request,self.request.user.get_full_name())
        active_user_group = security.get_user_group() 
        security=Security(request,'Senior Management')    
        active_group=security.get_active_group()
        #print ("active_group ", active_group)
        active_manager=security.get_active_manager()
        active_executive=security.get_executive_manager()
        active_administrator=security.get_active_administrator()
        active_department_manager=security.get_dept_Manager()
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~active~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Assign Lists~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if active_executive or active_administrator:
            active_users=all_users #Manager/Admin can see all users
            assigned_list=all_users #Manager/Admin  can assign any user
            initiate_list=all_users#Manager/Admin  can change initiator
            active_costing_users=sales_costing
        elif active_department_manager and  'Sales' in active_group:
            active_users=all_users #Manager/Admin can see all users
            assigned_list=all_users #Manager/Admin  can assign any user
            initiate_list=all_users#Manager/Admin  can change initiator
            active_costing_users=sales_costing
        elif active_department_manager:
            active_users=all_users #Manager/Admin can see all users
            assigned_list=all_users #Manager/Admin  can assign any user
            initiate_list=all_users#Manager/Admin  can change initiator
            active_costing_users=get_active_costing_users(active_group,sales_costing,eng_costing,test_costing,stock_costing,software_costing,admin_costing,manuf_costing,design_costing,qa_costing,Purchasing_costing,hr_costing)
        elif 'Sales' in active_group:
            print('in sales')
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users #Sales gets to assign everyone
            initiate_list=all_users #active user is the only initiator
            active_costing_users=sales_costing
        elif 'Engineering' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=eng_costing
        elif 'Test' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=test_costing
        elif 'Stock' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=stock_costing
        elif 'Software' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=software_costing
        elif 'Administrator' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=admin_costing
        elif 'Manufacturing' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=manuf_costing
        elif 'Design' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=manuf_costing
        elif 'Quality' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=qa_costing
        elif 'Purchasing' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=Purchasing_costing
        elif 'Human Resources' in active_group:
            active_users=security.get_active_users() #users in your department
            assigned_list=all_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=hr_costing
        else:
            active_users=security.get_active_users() #users in your department
            assigned_list=active_users
            initiate_list=[] #active user is the only initiator
            active_costing_users=[]
        
        if not save==-1:	
            try:		
                Model.objects.create(description=description, category=category, band=band, vendor=vendor, model=model, 
                        comments=comments, status=active, last_update=timestamp)
                        
                m=Model.objects.filter(description=description,band=band, vendor=vendor, model=model)
                form = ModelsForm(self.request.POST, self.request.FILES, instance = m[0], use_required_attribute=False)
                print('form',form)       
                if form.is_valid():
                    print('form is valid')
                    form.save()
                mod = Model.objects.filter(description=description,band=band, vendor=vendor, model=model).all()
            except IOError as e:
                success = False
                print ("Models Save Failure ", e)
        elif not update==-1: 
            try:
                #update existing event
                Model.objects.filter(id=model_id).update(description=description, category=category, band=band, vendor=vendor, model=model, 
                        comments=comments, status=active, last_update=timestamp)
                m=Model.objects.filter(description=description, band=band, vendor=vendor, model=model)
                form = ModelsForm(self.request.POST, self.request.FILES, instance = m[0], use_required_attribute=False)
                print('form',form)       
                if form.is_valid():
                    print('form is valid')
                    form.save()
                mod = Model.objects.filter(description=description,band=band, vendor=vendor, model=model).all()
            except IOError as e:
                print ("Models Update Failure ", e)	
        elif not delete==-1: 
            try:
                Model.objects.filter(id=model_id).delete()
            except IOError as e:
                print ("Models Delete Failure ", e)		
        return render (self.request,"equipment/model.html",{"form": form, "models": models, 'vendor_list':vendor_list,  "mod": mod, "index_type":"EQUIPMENT",
                                                            'active_user':active_user,'active_user_name':active_user_name,'active_user_firstname':active_user_firstname,'active_user_group':active_user_group,'active_manager':active_manager,
                                                            'active_executive':active_executive,'active_administrator':active_administrator})

       


@login_required
def showimage(request):
    image_file = -1
    if request.method == 'POST': 
        form = ModelsForm(request.POST, request.FILES)
        print('form =',form)
        model_id=308
        print('model_id =',model_id)       
        instance = Model.objects.get(id=model_id)
        print('instance =',instance) 
        form = ModelsForm(request.POST or None, instance=instance)
            
        #print('imagefile =',imagefile)
        media_folder = settings.MEDIA_URL
        print('media_folder = ',media_folder)
        file_path = media_folder+image_file
        image_file = media_folder + imagefile
        
        os.rename(file_path,image_file)
       
        if form.is_valid(): 
            form.save() 
    else: 
        form = ModelsForm()
        imagefile = request.POST.get('photo',-1)
        #print('imagefile =',imagefile)
    return render(request, 'equipment/images.html', {'form' : form}) 
   

@login_required
def savemodel(request):
    if request.method == 'POST':
        model_id = request.POST.get('m_id',-1)
        models = Model.objects.all()
        print('model_id=',model_id)
        mod = Model.objects.filter(id__contains=model_id)
        mod=mod[0]
        print('mod=',mod)
        try:        
            image_file = request.FILES.get('_upload',-1)
        except IOError as e:
             image_file = -1
        print('image_file=',image_file)  
        if image_file==-1 or image_file=='inv1.jpg' or image_file== None or image_file== "":
            image_file = mod.image_file
            print(image_file)
            uploaded_file_url = mod.photo
            print('uploaded_file_url =',uploaded_file_url )
        else:    
            myfile = request.FILES['_upload']
            print('MYFILE =', myfile)
            fs = FileSystemStorage()
            print('fs=',fs)
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            print('uploaded_file_url =',uploaded_file_url )
            print(image_file)
            
        if uploaded_file_url == None or uploaded_file_url =="":
            uploaded_file_url='/ATS/media/inv1.jpg' 
            image_file='inv1.jpg'
        
        timestamp = date.today()
        band = request.POST.get('_band',-1)
        category = request.POST.get('_category',-1)
        description = request.POST.get('_desc',-1)
        model = request.POST.get('_model',-1)
        vendor= request.POST.get('_vendor',-1)
        active = True
        comments = request.POST.get('_com',-1)
        if comments==-1:
            comments=""
        print('comments=',comments)
        save = request.POST.get('_save',-1)
        update = request.POST.get('_update',-1)
        delete = request.POST.get('_delete',-1)
        
                      
        if not save==-1:	
            try:		
                Model.objects.create(description=description, category=category, band=band, vendor=vendor, model=model, comments=comments, 
                            image_file=image_file, photo=uploaded_file_url, status=active, last_update=timestamp)
                if pic_form.is_valid():
                    pic_form.save()
            except IOError as e:
                success = False
                print ("Models Save Failure ", e)
        elif not update==-1: 
            try:
                #update existing event
                Model.objects.filter(id=model_id).update(description=description, category=category, band=band, vendor=vendor, model=model, 
                        comments=comments, image_file=image_file, photo=uploaded_file_url, status=active, last_update=timestamp)
            except IOError as e:
                print ("Models Update Failure ", e)	
        elif not delete==-1: 
            try:
                Model.objects.filter(id=model_id).delete()
            except IOError as e:
                print ("Models Delete Failure ", e)		
        return render(request,"equipment/model.html",{"models": models, "mod": mod, "image_file":image_file, 'uploaded_file_url':uploaded_file_url,  "index_type":"Model"})