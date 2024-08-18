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
from atspublic.models import Blog, Category, Visitor
from ATS.overhead import Comunication, Email, Style, Security
from django.contrib.auth.models import User
from users.models import UserProfileInfo
from django.db.models import Q
#from django.shortcuts import render_to_response, get_object_or_404
 
   
# Create your views here.
def index(request):
    template_name = "index.html"
    success_url = reverse_lazy('atspublic:public')
    timestamp = date.today()
    security = Security(request,'signup')
    error_message=''
    visitor=''
    #error_message = security.visitor_monitor()
    #print('security = ', security.visitor_monitor())
    #email = security.get_email()
    #visitor = security.get_visitor()
    #print('error_message=',error_message)
    '''
    if error_message !=-1:
        return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
    '''
    return render(request,'atspublic/index.html',{"error_message":error_message,"visitor":visitor})

class SignupView(View):
    template_name = "signup.html"
    success_url = reverse_lazy('atspublic:signup')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            timestamp = date.today()
            #security = Security(self.request,'signup')
            #error_message = security.visitor_monitor()
            #email = security.get_email()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            
            client_id=security.get_client_id()
            print('client_id=',client_id)
            phone_list = security.get_monitor_phone_list()
            print('phone_lis=',phone_list)
            message = 'ATS ' + visitor +' is Signing up for updates and news letters.\n' + 'Client_Id:  ' + client_id 
            print(message)
            com=Comunication(phone_list,message)
            print('com=',com)
            com.send_sms()
            success = True
            
        except IOError as e:
            print('error = ',e) 
        return render(self.request,'signup.html',{"error_message": error_message,'email':email, "visitor": visitor})
    
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            timestamp = date.today()
            print("in POST")
            username = self.request.POST.get('_user_name', -1)
            print('username=',username)
            email = self.request.POST.get('_email', -1)
            email_list = [email]
            print('email=',email_list)
            error_message = -1
            security = Security(self.request,'signup')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            client_id=security.get_client_id()
            user_agent=security.get_user_agent()
            session_id = security.get_session_id()
            visitor_ip = security.get_visitor_ip()
            phone_list = security.get_security_phone_list()
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Save ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if Visitor.objects.filter(visitor=username).exists():
                error_message = 'Username: ' + username + ' already exists please choose another'
                return render(self.request,'signup.html',{"error_message": error_message,'email':email})
            else:
                Visitor.objects.create(visitor=visitor,email=email,session_id=session_id,client_id=client_id,
                                    user_agent=user_agent,visitor_ip=visitor_ip,created_on=timestamp,last_entry=timestamp)
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~Send Message ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            subject = 'Welcome to Automated Test Solutions' 
            email_body = 'Hello ' + username + ' Nice to meet you!\n\nYou are now on the ATS list to recieve our News Letter, price updates, and any new technology advances.\n\nThanks,\nATS Staff\nhttps://automatedtestsolutions.herokuapp.com/.'
            print(email_body)
            email=Email(email_list,subject, email_body)
            print('email=',email)
            email.send_email()
           
            
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        return render(self.request,'signup.html',{"error_message": error_message, "visitor": visitor})
        
class SigninView(View):
    template_name = "signin.html"
    success_url = reverse_lazy('atspublic:signin')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            timestamp = date.today()
            username = self.request.POST.get('_user_name', -1)
            print('username=',username)
            email = self.request.POST.get('_email', -1)
            email_list = [email]
            print('email=',email_list)
            security = Security(self.request,'signin')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
           
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            visitor = security.get_visitor()
            client_id=security.get_client_id()
            phone_list = security.get_monitor_phone_list()
            email_list = security.get_monitor_email_list()
            cookie = security.get_cookie()
            
            print(self.request.user)        
            message = 'ATS ' + visitor +' is Signing up for updates and news letters.\n' + 'Client_Id:  ' + client_id 
            print(message)
            com=Comunication(phone_list,message)
            print('com=',com)
            com.send_sms()
            success = True
            success = True
        except IOError as e:
            print('error = ',e) 
        return render(self.request,'signin.html',{"inventory": inv})
    
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            timestamp = date.today()
            print("in POST")
            username = self.request.POST.get('_user_name', -1)
            print('username=',username)
            email = self.request.POST.get('_email', -1)
            email_list = [email]
            print('email=',email_list)
            error_message = -1
            security = Security(self.request,'signup')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            client_id=security.get_client_id()
            user_agent=security.get_user_agent()
            session_id = security.get_session_id()
            visitor_ip = security.get_visitor_ip()
            phone_list = security.get_security_phone_list()
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Save ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if Visitor.objects.filter(Q(visitor=username) | Q(session_id=session_id) | Q(visitor_ip=visitor_ip) | Q(user_agent=user_agent)).exists():
                Visitor.objects.filter(Q(visitor=username) | Q(session_id=session_id) | Q(visitor_ip=visitor_ip) | Q(user_agent=user_agent)).update(visitor=username,email=email,session_id=session_id,client_id=client_id,
                                    user_agent=user_agent,visitor_ip=visitor_ip,created_on=timestamp,last_entry=timestamp)
            else:
                error_message = 'Username: ' + username + ' does not exist in out database. please signup'
                return render(self.request,'signup.html',{"error_message": error_message,'email':email})
            
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        return render(self.request,'signin.html',{"visitor": visitor})

class TestimonialView(View):
    template_name = "testimonial.html"
    success_url = reverse_lazy('atspublic:testimonial')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            security = Security(self.request,'testimonial')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            success = True
        except IOError as e:
            print('error = ',e) 
        return render(self.request,'testimonial.html',{"visitor": visitor})
    
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            security = Security(self.request,'testimonial')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        return render(self.request,'testimonial.html',{"visitor": visitor})
        
class ContactView(View):
    template_name = "contact_us.html"
    success_url = reverse_lazy('atspublic:contacts')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            timestamp = date.today()
            security = Security(self.request,'contact us')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            client_id=security.get_client_id()
            visitor_ip = security.get_visitor_ip()
            phone_list = security.get_monitor_phone_list()
                                 
            success = True
        except IOError as e:
            print('error = ',e) 
        return render(self.request,'contact_us.html',{"visitor": visitor})
    
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            timestamp = date.today()
            print("in POST")
            username = self.request.POST.get('_user_name', -1)
            print('username=',username)
            email = self.request.POST.get('_email', -1)
            user_email = [email]
            message = self.request.POST.get('_message', -1)
            print('email123=',user_email)
            print('message=',message)
            error_message = -1
            security = Security(self.request,'contact us')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            #if error_message !=-1:
             #   return render(self.request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            client_id=security.get_client_id()
            user_agent=security.get_user_agent()
            session_id = security.get_session_id()
            visitor_ip = security.get_visitor_ip()
            phone_list = security.get_contactus_phone_list()
            email_list = security.get_contactus_email_list()
            print('email_list1234=',email_list)
            print('phone_list1234=',phone_list)
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Save ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if not Visitor.objects.filter(Q(visitor=username) | Q(session_id=session_id) | Q(visitor_ip=visitor_ip) | Q(user_agent=user_agent)).exists():
                Visitor.objects.create(visitor=visitor,email=email,session_id=session_id,client_id=client_id,
                                    user_agent=user_agent,visitor_ip=visitor_ip,created_on=timestamp,last_entry=timestamp)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Save ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
           
           #~~~~~~~~~~~~~~~~~~~~~~~~~~~~Send Message to user ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            subject = 'Automated Test Solutions'
            email_body = 'Hello ' + username + ' We have recieved your request and we will contact you soon.\n\nThanks,\nATS Staff\nhttps://automatedtestsolutions.herokuapp.com/.'
            print(email_body)
            email=Email(user_email,subject, email_body)
            email.send_email()
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~Send Message ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~Send Message to staff ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            subject = 'Customer Contact Request'
            email_body = message
            email=Email(email_list,subject, email_body)
            print('email=',email)
            email.send_email()
            mes= 'Customer Contact Request. Check your email' 
            com=Comunication(phone_list,mes)
            print('com=',com)
            com.send_sms()
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~Send Message to staff ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        return render(self.request,'contact_us.html',{"visitor": visitor})

class NewsView(View):
    template_name = "newsletter.html"
    success_url = reverse_lazy('atspublic:news')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            timestamp = date.today()
            security = Security(self.request,'News letter')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            visitor = security.get_visitor()
            client_id=security.get_client_id()
            visitor_ip = security.get_visitor_ip()
            phone_list = security.get_monitor_phone_list()
                                 
            print(self.request.user)        
            message = 'ATS ' + visitor +' is visiting news letters.\n' + 'Client_Id:  ' + client_id 
            print(message)
            com=Comunication(phone_list,message)
            print('com=',com)
            com.send_sms()
            success = True
        except IOError as e:
            print('error = ',e) 
        return render(self.request,'newsletter.html',{"visitor": visitor})
    
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            timestamp = date.today()
            security = Security(self.request,'News letter')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        return render(self.request,'newsletter.html',{"inventory": inv})
        
class BlogView(View):
    template_name = "blog.html"
    success_url = reverse_lazy('atspublic:blog')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            security = Security(self.request,'blog')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            success = True
        except IOError as e:
            print('error = ',e) 
        return render(self.request,'view_category.html', {'category': category,'posts': Blog.objects.filter(category=category)[:5]})
    
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            security = Security(self.request,'blog')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            if error_message !=-1:
                return render(self.request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        return render(self.request,'view_category.html', {'category': category,'posts': Blog.objects.filter(category=category)[:5]})
       

class CategoryView(View):
    template_name = "blog.html"
    success_url = reverse_lazy('atspublic:view_category_post')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            #slug = request.POST.get('slug', -1)
            #category = get_object_or_404(Category, slug=slug)
            category = -1
            security = Security(self.request,'robot')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        return render(self.request,'view_category.html', {'category': category,"visitor": visitor, 'posts': Blog.objects.filter(category=category)[:5]})
 

# Create your views here.
class PostView(View):
    template_name = "view_post.html"
    success_url = reverse_lazy('atspublic:view_blog_post')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            category = -1
            security = Security(self.request,'blog')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        #return render(self.request,'view_post.html', {'post': get_object_or_404(Blog, slug=slug)}) 
        return render(self.request,'view_post.html') 
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        #return render(self.request,'view_post.html', {'post': get_object_or_404(Blog, slug=slug)})
        return render(self.request,'view_post.html') 

# Create your views here.
class PublicView(View):
    template_name = "index.html"
    success_url = reverse_lazy('atspublic:public')
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in index Get')
            success = True
            security = Security(self.request,'ATS')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
           
        except IOError as e:
            print('error = ',e) 
        return render (self.request,"index.html",{"visitor": visitor})
    
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        print('inv_list',inv)
        return render (self.request,"index.html",{"visitor": visitor})

		   
class WorkstationView(View):
    template_name = "racks.html"
    success_url = reverse_lazy('atspublic:racks')
	
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            security = Security(self.request,'workstation')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            success = True
        except IOError as e:
            print('error = ',e) 
        return render (self.request,"racks.html",{"visitor": visitor})
		
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            security = Security(self.request,'workstation')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        print('inv_list',inv)
        return render (self.request,"racks.html",{"visitor": visitor})
        
class RobotView(View):
    template_name = "robotLab.html"
    success_url = reverse_lazy('atspublic:robot')
	
    def get(self, *args, **kwargs):
        inv=-1
        try:
            security = Security(self.request,'robot')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            video = self.request.GET.get('video', -1)
            print('video=',video)
            print('in Get')
            success = True
        except IOError as e:
            print('error = ',e) 
        return render (self.request,"robotLab.html",{"visitor": visitor, 'video':video})
		
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            security = Security(self.request,'robot')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        print('inv_list',inv)
        return render (self.request,"robotLab.html",{"visitor": visitor})
        
class FieldView(View):
    template_name = "field.html"
    success_url = reverse_lazy('atspublic:site')
	
    def get(self, *args, **kwargs):
        inv=-1
        try:
            print('in Get')
            video=-1
            security = Security(self.request,'field')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            success = True
        except IOError as e:
            print('error = ',e) 
        return render (self.request,"field.html",{"visitor": visitor})
		
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            security = Security(self.request,'field')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        print('inv_list',inv)
        return render (self.request,"field.html",{"inventory": inv, 'video':video})
        
class SoftwareView(View):
    template_name = "software.html"
    success_url = reverse_lazy('atspublic:software')
	
    def get(self,request, *args, **kwargs):
        inv=-1
        try:
            print('in Software Get')
            security = Security(self.request,'Software')
            error_message = security.visitor_monitor()
            print('error_message=',error_message)
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
           
            success = True
        except IOError as e:
            print('error = ',e) 
        return render (self.request,"software.html",{"visitor": visitor})
		
    def post(self, request, *args, **kwargs):
        inv=-1
        try: 
            print("in POST")
            security = Security(self.request,'software')
            error_message = security.visitor_monitor()
            visitor = security.get_visitor()
            
            if error_message !=-1:
                return render(request,'blocked.html',{"error_message":error_message,"visitor":visitor})
            
            success = True
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        print('inv_list',inv)
        return render (self.request,"software.html",{"visitor": visitor})
