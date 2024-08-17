import math
import os, requests
from django.http import request
#from client.models import Clients
#from contractors.models import Contractors
#from googlevoice import Voice
#from googlevoice.util import input
import sys
from datetime import date, datetime, timedelta
import datetime as dt
from calendar import WEDNESDAY
from django.utils import timezone
from BCSystems import settings
from BCSystems.settings import BASE_DIR
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from ics import Calendar, Event 
import icalendar
from django.template import loader,Context,Template
from users.models import UserProfileInfo
from django.contrib.auth.models import User
from django.db.models import Q
#from atspublic.models import Visitor
from django.shortcuts import render
import configparser
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from users.models import UserProfileInfo
import ast
import pytz
from mimetypes import guess_type
from os.path import basename
import html2text
import random
import shutil

#import lxml.html
#import lxml.html.clean

class Greetings:
    def hello():
        hour = datetime.now().hour
        response = "Good morning" if 5<=hour<12 else "Good afternoon" if hour<18 else "Good evening"
        return response
       
    def how_are_you():
        hour = datetime.now().hour
        morning=["What's your agenda for the day?", "Have a great day!", "Have a great morning!","Have you checked your Leader Standard?", "What are your goals for this morning?", "Hope you're doing well!","We need to talk! LOL"]
        afternoon=["Hope you're having a great week!", "Hope you're having a great day!", "How's you're day going?", "Hope you're doing well!", "Hope you're doing well!","Did you meet your goals this morning?", "What are your goals for this afternoon?"]
        evening=["Hope you're having a great week!", "Hope you had a great day!", "How's you're day going?", "Where did the day go?", "DMS says..Go Home!!! Its late", "Hope you're doing well!","Did you meet your goals this afternoon?", "It's getting late. Don't forget your home life","We need to talk! LOL"]
        hope = morning if 5<=hour<12 else afternoon if hour<18 else evening
        response = random.choice(hope)
        return response

def get_customer_code_id(customer_code):
    customer_code=Customer_Code.objects.using('E2').filter(customer_code=customer_code).last()
    if customer_code:
        customer_code_id=customer_code.customer_code_id
    else:
        customer_code_id=0
    
    return customer_code_id 


def check_bad_orders(today):# Test to see if an email address is include in this order
    try:
        days=1 # end_date is today -1
        time_code = TimeCode(days)
        hour = time_code.this_hour()
        yesterday = time_code.today_minus().date() # yesterday is today - days 
        bad_orders=Order_Header.objects.using('E2').exclude(customer_code='IPPMISC').exclude(customer_code='IPP').exclude(customer_code='IPP-STOCK').exclude(customer_code='STOCKIT').filter(company_code='IPPSQL',status='Open',notification_email_address='').all()
        order_number_list=[]
        return_list=[]
        for bad_order in bad_orders:
            order_header_id=bad_order.order_header_id
            customer_code=bad_order.customer_code
            customer_code_id=get_customer_code_id(customer_code)
            order_number=bad_order.order_number
            order_number_list.append(order_number)
            order_date=bad_order.due_date
            customer_po_number=bad_order.customer_po_number
            order_detail=Order_Detail.objects.using('E2').filter(order_header_id=order_header_id).last()
            if order_detail:
                order_detail_id=order_detail.order_detail_id
                job_number=order_detail.job_number
                part_number=order_detail.part_number
            else:
                order_detail_id='N/A'
                job_number='N/A'
                part_number='N/A'
            if not 'TF' in part_number:
                if  Bad_Order.objects.filter(order_number=order_number).exists():
                    Bad_Order.objects.filter(order_number=order_number).update(timestamp=today)
                else:
                    Bad_Order.objects.create(order_number=order_number,order_header_id=order_header_id,customer_code=customer_code,customer_code_id=customer_code_id,order_date=order_date,customer_po_number=customer_po_number,
                                        order_detail_id=order_detail_id,job_number=job_number,part_number=part_number,closed=False,checked_date=yesterday)
    
        #~~~~~~~~~~~~~~~~~close old bad orders in the DMS table~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        bad_order_list=Bad_Order.objects.filter(closed=False).all()# Get all open bad orders
        for order in bad_order_list:
            if not order.closed:
                if not order.order_number in order_number_list: #order is open in DMS, But closed in E2
                    Bad_Order.objects.filter(order_number=order_number).update(timestamp=today,closed=True)
        #~~~~~~~~~~~~~~~~~close old bad orders in the DMS table~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
        return_list=Bad_Order.objects.exclude(checked_date=today).filter(closed=False).all()# Get all open bad ordersfor bad_order in bad_orders:
        return return_list
    
    except IOError as e:
        print ("Lists load Failure ", e)
        return return_list


def get_connection(backend=None, fail_silently=False, **kwds):
    """Load an email backend and return an instance of it.

    If backend is None (default), use settings.EMAIL_BACKEND.

    Both fail_silently and other keyword arguments are used in the
    constructor of the backend.
    """
    klass = import_string(backend or settings.EMAIL_BACKEND)
    return klass(fail_silently=fail_silently, **kwds)


def update_name_list(pick_list,name_list):
    this_list=[]
    x=0
    #print('pick_list=',pick_list,' name_list',name_list)
    for name in name_list:
        try:
            if 'True' in pick_list[x]:
                this_list.append(name)
            
        except IndexError as e:
           print('error=',e)
            
        x+=1   
    #print('this_list=',this_list)
    return this_list

def format_time(date,this_time):
   #print('date=',date)
    temp=str(this_time).split()
   #print('this_time=',this_time)
    temp=str(temp[0]).split(":")
   #print('this_time temp=',temp)
    this_hour=temp[0]
    this_minute=temp[1]
    this_second=temp[2]
    temp=str(date).split()
    temp=str(temp[0]).split("-")
   #print('temp=',temp)
    this_year=temp[0]
    this_month=temp[1]
    this_day=temp[2]
    new_time= this_year + this_month + this_day + 'T' + this_hour + this_minute + this_second
   #print('converted time=',new_time)
    # accepted standard
    #July 14, 1997, at 1
    #19970714T133000
    return new_time

def update_settings(address_type):
    if address_type=='SHIPPING':
        src_file='c:\\src\\ipp\\ipp\\settings_shipping.py'
    elif address_type=='CI':
        src_file='c:\\src\\ipp\\ipp\\settings_ci.py'
    else:
        src_file='c:\\src\\ipp\\ipp\\settings_tickets.py'
    dest_file='c:\\src\\ipp\\ipp\\settings.py'
    
    shutil.copy(src_file, dest_file) 
    #print('src_file=',src_file)
    #print('dest_file=',dest_file)

class INI_Files:
    def __init__ (self, path,section,key,value):
        self.path = path
        self.section = section
        self.key = key
        self.value = str(value)
        
    def get_label_values(self):
        try:
            config = configparser.ConfigParser()
            config.read(self.path)      # Read f
        except IOError as e:
            print ("Couldn't open {path}: {reason}".format(path=self.path, reason=e))
        else:
            #speak.talk(config.sections())
            po_num = config.get("Label", "po_num")
            customer_part = config.get("Label", "customer_part")
            part_num = config.get("Label", "part_num")
            date_code_list1 = config.get("Label", "date_code_list")
            job_list = config.get("Label", "job_list")
            barcode = config.get("Label", "barcode")
            quantity_list = config.get("Label", "quantity_list")
            description = config.get("Label", "description")
                               
            return (po_num,customer_part,part_num,date_code_list1,job_list,barcode,quantity_list,description)
    
    def set_values(self):
        config = configparser.ConfigParser(delimiters=(':'))
        config.read(self.path)
        cfgfile = open(self.path, 'w')
        config.set(self.section, self.key, self.value)
        config.write(cfgfile)
        cfgfile.close()



#https://data-flair.training/blogs/django-send-email/
class Email:
    def __init__ (self,recepient_list,cc_list,bcc_list,subject,message,attachment):
        self.subject = subject
        self.message = message
        self.recepient = recepient_list
        self.cc = cc_list
        self.bcc = bcc_list
        self.attachment=attachment
        #print('recepient=',self.recepient)
        if not isinstance(self.recepient, list):
            self.recepient = [self.recepient]
            #print('recepient=',self.recepient)
    
    def send_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        res = send_mail(self.subject, self.message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False)
        #print('response=',res)
        return res
        
    
    def send_shipment_notifications_fail(self):
        #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\shipping\\templates\\shipping\\' + 'customer_notifications_fail.html')
        message=''
        customer=self.message
        subject= 'Missing Contact Info (' + str(customer) + ')'
        tracking_number=self.subject[0]
        po_number=self.subject[1]
        shipment_number=self.subject[2]
        tracking_link=self.subject[3]
        if self.attachment=='No Attachment':
            attachments =[]
        else:
            attachments = [self.attachment]
        num_attached=len(attachments)
        #~~~~~~~~~~~~~~~~~~~~~~~~~Code for using a second password ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        #https://docs.djangoproject.com/en/4.0/_modules/django/core/mail/#:~:text=New%20code%20wanting%20to%20extend%20the%20functionality%20should,recipient_list%2C%20connection%3Dconnection%29%20if%20html_message%3A%20mail.attach_alternative%28html_message%2C%20%22text%2Fhtml%22%29%20return%20mail.send%28%29
        #connection = connection or get_connection(username=auth_user,password=auth_password, fail_silently=fail_silently,)
        #message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER2, self.recepient, cc=self.cc, bcc=self.bcc,connection=connection)
        #~~~~~~~~~~~~~~~~~~~~~~~~~Code for using a second password ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        
        html_message = loader.render_to_string(file_path, {'tracking_number':tracking_number,'po_number':po_number,'shipment_number':shipment_number,'customer':customer,'num_attached':num_attached,'tracking_link':tracking_link})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        for attachment in attachments:
            try:
                message.attach_file(attachment)
                old_way=True
            except BaseException as e:
                print ("Couldn't open self.attachment" , e)
        print('attachments',attachments)
        res = message.send()   
        return res
        
    def send_shipment_notifications(self):
        #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\shipping\\templates\\shipping\\' + 'customer_notifications.html')
        message=''
        customer=self.message
        subject= 'Shipment Notification (' + str(customer) + ')'
        tracking_number=self.subject[0]
        po_number=self.subject[1]
        shipment_number=self.subject[2]
        tracking_link=self.subject[3]
        if self.attachment=='No Attachment':
            attachments =[]
        else:
            attachments = [self.attachment]
        num_attached=len(attachments)
       
        
        html_message = loader.render_to_string(file_path, {'tracking_number':tracking_number,'po_number':po_number,'shipment_number':shipment_number,'customer':customer,'num_attached':num_attached,'tracking_link':tracking_link})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        for attachment in attachments:
            try:
                message.attach_file(attachment)
                old_way=True
            except BaseException as e:
                print ("Couldn't open self.attachment" , e)
        print('attachments',attachments)
        res = message.send()   
        return res
    
    def send_quote_flag_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_quote_flag.html')
        opp=self.message
        part=self.attachment
        subject= 'Opportunity Ticket#' + str(opp.pk) + ' --QUOTE REMINDER--'
        message=''
        firstname_arr = opp.owner
        #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
        
        #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'opp':opp,'firstname':firstname,'subject':subject,'part':part})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        res = message.send()   
        return res
    
    
    def send_samples_flag_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_sample_flag.html')
        ticket=self.message
        subject= 'Reminder Ticket#' + str(ticket.pk) + ' --SAMPLE REMINDER--'
        message=ticket.description
        firstname_arr = ticket.assigned
        #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
        
        #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'ticket':ticket,'firstname':firstname,'subject':subject})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = RMA_Attachments.objects.select_related().filter(ticket = ticket.pk).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        
        for attachment in attachments:
           #print('attachment1',attachment)
            if attachment.name!='N/A':
                try:
                    if self.attachment!='N/A':
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        
        res = message.send()   
        return res
    
    def send_RMA_red_flag_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\rma\\templates\\rma\\' + 'email_RMA_red_flag.html')
       #print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~file_path=',file_path)
        rma=self.message
        eng_test=self.attachment
        
        subject=self.subject
        dept=self.bcc
        if self.subject == 'RMA Stop Work':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --STOP WORK--'
        else:
            subject= 'RMA Ticket#' + str(rma.pk) + ' --RESUME WORK--'
        message= ''
        
        #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'rma':rma,'eng_test':eng_test,'subject':subject,'dept':dept})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=[])
        message.attach_alternative(html_message, "text/html")
        attachments = RMA_Attachments.objects.select_related().filter(ticket = rma.pk).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        
        for attachment in attachments:
           #print('attachment1',attachment)
            if attachment.name!='N/A':
                try:
                    if self.attachment!='N/A':
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        
        res = message.send()   
        return res
    
    def send_RMA_late_flag_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\rma\\templates\\rma\\' + 'email_RMA _late_flag.html')
       #print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~file_path=',file_path)
        message=self.message
        rma=self.attachment
        
        subject=self.subject
        dept=self.bcc
        
        
        #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'rma':rma,'message':message,'subject':subject,'dept':dept})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=[])
        message.attach_alternative(html_message, "text/html")
        attachments = RMA_Attachments.objects.select_related().filter(ticket = rma.pk).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        
        for attachment in attachments:
           #print('attachment1',attachment)
            if attachment.name!='N/A':
                try:
                    if self.attachment!='N/A':
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        
        res = message.send()   
        print('message.send=',res)
        return res
    
    def send_RMA_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\rma\\templates\\rma\\' + 'email_RMA.html')
        rma=self.message
        active=self.attachment
        subject=self.subject
        dept=self.bcc
        if self.subject == 'RMA Bad Count':
            subject= 'RMA Ticket#' + str(rma.pk) + ' -- BAD COUNT--'
        elif self.subject == 'Receiving Issue':
            subject= 'RMA Ticket#' + str(rma.pk) + ' -- RCV ISSUE--'
        elif self.subject == 'Receiving to Engineering':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --RCV TO ENG--'
        elif self.subject == 'Receiving to Test':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --RCV TO TEST--'
        elif self.subject == 'Receiving to Manufacturing':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --RCV TO MANUF--'
        elif self.subject == 'Receiving to Inspection':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --RCV TO INSP--'
        elif self.subject == 'Receiving to Sales':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --RCV TO SALES--'
        elif self.subject == 'Receiving to Quality Manager':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --RCV TO MANAGER--'
        elif self.subject == 'Inspection to Engineering':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --INSP TO ENG--'
        elif self.subject == 'Inspection to Test':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --INSP TO TEST--'
        elif self.subject == 'Inspection to Quality Manager':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --INSP TO MANAGER--'
        elif self.subject == 'Inspection to Manufacturing':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --INSP TO MANUF--'
        elif self.subject == 'Inspection to Sales':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --INSP TO SALES--'
        elif self.subject == 'Sales to Receiving':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --SALES TO RCV--'
        elif self.subject == 'Sales to Engineering':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --SALES TO ENG--'
        elif self.subject == 'Sales to Quality Manager':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --SALES TO MANAGER--'
        elif self.subject == 'Manufacturing to Engineering':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --MANUF TO ENG--'
        elif self.subject == 'Manufacturing to Test':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --MANUF TO TEST--'
        elif self.subject == 'Manufacturing to Sales':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --MANUF TO SALES--'
        elif self.subject == 'Manufacturing to Inspection':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --MANUF TO INSP--'
        elif self.subject == 'Manufacturing to Quality Manager':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --MANUF TO MANAGER--'
        elif self.subject == 'Engineering to Test':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --ENG TO TEST--'
        elif self.subject == 'Engineering to Manufacturing':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --ENG TO MANUF--'
        elif self.subject == 'Engineering to Inspection':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --ENG TO INSP--'
        elif self.subject == 'Engineering to Sales':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --ENG TO SALES--'
        elif self.subject == 'Engineering to Quality Manager':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --ENG TO MANAGER--'
        elif self.subject == 'Test to Engineering':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --TEST TO ENG--'
        elif self.subject == 'Test to Manufacturing':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --TEST TO MANUF--'
        elif self.subject == 'Test to Inspection':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --TEST TO INSP--'
        elif self.subject == 'Test to Sales':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --TEST TO SALES--'
        elif self.subject == 'Test to Quality Manager':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --TEST TO MANAGER--'
        elif self.subject == 'No ACTION':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --No ACTION Taken yet--'
        elif self.subject == 'RMA Stop Work':
            subject= 'RMA Ticket#' + str(rma.pk) + ' --RMA Stop Work--'
        
        
        message= ''
        html_message = loader.render_to_string(file_path, {'rma':rma,'active':active,'subject':subject,'dept':dept})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=['mford@innovativepp.com'])
        message.attach_alternative(html_message, "text/html")
        attachments = RMA_Attachments.objects.select_related().filter(ticket = rma.pk).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        for attachment in attachments:
           #print('attachment1',attachment)
            if attachment.name!='N/A':
                try:
                    if self.attachment!='N/A':
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
    
    def send_deviations_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\qa\\templates\\qa\\' + 'email_deviations.html')
       #print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~file_path=',file_path)
        ticket=self.message
        active_manager=self.subject
        if 'Customer' in ticket.dev_type:
            subject= str(ticket.dev_type) +' Ticket ' + str(ticket.ticket_num) + '  ' + str(ticket.customer_code) + '  ' + str(ticket.part_number) + ' --NEW--'
        elif 'Vendor' in ticket.dev_type:
            subject= str(ticket.dev_type) +' Ticket ' + str(ticket.ticket_num) + '  ' + str(ticket.vendor_code) + '  ' + str(ticket.part_number) + ' --NEW--'
        else:
            subject= str(ticket.dev_type) +' Ticket ' + str(ticket.ticket_num) + ' --NEW--'
        message= ''
        
        #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'ticket':ticket,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = QA_Attachments.objects.select_related().filter(ticket = ticket.pk).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        
        for attachment in attachments:
           #print('attachment1',attachment)
            if attachment.name!='N/A':
                try:
                    if self.attachment!='N/A':
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
        
    def send_pto_request_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\hr\\templates\\hr\\' + 'email_pto_request.html')
       #print('file_path=',file_path)
        ticket=self.message
        active_manager=self.subject
        firstname_arr = self.subject
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
        subject= 'Action Ticket#' + str(ticket.pk) + '  ' + str(ticket.customer) + '  ' + str(ticket.ipp_part_number) + ' --CLOSED--'
        message= ''
        log = ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Gemba_Walk_Attachments.objects.select_related().filter(gemba_walk = ticket.pk).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
        
        
        
    def send_new_problem_solving_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\problem_solving\\templates\\problem_solving\\' + 'email_problem_solving_new.html')
        #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        if "@" in self.recepient:
            email_list=self.recepient
        else:
            security=Security('N/A',self.recepient)
            email_list=security.get_user_emails()
        
        try:
            assigned_list=ast.literal_eval(ticket.assigned_list)
            assigned_pick_list=ast.literal_eval(ticket.assigned_pick_list)
            assigned_actual_list=update_name_list(assigned_pick_list,assigned_list)
           #print('email_list=',email_list)
        except ValueError as e:
            assigned_list=[]
            assigned_pick_list=[]
            assigned_actual_list=[]
            firstname_arr = ticket.assigned
        current_time = datetime.now()
        temp=str(current_time).split()
        date=temp[0]
        this_time=temp[1]
        temp=str(this_time).split('.')
        this_time=temp[0]
        current_time = format_time(date,this_time)
        date=ticket.requested_date
        start_time=ticket.start_time
        start_time = format_time(date,start_time)
        reminder_hours = '0:0'
        stop_time=ticket.stop_time
        stop_time = format_time(date,stop_time)
        firstname = 'problem_solving  Group'  
        security=Security('N/A',ticket.leader)
        organizer=security.get_user_email()
        subject= 'Problem Solving# ' + str(ticket.pk) + '  ' + str(ticket.department)
        message= ''
        log = ''
        
        logs = ProblemSolving_Logs.objects.select_related().filter(problem = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('subject=',subject)
        ICS_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        # Send to organizer and cc bcc
        calendar = icalendar.Calendar()
        calendar.add('version', '2.0')
        calendar.add('prodid', '-//events.hel.fi//NONSGML Feeder//EN')
        event = ical_event.create_new_event(start_time, stop_time,current_time, ticket.problem_statement, ticket.process,[organizer],email_list,reminder_hours,ticket.department)
        #print('event=',event)
        calendar.add_component(event)
        #print('calendar=',calendar)
        filename_event = 'problem_solving session invite-%d.ics' % ticket.pk
        with open(filename_event, 'wb') as o:
            o.write(calendar.to_ical())
        #print('filename_event',filename_event)
        
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, email_list, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        message.attach_file(filename_event, 'text/icalendar')
        #message.attach_file('assets/invite.ics', 'text/calendar')
        #print('message=',message)
        attachments = ProblemSolving_Attachments.objects.select_related().filter(problem = ticket.pk)
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
            
        res = message.send() 
        os.remove(filename_event)        
        
         
        #res = send_mail(subject, message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False,html_message=html_message)
        return res
    
    def send_update_schedule_problem_solving_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\problem_solving\\templates\\problem_solving\\' + 'email_problem_solving_update_schedule.html')
        #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        if "@" in self.recepient:
            email_list=self.recepient
        else:
            security=Security('N/A',self.recepient)
            email_list=security.get_user_emails()
        
        try:
            assigned_list=ast.literal_eval(ticket.assigned_list)
            assigned_pick_list=ast.literal_eval(ticket.assigned_pick_list)
            assigned_actual_list=update_name_list(assigned_pick_list,assigned_list)
           #print('email_list=',email_list)
        except ValueError as e:
            assigned_list=[]
            assigned_pick_list=[]
            assigned_actual_list=[]
            firstname_arr = ticket.assigned
        current_time = datetime.now()
        temp=str(current_time).split()
        date=temp[0]
        this_time=temp[1]
       #print('this_time111=',this_time)
        temp=str(this_time).split('.')
        this_time=temp[0]
        current_time = format_time(date,this_time)
       #print('current_time=',current_time)
        date=ticket.requested_date
        start_time=ticket.start_time
        start_time = format_time(date,start_time)
        
        #reminder_hours = datetime.strptime(ticket.reminder_hours, '%H:%M:%S')
        #temp=str(reminder_hours).split()
        #reminder_hours=temp[1]
        #print('reminder_hours',reminder_hours)
        #temp=str(reminder_hours).split(":")
        #start_hour=int(temp[0])
        #start_minute=int(temp[1])
        #reminder_hours = tz.localize(dt.datetime.combine(date, dt.time(start_hour, start_minute, 0)))
        reminder_hours = '0:0'
       #print('reminder_hours=',reminder_hours)
        
        stop_time=ticket.stop_time
       #print('dB stop_time',stop_time)
        #temp=str(stop_time).split(":")
        #stop_hour=int(temp[0])
        #stop_minute=int(temp[1])
        #stop_time = tz.localize(dt.datetime.combine(date, dt.time(stop_hour, stop_minute, 0)))
        stop_time = format_time(date,stop_time)
        firstname = 'Problem Solving Group'  
       #print('start_time=',start_time)
       #print('stop_time=',stop_time)
        security=Security('N/A',ticket.leader)
        organizer=security.get_user_email()
       #print('organizer=',organizer)
        
        subject= 'Problem Solving# ' + str(ticket.pk) + '  ' + str(ticket.department)
        message= ''
        log = ''
        
        logs = ProblemSolving_Logs.objects.select_related().filter(problem = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('subject=',subject)
        ICS_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        # Send to organizer and cc bcc
        calendar = icalendar.Calendar()
        calendar.add('version', '2.0')
        calendar.add('prodid', '-//events.hel.fi//NONSGML Feeder//EN')
        event = ical_event.create_new_event(start_time, stop_time,current_time, ticket.problem_statement, ticket.process,[organizer],email_list,reminder_hours,ticket.department)
        #print('event=',event)
        calendar.add_component(event)
        #print('calendar=',calendar)
        filename_event = 'Problem Solving session update-%d.ics' % ticket.pk
        with open(filename_event, 'wb') as o:
            o.write(calendar.to_ical())
        #print('filename_event',filename_event)
        
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, email_list, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        message.attach_file(filename_event, 'text/icalendar')
        #message.attach_file('assets/invite.ics', 'text/calendar')
        #print('message=',message)
        attachments = ProblemSolving_Attachments.objects.select_related().filter(problem = ticket.pk)
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
            
        res = message.send() 
        os.remove(filename_event)        
        
         
        #res = send_mail(subject, message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False,html_message=html_message)
        return res
        
    def send_update_team_problem_solving_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\problem_solving\\templates\\problem_solving\\' + 'email_problem_solving_update_team.html')
        #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        if "@" in self.recepient:
            email_list=self.recepient
        else:
            security=Security('N/A',self.recepient)
            email_list=security.get_user_emails()
        
        try:
            assigned_list=ast.literal_eval(ticket.assigned_list)
            assigned_pick_list=ast.literal_eval(ticket.assigned_pick_list)
            assigned_actual_list=update_name_list(assigned_pick_list,assigned_list)
           #print('email_list=',email_list)
        except ValueError as e:
            assigned_list=[]
            assigned_pick_list=[]
            assigned_actual_list=[]
            firstname_arr = ticket.assigned
        current_time = datetime.now()
        temp=str(current_time).split()
        date=temp[0]
        this_time=temp[1]
       #print('this_time111=',this_time)
        temp=str(this_time).split('.')
        this_time=temp[0]
        current_time = format_time(date,this_time)
       #print('current_time=',current_time)
        date=ticket.requested_date
        start_time=ticket.start_time
        start_time = format_time(date,start_time)
        
        #reminder_hours = datetime.strptime(ticket.reminder_hours, '%H:%M:%S')
        #temp=str(reminder_hours).split()
        #reminder_hours=temp[1]
        #print('reminder_hours',reminder_hours)
        #temp=str(reminder_hours).split(":")
        #start_hour=int(temp[0])
        #start_minute=int(temp[1])
        #reminder_hours = tz.localize(dt.datetime.combine(date, dt.time(start_hour, start_minute, 0)))
        reminder_hours = '0:0'
       #print('reminder_hours=',reminder_hours)
        
        stop_time=ticket.stop_time
       #print('dB stop_time',stop_time)
        #temp=str(stop_time).split(":")
        #stop_hour=int(temp[0])
        #stop_minute=int(temp[1])
        #stop_time = tz.localize(dt.datetime.combine(date, dt.time(stop_hour, stop_minute, 0)))
        stop_time = format_time(date,stop_time)
        firstname = 'Problem Solbing Group'  
       #print('start_time=',start_time)
       #print('stop_time=',stop_time)
        security=Security('N/A',ticket.leader)
        organizer=security.get_user_email()
       #print('organizer=',organizer)
        
        subject= 'Problem Solving#' + str(ticket.pk) + '  ' + str(ticket.department)
        message= ''
        log = ''
        
        logs = ProblemSolving_Logs.objects.select_related().filter(problem = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('subject=',subject)
        ICS_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        # Send to organizer and cc bcc
        calendar = icalendar.Calendar()
        calendar.add('version', '2.0')
        calendar.add('prodid', '-//events.hel.fi//NONSGML Feeder//EN')
        event = ical_event.create_new_event(start_time, stop_time,current_time, ticket.problem_statement, ticket.process,[organizer],email_list,reminder_hours,ticket.department)
        #print('event=',event)
        calendar.add_component(event)
        #print('calendar=',calendar)
        filename_event = 'Problem Solving session update-%d.ics' % ticket.pk
        with open(filename_event, 'wb') as o:
            o.write(calendar.to_ical())
        #print('filename_event',filename_event)
        
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, email_list, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        message.attach_file(filename_event, 'text/icalendar')
        #message.attach_file('assets/invite.ics', 'text/calendar')
        #print('message=',message)
        attachments = ProblemSolving_Attachments.objects.select_related().filter(problem = ticket.pk)
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
            
        res = message.send() 
        os.remove(filename_event)        
        
         
        #res = send_mail(subject, message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False,html_message=html_message)
        return res
        
    def send_complete_problem_solving_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\problem_solving\\templates\\problem_solving\\' + 'email_problem_solving_complete.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.approver
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Problem Solving#' + str(ticket.pk) + ' Action Item# ' + str(action_item.action_item) +  ' --COMPLETED--'
        message= ''
        log = ''
        logs = ProblemSolving_Logs.objects.select_related().filter(problem = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        #print(' EMAIL            finding',finding)        
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = ProblemSolving_Attachments.objects.select_related().filter(problem = ticket.pk).filter(action_item=action_item.action_item).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
    
    def send_approved_problem_solving_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\problem_solving\\templates\\problem_solving\\' + 'email_problem_solving_approved.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Problem Solving#' + str(ticket.pk) + ' Action Item# ' + str(action_item.action_item) +  ' --APPROVED--'
        message= ''
        log = ''
        #logs = Gemba_Walk_Logs.objects.filter(action_item=action_item_id).select_related().filter(gemba_walk = active_ticket.pk).order_by('id')
        log = ''
        logs = ProblemSolving_Logs.objects.select_related().filter(problem = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = ProblemSolving_Attachments.objects.select_related().filter(problem = ticket.pk).filter(action_item=action_item.action_item).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res    
    
    def send_rejected_problem_solving_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\problem_solving\\templates\\problem_solving\\' + 'email_problem_solving_rejected.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'GEMB Ticket#' + str(ticket.pk) + ' Action Item# ' + str(action_item.action_item) +  ' --REJECTED--'
        message= ''
        log = ''
        log = ''
        logs = ProblemSolving_Logs.objects.select_related().filter(problem = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = ProblemSolving_Attachments.objects.select_related().filter(problem = ticket.pk).filter(action_item=action_item.action_item).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()  
       #print('message.send=',res)
        return res    
    
    def send_action_problem_solving_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\problem_solving\\templates\\problem_solving\\' + 'email_problem_solving_action.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Problem Solving#' + str(ticket.pk) + '  Action Item# ' + str(action_item.action_item) +  ' --ASSIGNED--'
        message= ''
        log = ''
        log = ''
        logs = ProblemSolving_Logs.objects.select_related().filter(problem = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = ProblemSolving_Attachments.objects.select_related().filter(problem = ticket.pk).filter(action_item=action_item.action_item).all()
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res    
    
    def send_reassign_problem_solving_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\problem_solving\\templates\\problem_solving\\' + 'email_problem_solving_reassign.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Problem Solving#' + str(ticket.pk) + '  Action Item# ' + str(action_item.action_item) +  ' --RE-ASSIGNED--'
        message= ''
        log = ''
        log = ''
        logs = ProblemSolving_Logs.objects.select_related().filter(problem = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = ProblemSolving_Attachments.objects.select_related().filter(problem = ticket.pk).filter(action_item=action_item.action_item).all()
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    def send_gemba_reminder_email(self):
        #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\gemba\\templates\\gemba\\' + 'email_new_inquiry.html')
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
        #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        #print('firstname_arr=',firstname_arr)
        firstname='Gemba Group'
        subject= 'Gemba Ticket#' + str(ticket.pk) + '  ' + str(ticket.customer)
        message= ''
        log = ''
        if goto=='inquiry':
            logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
            saved_log=[]
            message=''
            for this_log in logs:
                saved_log=html2text.html2text(this_log.log)
                res=saved_log.split('![')
                #print('res=',res)
                descriptions=[]
                image_names=[]
                images=[]
                if res:
                    x=1
                    for text in res:
                        if text[0]==']':
                            text = text.split('(')
                            text= text[1].split(')')
                            for f in text:
                                if 'data:image' in f:
                                    file = text[0]
                                    imagename = 'image_' + str(x) +'.png'  
                                    file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                    descriptions.append(file_link)
                                else:
                                    descriptions.append(f)
                                x+=1
                        
                        elif ']' in text:
                            text = text.split('(')
                            text= text[1].split(')')
                            link = text[0]
                            if '\n' in link:
                                link = link.replace('\n','')
                            descriptions.append(link)
                            try:
                                link2=text[1]
                                if '\n' in link2:
                                    link2 = link2.replace('\n','')
                                descriptions.append(link2)
                            except BaseException as e:
                               print('error1=',e)
                        else: 
                           #print('text=',text)
                            descriptions.append(text)
                        
                    description_log=''
                    for desc in descriptions:
                        description_log= description_log + desc + ' '
                    
                    message = message + this_log.log + '\r\n'
                    log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        message.attach_file(filename_event, 'text/calendar')
       #print('message=',message)
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        res = message.send()   
        #res = send_mail(subject, message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False,html_message=html_message)
        return res
        
    def send_new_gemba_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\gemba\\templates\\gemba\\' + 'email_gemba_new.html')
        #print('file_path=',file_path)
        ticket=self.message
        print('ticket=',ticket)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
                #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        if "@" in self.recepient:
            email_list=self.recepient
        else:
            security=Security('N/A',self.recepient)
            email_list=security.get_user_emails()
        
        try:
            assigned_list=ast.literal_eval(ticket.assigned_list)
            assigned_pick_list=ast.literal_eval(ticket.assigned_pick_list)
            assigned_actual_list=update_name_list(assigned_pick_list,assigned_list)
           #print('email_list=',email_list)
        except ValueError as e:
            assigned_list=[]
            assigned_pick_list=[]
            assigned_actual_list=[]
            firstname_arr = ticket.assigned
        current_time = datetime.now()
        temp=str(current_time).split()
        date=temp[0]
        this_time=temp[1]
        temp=str(this_time).split('.')
        this_time=temp[0]
        current_time = format_time(date,this_time)
        date=ticket.requested_date
        start_time=ticket.start_time
        start_time = format_time(date,start_time)
        reminder_hours = '0:0'
        stop_time=ticket.stop_time
        stop_time = format_time(date,stop_time)
        firstname = 'Gemba Walk Group'  
        security=Security('N/A',ticket.leader)
        organizer=security.get_user_email()
        subject= 'GEMBA Walk#' + str(ticket.pk) + '  ' + str(ticket.department)
        message= ''
        log = ''
        
        logs = Gemba_Walk_Logs.objects.select_related().filter(gemba_walk = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('subject=',subject)
        ICS_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        # Send to organizer and cc bcc
        calendar = icalendar.Calendar()
        calendar.add('version', '2.0')
        calendar.add('prodid', '-//events.hel.fi//NONSGML Feeder//EN')
        event = ical_event.create_new_event(start_time, stop_time,current_time, ticket.purpose, ticket.plan,[organizer],email_list,reminder_hours,ticket.department)
        #print('event=',event)
        calendar.add_component(event)
        #print('calendar=',calendar)
        filename_event = 'Gemba walk invite-%d.ics' % ticket.pk
        with open(filename_event, 'wb') as o:
            o.write(calendar.to_ical())
        #print('filename_event',filename_event)
        
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, email_list, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        message.attach_file(filename_event, 'text/icalendar')
        #message.attach_file('assets/invite.ics', 'text/calendar')
        #print('message=',message)
        attachments = Gemba_Walk_Attachments.objects.select_related().filter(gemba_walk = ticket.pk)
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
            
        res = message.send() 
        os.remove(filename_event)        
        
         
        #res = send_mail(subject, message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False,html_message=html_message)
        return res
    
    def send_update_schedule_gemba_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\gemba\\templates\\gemba\\' + 'email_gemba_update_schedule.html')
        #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        if "@" in self.recepient:
            email_list=self.recepient
        else:
            security=Security('N/A',self.recepient)
            email_list=security.get_user_emails()
        
        try:
            assigned_list=ast.literal_eval(ticket.assigned_list)
            assigned_pick_list=ast.literal_eval(ticket.assigned_pick_list)
            assigned_actual_list=update_name_list(assigned_pick_list,assigned_list)
           #print('email_list=',email_list)
        except ValueError as e:
            assigned_list=[]
            assigned_pick_list=[]
            assigned_actual_list=[]
            firstname_arr = ticket.assigned
        current_time = datetime.now()
        temp=str(current_time).split()
        date=temp[0]
        this_time=temp[1]
       #print('this_time111=',this_time)
        temp=str(this_time).split('.')
        this_time=temp[0]
        current_time = format_time(date,this_time)
       #print('current_time=',current_time)
        date=ticket.requested_date
        start_time=ticket.start_time
        start_time = format_time(date,start_time)
        
        #reminder_hours = datetime.strptime(ticket.reminder_hours, '%H:%M:%S')
        #temp=str(reminder_hours).split()
        #reminder_hours=temp[1]
        #print('reminder_hours',reminder_hours)
        #temp=str(reminder_hours).split(":")
        #start_hour=int(temp[0])
        #start_minute=int(temp[1])
        #reminder_hours = tz.localize(dt.datetime.combine(date, dt.time(start_hour, start_minute, 0)))
        reminder_hours = '0:0'
       #print('reminder_hours=',reminder_hours)
        
        stop_time=ticket.stop_time
       #print('dB stop_time',stop_time)
        #temp=str(stop_time).split(":")
        #stop_hour=int(temp[0])
        #stop_minute=int(temp[1])
        #stop_time = tz.localize(dt.datetime.combine(date, dt.time(stop_hour, stop_minute, 0)))
        stop_time = format_time(date,stop_time)
        firstname = 'Gemba Walk Group'  
       #print('start_time=',start_time)
       #print('stop_time=',stop_time)
        security=Security('N/A',ticket.leader)
        organizer=security.get_user_email()
       #print('organizer=',organizer)
        
        subject= 'GEMBA Walk#' + str(ticket.pk) + '  ' + str(ticket.department)
        message= ''
        log = ''
        
        logs = Gemba_Walk_Logs.objects.select_related().filter(gemba_walk = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('subject=',subject)
        ICS_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        # Send to organizer and cc bcc
        calendar = icalendar.Calendar()
        calendar.add('version', '2.0')
        calendar.add('prodid', '-//events.hel.fi//NONSGML Feeder//EN')
        event = ical_event.create_new_event(start_time, stop_time,current_time, ticket.purpose, ticket.plan,[organizer],email_list,reminder_hours,ticket.department)
        #print('event=',event)
        calendar.add_component(event)
        #print('calendar=',calendar)
        filename_event = 'Gemba walk invite-%d.ics' % ticket.pk
        with open(filename_event, 'wb') as o:
            o.write(calendar.to_ical())
        #print('filename_event',filename_event)
        
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, email_list, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        message.attach_file(filename_event, 'text/icalendar')
        #message.attach_file('assets/invite.ics', 'text/calendar')
        #print('message=',message)
        attachments = Gemba_Walk_Attachments.objects.select_related().filter(gemba_walk = ticket.pk)
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
            
        res = message.send() 
        os.remove(filename_event)        
        
         
        #res = send_mail(subject, message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False,html_message=html_message)
        return res
        
    def send_update_team_gemba_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\gemba\\templates\\gemba\\' + 'email_gemba_update_team.html')
        #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        if "@" in self.recepient:
            email_list=self.recepient
        else:
            security=Security('N/A',self.recepient)
            email_list=security.get_user_emails()
        
        try:
            assigned_list=ast.literal_eval(ticket.assigned_list)
            assigned_pick_list=ast.literal_eval(ticket.assigned_pick_list)
            assigned_actual_list=update_name_list(assigned_pick_list,assigned_list)
           #print('email_list=',email_list)
        except ValueError as e:
            assigned_list=[]
            assigned_pick_list=[]
            assigned_actual_list=[]
            firstname_arr = ticket.assigned
        current_time = datetime.now()
        temp=str(current_time).split()
        date=temp[0]
        this_time=temp[1]
       #print('this_time111=',this_time)
        temp=str(this_time).split('.')
        this_time=temp[0]
        current_time = format_time(date,this_time)
       #print('current_time=',current_time)
        date=ticket.requested_date
        start_time=ticket.start_time
        start_time = format_time(date,start_time)
        
        #reminder_hours = datetime.strptime(ticket.reminder_hours, '%H:%M:%S')
        #temp=str(reminder_hours).split()
        #reminder_hours=temp[1]
        #print('reminder_hours',reminder_hours)
        #temp=str(reminder_hours).split(":")
        #start_hour=int(temp[0])
        #start_minute=int(temp[1])
        #reminder_hours = tz.localize(dt.datetime.combine(date, dt.time(start_hour, start_minute, 0)))
        reminder_hours = '0:0'
       #print('reminder_hours=',reminder_hours)
        
        stop_time=ticket.stop_time
       #print('dB stop_time',stop_time)
        #temp=str(stop_time).split(":")
        #stop_hour=int(temp[0])
        #stop_minute=int(temp[1])
        #stop_time = tz.localize(dt.datetime.combine(date, dt.time(stop_hour, stop_minute, 0)))
        stop_time = format_time(date,stop_time)
        firstname = 'Gemba Walk Group'  
       #print('start_time=',start_time)
       #print('stop_time=',stop_time)
        security=Security('N/A',ticket.leader)
        organizer=security.get_user_email()
       #print('organizer=',organizer)
        
        subject= 'GEMBA Walk#' + str(ticket.pk) + '  ' + str(ticket.department)
        message= ''
        log = ''
        
        logs = Gemba_Walk_Logs.objects.select_related().filter(gemba_walk = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('subject=',subject)
        ICS_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        # Send to organizer and cc bcc
        calendar = icalendar.Calendar()
        calendar.add('version', '2.0')
        calendar.add('prodid', '-//events.hel.fi//NONSGML Feeder//EN')
        event = ical_event.create_new_event(start_time, stop_time,current_time, ticket.purpose, ticket.plan,[organizer],email_list,reminder_hours,ticket.department)
        #print('event=',event)
        calendar.add_component(event)
        #print('calendar=',calendar)
        filename_event = 'Gemba walk invite-%d.ics' % ticket.pk
        with open(filename_event, 'wb') as o:
            o.write(calendar.to_ical())
        #print('filename_event',filename_event)
        
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, email_list, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        message.attach_file(filename_event, 'text/icalendar')
        #message.attach_file('assets/invite.ics', 'text/calendar')
        #print('message=',message)
        attachments = Gemba_Walk_Attachments.objects.select_related().filter(gemba_walk = ticket.pk)
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
            
        res = message.send() 
        os.remove(filename_event)        
        
         
        #res = send_mail(subject, message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False,html_message=html_message)
        return res
        
    def send_complete_gemba_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\gemba\\templates\\gemba\\' + 'email_gemba_complete.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.approver
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'GEMBA Walk#' + str(ticket.pk) + ' Action Item# ' + str(action_item.action_item) +  ' --COMPLETED--'
        message= ''
        log = ''
        logs = Gemba_Walk_Logs.objects.select_related().filter(gemba_walk = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Gemba_Walk_Findings.objects.select_related().filter(gemba_walk=ticket.pk).filter(action_item=action_item.action_item).last()   
       #print(' EMAIL            finding',finding)        
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Gemba_Walk_Attachments.objects.select_related().filter(gemba_walk = ticket.pk).filter(action_item=action_item.action_item).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
    
    def send_approved_gemba_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\gemba\\templates\\gemba\\' + 'email_gemba_approved.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'GEMBA Walk#' + str(ticket.pk) + ' Action Item# ' + str(action_item.action_item) +  ' --APPROVED--'
        message= ''
        log = ''
        #logs = Gemba_Walk_Logs.objects.filter(action_item=action_item_id).select_related().filter(gemba_walk = active_ticket.pk).order_by('id')
        log = ''
        logs = Gemba_Walk_Logs.objects.select_related().filter(gemba_walk = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Gemba_Walk_Findings.objects.select_related().filter(gemba_walk=ticket.pk).filter(action_item=action_item.action_item).last()             
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Gemba_Walk_Attachments.objects.select_related().filter(gemba_walk = ticket.pk).filter(action_item=action_item.action_item).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res    
    
    def send_rejected_gemba_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\gemba\\templates\\gemba\\' + 'email_gemba_rejected.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'GEMB Ticket#' + str(ticket.pk) + ' Action Item# ' + str(action_item.action_item) +  ' --REJECTED--'
        message= ''
        log = ''
        log = ''
        logs = Gemba_Walk_Logs.objects.select_related().filter(gemba_walk = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Gemba_Walk_Findings.objects.select_related().filter(gemba_walk=ticket.pk).filter(action_item=action_item.action_item).last()             
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Gemba_Walk_Attachments.objects.select_related().filter(gemba_walk = ticket.pk).filter(action_item=action_item.action_item).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()  
       #print('message.send=',res)
        return res    
    
    def send_action_gemba_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\gemba\\templates\\gemba\\' + 'email_gemba_action.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'GEMBA Walk#' + str(ticket.pk) + '  Action Item# ' + str(action_item.action_item) +  ' --ASSIGNED--'
        message= ''
        log = ''
        log = ''
        logs = Gemba_Walk_Logs.objects.select_related().filter(gemba_walk = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Gemba_Walk_Findings.objects.select_related().filter(gemba_walk=ticket.pk).filter(action_item=action_item.action_item).last()             
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Gemba_Walk_Attachments.objects.select_related().filter(gemba_walk = ticket.pk).filter(action_item=action_item.action_item).all()
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res    
    
    def send_reassign_gemba_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\gemba\\templates\\gemba\\' + 'email_gemba_reassign.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'GEMBA Walk#' + str(ticket.pk) + '  Action Item# ' + str(action_item.action_item) +  ' --RE-ASSIGNED--'
        message= ''
        log = ''
        log = ''
        logs = Gemba_Walk_Logs.objects.select_related().filter(gemba_walk = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Gemba_Walk_Findings.objects.select_related().filter(gemba_walk=ticket.pk).filter(action_item=action_item.action_item).last()             
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Gemba_Walk_Attachments.objects.select_related().filter(gemba_walk = ticket.pk).filter(action_item=action_item.action_item).all()
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res    
    
    def send_datechange_gemba_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\gemba\\templates\\gemba\\' + 'email_gemba_date.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'GEMBA Walk#' + str(ticket.pk) + '  Action Item# ' + str(action_item.action_item) +  ' --NEW DATE--'
        message= ''
        log = ''
        log = ''
        logs = Gemba_Walk_Logs.objects.select_related().filter(gemba_walk = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Gemba_Walk_Findings.objects.select_related().filter(gemba_walk=ticket.pk).filter(action_item=action_item.action_item).last()             
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Gemba_Walk_Attachments.objects.select_related().filter(gemba_walk = ticket.pk).filter(action_item=action_item.action_item).all()
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res    
    
    def send_gemba_closed_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\gemba\\templates\\gemba\\' + 'email_gemba_closed.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname='Gemba Group'
        subject= 'Action Ticket#' + str(ticket.pk) + '  ' + str(ticket.customer) + '  ' + str(ticket.ipp_part_number) + ' --CLOSED--'
        message= ''
        log = ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Gemba_Walk_Attachments.objects.select_related().filter(gemba_walk = ticket.pk).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
        
        
        
    def send_kaizen_reminder_email(self):
        #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\kaizen\\templates\\kaizen\\' + 'email_new_inquiry.html')
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
        #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        #print('firstname_arr=',firstname_arr)
        firstname='Gemba Group'
        subject= 'Kaizen#' + str(ticket.pk) + '  ' + str(ticket.customer)
        message= ''
        log = ''
        if goto=='inquiry':
            logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
            saved_log=[]
            message=''
            for this_log in logs:
                saved_log=html2text.html2text(this_log.log)
                res=saved_log.split('![')
                #print('res=',res)
                descriptions=[]
                image_names=[]
                images=[]
                if res:
                    x=1
                    for text in res:
                        if text[0]==']':
                            text = text.split('(')
                            text= text[1].split(')')
                            for f in text:
                                if 'data:image' in f:
                                    file = text[0]
                                    imagename = 'image_' + str(x) +'.png'  
                                    file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                    descriptions.append(file_link)
                                else:
                                    descriptions.append(f)
                                x+=1
                        
                        elif ']' in text:
                            text = text.split('(')
                            text= text[1].split(')')
                            link = text[0]
                            if '\n' in link:
                                link = link.replace('\n','')
                            descriptions.append(link)
                            try:
                                link2=text[1]
                                if '\n' in link2:
                                    link2 = link2.replace('\n','')
                                descriptions.append(link2)
                            except BaseException as e:
                               print('error1=',e)
                        else: 
                           #print('text=',text)
                            descriptions.append(text)
                        
                    description_log=''
                    for desc in descriptions:
                        description_log= description_log + desc + ' '
                    
                    message = message + this_log.log + '\r\n'
                    log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        message.attach_file(filename_event, 'text/calendar')
        #print('message=',message)
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        res = message.send()   
        #res = send_mail(subject, message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False,html_message=html_message)
        return res
        
    def send_new_kaizen_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\kaizen\\templates\\kaizen\\' + 'email_kaizen_new.html')
        #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        if "@" in self.recepient:
            email_list=self.recepient
        else:
            security=Security('N/A',self.recepient)
            email_list=security.get_user_emails()
        
        try:
            assigned_list=ast.literal_eval(ticket.assigned_list)
            assigned_pick_list=ast.literal_eval(ticket.assigned_pick_list)
            assigned_actual_list=update_name_list(assigned_pick_list,assigned_list)
           #print('email_list=',email_list)
        except ValueError as e:
            assigned_list=[]
            assigned_pick_list=[]
            assigned_actual_list=[]
            firstname_arr = ticket.assigned
        current_time = datetime.now()
        temp=str(current_time).split()
        date=temp[0]
        this_time=temp[1]
        temp=str(this_time).split('.')
        this_time=temp[0]
        current_time = format_time(date,this_time)
        date=ticket.requested_date
        start_time=ticket.start_time
        start_time = format_time(date,start_time)
        reminder_hours = '0:0'
        stop_time=ticket.stop_time
        stop_time = format_time(date,stop_time)
        firstname = 'Kaizen Event Group'  
        security=Security('N/A',ticket.leader)
        organizer=security.get_user_email()
        subject= 'Kaizen#' + str(ticket.pk) + '  ' + str(ticket.department)
        message= ''
        log = ''
        
        logs = Kaizen_Logs.objects.select_related().filter(kaizen = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('subject=',subject)
        ICS_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        # Send to organizer and cc bcc
        calendar = icalendar.Calendar()
        calendar.add('version', '2.0')
        calendar.add('prodid', '-//events.hel.fi//NONSGML Feeder//EN')
        event = ical_event.create_new_event(start_time, stop_time,current_time, ticket.purpose, ticket.plan,[organizer],email_list,reminder_hours,ticket.department)
        #print('event=',event)
        calendar.add_component(event)
        #print('calendar=',calendar)
        filename_event = 'Kaizen invite-%d.ics' % ticket.pk
        with open(filename_event, 'wb') as o:
            o.write(calendar.to_ical())
        #print('filename_event',filename_event)
        
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, email_list, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        message.attach_file(filename_event, 'text/icalendar')
        #message.attach_file('assets/invite.ics', 'text/calendar')
        #print('message=',message)
        attachments = Kaizen_Attachments.objects.select_related().filter(kaizen = ticket.pk)
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
            
        res = message.send() 
        os.remove(filename_event)        
        
         
        #res = send_mail(subject, message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False,html_message=html_message)
        return res
    
    def send_update_schedule_kaizen_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\kaizen\\templates\\kaizen\\' + 'email_kaizen_update_schedule.html')
        #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        if "@" in self.recepient:
            email_list=self.recepient
        else:
            security=Security('N/A',self.recepient)
            email_list=security.get_user_emails()
        
        try:
            assigned_list=ast.literal_eval(ticket.assigned_list)
            assigned_pick_list=ast.literal_eval(ticket.assigned_pick_list)
            assigned_actual_list=update_name_list(assigned_pick_list,assigned_list)
           #print('email_list=',email_list)
        except ValueError as e:
            assigned_list=[]
            assigned_pick_list=[]
            assigned_actual_list=[]
            firstname_arr = ticket.assigned
        current_time = datetime.now()
        temp=str(current_time).split()
        date=temp[0]
        this_time=temp[1]
       #print('this_time111=',this_time)
        temp=str(this_time).split('.')
        this_time=temp[0]
        current_time = format_time(date,this_time)
       #print('current_time=',current_time)
        date=ticket.requested_date
        start_time=ticket.start_time
        start_time = format_time(date,start_time)
        
        #reminder_hours = datetime.strptime(ticket.reminder_hours, '%H:%M:%S')
        #temp=str(reminder_hours).split()
        #reminder_hours=temp[1]
        #print('reminder_hours',reminder_hours)
        #temp=str(reminder_hours).split(":")
        #start_hour=int(temp[0])
        #start_minute=int(temp[1])
        #reminder_hours = tz.localize(dt.datetime.combine(date, dt.time(start_hour, start_minute, 0)))
        reminder_hours = '0:0'
       #print('reminder_hours=',reminder_hours)
        
        stop_time=ticket.stop_time
       #print('dB stop_time',stop_time)
        #temp=str(stop_time).split(":")
        #stop_hour=int(temp[0])
        #stop_minute=int(temp[1])
        #stop_time = tz.localize(dt.datetime.combine(date, dt.time(stop_hour, stop_minute, 0)))
        stop_time = format_time(date,stop_time)
        firstname = 'Kaizen Event Group'  
       #print('start_time=',start_time)
       #print('stop_time=',stop_time)
        security=Security('N/A',ticket.leader)
        organizer=security.get_user_email()
       #print('organizer=',organizer)
        
        subject= 'Kaizen#' + str(ticket.pk) + '  ' + str(ticket.department)
        message= ''
        log = ''
        
        logs = Kaizen_Logs.objects.select_related().filter(kaizen = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('subject=',subject)
        ICS_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        # Send to organizer and cc bcc
        calendar = icalendar.Calendar()
        calendar.add('version', '2.0')
        calendar.add('prodid', '-//events.hel.fi//NONSGML Feeder//EN')
        event = ical_event.create_new_event(start_time, stop_time,current_time, ticket.purpose, ticket.plan,[organizer],email_list,reminder_hours,ticket.department)
        #print('event=',event)
        calendar.add_component(event)
        #print('calendar=',calendar)
        filename_event = 'Kaizen invite-%d.ics' % ticket.pk
        with open(filename_event, 'wb') as o:
            o.write(calendar.to_ical())
        print('settings.EMAIL_HOST_USER',settings.EMAIL_HOST_USER)
        
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, email_list, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        message.attach_file(filename_event, 'text/icalendar')
        #message.attach_file('assets/invite.ics', 'text/calendar')
        #print('message=',message)
        attachments = Kaizen_Attachments.objects.select_related().filter(kaizen = ticket.pk)
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
            
        res = message.send() 
        os.remove(filename_event)        
        
         
        #res = send_mail(subject, message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False,html_message=html_message)
        return res
        
    def send_update_team_kaizen_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\kaizen\\templates\\kaizen\\' + 'email_kaizen_update_team.html')
        #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        if "@" in self.recepient:
            email_list=self.recepient
        else:
            security=Security('N/A',self.recepient)
            email_list=security.get_user_emails()
        
        try:
            assigned_list=ast.literal_eval(ticket.assigned_list)
            assigned_pick_list=ast.literal_eval(ticket.assigned_pick_list)
            assigned_actual_list=update_name_list(assigned_pick_list,assigned_list)
           #print('email_list=',email_list)
        except ValueError as e:
            assigned_list=[]
            assigned_pick_list=[]
            assigned_actual_list=[]
            firstname_arr = ticket.assigned
        current_time = datetime.now()
        temp=str(current_time).split()
        date=temp[0]
        this_time=temp[1]
       #print('this_time111=',this_time)
        temp=str(this_time).split('.')
        this_time=temp[0]
        current_time = format_time(date,this_time)
       #print('current_time=',current_time)
        date=ticket.requested_date
        start_time=ticket.start_time
        start_time = format_time(date,start_time)
        
        #reminder_hours = datetime.strptime(ticket.reminder_hours, '%H:%M:%S')
        #temp=str(reminder_hours).split()
        #reminder_hours=temp[1]
        #print('reminder_hours',reminder_hours)
        #temp=str(reminder_hours).split(":")
        #start_hour=int(temp[0])
        #start_minute=int(temp[1])
        #reminder_hours = tz.localize(dt.datetime.combine(date, dt.time(start_hour, start_minute, 0)))
        reminder_hours = '0:0'
       #print('reminder_hours=',reminder_hours)
        
        stop_time=ticket.stop_time
       #print('dB stop_time',stop_time)
        #temp=str(stop_time).split(":")
        #stop_hour=int(temp[0])
        #stop_minute=int(temp[1])
        #stop_time = tz.localize(dt.datetime.combine(date, dt.time(stop_hour, stop_minute, 0)))
        stop_time = format_time(date,stop_time)
        firstname = 'Kaizen Event Group'  
       #print('start_time=',start_time)
       #print('stop_time=',stop_time)
        security=Security('N/A',ticket.leader)
        organizer=security.get_user_email()
       #print('organizer=',organizer)
        
        subject= 'Kaizen Event#' + str(ticket.pk) + '  ' + str(ticket.department)
        message= ''
        log = ''
        
        logs = Kaizen_Logs.objects.select_related().filter(kaizen = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('subject=',subject)
        ICS_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        # Send to organizer and cc bcc
        calendar = icalendar.Calendar()
        calendar.add('version', '2.0')
        calendar.add('prodid', '-//events.hel.fi//NONSGML Feeder//EN')
        event = ical_event.create_new_event(start_time, stop_time,current_time, ticket.purpose, ticket.plan,[organizer],email_list,reminder_hours,ticket.department)
        #print('event=',event)
        calendar.add_component(event)
        #print('calendar=',calendar)
        filename_event = 'Kaizen invite-%d.ics' % ticket.pk
        with open(filename_event, 'wb') as o:
            o.write(calendar.to_ical())
        #print('filename_event',filename_event)
        
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, email_list, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        message.attach_file(filename_event, 'text/icalendar')
        #message.attach_file('assets/invite.ics', 'text/calendar')
        #print('message=',message)
        attachments = Kaizen_Attachments.objects.select_related().filter(kaizen = ticket.pk)
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
            
        res = message.send() 
        os.remove(filename_event)        
        
         
        #res = send_mail(subject, message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False,html_message=html_message)
        return res
        
    def send_complete_kaizen_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\kaizen\\templates\\kaizen\\' + 'email_kaizen_complete.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.approver
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Kaizen Event#' + str(ticket.pk) + ' Action Item# ' + str(action_item.action_item) +  ' --COMPLETED--'
        message= ''
        log = ''
        logs = Kaizen_Logs.objects.select_related().filter(kaizen = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Kaizen_Findings.objects.select_related().filter(kaizen=ticket.pk).filter(action_item=action_item.action_item).last()   
       #print(' EMAIL            finding',finding)        
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Kaizen_Attachments.objects.select_related().filter(kaizen = ticket.pk).filter(action_item=action_item.action_item).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
    
    def send_approved_kaizen_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\kaizen\\templates\\kaizen\\' + 'email_kaizen_approved.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Kaizen Event#' + str(ticket.pk) + ' Action Item# ' + str(action_item.action_item) +  ' --APPROVED--'
        message= ''
        log = ''
        #logs = Kaizen_Logs.objects.filter(action_item=action_item_id).select_related().filter(kaizen = active_ticket.pk).order_by('id')
        log = ''
        logs = Kaizen_Logs.objects.select_related().filter(kaizen = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Kaizen_Findings.objects.select_related().filter(kaizen=ticket.pk).filter(action_item=action_item.action_item).last()             
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Kaizen_Attachments.objects.select_related().filter(kaizen = ticket.pk).filter(action_item=action_item.action_item).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res    
    
    def send_rejected_kaizen_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\kaizen\\templates\\kaizen\\' + 'email_kaizen_rejected.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'GEMB Ticket#' + str(ticket.pk) + ' Action Item# ' + str(action_item.action_item) +  ' --REJECTED--'
        message= ''
        log = ''
        log = ''
        logs = Kaizen_Logs.objects.select_related().filter(kaizen = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Kaizen_Findings.objects.select_related().filter(kaizen=ticket.pk).filter(action_item=action_item.action_item).last()             
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Kaizen_Attachments.objects.select_related().filter(kaizen = ticket.pk).filter(action_item=action_item.action_item).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()  
       #print('message.send=',res)
        return res    
    
    def send_action_kaizen_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\kaizen\\templates\\kaizen\\' + 'email_kaizen_action.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Kaizen Event#' + str(ticket.pk) + '  Action Item# ' + str(action_item.action_item) +  ' --ASSIGNED--'
        message= ''
        log = ''
        log = ''
        logs = Kaizen_Logs.objects.select_related().filter(kaizen = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Kaizen_Findings.objects.select_related().filter(kaizen=ticket.pk).filter(action_item=action_item.action_item).last()             
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Kaizen_Attachments.objects.select_related().filter(kaizen = ticket.pk).filter(action_item=action_item.action_item).all()
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res    
    
    def send_reassign_kaizen_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\kaizen\\templates\\kaizen\\' + 'email_kaizen_reassign.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Kaizen Event#' + str(ticket.pk) + '  Action Item# ' + str(action_item.action_item) +  ' --RE-ASSIGNED--'
        message= ''
        log = ''
        log = ''
        logs = Kaizen_Logs.objects.select_related().filter(kaizen = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Kaizen_Findings.objects.select_related().filter(kaizen=ticket.pk).filter(action_item=action_item.action_item).last()             
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Kaizen_Attachments.objects.select_related().filter(kaizen = ticket.pk).filter(action_item=action_item.action_item).all()
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res    
    
    def send_datechange_kaizen_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\kaizen\\templates\\kaizen\\' + 'email_kaizen_date.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Kaizen Event#' + str(ticket.pk) + '  Action Item# ' + str(action_item.action_item) +  ' --NEW DATE--'
        message= ''
        log = ''
        log = ''
        logs = Kaizen_Logs.objects.select_related().filter(kaizen = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Kaizen_Findings.objects.select_related().filter(kaizen=ticket.pk).filter(action_item=action_item.action_item).last()             
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Kaizen_Attachments.objects.select_related().filter(kaizen = ticket.pk).filter(action_item=action_item.action_item).all()
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res    
    
    
    
    def send_task_closed_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\task\\templates\\task\\' + 'email_task_closed.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname='Gemba Group'
        subject= 'Action Ticket#' + str(ticket.pk) + '  ' + str(ticket.customer) + '  ' + str(ticket.ipp_part_number) + ' --CLOSED--'
        message= ''
        log = ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Task_Attachments.objects.select_related().filter(task = ticket.pk).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
    
    def send_task_reminder_email(self):
        #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\task\\templates\\task\\' + 'email_new_inquiry.html')
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
        #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        #print('firstname_arr=',firstname_arr)
        firstname='Gemba Group'
        subject= 'Task#' + str(ticket.pk) + '  ' + str(ticket.customer)
        message= ''
        log = ''
        if goto=='inquiry':
            logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
            saved_log=[]
            message=''
            for this_log in logs:
                saved_log=html2text.html2text(this_log.log)
                res=saved_log.split('![')
                #print('res=',res)
                descriptions=[]
                image_names=[]
                images=[]
                if res:
                    x=1
                    for text in res:
                        if text[0]==']':
                            text = text.split('(')
                            text= text[1].split(')')
                            for f in text:
                                if 'data:image' in f:
                                    file = text[0]
                                    imagename = 'image_' + str(x) +'.png'  
                                    file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                    descriptions.append(file_link)
                                else:
                                    descriptions.append(f)
                                x+=1
                        
                        elif ']' in text:
                            text = text.split('(')
                            text= text[1].split(')')
                            link = text[0]
                            if '\n' in link:
                                link = link.replace('\n','')
                            descriptions.append(link)
                            try:
                                link2=text[1]
                                if '\n' in link2:
                                    link2 = link2.replace('\n','')
                                descriptions.append(link2)
                            except BaseException as e:
                               print('error1=',e)
                        else: 
                           #print('text=',text)
                            descriptions.append(text)
                        
                    description_log=''
                    for desc in descriptions:
                        description_log= description_log + desc + ' '
                    
                    message = message + this_log.log + '\r\n'
                    log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        message.attach_file(filename_event, 'text/calendar')
       #print('message=',message)
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        res = message.send()   
        #res = send_mail(subject, message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False,html_message=html_message)
        return res
        
    def send_new_task_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\task\\templates\\task\\' + 'email_task_new.html')
        #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        if "@" in self.recepient:
            email_list=self.recepient
        else:
            security=Security('N/A',self.recepient)
            email_list=security.get_user_emails()
        
        try:
            assigned_list=ast.literal_eval(ticket.assigned_list)
            assigned_pick_list=ast.literal_eval(ticket.assigned_pick_list)
            assigned_actual_list=update_name_list(assigned_pick_list,assigned_list)
           #print('email_list=',email_list)
        except ValueError as e:
            assigned_list=[]
            assigned_pick_list=[]
            assigned_actual_list=[]
            firstname_arr = ticket.assigned
        current_time = datetime.now()
        temp=str(current_time).split()
        date=temp[0]
        this_time=temp[1]
        temp=str(this_time).split('.')
        this_time=temp[0]
        current_time = format_time(date,this_time)
        date=ticket.requested_date
        start_time=ticket.start_time
        start_time = format_time(date,start_time)
        reminder_hours = '0:0'
        stop_time=ticket.stop_time
        stop_time = format_time(date,stop_time)
        firstname = 'Task Event Group'  
        security=Security('N/A',ticket.leader)
        organizer=security.get_user_email()
        subject= 'Task#' + str(ticket.pk) + '  ' + str(ticket.department)
        message= ''
        log = ''
        
        logs = Task_Logs.objects.select_related().filter(task = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('subject=',subject)
        ICS_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        # Send to organizer and cc bcc
        calendar = icalendar.Calendar()
        calendar.add('version', '2.0')
        calendar.add('prodid', '-//events.hel.fi//NONSGML Feeder//EN')
        event = ical_event.create_new_event(start_time, stop_time,current_time, ticket.purpose, ticket.plan,[organizer],email_list,reminder_hours,ticket.department)
        #print('event=',event)
        calendar.add_component(event)
        #print('calendar=',calendar)
        filename_event = 'Task invite-%d.ics' % ticket.pk
        with open(filename_event, 'wb') as o:
            o.write(calendar.to_ical())
        #print('filename_event',filename_event)
        
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, email_list, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        message.attach_file(filename_event, 'text/icalendar')
        #message.attach_file('assets/invite.ics', 'text/calendar')
        #print('message=',message)
        attachments = Task_Attachments.objects.select_related().filter(task = ticket.pk)
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
            
        res = message.send() 
        os.remove(filename_event)        
        
         
        #res = send_mail(subject, message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False,html_message=html_message)
        return res
    
    def send_update_schedule_task_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\task\\templates\\task\\' + 'email_task_update_schedule.html')
        #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        if "@" in self.recepient:
            email_list=self.recepient
        else:
            security=Security('N/A',self.recepient)
            email_list=security.get_user_emails()
        
        try:
            assigned_list=ast.literal_eval(ticket.assigned_list)
            assigned_pick_list=ast.literal_eval(ticket.assigned_pick_list)
            assigned_actual_list=update_name_list(assigned_pick_list,assigned_list)
           #print('email_list=',email_list)
        except ValueError as e:
            assigned_list=[]
            assigned_pick_list=[]
            assigned_actual_list=[]
            firstname_arr = ticket.assigned
        current_time = datetime.now()
        temp=str(current_time).split()
        date=temp[0]
        this_time=temp[1]
       #print('this_time111=',this_time)
        temp=str(this_time).split('.')
        this_time=temp[0]
        current_time = format_time(date,this_time)
       #print('current_time=',current_time)
        date=ticket.requested_date
        start_time=ticket.start_time
        start_time = format_time(date,start_time)
        
        #reminder_hours = datetime.strptime(ticket.reminder_hours, '%H:%M:%S')
        #temp=str(reminder_hours).split()
        #reminder_hours=temp[1]
        #print('reminder_hours',reminder_hours)
        #temp=str(reminder_hours).split(":")
        #start_hour=int(temp[0])
        #start_minute=int(temp[1])
        #reminder_hours = tz.localize(dt.datetime.combine(date, dt.time(start_hour, start_minute, 0)))
        reminder_hours = '0:0'
       #print('reminder_hours=',reminder_hours)
        
        stop_time=ticket.stop_time
       #print('dB stop_time',stop_time)
        #temp=str(stop_time).split(":")
        #stop_hour=int(temp[0])
        #stop_minute=int(temp[1])
        #stop_time = tz.localize(dt.datetime.combine(date, dt.time(stop_hour, stop_minute, 0)))
        stop_time = format_time(date,stop_time)
        firstname = 'Task Event Group'  
       #print('start_time=',start_time)
       #print('stop_time=',stop_time)
        security=Security('N/A',ticket.leader)
        organizer=security.get_user_email()
       #print('organizer=',organizer)
        
        subject= 'Task#' + str(ticket.pk) + '  ' + str(ticket.department)
        message= ''
        log = ''
        
        logs = Task_Logs.objects.select_related().filter(task = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('subject=',subject)
        ICS_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        # Send to organizer and cc bcc
        calendar = icalendar.Calendar()
        calendar.add('version', '2.0')
        calendar.add('prodid', '-//events.hel.fi//NONSGML Feeder//EN')
        event = ical_event.create_new_event(start_time, stop_time,current_time, ticket.purpose, ticket.plan,[organizer],email_list,reminder_hours,ticket.department)
        #print('event=',event)
        calendar.add_component(event)
        #print('calendar=',calendar)
        filename_event = 'Task invite-%d.ics' % ticket.pk
        with open(filename_event, 'wb') as o:
            o.write(calendar.to_ical())
        #print('filename_event',filename_event)
        
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, email_list, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        message.attach_file(filename_event, 'text/icalendar')
        #message.attach_file('assets/invite.ics', 'text/calendar')
        #print('message=',message)
        attachments = Task_Attachments.objects.select_related().filter(task = ticket.pk)
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
            
        res = message.send() 
        os.remove(filename_event)        
        
         
        #res = send_mail(subject, message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False,html_message=html_message)
        return res
        
    def send_update_team_task_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\task\\templates\\task\\' + 'email_task_update_team.html')
        #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        if "@" in self.recepient:
            email_list=self.recepient
        else:
            security=Security('N/A',self.recepient)
            email_list=security.get_user_emails()
        
        try:
            assigned_list=ast.literal_eval(ticket.assigned_list)
            assigned_pick_list=ast.literal_eval(ticket.assigned_pick_list)
            assigned_actual_list=update_name_list(assigned_pick_list,assigned_list)
           #print('email_list=',email_list)
        except ValueError as e:
            assigned_list=[]
            assigned_pick_list=[]
            assigned_actual_list=[]
            firstname_arr = ticket.assigned
        current_time = datetime.now()
        temp=str(current_time).split()
        date=temp[0]
        this_time=temp[1]
       #print('this_time111=',this_time)
        temp=str(this_time).split('.')
        this_time=temp[0]
        current_time = format_time(date,this_time)
       #print('current_time=',current_time)
        date=ticket.requested_date
        start_time=ticket.start_time
        start_time = format_time(date,start_time)
        
        #reminder_hours = datetime.strptime(ticket.reminder_hours, '%H:%M:%S')
        #temp=str(reminder_hours).split()
        #reminder_hours=temp[1]
        #print('reminder_hours',reminder_hours)
        #temp=str(reminder_hours).split(":")
        #start_hour=int(temp[0])
        #start_minute=int(temp[1])
        #reminder_hours = tz.localize(dt.datetime.combine(date, dt.time(start_hour, start_minute, 0)))
        reminder_hours = '0:0'
       #print('reminder_hours=',reminder_hours)
        
        stop_time=ticket.stop_time
       #print('dB stop_time',stop_time)
        #temp=str(stop_time).split(":")
        #stop_hour=int(temp[0])
        #stop_minute=int(temp[1])
        #stop_time = tz.localize(dt.datetime.combine(date, dt.time(stop_hour, stop_minute, 0)))
        stop_time = format_time(date,stop_time)
        firstname = 'Task Event Group'  
       #print('start_time=',start_time)
       #print('stop_time=',stop_time)
        security=Security('N/A',ticket.leader)
        organizer=security.get_user_email()
       #print('organizer=',organizer)
        
        subject= 'Task Event#' + str(ticket.pk) + '  ' + str(ticket.department)
        message= ''
        log = ''
        
        logs = Task_Logs.objects.select_related().filter(task = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('subject=',subject)
        ICS_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        # Send to organizer and cc bcc
        calendar = icalendar.Calendar()
        calendar.add('version', '2.0')
        calendar.add('prodid', '-//events.hel.fi//NONSGML Feeder//EN')
        event = ical_event.create_new_event(start_time, stop_time,current_time, ticket.purpose, ticket.plan,[organizer],email_list,reminder_hours,ticket.department)
        #print('event=',event)
        calendar.add_component(event)
        #print('calendar=',calendar)
        filename_event = 'Task invite-%d.ics' % ticket.pk
        with open(filename_event, 'wb') as o:
            o.write(calendar.to_ical())
        #print('filename_event',filename_event)
        
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, email_list, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        message.attach_file(filename_event, 'text/icalendar')
        #message.attach_file('assets/invite.ics', 'text/calendar')
        #print('message=',message)
        attachments = Task_Attachments.objects.select_related().filter(task = ticket.pk)
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
            
        res = message.send() 
        os.remove(filename_event)        
        
         
        #res = send_mail(subject, message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False,html_message=html_message)
        return res
        
    def send_complete_task_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\task\\templates\\task\\' + 'email_task_complete.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.approver
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Task Event#' + str(ticket.pk) + ' Action Item# ' + str(action_item.action_item) +  ' --COMPLETED--'
        message= ''
        log = ''
        logs = Task_Logs.objects.select_related().filter(task = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Task_Findings.objects.select_related().filter(task=ticket.pk).filter(action_item=action_item.action_item).last()   
       #print(' EMAIL            finding',finding)        
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Task_Attachments.objects.select_related().filter(task = ticket.pk).filter(action_item=action_item.action_item).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
    
    def send_approved_task_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\task\\templates\\task\\' + 'email_task_approved.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Task Event#' + str(ticket.pk) + ' Action Item# ' + str(action_item.action_item) +  ' --APPROVED--'
        message= ''
        log = ''
        #logs = Task_Logs.objects.filter(action_item=action_item_id).select_related().filter(task = active_ticket.pk).order_by('id')
        log = ''
        logs = Task_Logs.objects.select_related().filter(task = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Task_Findings.objects.select_related().filter(task=ticket.pk).filter(action_item=action_item.action_item).last()             
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Task_Attachments.objects.select_related().filter(task = ticket.pk).filter(action_item=action_item.action_item).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res    
    
    def send_rejected_task_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\task\\templates\\task\\' + 'email_task_rejected.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'GEMB Ticket#' + str(ticket.pk) + ' Action Item# ' + str(action_item.action_item) +  ' --REJECTED--'
        message= ''
        log = ''
        log = ''
        logs = Task_Logs.objects.select_related().filter(task = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Task_Findings.objects.select_related().filter(task=ticket.pk).filter(action_item=action_item.action_item).last()             
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Task_Attachments.objects.select_related().filter(task = ticket.pk).filter(action_item=action_item.action_item).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()  
       #print('message.send=',res)
        return res    
    
    def send_action_task_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\task\\templates\\task\\' + 'email_task_action.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Task Event#' + str(ticket.pk) + '  Action Item# ' + str(action_item.action_item) +  ' --ASSIGNED--'
        message= ''
        log = ''
        log = ''
        logs = Task_Logs.objects.select_related().filter(task = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Task_Findings.objects.select_related().filter(task=ticket.pk).filter(action_item=action_item.action_item).last()             
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Task_Attachments.objects.select_related().filter(task = ticket.pk).filter(action_item=action_item.action_item).all()
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res    
    
    def send_reassign_task_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\task\\templates\\task\\' + 'email_task_reassign.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Task Event#' + str(ticket.pk) + '  Action Item# ' + str(action_item.action_item) +  ' --RE-ASSIGNED--'
        message= ''
        log = ''
        log = ''
        logs = Task_Logs.objects.select_related().filter(task = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Task_Findings.objects.select_related().filter(task=ticket.pk).filter(action_item=action_item.action_item).last()             
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Task_Attachments.objects.select_related().filter(task = ticket.pk).filter(action_item=action_item.action_item).all()
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res    
    
    def send_datechange_task_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\task\\templates\\task\\' + 'email_task_date.html')
       #print('file_path=',file_path)
        ticket=self.message
        action_item=self.subject
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        firstname_arr = action_item.owner
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Task Event#' + str(ticket.pk) + '  Action Item# ' + str(action_item.action_item) +  ' --NEW DATE--'
        message= ''
        log = ''
        log = ''
        logs = Task_Logs.objects.select_related().filter(task = ticket.pk).filter(action_item=action_item.action_item).filter(Q(log_type='finding') | Q(log_type='action reassign') | Q(log_type='action') | Q(log_type='action approved') | Q(log_type='action complete')).order_by('id')
        finding = Task_Findings.objects.select_related().filter(task=ticket.pk).filter(action_item=action_item.action_item).last()             
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'action_item':action_item,'finding':finding,'firstname':firstname})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Task_Attachments.objects.select_related().filter(task = ticket.pk).filter(action_item=action_item.action_item).all()
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res    
    
    def send_task_closed_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\task\\templates\\task\\' + 'email_task_closed.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname='Gemba Group'
        subject= 'Action Ticket#' + str(ticket.pk) + '  ' + str(ticket.customer) + '  ' + str(ticket.ipp_part_number) + ' --CLOSED--'
        message= ''
        log = ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
       #print('subject=',subject)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Task_Attachments.objects.select_related().filter(task = ticket.pk).all()
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res

    
        
    def send_pricing_email_update(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_pricing_request_update.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Action Ticket#' + str(ticket.pk) + '  ' + str(ticket.customer) + '  ' + str(ticket.ipp_part_number) + ' --PRICING REQUEST--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
                    
        res = message.send()   
        return res
        
    def send_pricing_email_new(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_pricing_request_new.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Action Ticket#' + str(ticket.pk) + '  ' + str(ticket.customer) + '  ' + str(ticket.ipp_part_number) + ' --PRICING REQUEST--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
                    
        res = message.send()   
        return res
    def send_inquiry_new_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_inquiry_new.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Action Ticket#' + str(ticket.pk) + '  ' + str(ticket.customer) + '  ' + str(ticket.ipp_part_number)
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        if len(text) > 1:
                            text= text[1].split(')')
                            link = text[0]
                            if '\n' in link:
                                link = link.replace('\n','')
                            descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        template = Template(file_path)
        context = Context({'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        template.render(context)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
            
        res = message.send()   
        #res = send_mail(subject, message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False,html_message=html_message)
        return res
        
     
    def send_inquiry_update_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_inquiry_update.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Action Ticket#' + str(ticket.pk) + '  ' + str(ticket.customer) + '  ' + str(ticket.ipp_part_number) + ' --UPDATE--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        if len(text)>1:
                            text= text[1].split(')')
                            link = text[0]
                            if '\n' in link:
                                link = link.replace('\n','')
                            descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
                    
        res = message.send()   
        return res
     
    def send_inquiry_closed_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_inquiry_closed.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Action Ticket#' + str(ticket.pk) + '  ' + str(ticket.customer) + '  ' + str(ticket.ipp_part_number) + ' --CLOSED--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        if len(text) > 1:
                            text= text[1].split(')')
                            link = text[0]
                            if '\n' in link:
                                link = link.replace('\n','')
                            descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res

    def send_inquiry_reopen_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_inquiry_reopened.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Action Ticket#' + str(ticket.pk) + '  ' + str(ticket.customer) + '  ' + str(ticket.ipp_part_number) + ' --RE-OPENED--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        if len(text) > 1:
                            text= text[1].split(')')
                            link = text[0]
                            if '\n' in link:
                                link = link.replace('\n','')
                            descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
    
    def send_inquiry_reassign_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_inquiry_reassign.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
       #print('ticket.assigned=',ticket.assigned)
        firstname_arr=firstname_arr.split( )
       #print('firstname_arr=',firstname_arr)
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Action Ticket#' + str(ticket.pk) + '  ' + str(ticket.customer) + '  ' + str(ticket.ipp_part_number) + ' --RE-ASSIGNED--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            try:
                if res:
                    x=1
                    for text in res:
                        if text[0]==']':
                            text = text.split('(')
                            text= text[1].split(')')
                            for f in text:
                                if 'data:image' in f:
                                    file = text[0]
                                    imagename = 'image_' + str(x) +'.png'  
                                    file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                    descriptions.append(file_link)
                                else:
                                    descriptions.append(f)
                                x+=1
                        
                        elif ']' in text:
                            text = text.split('(')
                            if len(text) > 1:
                                text= text[1].split(')')
                                link = text[0]
                                if '\n' in link:
                                    link = link.replace('\n','')
                                descriptions.append(link)
                            try:
                                link2=text[1]
                                if '\n' in link2:
                                    link2 = link2.replace('\n','')
                                descriptions.append(link2)
                            except BaseException as e:
                               print('error1=',e)
                        else: 
                           #print('text=',text)
                            descriptions.append(text)
                        
                    description_log=''
                    for desc in descriptions:
                        description_log= description_log + desc + ' '
                    
                    message = message + this_log.log + '\r\n'
                    log = log + description_log + '\r\n'
            except BaseException as e:
                print ("couldn't do message" , e)
        
        #print('log=',log)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
    
    def send_peakpower_new_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_peakpower_new.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
       #print('firstname_arr=',firstname_arr)
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Peak Power Inquiry#' + str(ticket.pk) + '  ' + str(ticket.customer) + '  ' + str(ticket.ipp_part_number)
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        if len(text) > 1:
                            text= text[1].split(')')
                            link = text[0]
                            if '\n' in link:
                                link = link.replace('\n','')
                            descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        template = Template(file_path)
        context = Context({'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        template.render(context)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
            
        res = message.send()   
        #res = send_mail(subject, message, settings.EMAIL_HOST_USER, self.recepient, fail_silently = False,html_message=html_message)
        return res
        
     
    def send_peakpower_update_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_peakpower_update.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Peak Power Inquiry Ticket#' + str(ticket.pk) + '  ' + str(ticket.customer) + '  ' + str(ticket.ipp_part_number) + ' --UPDATE--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
                    
        res = message.send()   
        return res
     
    def send_peakpower_closed_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_inquiry_closed.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Peak Power Inquiry Ticket#' + str(ticket.pk) + '  ' + str(ticket.customer) + '  ' + str(ticket.ipp_part_number) + ' --CLOSED--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res

    def send_peakpower_reopen_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_peakpower_reopened.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Peak Power Inquiry Ticket#' + str(ticket.pk) + '  ' + str(ticket.customer) + '  ' + str(ticket.ipp_part_number) + ' --RE-OPENED--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
    
    def send_peakpower_reassign_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_peakpower_reassign.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
       #print('ticket.assigned=',ticket.assigned)
        firstname_arr=firstname_arr.split( )
       #print('firstname_arr=',firstname_arr)
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Peak Power Inquiry Ticket#' + str(ticket.pk) + '  ' + str(ticket.customer) + '  ' + str(ticket.ipp_part_number) + ' --RE-ASSIGNED--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res    
        
    def send_task_new_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_task_new.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split()
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Action Ticket#' + str(ticket.pk) + '  ' + str(ticket.ipp_part_number) + '  ' + str(ticket.customer)
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
        
    def send_task_update_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_task_update.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Action Ticket#' + str(ticket.pk) + '  ' + str(ticket.ipp_part_number) + '  ' + str(ticket.customer) + ' --UPDATE--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
        
    def send_task_closed_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_task_closed.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Action Ticket#' + str(ticket.pk) + '  ' + str(ticket.ipp_part_number) + '  ' + str(ticket.customer) + ' --CLOSED--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
    
    def send_task_reopen_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_task_reopened.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Action Ticket#' + str(ticket.pk) + '  ' + str(ticket.ipp_part_number) + '  ' + str(ticket.customer) + ' --RE-OPENED--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
    
    def send_task_reassign_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_task_reassign.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
       #print('ticket.assigned=',ticket.assigned)
        firstname_arr=firstname_arr.split( )
       #print('firstname_arr=',firstname_arr)
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Action Ticket#' + str(ticket.pk) + '  ' + str(ticket.ipp_part_number) + '  ' + str(ticket.customer) + ' --RE-ASSIGNED--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
                    
        res = message.send()   
        return res    
    
    def send_personal_message_new_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_personal_message_new.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Leader Standard Work Ticket#' + str(ticket.pk) + '  ' + str(ticket.department) + ' --NEW--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
   
    def send_personal_message_update_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_personal_message_update.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Leader Standard Work Ticket#' + str(ticket.pk) + '  ' + str(ticket.department) + ' --UPDATED--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
                    
        res = message.send()   
        return res
   
    def send_personal_message_reminder_email(self):
        #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_personal_message_reminder.html')
        #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        #print('active_manager=',active_manager)
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
        #print('firstname=',firstname)
        subject = 'Personal Message Reminder Ticket#' + str(ticket.pk) + '  ' + str(ticket.department) 
        #print('subject=',subject)
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        if self.cc and self.bcc:
            message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        elif self.cc:
            message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc)
        else:
            message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient)
        
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        #print('right before send')
        res = message.send()   
        #print('res=',res)
        return res
    
    def send_oportunity_reminder_email(self):
        #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_oportunity_message_reminder.html')
        #print('file_path=',file_path)
        ticket=self.message
        next_step=NextStep.objects.filter(pk=ticket.pk).last()
        print('next_step=',next_step)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        checked_list=[]
        #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        #print('active_manager=',active_manager)
        firstname_arr = ticket.owner
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
        #print('firstname=',firstname)
        subject = 'Opportunity Reminder Ticket#' + str(ticket.pk) + '  ' + str(ticket.account_name) 
        #print('subject=',subject)
        log= ''
        logs = CRMNote.objects.select_related().filter(opportunity = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager,'next_step':next_step})
        if self.cc and self.bcc:
            message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        elif self.cc:
            message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc)
        else:
            message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient)
        
        message.attach_alternative(html_message, "text/html")
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        #print('right before send')
        res = message.send()   
        print('res=',res)
        return res
    
    def send_personal_message_closed_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_personal_message_closed.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Leader Standard Work Ticket#' + str(ticket.pk) + '  ' + str(ticket.department) + ' --CLOSED--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
                    
        
        res = message.send()   
        return res
        
    def send_trouble_new_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_trouble_new.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Trouble Ticket#' + str(ticket.pk) + '  ' + str(ticket.department)
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
        
    def send_trouble_update_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_trouble_update.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Trouble Ticket#' + str(ticket.pk) + '  ' + str(ticket.department) + ' --UPDATE--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        res = message.send()   
        return res
   
    def send_trouble_closed_email(self):
       #print('EMAIL_HOST_USER=',settings.EMAIL_HOST_USER)
        file_path = os.path.join(BASE_DIR+'\\tickets\\templates\\tickets\\' + 'email_trouble_closed.html')
       #print('file_path=',file_path)
        ticket=self.message
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        if not 'N/A' in ticket.checked_list:
            try:
                checked_list=ast.literal_eval(ticket.checked_list)
               #print('checked_list=',checked_list)
            except ValueError as e:
                checked_list=[]
        else:
            checked_list=[]
       #print('checked_list=',checked_list)
        #~~~~~~~~~checked_list~~~~~~~~~~~~~~~~~~~~~#
        active_manager=self.subject
        firstname_arr = ticket.assigned
        firstname_arr=firstname_arr.split( )
        if firstname_arr:
            firstname=firstname_arr[0]
        else:
            firstname='Unknown'
       #print('firstname=',firstname)
        subject= 'Trouble Ticket#' + str(ticket.pk) + '  ' + str(ticket.department) + ' --CLOSED--'
        log= ''
        logs = Logs.objects.select_related().filter(inquiry = ticket.pk)
        saved_log=[]
        message=''
        for this_log in logs:
            saved_log=html2text.html2text(this_log.log)
            res=saved_log.split('![')
            #print('res=',res)
            descriptions=[]
            image_names=[]
            images=[]
            if res:
                x=1
                for text in res:
                    if text[0]==']':
                        text = text.split('(')
                        text= text[1].split(')')
                        for f in text:
                            if 'data:image' in f:
                                file = text[0]
                                imagename = 'image_' + str(x) +'.png'  
                                file_link="href='file:///C:\src\ipp\media\images\'" + imagename
                                descriptions.append(file_link)
                            else:
                                descriptions.append(f)
                            x+=1
                    
                    elif ']' in text:
                        text = text.split('(')
                        text= text[1].split(')')
                        link = text[0]
                        if '\n' in link:
                            link = link.replace('\n','')
                        descriptions.append(link)
                        try:
                            link2=text[1]
                            if '\n' in link2:
                                link2 = link2.replace('\n','')
                            descriptions.append(link2)
                        except BaseException as e:
                           print('error1=',e)
                    else: 
                       #print('text=',text)
                        descriptions.append(text)
                    
                description_log=''
                for desc in descriptions:
                    description_log= description_log + desc + ' '
                
                message = message + this_log.log + '\r\n'
                log = log + description_log + '\r\n'
        #print('log=',log)
        html_message = loader.render_to_string(file_path, {'log':log,'ticket':ticket,'firstname':firstname,'active_manager':active_manager})
        message = EmailMultiAlternatives(subject, log, settings.EMAIL_HOST_USER, self.recepient, cc=self.cc, bcc=self.bcc)
        message.attach_alternative(html_message, "text/html")
        attachments = Attachments.objects.select_related().filter(inquiry = ticket.pk)
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachements
        attachments = []
        #~~~~~~~~~~~~~~~~~~~~~~~~Due to ITAR restrictions we will not be sending attachement
        if not checked_list:
            for attachment in attachments:
               #print('attachment1',attachment)
                if attachment.name!='N/A':
                    try:
                        if self.attachment!='N/A':
                            message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                            old_way=True
                    except BaseException as e:
                        print ("Couldn't open self.attachment" , e)
        else:
            for attachment in attachments:
                try:
                    if self.attachment!='N/A' and attachment.this_date in checked_list:
                        message.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.name))
                        old_way=True
                except BaseException as e:
                    print ("Couldn't open self.attachment" , e)
        
        
        res = message.send()   
        return res


#https://sphinxdoc.github.io/pygooglevoice/examples.html#send-sms-messages
class Comunication:
    def __init__ (self, number,message):
        num_list = []
        if isinstance(number, list):
           #print('list number=',number)
            for num in number:
                if '+1' in num:
                    num_list.append(num)
                   #print('this phone number in this list is already properly formated')
                else:
                   #print('number=',num)
                    numeric_filter = filter(str.isdigit, str(num))
                    number = "".join(numeric_filter)
                   #print('numeric_string=',number)
                   #print('numeric_string=',number[0])
                    if not number[0] == '1':
                       #print('adding 1')
                        num_list.append('+1' + number)
                    else:
                       #print('not adding 1')
                        num_list.append('+' + number)
        else:
            if '+1' in number:
                num_list.append(number)
               #print('phone number is already properly formated')
            else:
               #print('number=',number)
                numeric_filter = filter(str.isdigit, str(number))
                number = "".join(numeric_filter)
               #print('numeric_string=',number)
               #print('numeric_string=',number[0])
                if not number[0] == '1':
                   #print('adding 1')
                    num_list.append('+1' + number)
                else:
                   #print('not adding 1')
                    num_list.append('+' + number)
                
            
        self.message = message
        self.number = num_list
       #print('message=',self.message)
       #print('num_list in com =',self.number)
                

    def send_sms(self):
        till_username = settings.TILL_USERNAME
        till_api_key = settings.TILL_API_KEY
                        
        requests.post(
            "https://platform.tillmobile.com/api/send?username=%s&api_key=%s" % (
                till_username,
                till_api_key
            ), 
            json={
                "phone": self.number,
                "text" : self.message,
                "tag": "New User Alert"
            }
        )
    def send_sms_question(self):
        till_username = settings.TILL_USERNAME
        till_api_key = settings.TILL_API_KEY

        requests.post(
            "https://platform.tillmobile.com/api/send?username=%s&api_key=%s" % (
                till_username,
                till_api_key
            ), 
            json={
                "phone": [self.number],
                "introduction": "Hello from Till.",
                "questions" : [{
                    "text": "Do you have a few moments to answer a question or two?",
                    "tag": "have_a_few_moments",
                    "responses": ["Yes", "No"],
                    "conclude_on": "No",
                    "webhook": "https://yourapp.com/have_a_few_moments_results/"
                },
                {
                    "text": "What is your favorite color?",
                    "tag": "favorite_color",
                    "responses": ["Red", "Green", "Yellow"],
                    "webhook": "https://yourapp.com/favorite_color_results/"
                },
                {
                    "text": "Who is you favorite Star Wars character?",
                    "tag": "favorite_star_wars_character",
                    "webhook": "https://yourapp.com/favorite_star_wars_character_results/"
                }],
                "conclusion": "Thank you for your time"
            }
        )
        
    
    
    def call(self):
        user = 'atetestalerts@gmail.com'
        password = 'Gadget2021'
       #print('self.number=',self.number)
        voice = Voice()
       #print('voice=',voice)
       #print(voice.login(user, password))
       #print('in communication')
        outgoingNumber = input('Number to call: ')
        forwardingNumber = input('Number to call from [optional]: ') or None

        voice.call(outgoingNumber, forwardingNumber)

        if input('Calling now... cancel?[y/N] ').lower() == 'y':
            voice.cancel(outgoingNumber, forwardingNumber)
    
    def voice_mails(self):
        user = 'atetestalerts@gmail.com'
        password = 'Gadget2021'
       #print('self.number=',self.number)
        voice = Voice()
       #print('voice=',voice)
       #print(voice.login(user, password))
       #print('in communication')
        for message in voice.voicemail().messages:
            util.print_(message)
        
    def delete_messages(self):
        user = 'atetestalerts@gmail.com'
        password = 'Gadget2021'
       #print('self.number=',self.number)
        voice = Voice()
       #print('voice=',voice)
       #print(voice.login(user, password))
       #print('in communication')
        for message in voice.sms().messages:
            if message.isRead:
                message.delete()
        
 
class StringThings:
    def __init__ (self, this_string):
        self.this_string = this_string
        
    def number_count(self):
        numCount=0
        for item in self.this_string:
            if item.isdigit():
                numCount +=1
        return numCount
    
    def find_number(self):
        number=''
        print('self.this_string',self.this_string)
        for item in self.this_string:
            if item.isdigit():
                number = number + str(item)
        if number!=-1:
            number = int(number)
        return number
        
    def parse_log(self):
        #doc = lxml.html.fromstring(self.this_string)
        #cleaner = lxml.html.clean.Cleaner(style=True)
        #doc = cleaner.clean_html(doc)
        #text = doc.text_content()
        #log_split=self.this_string.split('#')
        #log_split=log_split[1].split('        ')
        print('log_split!!!!!!!!!!!!!!!!!!!!!!!!!!=',self.this_string)
        

class NumberThings:     
    def __init__ (self, this_number,pad):
        self.this_number = this_number
        self.pad = pad
        
    def pad_number(self):
        number_str=str(str(self.this_number))
        length=len(str(self.this_number))
        count=int(self.pad)
        pad='0'
        for x in range(count-1):
            pad=pad+'0'
        number_str = pad + number_str
        return number_str



#https://www.programiz.com/python-programming/modules/math
class DateCode:
    #getting days by selected day
    def __init__ (self,today,year,week):
        if today!='N/A':
            self.this_day = datetime.strptime(today, '%Y-%m-%d')
        if week=='N/A':
            self.today = today
            date_obj = datetime.strptime(today, '%Y-%m-%d')
            self.year = date_obj.year
            self.month = date_obj.month
            self.day =date_obj.day
           #print('self.today=',self.today)
            self.week=week
        else:
            self.year=year
            self.week=int(week)
           
    def this_year(self):
        return self.year
        
    def this_month(self):
        return self.month
        
    def this_day(self):
        return self.day
        
    
    def monday_of_calenderweek(self):
        first = date(int(self.year), 1, 1)
        base = 1 if first.isocalendar()[1] == 1 else 8
        return first + timedelta(days=base - first.isocalendar()[2] + 7 * (int(self.week) - 1))
    
    def weekday(self): 
        weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
        week_num=self.this_day.weekday()
        weekday=weekDays[week_num]
        return weekday
    
    def first_day_month(self): 
        first_day=self.today.replace(day=1)
        return first_day    
    
    def start_of_week(self): 
        date_obj = datetime.strptime(self.today, '%Y-%m-%d')
        return date_obj - timedelta(days=date_obj.weekday())  # Monday
    
    def end_of_week(self): 
        date_obj = datetime.strptime(self.today, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        return start_of_week + timedelta(days=5)  # Saturday
        
    def sunday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday
        #print(start_of_week)
        #print(end_of_week)
        return end_of_week
    
    def monday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=1)  # Monday
        return start_of_week
    
    def tuesday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        day = start_of_week + timedelta(days=1)  # Tuesday
        return day
    def last_wednesday_month(self):
        date_obj = datetime.strptime(self.today, '%Y-%m-%d')
        print('date_obj=',date_obj)
        offset = (date_obj.weekday() - WEDNESDAY) % 7
        last_wednesday = date_obj - timedelta(days=offset)
        return last_wednesday
    
    def wednesday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        day = start_of_week + timedelta(days=2)  # Wednesday
        return day
    def thursday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        day = start_of_week + timedelta(days=3)  # Thursday
        return day
    
    def friday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day) + ' 00:00:00'
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=4)  # Friday
        #print(start_of_week)
        #print(end_of_week)
        return end_of_week 
        
    def saturday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day) + ' 00:00:00'
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=5)  # Friday
        #print(start_of_week)
        #print(end_of_week)
        return end_of_week

class WeekCode:
    def __init__ (self,today,days):
        if today=='N/A':
            timestamp = datetime.today() 
            self.today = timezone.now()
        else:
            self.today=today
        
        self.year = today.year
        self.month = today.month
        self.day = today.day
        self.hour = today.hour
        self.minute = today.minute
        self.sec = today.second
        self.days = days
        try:
            a = int(days)
        except:
            print('Now we can extract year from days=', days)
            if 'year' in days:
                year_str= days.split(',')
                self.year=int(year_str[1])
                self.days = days=1
        self.monthstr = {1: "Jan", 2: "Feb",  3: "March", 4: 'April', 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sept", 10: "Oct", 11: "Nov", 12: "Dec"}
        self.monthnum = {"Jan":1,"Feb":2,"March":3,'April':4,"May":5,"Jun":6,"Jul":7, "Aug":8,"Sept":9,"Oct":10,"Nov":11,"Dec":11}
        self.month_list = ["Jan","Feb","March",'April',"May","Jun","Jul","Aug","Sept","Oct","Nov","Dec"]
    
    def leap_year(self):
        if (self.year % 4) == 0:
           if (self.year % 100) == 0:
               if (self.year % 400) == 0:
                   return True
               else:
                   return False
           else:
               return True
        else:
           return False
    
    def last_month_length(self):
        leap = self.leap_year()
        month=self.month-1
        if month==2 and leap:
            return 29
        elif month==2 and not leap:
            return 28
        elif month==4 or month ==6 or month==9 or month==11:
            return 30
        else:
            return 31
    def today_plus(self): 
        #Equations to get today + x days
        #print(self.days)
        #print('look here',self.year, self.month, self.day+1)
        new_date=self.today
        new_date += timedelta(days=self.days)
        return new_date
    
    def today_minus(self):
        leap_year = self.leap_year()
        last_month_days = self.last_month_length()
        newday=last_month_days+self.day-self.days
        #print('newday=',newday)
        #print('last_month_days',last_month_days)
        #print('self.day=',self.day)
        #print('self.days=',self.days)
        #print('self.month=',self.month)
        new_date=self.today
        #print('new_date=',new_date,' self.days=',self.days)
        new_date -= timedelta(days=self.days)
        return new_date
    
    
    def sunday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday
        #print(start_of_week)
        #print(end_of_week)
        return end_of_week
    
    def monday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=1)  # Sunday
        return start_of_week
    
    def tuesday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        day = start_of_week + timedelta(days=1)  # Sunday
        return day
    
    def wednesday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        day = start_of_week + timedelta(days=2)  # Sunday
        return day
    def thursday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        day = start_of_week + timedelta(days=3)  # Sunday
        return day
    
    def friday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day) + ' 00:00:00'
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=4)  # Friday
        #print(start_of_week)
        #print(end_of_week)
        return end_of_week 
        
    def saturday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day) + ' 00:00:00'
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=5)  # Friday
        #print(start_of_week)
        #print(end_of_week)
        return end_of_week

class TimeCode:
    def __init__ (self,days):
        timestamp = datetime.today() 
        self.today = timezone.now()
        self.year = timestamp.year
        self.month = timestamp.month
        self.day = timestamp.day
        self.hour = timestamp.hour
        self.minute = timestamp.minute
        self.sec = timestamp.second
        self.days = days
        try:
            a = int(days)
        except:
            print('Now we can extract year from days=', days)
            if 'year' in days:
                year_str= days.split(',')
                self.year=int(year_str[1])
                self.days = days=1
        self.monthstr = {1: "Jan", 2: "Feb",  3: "March", 4: 'April', 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sept", 10: "Oct", 11: "Nov", 12: "Dec"}
        self.monthnum = {"Jan":1,"Feb":2,"March":3,'April':4,"May":5,"Jun":6,"Jul":7, "Aug":8,"Sept":9,"Oct":10,"Nov":11,"Dec":11}
        self.month_list = ["Jan","Feb","March",'April',"May","Jun","Jul","Aug","Sept","Oct","Nov","Dec"]
        
    
    def this_today(self):
        return timezone.now()
        
    def this_year(self):
        return self.year
        
    def this_month(self):
        return self.month
        
    def this_day(self):
        return self.day
    
    def this_hour(self):
        return self.hour   
    
    def this_minute(self):
        return self.minute
        
    def this_sec(self):
        return self.sec
    
    def this_quarter(self):
        quarter = f'Q{(self.month-1)//3+1}'
        return quarter
    
    def quarterly(self):
        import datetime

        results=[]
        start_date_str = "01/01/" + str(self.year)
        end_date_str = "12/31/" + str(self.year)

        start_date = datetime.datetime.strptime(start_date_str, "%m/%d/%Y").date()
        end_date = datetime.datetime.strptime(end_date_str, "%m/%d/%Y").date()
        #print(f"Quarters within {start_date_str} and {end_date_str}:")
        start_of_quarter = start_date
        while True:
            far_future = start_of_quarter + datetime.timedelta(days=93)
            start_of_next_quarter = far_future.replace(day=1)
            end_of_quarter = start_of_next_quarter - datetime.timedelta(days=1)
            if end_of_quarter > end_date:
                break
            #print(f"\t{start_of_quarter:%d/%m/%Y} - {end_of_quarter:%m/%d/%Y}")
            results.append(start_of_quarter)
            start_of_quarter = start_of_next_quarter
            results.append(end_of_quarter)
            
        results=[[results[0],results[1]],[results[1],results[3]],[results[3],results[5]],[results[5],results[7]]]
        return results
    
    def leap_year(self):
        if (self.year % 4) == 0:
           if (self.year % 100) == 0:
               if (self.year % 400) == 0:
                   return True
               else:
                   return False
           else:
               return True
        else:
           return False
    
    def month_length(self):
        leap = self.leap_year()
        if self.month==2 and leap:
            return 29
        elif self.month==2 and not leap:
            return 28
        elif self.month==4 or self.month ==6 or self.month==9 or self.month==11:
            return 30
        else:
            return 31
            
    def last_month_length(self):
        leap = self.leap_year()
        month=self.month-1
        if month==2 and leap:
            return 29
        elif month==2 and not leap:
            return 28
        elif month==4 or month ==6 or month==9 or month==11:
            return 30
        else:
            return 31
            
    def month_string(self):        
        return self.monthstr[self.month]
       
    def month_number(self):        
        return self.month
    
    def today_plus(self): 
        #Equations to get today + x days
        leap_year = self.leap_year()
        #print(self.days)
        #print('look here',self.year, self.month, self.day+1)
        new_date=self.today
        new_date += timedelta(days=self.days)
        return new_date
    
    def today_minus(self):
        leap_year = self.leap_year()
        last_month_days = self.last_month_length()
        newday=last_month_days+self.day-self.days
        #print('newday=',newday)
        #print('last_month_days',last_month_days)
        #print('self.day=',self.day)
        #print('self.days=',self.days)
        #print('self.month=',self.month)
        new_date=self.today
        #print('new_date=',new_date,' self.days=',self.days)
        new_date -= timedelta(days=self.days)
        return new_date
    
    def sunday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday
        #print(start_of_week)
        #print(end_of_week)
        return end_of_week
    
    def monday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=1)  # Sunday
        return start_of_week
    
    def tuesday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        day = start_of_week + timedelta(days=1)  # Sunday
        return day
    
    def wednesday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        day = start_of_week + timedelta(days=2)  # Sunday
        return day
    def thursday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        day = start_of_week + timedelta(days=3)  # Sunday
        return day
    
    def friday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day) + ' 00:00:00'
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=4)  # Friday
        #print(start_of_week)
        #print(end_of_week)
        return end_of_week 
        
    def saturday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day) + ' 00:00:00'
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=5)  # Friday
        #print(start_of_week)
        #print(end_of_week)
        return end_of_week
    
    def is_monday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
       #print('start_of_week=',start_of_week)
        monday = str(start_of_week).split('-')
        monday = monday[2]
        monday = monday.split()
        monday = monday[0]
       #print('monday=',monday,' self.day=',self.day)
        if str(monday) in str(self.day):
            return True
        else:
            return False
    
    def is_tuesday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        tuesday = str(start_of_week).split('-')
        tuesday = tuesday[2]
        tuesday = tuesday.split()
        tuesday = tuesday[0]
        if str(tuesday) in str(self.day):
            return True
        else:
            return False
            
    def is_wednesday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        wednesday = str(start_of_week).split('-')
        wednesday = wednesday[2]
        wednesday = wednesday.split()
        wednesday = wednesday[0]
        if str(wednesday) in str(self.day):
            return True
        else:
            return False
                
    def is_thursday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        thursday = str(start_of_week).split('-')
        thursday = thursday [2]
        thursday = thursday .split()
        thursday = thursday[0]
        if str(thursday) in str(self.day):
            return True
        else:
            return False
    
    
    def is_friday(self):
        date_str = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=4)  # Sunday
        friday = str(end_of_week).split('-')
        friday = friday[2]
        friday = friday.split()
        friday = friday[0]
       #print('friday=',friday,'self.day=',self.day)
        if str(friday) in str(self.day):
            return True
        else:
            return False
            
    def end_of_month(self):
        eom=self.month_length()
       #print('eom=',eom)
        if self.day==eom:
            return True
        else:
            return False
   
    def weekday_num(self):
        week_num=self.today.weekday()+1
        return week_num
    
    def weekday(self):
        weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
        week_num=self.today.weekday()
        weekday=weekDays[week_num]
        return weekday
    
    def week_of_month(self):  
        day_of_month = datetime.now().day
        week_number = (day_of_month - 1) // 7 + 1
        print('week_number=',week_number)
        return week_number
    
    def week(self):
        ww=datetime.date(self.today).strftime("%V")
        return ww
        
 
class GPSCode:
    def __init__ (lat1,lon1,lat2,lon2,unit):
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2
        self.unit = unit
              
    def distance(self):
        try:
            if self.lat1==self.lat2 and self.lon1==lself.on2:
                return 0
            else:
                theta = self.lon1 - self.lon2
                
                dist = math.sin(self.deg2rad(self.lat1)) * math.sin(self.deg2rad(self.lat2)) + math.cos(self.deg2rad(self.lat1)) * math.cos(self.deg2rad(self.lat2)) * math.cos(self.deg2rad(theta))
                dist = math.acos(dist)
                dist = self.rad2deg(dist)
                dist = dist * 60 * 1.1515
                if unit == "K":
                    dist = dist * 1.609344
                elif unit == "N":
                    dist = dist * 0.8684
                return dist
        except IOError as e:
            print('error = ',e) 
            return 0            
            
   
    def deg2rad (self,deg):
        ans = deg * math.pi / 180.0
        return ans
        
    def rad2deg (self,rad):
        ans = rad / math.pi * 180.0
        return ans
        
    def get_num(self,x):
        return float(''.join(ele for ele in x if ele.isdigit() or ele == '.'))


class Costing:        
    def __init__ (self, request,charge_time):
        self.request = request
        self.charge_time = charge_time
        #print('In security')
        #print('self.page=',self.page)
        #print('self.request=',self.request)
    
    def user_hourly_cost(self):
        weeks = 52
        hours = 40
        cost = 0
        hourly = 0
        profile = UserProfileInfo.objects.filter(user=self.request.user).last()
       #print('profile=',profile)
        if profile:
           print('profile.salaried=',profile.salaried)
            
        if profile.salaried==0 and profile.hourly==0:
            cost=0
        elif profile.salaried!=0:
            #calculate hourly rate from year salary
            hourly = (profile.salaried/weeks)/hours
           #print('hourly=',hourly)
           #print('self.charge_time=',self.charge_time)
            #cannot exceed 8 hours for salaried employees
            if self.charge_time >8:
                charge_time=8
            else:
                charge_time=float(self.charge_time)
            cost=charge_time * float(hourly)
        elif profile.hourly!=0: 
            if self.charge_time >8:# time + 1/2 for hourly employees over 8 hours
                overtime=float(self.charge_time)-8
                overtime_charge = profile.hourly + (profile.hourly/2) # time and 1/2
                cost = 8 * profile.hourly
                overtime_cost=overtime*overtime_charge
                cost = cost + overtime_cost
            else:
                cost=float(self.charge_time) * float(profile.hourly)
       #print('cost11=',cost)
        return cost


class Security:
    def __init__ (self, request, page):
        self.page = page
        self.request = request
        #print('In security')
        #print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!self.page=',self.page)
        #print('self.request=',self.request)
        
        
    def visitor_monitor(self):
        timestamp = date.today()
        visitor =  self.get_visitor()
       #print('visitor-',visitor)
        client_id=self.get_client_id()
        user_agent=self.get_user_agent()
        session_id = self.get_session_id()
        visitor_ip = self.get_visitor_ip()
        phone_list = self.get_security_phone_list()
        email_list = self.get_security_email_list()
        cookie = self.get_cookie()
        email = self.get_email()
       #print('In visitor_monitor')
        reason = -1
        error_message =-1
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Check Database~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       #print('visitor+',visitor)
        if Visitor.objects.filter(Q(client_id=client_id) | Q(visitor=visitor) | Q(user_agent=user_agent) | Q(visitor_ip=visitor_ip)).exists():
            isthere = Visitor.objects.filter(Q(client_id=client_id) | Q(visitor=visitor) | Q(user_agent=user_agent) | Q(visitor_ip=visitor_ip))
           #print('isthere=',isthere)
            if isthere:
               #print('isthere=',isthere)
                visitor = isthere[0].visitor
                email = isthere[0].email
                reason = isthere[0].blocked_reason
                isblocked = isthere[0].blocked
               #print('blocked=',isblocked)
               #print('visitor=',visitor)
                if isblocked:
                    error_message = isthere[0].blocked_reason
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~Send Message to staff ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    subject = 'Blocked user visiting ATS ' + self.page + ' page'
                    email_body = visitor + ' is attempting re-entry onto this page after being blocked\n\nBlocked Reason: ' + reason + '\n\nvisitor_ip: ' + visitor_ip + '\n\nClient_id: ' + client_id + '\n\nCookie: ' + cookie + '\n\nUser Agent: ' + user_agent
                    email=Email(email_list,subject, email_body)
                   #print('email=',email)
                    email.send_email()
                    mes= 'Blocked user visiting  ' + self.page + ' page' + ' Check your email' 
                    com=Comunication(phone_list,mes)
                   #print('com=',com)
                    com.send_sms()
                    blocked = True
        else:
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Save New visitor info to Database~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            Visitor.objects.create(visitor=visitor,email=email,session_id=session_id,client_id=client_id,
                                user_agent=user_agent,visitor_ip=visitor_ip,created_on=timestamp,last_entry=timestamp)
        return error_message
    

    def get_cookie(self):
        cookie = str(self.request.headers.get('Cookie'))
       #print('cookie=',cookie)
        return cookie
        
    def get_visitor(self):
        visitor = str(self.request.user)
        client_id=self.get_client_id()
        if Visitor.objects.filter(client_id=client_id).exists():
            isthere = Visitor.objects.filter(client_id=client_id)
           #print('isthere=',isthere)
            visitor = isthere[0].visitor
        
       #print('visitor=',visitor)
        return visitor
        
    def get_email(self):
        if str(self.request.user) != 'AnonymousUser':
            email = str(self.request.user.email)
        else:
            email = 'N/A'
       #print('email=',email)
        return email
        
    def get_client_id(self):
        cookie_array =[]
        inner_array =[]
        email='N/A'
        cookie = str(self.request.headers.get('Cookie'))
        cookie_array= cookie.split( ';',-1)
       #print('Cookie=',cookie)
        inner_array=cookie_array[0].split( '=',-1) 
       #print('inner_array=',inner_array)
       #print('len(inner_array=',len(inner_array))
        if len(inner_array) >=2:
            client_id=inner_array[1]
        else:
            client_id='Unknown'
       #print('client_id=',client_id)
        return client_id    
    
    def get_session_id(self):
        cookie_array =[]
        inner_array =[]
        email='N/A'
        cookie = str(self.request.headers.get('Cookie'))
        cookie_array= cookie.split( ';',-1)
        visitor = str(self.request.user)
        session_id ='N/A'
        if visitor!='AnonymousUser':
            inner_array=cookie_array[2].split( '=',-1) 
            if len(inner_array) >=2:
                session_id=inner_array[1]
            else:
                session_id='Unknown'
           #print('session_id=',session_id)
 
        return session_id    
    
    def get_user_agent(self):
        user_agent = str(self.request.headers.get('User-Agent'))
        return user_agent    
        
   
    def get_contactus_phone_list(self):
        #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list/security ~~~~~~~~~~~~~~~~~~~~~~~~
        profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_developer=True) |  Q(alerts_security=True) | Q(alerts_sales=True) | Q(alerts_marketing=True)).all()
       #print('profiles=',profiles)
        phone_list=[]
        for staff in profiles:
            if staff.alerts_web_monitor:
                phone_list.append(staff.phone)
       #print('phone_list=',phone_list)
        return phone_list
    
    def get_contactus_email_list(self):
        #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list/security ~~~~~~~~~~~~~~~~~~~~~~~~
        profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_developer=True) | Q(alerts_help_desk=True) | Q(alerts_security=True) | Q(alerts_sales=True) | Q(alerts_marketing=True)).all()
       #print('profiles=',profiles)
        email_list=[]
        for staff in profiles:
            if staff.alerts_web_monitor:
                email_list.append(staff.email)
       #print('email_list=',email_list)
        return email_list
    
    def get_sales_phone_list(self):
        #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list/security ~~~~~~~~~~~~~~~~~~~~~~~~
        profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_developer=True) | Q(alerts_sales=True)).all()
       #print('profiles=',profiles)
        phone_list=[]
       #print('profiles[0]=',profiles[0].address)
        for staff in profiles:
            if staff.alerts_web_monitor:
                phone_list.append(staff.phone)
       #print('phone_list=',phone_list)
        return phone_list
    
    def get_sales_email_list(self):
        #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list/security ~~~~~~~~~~~~~~~~~~~~~~~~
        profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_developer=True) | Q(alerts_help_desk=True)| Q(alerts_sales=True)).all()
       #print('profiles=',profiles)
        phone_list=[]
        email_list=[]
       #print('profiles[0]=',profiles[0].address)
        for staff in profiles:
            if staff.alerts_web_monitor:
                email_list.append(staff.email)
       #print('email_list=',email_list)
        return email_list
    
    def get_marketing_phone_list(self):
        #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list/security ~~~~~~~~~~~~~~~~~~~~~~~~
        profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_developer=True) | Q(alerts_marketing=True)).all()
       #print('profiles=',profiles)
        phone_list=[]
       #print('profiles[0]=',profiles[0].address)
        for staff in profiles:
            if staff.alerts_web_monitor:
                phone_list.append(staff.phone)
       #print('phone_list=',phone_list)
        return phone_list
    
    def get_marketing_email_list(self):
        #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list/security ~~~~~~~~~~~~~~~~~~~~~~~~
        profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_developer=True) | Q(alerts_marketing=True)).all()
       #print('profiles=',profiles)
        phone_list=[]
        email_list=[]
       #print('profiles[0]=',profiles[0].address)
        for staff in profiles:
            if staff.alerts_web_monitor:
                email_list.append(staff.email)
       #print('email_list=',email_list)
        return email_list
        
    def get_security_phone_list(self):
        #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list/security ~~~~~~~~~~~~~~~~~~~~~~~~
        profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_developer=True) |  Q(alerts_security=True)).all()
       #print('profiles=',profiles)
        phone_list=[]
       #print('profiles[0]=',profiles[0].address)
        for staff in profiles:
            if staff.alerts_web_monitor:
                phone_list.append(staff.phone)
       #print('phone_list=',phone_list)
        return phone_list
    
    def get_security_email_list(self):
        #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list/security ~~~~~~~~~~~~~~~~~~~~~~~~
        profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_developer=True) |  Q(alerts_security=True)).all()
       #print('profiles=',profiles)
        phone_list=[]
        email_list=[]
       #print('profiles[0]=',profiles[0].address)
        for staff in profiles:
            if staff.alerts_web_monitor:
                email_list.append(staff.email)
       #print('email_list=',email_list)
        return email_list
   
    
    def get_newuser_phone_list(self):
        #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list/security ~~~~~~~~~~~~~~~~~~~~~~~~
        profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_developer=True) | Q(alerts_sales=True) | Q(alerts_marketing=True)).all()
       #print('profiles=',profiles)
        phone_list=[]
       #print('profiles[0]=',profiles[0].address)
        for staff in profiles:
            if staff.alerts_web_monitor:
                phone_list.append(staff.phone)
       #print('phone_list=',phone_list)
        return phone_list
    
    def get_newuser_email_list(self):
        #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list/security ~~~~~~~~~~~~~~~~~~~~~~~~
        profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_developer=True) | Q(alerts_sales=True) | Q(alerts_marketing=True)).all()
       #print('profiles=',profiles)
        phone_list=[]
        email_list=[]
       #print('profiles[0]=',profiles[0].address)
        for staff in profiles:
            if staff.alerts_web_monitor:
                email_list.append(staff.email)
       #print('email_list=',email_list)
        return email_list
    
    def get_monitor_phone_list(self):
        #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list/security ~~~~~~~~~~~~~~~~~~~~~~~~
        profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_developer=True)).all()
       #print('profiles=',profiles)
        phone_list=[]
       #print('profiles[0]=',profiles[0].address)
        for staff in profiles:
            if staff.alerts_web_monitor:
                phone_list.append(staff.phone)
       #print('phone_list=',phone_list)
        return phone_list
    
    def get_monitor_email_list(self):
        #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list/security ~~~~~~~~~~~~~~~~~~~~~~~~
        profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_developer=True)).all()
       #print('profiles=',profiles)
        email_list=[]
       #print('profiles[0]=',profiles[0].address)
        for staff in profiles:
            if staff.alerts_web_monitor:
                email_list.append(staff.email)
       #print('email_list=',email_list)
        return email_list
    
    def get_security_phone_list(self):
        #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list/security ~~~~~~~~~~~~~~~~~~~~~~~~
        profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_security=True) | Q(alerts_developer=True)).all()
       #print('profiles=',profiles)
        phone_list=[]
       #print('profiles[0]=',profiles[0].address)
        for staff in profiles:
            if staff.alerts_web_monitor:
                phone_list.append(staff.phone)
       #print('phone_list=',phone_list)
        return phone_list
    
    def get_security_email_list(self):
        #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list/security ~~~~~~~~~~~~~~~~~~~~~~~~
        profiles = UserProfileInfo.objects.filter(Q(alerts_web_monitor=True) | Q(alerts_security=True) | Q(alerts_developer=True)).all()
       #print('profiles=',profiles)
        email_list=[]
       #print('profiles[0]=',profiles[0].address)
        for staff in profiles:
            if staff.alerts_web_monitor:
                email_list.append(staff.email)
       #print('email_list=',email_list)
        return email_list
    
    def get_visitor_ip(self):
        PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', )
        remote_address = self.request.META.get('HTTP_X_FORWARDED_FOR') or self.request.META.get('REMOTE_ADDR')
       #print("remote_address=",remote_address)
        ip = remote_address
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
       #print("x_forwarded_for=",x_forwarded_for)
        if x_forwarded_for:
            proxies = x_forwarded_for.split(',')
            while (len(proxies) > 0 and proxies[0].startswith(PRIVATE_IPS_PREFIX)):
                proxies.pop(0)
                if len(proxies) > 0:
                    ip = proxies[0]
                   #print("IP Address",ip)
        visitor_ip = ip
        #print('visitor_ip=',visitor_ip)
        if UserProfileInfo.objects.filter(user=self.request.user).exists():
            UserProfileInfo.objects.filter(user=self.request.user).update(ip_address=ip)
        return visitor_ip
 

    def get_active_user(self):
        return self.request.user
        
    def get_active_user_name(self):
        return self.request.user.get_full_name()

    def get_active_user_firstname(self):
        return self.request.user.get_short_name()
        
    def get_active_group(self):
        active_group=UserProfileInfo.objects.filter(user=self.request.user).last()
        active_group=active_group.active_group
        return active_group
     
    def get_lean_status(self):
        lean=UserProfileInfo.objects.filter(user=self.request.user).last()
        lean_status=lean.lean_status
        return lean_status
    
    def get_user_name_from_user_code(self):
        this_user=self.page.split('.')
        this_user=str(this_user[0]) + str(this_user[1])
        if User.objects.filter(username__icontains=this_user).exists():
            user=User.objects.filter(username__icontains=this_user).last()
            user_name = user.get_full_name()
        else:
            user_name ='AnonymousUser'
        return user_name
    
    def get_user_code(self):
        # ex. Michael Ford = M.FORD
        custom_code=False
        full_name = self.page.split( )
        #print('full_name=',full_name)
        firstname=full_name[0]
        lastname=full_name[1]
        #~~~~~~~~~~~~~Special Cases~~~~~~~~~~~~~~~~~~~~
        if firstname=='Theodore':
            firstname='Theo'
        if firstname=='Chevy':
            firstname='Sevket'
        if firstname=='Kayla' and lastname=='Ford':
            lastname='FORD (KAYLA)'
        if firstname=='Dylan' and lastname=='Guiffre':
            lastname='GUIFFRE (DYLAN)'
        if firstname=='Arvils' and lastname=='Ozols':
            lastname='OZOLS (OZZIE)'    
        if firstname=='Linavel' and lastname=='Hernandez':
            lastname=' RODRIGUEZ'  
        if firstname=='Vernon' and lastname=='Thornton':
            lastname=' THORNTON'      
        if firstname=='Nancy' and lastname=='Romero':
            user_code='NANCY R'
            custom_code=True
        #~~~~~~~~~~~~~Special Cases~~~~~~~~~~~~~~~~~~~~
        
        if not custom_code:
            user_code= firstname[0].upper() + '.' + lastname.upper()
        return user_code  
    
    def create_user_name(self):
        # ex.  M.FORD = Michael Ford 
        full_name = self.page.split( )
        #print('full_name=',full_name)
        firstname=full_name[0]
        lastname=full_name[1]
        if firstname=='Theodore':
            firstname='Theo'
        user_code= firstname[0].upper() + lastname[0].upper()
        return user_code  
    
    def get_user_group(self):
        full_name = self.page.split( )
        firstname=full_name[0]
        lastname=full_name[1]
        if firstname=='Theodore':
            firstname='Theo'
        #print('firstname=',firstname,' lastname=',lastname) 
        user = User.objects.filter(first_name=firstname).filter(last_name=lastname).last()
        if user:
            #print('user=',user)
            active_group=UserProfileInfo.objects.filter(user=user.pk).last()
            active_group=active_group.active_group
            #print('active_group=',active_group)
        else:
            active_group='UNK'
        return active_group  

    def get_user_position(self):
        user_position  = 'Operator'
        full_name = self.page.split()
        print('full_name=',full_name)
        firstname=full_name[0]
        lastname=full_name[1]
        #print('firstname=',firstname,' lastname=',lastname) 
        user = User.objects.filter(first_name=firstname).filter(last_name=lastname).last()
        query_set = Group.objects.filter(user=user.pk)
        #print('user=',user)
        for g in query_set:
            if 'Management'in g.name:
                user_position  = 'Executive'
                break 
            elif 'Manager'in g.name:
                user_position  = 'Manager'
                break 
            elif 'Supervisor'in g.name:
                user_position  = 'Supervisor'
                break 
            elif 'Administrator'in g.name:
                user_position  = 'Administrator'
                break 
            else:
                user_position  = 'Operator'
        return user_position  
        
        
    def get_user_email(self):
        #~~~~~~~~~~~~~~~~~~~~Get Web_monitor email/phone list/security ~~~~~~~~~~~~~~~~~~~~~~~~
        name = self.page
        full_name = name.split( )
        firstname=full_name[0]
        lastname=full_name[1]
        if firstname=='Theodore':
            firstname='Theo'
        #print('firstname=',firstname,' lastname=',lastname) 
        user = User.objects.filter(first_name=firstname).filter(last_name=lastname).last()
        email=user.email
       #print('email=',email)
        return email
        
    def get_user_profile(self):
        print('self.page=',self.page)
        full_name = self.page.split( )
       #print('full_name=',full_name)
        firstname=full_name[0]
        lastname=full_name[1]
        if firstname=='Theodore':
            firstname='Theo'
        #print('firstname=',firstname,' lastname=',lastname) 
        user = User.objects.filter(first_name=firstname).filter(last_name=lastname).last()
        active_profile =[]
        if user:
            #print('user=',user)
            active_profile=UserProfileInfo.objects.filter(user=user.pk).last()
        return active_profile  
        
    def get_user_emails(self):
        email_list=[]
        name_list = self.page
        print('name_list=',name_list)
        for name in name_list:
            if name==-1:
                return name_list
            if '@' in name:
                return name_list
            if name!=-1 and name!='':
                full_name = name.split()
                if len(full_name) == 1:
                    email_list.append(str(name) +'@innovativepp.com')
                else:
                    firstname=full_name[0]
                    lastname=full_name[1]
                    if firstname=='Theodore':
                        firstname='Theo'
                    #print('firstname=',firstname,' lastname=',lastname) 
                    user = User.objects.filter(first_name=firstname).filter(last_name=lastname).last()
                    if user:
                        print('user.email=',user.email)
                        email_list.append(user.email)
                    #print('email_list=',email_list)
        email_list=sorted(email_list)
        return email_list           
   
    def get_all_users(self):
        users=[]
        all_users = User.objects.exclude(email__isnull=True).values()
        for this_user in all_users:
            user_name=this_user['username']
            user = User.objects.filter(username=user_name).last()
            #print('user.email=',user.email)
            users.append(user_name)
        users=sorted(users)
        return users
           
    def get_all_user_names(self):
        users=[]
        all_users = User.objects.values()
        for this_user in all_users:
            name=this_user['first_name'] + " " + this_user['last_name']
            #print('name=',name)
            users.append(name)
        users=sorted(users)
        #print('users=',users)
        return users
    
    def get_active_user_names(self):
        users=[]
        all_users = User.objects.values()
        for this_user in all_users:
            name=this_user['first_name'] + " " + this_user['last_name']
            active_profile=UserProfileInfo.objects.filter(active=True).filter(user=this_user['id']).last()
            if active_profile and name!=' ' :
                users.append(name)
        users=sorted(users)
        #print('users=',users)
        return users
    
    def get_ticket_user_names(self):
        users=[]
        all_users = User.objects.values()
        for this_user in all_users:
            name=this_user['first_name'] + " " + this_user['last_name']
            active_profile=UserProfileInfo.objects.filter(active=True).filter(user=this_user['id']).last()
            if active_profile and name!=' ' :
                if active_profile.ticket_list:
                    users.append(name)
        users=sorted(users)
       #print('users=',users)
        return users
    
    def get_gemba_user_names(self):
        users=[]
        all_users = User.objects.values()
        #Find users with the Gemba Flag
        for this_user in all_users:
            name=this_user['first_name'] + " " + this_user['last_name']
            active_profile=UserProfileInfo.objects.filter(gemba_team=True).filter(active=True).filter(user=this_user['id']).last()
            if active_profile and name!=' ' :
                users.append(name)
        users=sorted(users)
                   
        #print('users=',users)
        return users
    
       
    def get_time_card_user_names(self):
        users=[]
        all_users = User.objects.values()
        #print('all_users=',all_users)
        for this_user in all_users:
            name=this_user['first_name'] + " " + this_user['last_name']
           #print('name=',name)
            active_profile=UserProfileInfo.objects.filter(active=True).filter(paychex=True).filter(user=this_user['id']).last()
           #print('active_profile=',active_profile)
            if active_profile:
                if active_profile:
                    #print('name=',name)
                    users.append(name)
        users=sorted(users)
       #print('users=',users)
        return users
    
    def get_ci_user_names(self):
        users=[]
        all_users = User.objects.values()
        for this_user in all_users:
            name=this_user['first_name'] + " " + this_user['last_name']
           #print('name=',name)
            active_profile=UserProfileInfo.objects.filter(active=True).filter(user=this_user['id']).last()
            if active_profile:
                if active_profile.ci_list:
                    #print('name=',name)
                    users.append(name)
        users=sorted(users)
        #print('users=',users)
        return users
    
    def get_dept_users(self):
        users=[]
        #Sales
        group = Group.objects.get(name='Administrator')
        admin_users = group.user_set.all()
        #print('admin_users=',admin_users)
        group = Group.objects.get(name=self.page)
        dept_users = group.user_set.all()
        #print('dept_users1=',dept_users)
        for this_user in dept_users:
            active_role=UserProfileInfo.objects.filter(active=True).filter(user=this_user).last()
            if active_role:
                name=this_user.first_name + ' ' + this_user.last_name
                #print('name=',name)
                users.append(name)
        #print('dept_users2=',users)
        '''
        #Add administrators to each group list for software trouble tickets
        if not 'Senior Management' in self.page:
            for this_user in admin_users:
                if User.objects.exclude(email__isnull=True).filter(username=this_user).exists():
                    name=this_user.first_name + ' ' + this_user.last_name
                    #print('name=',name)
                    if not name in users:
                        users.append(name)
        '''
        users=sorted(users)
        #print('dept_users3=',users)
        return users
   
    def get_costing_users(self):
        users=[]
        #Sales
        #print('%%%%%%%%%%%%%% IN Costing $$$$$$$$$$$$$$$$$$$$$$$$$$')
        group = Group.objects.get(name=self.page)
        dept_users = group.user_set.all()
        #print('dept_users=',dept_users)
        for this_user in dept_users:
            #print('this_user=',this_user)
            this_user = User.objects.filter(username=this_user).last()
            #print('this_user=',this_user.first_name)
            active_role=UserProfileInfo.objects.filter(active=True).filter(user=this_user).last()
            if active_role:
                if active_role.role:
                    active_role=active_role.role
                    #print('this_user=',this_user,' active_role=',active_role)
                    if 'Costing' in active_role:
                        name=this_user.first_name + " " + this_user.last_name
                        users.append(name)
        #print('users=',users)
        return users
        
    def get_dept_Manager_list(self):
        users=[]
        group=self.get_active_group()
        group_manager=str(group) + ' Manager'
        print('group_manager1=',group_manager)
        u=User.objects.filter(groups__name=group_manager)
        for user in u:
            name=user.first_name + ' ' + user.last_name
            users.append(name)
        users=sorted(users)
        #this_user=print('dept_managers=',users)
        return users
        
    def get_action_aprovers_list(self):
        users=[]
        u=User.objects.filter(groups__name='Action Approver')
        for user in u:
            name=user.first_name + ' ' + user.last_name
            users.append(name)
        users=sorted(users)
        #this_user=print('dept_managers=',users)
        return users
    
    def get_dept_Supervisor_list(self):
        users=[]
        group=self.get_active_group()
        group_supervisor= str(group) + ' Supervisor'
        print('group_supervisor1=',group_supervisor)
        u=User.objects.filter(groups__name=group_supervisor)
        for user in u:
            name=user.first_name + ' ' + user.last_name
            users.append(name)
        users=sorted(users)
        #this_user=print('dept_supervisor=',users)
        return users
    
    def get_internal_dept_users(self,dept):
        users=[]
        #Sales
        group = Group.objects.get(name=dept)
        dept_users = group.user_set.all()
        #print(dept,'_users=',dept_users)
        for this_user in dept_users:
            if User.objects.exclude(email__isnull=True).filter(username=this_user).exists():
                name=this_user.first_name + ' ' + this_user.last_name
                #print('name=',name)
                users.append(name)
        users=sorted(users)
        return users
    
    def get_active_users(self):
        active_users=[]
        for g in self.request.user.groups.all():
            if 'Sales' in g.name:
                temp=self.get_internal_dept_users('Sales')
                for user in temp:
                    if not user in active_users:
                        active_users.append(user)
            if 'Engineering' in g.name:
                temp=self.get_internal_dept_users('Engineering')
                for user in temp:
                    if not user in active_users:
                        active_users.append(user)
            if 'Test' in g.name:
                temp=self.get_internal_dept_users('Test')
                for user in temp:
                    if not user in active_users:
                        active_users.append(user)
                
            if 'Stock' in g.name:
                temp=self.get_internal_dept_users('Stock')
                for user in temp:
                    if not user in active_users:
                        active_users.append(user)
                
            if 'Software' in g.name:
                temp=self.get_internal_dept_users('Software')
                for user in temp:
                    if not user in active_users:
                        active_users.append(user)
               
            if 'Quality' in g.name:
                temp=self.get_internal_dept_users('Quality')
                for user in temp:
                    if not user in active_users:
                        active_users.append(user)
        active_users=sorted(active_users)
        return active_users
        
    def get_accounting_users(self):
        active_users=[]
        for g in self.request.user.groups.all():
            if 'Accounting' in g.name:
                temp=self.get_internal_dept_users('Accounting')
                for user in temp:
                    if not user in active_costing_users:
                        active_users.append(user)
        active_users=sorted(active_users)                
        return active_users
    
    
    def get_active_administrator(self):
        active_administrator = False
        for g in self.request.user.groups.all():
            #print ("g.name=", g.name)
            if 'Administrator' in g.name:
                active_administrator = True
                break 
            else:
                active_administrator = False

        #print('active_administrator1=',active_administrator)
        return active_administrator

    def get_active_manager(self):
        active_manager = False
        for g in self.request.user.groups.all():
            #print ("g.name ", g.name)
            if 'Manager' in g.name:
                active_manager = True
                break 
            else:
                active_manager = False

        #print('active_manager=',active_manager)
        return active_manager

    def get_active_supervisor(self):
        active_supervisor = False
        for g in self.request.user.groups.all():
            #print ("g.name ", g.name)
            if 'Supervisor' in g.name:
                active_supervisor = True
                break 
            else:
                active_supervisor = False

        #print('active_manager=',active_manager)
        return active_supervisor
    
    def get_executive_manager(self):
        executive_manager = False
        for g in self.request.user.groups.all():
            #print ("g.name ", g.name)
            if 'Management'in g.name:
                executive_manager = True
                break 
            else:
                executive_manager = False

       #print('executive_manager=',executive_manager)
        return executive_manager
    
    def get_dept_Manager(self):
        group=self.get_active_group()
        group_manager=str(group) + ' Manager'
        #print('group_managerd=',group_manager)
        dept_manager = False
        u=User.objects.filter(groups__name=group_manager)
        for user in u:
            name=user.username
            #print('name=',name,' username=',self.request.user)
            if name in str(self.request.user):
                dept_manager = True
                break
       #print('dept_manager=',dept_manager)
        return dept_manager
    
 
class Style:
    BOLD = '\x1b[1m'
    DIM = '\x1b[2m'
    NORMAL = '\x1b[22m'
    ITALIC = '\x1b[2m'
    UNDERLINE = '\x1b[4m'
    DBL_UNDERLINE = '\x1b[21m'
    NO_UNDERLINE = '\x1b[24m'
    OVERLINE = '\x1b[53m'
    NOT_OVERLINE = '\x1b[55m'
    SLOW_BLINK = '\x1b[5m'
    FAST_BLINK = '\x1b[6m'
    NO_BLINK = '\x1b[25m'
    REVERSE= '\x1b[7m'
    NO_REVERSE = '\x1b[27m'
    STRIKE = '\x1b[9m'
    NO_STRIKE = '\x1b[29m'
    FONT1 = '\x1b[10m'
    FONT2 = '\x1b[11m'
    FONT3 = '\x1b[12m'
    FONT4 = '\x1b[13m'
    FONT5 = '\x1b[14m'
    FONT6 = '\x1b[15m'
    FONT7 = '\x1b[16m'
    FONT8 = '\x1b[17m'
    FONT9 = '\x1b[18m'
    FONT10 = '\x1b[19m'
    ITALIC_UNDERLINE = '\ x1b[2;4m'
    END = '\x1b[0m'
    RED = '\x1b[31m'
    GREEN = '\x1b[32m'
    BLUE = '\x1b[34m'
    YELLOW = '\x1b[33m'
    MAGENTA = '\x1b[35m'
    CYAN = '\x1b[36m'
    BLACK = '\x1b[30m'
    WHITE = '\x1b[37m'
    RED_BG = '\x1b[41m'
    GREEN_BG = '\x1b[42m'
    BLUE_BG = '\x1b[44m'
    YELLOW_BG = '\x1b[43m'
    MAGENTA_BG = '\x1b[45m'
    CYAN_BG = '\x1b[46m'
    BLACK_BG = '\x1b[40m'
    WHITE = '\x1b[37m'
    INVERSE = '\x1b[37;40m'
    INVERSE_BOLD= '\x1b[37;40m'
    BOLD_RED = '\x1b[1;31m'
    BOLD_GREEN = '\x1b[1;32m'
    HILITE = '\x1b[43m'
    BOLD_HILITE = '\x1b[1;43m'
    
        