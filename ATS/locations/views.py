from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from .forms import LocationForm
from datetime import date
from django.urls import reverse,  reverse_lazy
from ATS.overhead import TimeCode, Security,Email,Costing,DateCode,Greetings,StringThings
from locations.models import Location
from inventory.models import Inventory, Events
from django.views import View
site_id = 0

class UserLogin(View):
    template_name = "user_login.html"
    success_url = reverse_lazy('locations:login')
        
    def get(self, *args, **kwargs):
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
            operator = str(self.request.user.get_short_name())
        
        except IOError as e:
           print('error = ',e) 
        return render(request, 'locations/user_login.html', {})
 
    def post(self, request, *args, **kwargs):
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
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    redirect_to = resolve_url(LOGIN_REDIRECT_URL)
                    print('redirect =',LOGIN_REDIRECT_URL)
                    return render(request,'locations/index.html')
                else:
                    return render(request, 'locations/user_login.html', {'message':'Login Failed!!'})
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
            return render(request, 'locations/user_login.html', {'message':'Login Failed!!'})
        else:
            return render(request, 'locations/user_login.html', {})

class LocationView(View):
    form_class = LocationForm
    template_name = "index.html"
    success_url = reverse_lazy('locations:location')
    
    def get(self, request, *args, **kwargs):
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
            locations = Location.objects.all()
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"locations/index.html",{"form": form, "locations":locations, "index_type":"SIGNIN", "UserN":self.request.user, "index_type":"SITE LOCATIONS",
                                                            'active_user':active_user,'active_user_name':active_user_name,'active_user_firstname':active_user_firstname,'active_user_group':active_user_group,'active_manager':active_manager,
                                                           'active_executive':active_executive,'active_administrator':active_administrator})
        
    def post(self, request, *args, **kwargs):
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
        if request.method == 'POST':
            timestamp = date.today()
            type = request.POST.get('_type', -1)
            print('type=',type)
            name = request.POST.get('_name', -1)
            address = request.POST.get('_addr', -1)
            city = request.POST.get('_city', -1)
            state = request.POST.get('_state', -1)
            zip_code = request.POST.get('_zip', -1)
            phone = request.POST.get('_phone', -1)
            lat = request.POST.get('_lat', -1)
            lng = request.POST.get('_lng', -1)
            email = request.POST.get('_email', -1)
            website = request.POST.get('_web', -1)
            save = request.POST.get('_save', -1)
            update = request.POST.get('_update', -1)
            delete = request.POST.get('_delete', -1)
            id = request.POST.get('_id', -1)
            print('id=',id)
            inventory_id = None
            active=True
            try:        
                if save !=-1:
                    Location.objects.create(name=name, address=address, city=city, state=state, zip_code=zip_code, phone=phone, email=email, website=website,
                            active=active, inventory_id=inventory_id, created_on=timestamp, last_entry=timestamp, lat=lat, lng=lng,type=type)
                elif update !=-1:
                    Location.objects.filter(id=id).update(name=name, address=address, city=city, state=state, zip_code=zip_code, phone=phone, email=email, website=website,
                                active=active, inventory_id=inventory_id, created_on=timestamp, last_entry=timestamp, lat=lat, lng=lng,type=type)
                elif delete !=-1:
                    Location.objects.filter(id=id).delete()

            except IOError as e:
                print ("location Save Failure ", e)	
        return render (self.request,"locations/index.html",{"index_type":"SIGNIN", "UserN":self.request.user, "index_type":"SITE LOCATIONS",
                                                            'active_user':active_user,'active_user_name':active_user_name,'active_user_firstname':active_user_firstname,'active_user_group':active_user_group,'active_manager':active_manager,
                                                            'active_executive':active_executive,'active_administrator':active_administrator})

def save_csv(delete):               
    #~~~~~~~~~~~Load location database from csv. must put this somewhere else later"
    import csv
    timestamp  = date.today()
    CSV_PATH = 'locations.csv'
    print('csv = ',CSV_PATH)

    contSuccess = 0
    # Remove all data from Table
    Location.objects.all().delete()

    f = open(CSV_PATH)
    reader = csv.reader(f)
    print('reader = ',reader)
    for name, address, city, state,zip_code, phone, email, website, lat, lng, created_on ,last_entry in reader:
        if lat=="": lat=40.815320
        if lng=="": lng=-73.237710
        Location.objects.create(name=name, address=address, city=city, state=state, zip_code=zip_code, phone=phone, email=email,
                 website=website,active=True, lat=float(lat), lng=float(lng), created_on=timestamp, last_entry=timestamp)
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')
    
             
   	
def site(request,location_id):
    sites = []
    site = []
    print('we are here')
    # cast the request inventory_id from string to integer type.
    location_id = int(location_id)
    print('location_id=',location_id)
    success = True 
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
        sites = Location.objects.all()
        for site1 in sites:
            if site1.id ==location_id:
                site = site1
                break
        lat = float(site.lat)
        print(lat)
        lng = float(site.lng)
        print(lng)
    except IOError as e:
        print ("load model Failure ", e)
        print('error = ',e) 
    return render(request,"locations/site.html",{"sites": sites, "site": site, "lat":lat, "lng":lng, "index_type":"Model",'location_id':location_id,
                                                'active_user':active_user,'active_user_name':active_user_name,'active_user_firstname':active_user_firstname,'active_user_group':active_user_group,'active_manager':active_manager,
                                                'active_executive':active_executive,'active_administrator':active_administrator})
	
def searchsite(request):
    json_data = []
    row_header = []
    
    success = True  
    try:
        site_list = location.objects.all()
    except IOError as e:
        success = False
        print ("Sitelist load Failure ", e)    
	 
    if site_list == None:
        success = False
    else:
        site=[e.serialize() for e in site_list]
    return jsonify({"success": success, "site_list": site})
