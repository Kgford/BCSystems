from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from .forms import InventoryForm
from datetime import date
from django.urls import reverse, reverse_lazy
from equipment.models import Model
from locations.models import Location
from inventory.models import Inventory, Events
from django.views import View
import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
class InventoryView(View):
    #~~~~~~~~~~~Load Item database from csv. must put this somewhere else later"
    import csv
    timestamp  = date.today()      
    #load_iventory_csv(True)
    #load_events_csv(True)
    form_class = InventoryForm
    template_name = "index.html"
    success_url = reverse_lazy('inventory:inv')
    def get(self, *args, **kwargs):
        form = self.form_class()
        try:
            desc_list = Model.objects.order_by('description').values_list('description', flat=True).distinct()
            models_list = Model.objects.order_by('model').values_list('model', flat=True).distinct()
            locations_list = Location.objects.order_by('name').values_list('name', flat=True).distinct()
            shelves_list = Location.objects.order_by('shelf').values_list('shelf', flat=True).distinct()
            inv = Inventory.objects.all()
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"inventory/index.html",{"form": form, "inventory": inv, "desc_list":desc_list,
           "models_list":models_list, "locations_list":locations_list, "shelves_list":shelves_list, "index_type":"INVENTORY"})
    
    def post(self, request, *args, **kwargs):
        try:    
            json_data = []
            inv_list = []
            inv = []
            desc = request.POST.get('desc')
            print('request =',request)
            print('desc = ',desc)
            model = request.POST.get('_model')
            print('model = ',model)
            status = request.POST.get('status')
            print('status =',status)
            category = request.POST.get('_category')
            print('cat =',category)
            locationname = request.POST.get('_site')
            print('loc =',locationname)
            shelf = request.POST.get('_shelf')
            print('shelf =',shelf)
            select = request.POST.get('sel')
            print('select =',select)
            success = True  

            if select =="all" or select==None or select=='undefined':
                inv_list == Inventory.objects.all()
            elif desc == "select menu" and model == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":
                inv_list == Inventory.objects.all()
            elif select =="description": 
                if model == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":#description only 
                    inv_list == Inventory.objects.filter(Inventory.description__contains == desc).all()
                if not model == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #description, model 
                    inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model).all()  
                if model == "select menu" and not status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #description&status 
                    inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.status__contains == status).all()  
                if not model == "select menu" and not status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #description& model &  status 
                    inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory__contains == status).all()  
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and locationname == "select menu" and  shelf == "select": #description &  model, status, cat
                   inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory.status__contains == status & Inventory.category__contains == category).all() 
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and  shelf == "select": #description, model, status, cat' loc
                    inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory.status__contains == status & Inventory.category__contains == category & Inventory.locationname__contains == locationnamelocationname).all() 
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and not shelf == "select": #description &  model &  status &  cat' loc &  shelf
                    inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory.status__contains == status & Inventory.category__contains == category & Inventory.locationname__contains == locationnamelocationname & Inventory.shelf__contains == shelf).all()     
            elif select =="model": 
                if desc == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":#model only 
                    inv_list == Inventory.objects.filter(Inventory.modelname__contains == model).all()
                    print('Model we are here')
                if not model == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #model & description 
                    inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model).all()  
                if not model == "select menu" and not status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #model & description &  status 
                    inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory.status__contains == status).all()  
                if not model == "select menu" and not status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #model &  status 
                    inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory.status__contains == status).all()  
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and locationname == "select menu" and  shelf == "select": #model & description &   status &  cat
                   inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory.status__contains == status & Inventory.category__contains == category).all() 
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and  shelf == "select": #model & description &  status &  cat' loc
                    inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory.status__contains == status & Inventory.category__contains == category & Inventory.locationname__contains == locationnamelocationname).all() 
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and not shelf == "select": #model & description &  status &  cat' loc &  shelf
                    inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory.status__contains == status & Inventory.category__contains == category & Inventory.locationname__contains == locationnamelocationname & Inventory.shelf__contains == shelf).all()     
            elif select =="status": 
                if desc == "select menu" and model == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":#status only 
                    inv_list == Inventory.objects.filter(Inventory.status__contains == status).all()
                if not model == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #status &  model
                    inv_list == Inventory.objects.filter(Inventory.status__contains == status & Inventory.modelname__contains == model).all()  
                if model == "select menu" and not status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #status & description
                    inv_list == Inventory.objects.filter(Inventory.status__contains == status & Inventory.description__contains == desc).all()      
                if not model == "select menu" and not status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #status & model & description
                    inv_list == Inventory.objects.filter(Inventory.status__contains == status & Inventory.modelname__contains == model & Inventory.description__contains == desc).all()  
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and locationname == "select menu" and  shelf == "select": #status & model & description &  cat
                    inv_list == Inventory.objects.filter(Inventory.status__contains == status & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.category__contains == category).all() 
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and  shelf == "select": #status & model & description &  cat' loc
                    inv_list == Inventory.objects.filter(Inventory.status__contains == status & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.category__contains == category & Inventory.locationname__contains == locationnamelocationname).all() 
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and not shelf == "select": #status &  model & description &  cat' loc &  shelf
                    inv_list == Inventory.objects.filter(Inventory.status__contains == status & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.category__contains == category & Inventory.locationname__contains == locationnamelocationname & Inventory.shelf__contains == shelf+"%").all()     
            elif select =="category": 
                if desc == "select menu" and model == "select menu" and status == "select menu" and locationname == "select menu" and  shelf == "select":#category only 
                    inv_list == Inventory.objects.filter(Inventory.category__contains == category).all()
                if not model == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #category &  model
                    inv_list == Inventory.objects.filter(Inventory.category__contains == category & Inventory.modelname__contains == model).all()  
                if not model == "select menu" and not status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #category & status & model & description
                    inv_list == Inventory.objects.filter(Inventory.category__contains == category & Inventory.modelname__contains == model & Inventory.description__contains == desc).all()  
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and locationname == "select menu" and  shelf == "select": #category & status & model & description
                    inv_list == Inventory.objects.filter(Inventory.category__contains == category & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status).all() 
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and  shelf == "select": #category & status & model & description &  cat
                    inv_list == Inventory.objects.filter(Inventory.category__contains == category & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status & Inventory.locationname__contains == locationnamelocationname+"%").all() 
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and not shelf == "select": #category &  status &  model & description &  cat'shelf
                    inv_list == Inventory.objects.filter(Inventory.category__contains == category & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status & Inventory.locationname__contains == locationnamelocationname & Inventory.shelf__contains == shelf).all()     
            elif select =="locationname": 
                if desc == "select menu" and model == "select menu" and status == "select menu" and category == "select menu" and  shelf == "select":#locationname only 
                    inv_list == Inventory.objects.filter(Inventory.locationname__contains == locationname).all()
                if not model == "select menu" and status == "select menu" and category == "select menu" and category == "select menu" and  shelf == "select":  #locationname &  model
                    inv_list == Inventory.objects.filter(Inventory.locationname__contains == locationname & Inventory.modelname__contains == model).all()  
                if not model == "select menu" and not status == "select menu" and category == "select menu" and category == "select menu" and  shelf == "select":  #locationname & status & model & description
                    inv_list == Inventory.objects.filter(Inventory.locationname__contains == locationname & Inventory.modelname__contains == model & Inventory.description__contains == desc).all()  
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and category == "select menu" and  shelf == "select": #locationname & status & model & description &  cat
                    inv_list == Inventory.objects.filter(Inventory.locationname__contains == locationnamelocationname & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status).all() 
                if not model == "select menu" and not status == "select menu" and not locationname == "select menu" and not category == "select menu" and  shelf == "select": #locationname & status & model & description &  cat
                   inv_list == Inventory.objects.filter(Inventory.locationname__contains == locationnamelocationname & Inventory.modelname.__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status & Inventory.category__contains == category).all() 
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and not category == "select menu" and not shelf == "select": #locationname & status &  model & description &  cat &  shelf
                    inv_list == Inventory.objects.filter(Inventory.locationname__contains == locationnamelocationname & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status & Inventory.category__contains == category & Inventory.shelf__contains == shelf).all()     
            elif select =="shelf": 
                if desc == "select menu" and model == "select menu" and status == "select menu" and category == "select menu" and  locationname == "select menu":#locationname only 
                    inv_list == Inventory.objects.filter(Inventory.shelf__contains == shelf).all()
                if not model == "select menu" and status == "select menu" and category == "select menu" and category == "select menu" and locationname == "select menu":  #locationname &  model
                    inv_list == Inventory.objects.filter(Inventory.shelf__contains == shelf & Inventory.modelname__contains == model).all()  
                if not model == "select menu" and not status == "select menu" and category == "select menu" and category == "select menu" and locationname == "select menu":  #locationname & status & model & description
                    inv_list == Inventory.objects.filter(Inventory.shelf__contains == shelf & Inventory.modelname__contains == model & Inventory.description__contains == desc).all()  
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and category == "select menu" and locationname == "select menu": #locationname & status & model & description &  cat
                    inv_list == Inventory.objects.filter(Inventory.shelf__contains == shelf & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status).all() 
                if not model == "select menu" and not status == "select menu" and not locationname == "select menu" and not category == "select menu" and locationname == "select menu": #locationname & status & model & description &  cat
                    inv_list == Inventory.objects.filter(Inventory.shelf__contains == shelf & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status & Inventory.category__contains == category).all() 
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and not category == "select menu" and locationname == "select menu": #locationname & status &  model & description &  cat &  shelf
                    inv_list == Inventory.objects.filter(Inventory.shelf__contains == shelf & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status & Inventory.category__contains == category,Inventory.locationname__contains == locationname).all()     
            else:
                inv_list ==None
        except IOError as e:
            nv_list = None
            print ("Lists load Failure ", e)

        if inv_list == None:
            success = False
        else:
            inv=[e.serialize() for e in inv_list]
        return render (self.request,"inventory/index.html",{"form": form, "inventory": inv_list})
                
        
# Create your views here.
class SearchView(View):
    template_name = "search.html"
    print('in search view')
    def get(self, *args, **kwargs):
        form = self.form_class()
        print('we are here')
        try:
            desc_list = Model.objects.order_by('description').values_list('description', flat=True).distinct()
            models_list = Model.objects.order_by('model').values_list('model', flat=True).distinct()
            locations_list = Location.objects.order_by('name').values_list('name', flat=True).distinct()
            shelves_list = Location.objects.order_by('shelf').values_list('shelf', flat=True).distinct()
            inv = Inventory.objects.all()
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"inventory/index.html",{"form": form, "inventory": inv, "desc_list":desc_list,
           "models_list":models_list, "locations_list":locations_list, "shelves_list":shelves_list, "index_type":"INVENTORY"})
    
    def post(self, *args, **kwargs):
        form = self.form_class()
        print(form)
        print('we are here')
        
   
def load_iventory_csv(delete):
    #~~~~~~~~~~~Load Item database from csv. must put this somewhere else later"
    import csv
    timestamp  = date.today()
    CSV_PATH = 'items.csv'
    print('csv = ',CSV_PATH)

    contSuccess = 0
    # Remove all data from Table
    if delete:
        Inventory.objects.all().delete()
    f = open(CSV_PATH)
    reader = csv.reader(f)
    print('reader = ',reader)
    for serial_number, modelname,description, locationname,shelf, category,status, quantity, remarks, recieved_date,shipped_date,last_update, update_by in reader:
        Inventory.objects.create(serial_number=serial_number, modelname=modelname, description=description, locationname=locationname,
        shelf=shelf, category=category,status=status, quantity=quantity, remarks=remarks, recieved_date=datetime.datetime.strptime(recieved_date, '%m/%d/%Y'),
        shipped_date=datetime.datetime.strptime(shipped_date, '%m/%d/%Y'), last_update=datetime.datetime.strptime(last_update, '%m/%d/%Y'), update_by=update_by)
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')
    
def load_events_csv(delete):
    #~~~~~~~~~~~Load Item database from csv. must put this somewhere else later"
    import csv
    timestamp  = date.today()      
    #~~~~~~~~~~~Load Events database from csv. must put this somewhere else later"
    CSV_PATH = 'events.csv'
    print('csv = ',CSV_PATH)

    contSuccess = 0
    
    # Remove all data from Table
    if delete:
        Events.objects.all().delete()

    f = open(CSV_PATH)
    reader = csv.reader(f)
    print('reader = ',reader)
    for event_type, event_date, operator, comment,locationname, inventory_id ,mr, rma in reader:
        Events.objects.create(event_type=event_type, event_date=datetime.datetime.strptime(event_date, '%m/%d/%Y'), operator=operator,comment=comment, locationname=locationname, mr=mr, rma =rma, inventory_id=inventory_id)
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')
    
    #~~~~~~~~~~~Load Events database from csv. must put this somewhere else later"   
    
def search(request,description):
    try:
        json_data = []
        inv_list = []
        inv = []
        desc = request.GET.get('desc')
        print('request =',request)
        print('desc = ',desc)
        model = request.GET.get('model')
        print('model = ',model)
        status = request.GET.get('status')
        print('status =',status)
        category = request.GET.get('category')
        print('cat =',category)
        locationname = request.GET.get('locationname')
        print('loc =',locationname)
        shelf = request.GET.get('shelf')
        print('shelf =',shelf)
        select = request.GET.get('sel')
        print('select =',select)
        success = True  

        if select =="all" or select==None or select=='undefined':
            inv_list == Inventory.objects.all()
        elif desc == "select menu" and model == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":
            inv_list == Inventory.objects.all()
        elif select =="description": 
            if model == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":#description only 
                inv_list == Inventory.objects.filter(Inventory.description__contains == desc).all()
            if not model == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #description, model 
                inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model).all()  
            if model == "select menu" and not status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #description&status 
                inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.status__contains == status).all()  
            if not model == "select menu" and not status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #description& model &  status 
                inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory__contains == status).all()  
            if not model == "select menu" and not status == "select menu" and not category == "select menu" and locationname == "select menu" and  shelf == "select": #description &  model, status, cat
               inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory.status__contains == status & Inventory.category__contains == category).all() 
            if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and  shelf == "select": #description, model, status, cat' loc
                inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory.status__contains == status & Inventory.category__contains == category & Inventory.locationname__contains == locationnamelocationname).all() 
            if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and not shelf == "select": #description &  model &  status &  cat' loc &  shelf
                inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory.status__contains == status & Inventory.category__contains == category & Inventory.locationname__contains == locationnamelocationname & Inventory.shelf__contains == shelf).all()     
        elif select =="model": 
            if desc == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":#model only 
                inv_list == Inventory.objects.filter(Inventory.modelname__contains == model).all()
                print('Model we are here')
            if not model == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #model & description 
                inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model).all()  
            if not model == "select menu" and not status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #model & description &  status 
                inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory.status__contains == status).all()  
            if not model == "select menu" and not status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #model &  status 
                inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory.status__contains == status).all()  
            if not model == "select menu" and not status == "select menu" and not category == "select menu" and locationname == "select menu" and  shelf == "select": #model & description &   status &  cat
               inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory.status__contains == status & Inventory.category__contains == category).all() 
            if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and  shelf == "select": #model & description &  status &  cat' loc
                inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory.status__contains == status & Inventory.category__contains == category & Inventory.locationname__contains == locationnamelocationname).all() 
            if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and not shelf == "select": #model & description &  status &  cat' loc &  shelf
                inv_list == Inventory.objects.filter(Inventory.description__contains == desc & Inventory.modelname__contains == model & Inventory.status__contains == status & Inventory.category__contains == category & Inventory.locationname__contains == locationnamelocationname & Inventory.shelf__contains == shelf).all()     
        elif select =="status": 
            if desc == "select menu" and model == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":#status only 
                inv_list == Inventory.objects.filter(Inventory.status__contains == status).all()
            if not model == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #status &  model
                inv_list == Inventory.objects.filter(Inventory.status__contains == status & Inventory.modelname__contains == model).all()  
            if model == "select menu" and not status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #status & description
                inv_list == Inventory.objects.filter(Inventory.status__contains == status & Inventory.description__contains == desc).all()      
            if not model == "select menu" and not status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #status & model & description
                inv_list == Inventory.objects.filter(Inventory.status__contains == status & Inventory.modelname__contains == model & Inventory.description__contains == desc).all()  
            if not model == "select menu" and not status == "select menu" and not category == "select menu" and locationname == "select menu" and  shelf == "select": #status & model & description &  cat
                inv_list == Inventory.objects.filter(Inventory.status__contains == status & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.category__contains == category).all() 
            if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and  shelf == "select": #status & model & description &  cat' loc
                inv_list == Inventory.objects.filter(Inventory.status__contains == status & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.category__contains == category & Inventory.locationname__contains == locationnamelocationname).all() 
            if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and not shelf == "select": #status &  model & description &  cat' loc &  shelf
                inv_list == Inventory.objects.filter(Inventory.status__contains == status & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.category__contains == category & Inventory.locationname__contains == locationnamelocationname & Inventory.shelf__contains == shelf+"%").all()     
        elif select =="category": 
            if desc == "select menu" and model == "select menu" and status == "select menu" and locationname == "select menu" and  shelf == "select":#category only 
                inv_list == Inventory.objects.filter(Inventory.category__contains == category).all()
            if not model == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #category &  model
                inv_list == Inventory.objects.filter(Inventory.category__contains == category & Inventory.modelname__contains == model).all()  
            if not model == "select menu" and not status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #category & status & model & description
                inv_list == Inventory.objects.filter(Inventory.category__contains == category & Inventory.modelname__contains == model & Inventory.description__contains == desc).all()  
            if not model == "select menu" and not status == "select menu" and not category == "select menu" and locationname == "select menu" and  shelf == "select": #category & status & model & description
                inv_list == Inventory.objects.filter(Inventory.category__contains == category & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status).all() 
            if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and  shelf == "select": #category & status & model & description &  cat
                inv_list == Inventory.objects.filter(Inventory.category__contains == category & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status & Inventory.locationname__contains == locationnamelocationname+"%").all() 
            if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and not shelf == "select": #category &  status &  model & description &  cat'shelf
                inv_list == Inventory.objects.filter(Inventory.category__contains == category & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status & Inventory.locationname__contains == locationnamelocationname & Inventory.shelf__contains == shelf).all()     
        elif select =="locationname": 
            if desc == "select menu" and model == "select menu" and status == "select menu" and category == "select menu" and  shelf == "select":#locationname only 
                inv_list == Inventory.objects.filter(Inventory.locationname__contains == locationname).all()
            if not model == "select menu" and status == "select menu" and category == "select menu" and category == "select menu" and  shelf == "select":  #locationname &  model
                inv_list == Inventory.objects.filter(Inventory.locationname__contains == locationname & Inventory.modelname__contains == model).all()  
            if not model == "select menu" and not status == "select menu" and category == "select menu" and category == "select menu" and  shelf == "select":  #locationname & status & model & description
                inv_list == Inventory.objects.filter(Inventory.locationname__contains == locationname & Inventory.modelname__contains == model & Inventory.description__contains == desc).all()  
            if not model == "select menu" and not status == "select menu" and not category == "select menu" and category == "select menu" and  shelf == "select": #locationname & status & model & description &  cat
                inv_list == Inventory.objects.filter(Inventory.locationname__contains == locationnamelocationname & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status).all() 
            if not model == "select menu" and not status == "select menu" and not locationname == "select menu" and not category == "select menu" and  shelf == "select": #locationname & status & model & description &  cat
               inv_list == Inventory.objects.filter(Inventory.locationname__contains == locationnamelocationname & Inventory.modelname.__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status & Inventory.category__contains == category).all() 
            if not model == "select menu" and not status == "select menu" and not category == "select menu" and not category == "select menu" and not shelf == "select": #locationname & status &  model & description &  cat &  shelf
                inv_list == Inventory.objects.filter(Inventory.locationname__contains == locationnamelocationname & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status & Inventory.category__contains == category & Inventory.shelf__contains == shelf).all()     
        elif select =="shelf": 
            if desc == "select menu" and model == "select menu" and status == "select menu" and category == "select menu" and  locationname == "select menu":#locationname only 
                inv_list == Inventory.objects.filter(Inventory.shelf__contains == shelf).all()
            if not model == "select menu" and status == "select menu" and category == "select menu" and category == "select menu" and locationname == "select menu":  #locationname &  model
                inv_list == Inventory.objects.filter(Inventory.shelf__contains == shelf & Inventory.modelname__contains == model).all()  
            if not model == "select menu" and not status == "select menu" and category == "select menu" and category == "select menu" and locationname == "select menu":  #locationname & status & model & description
                inv_list == Inventory.objects.filter(Inventory.shelf__contains == shelf & Inventory.modelname__contains == model & Inventory.description__contains == desc).all()  
            if not model == "select menu" and not status == "select menu" and not category == "select menu" and category == "select menu" and locationname == "select menu": #locationname & status & model & description &  cat
                inv_list == Inventory.objects.filter(Inventory.shelf__contains == shelf & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status).all() 
            if not model == "select menu" and not status == "select menu" and not locationname == "select menu" and not category == "select menu" and locationname == "select menu": #locationname & status & model & description &  cat
                inv_list == Inventory.objects.filter(Inventory.shelf__contains == shelf & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status & Inventory.category__contains == category).all() 
            if not model == "select menu" and not status == "select menu" and not category == "select menu" and not category == "select menu" and locationname == "select menu": #locationname & status &  model & description &  cat &  shelf
                inv_list == Inventory.objects.filter(Inventory.shelf__contains == shelf & Inventory.modelname__contains == model & Inventory.description__contains == desc & Inventory.status__contains == status & Inventory.category__contains == category,Inventory.locationname__contains == locationname).all()     
        else:
            inv_list ==None
    except IOError as e:
        nv_list = None
        print ("Lists load Failure ", e)

    if inv_list == None:
        success = False
    else:
        inv=[e.serialize() for e in inv_list]
    return jsonify({"success": success, "inv_list": inv}) 

   
def save_event(request):
    if request.method == 'POST':
        timestamp = date.today()
        event_id = request.POST.get('e_id', -1)
        inventory_id = request.POST.get('i_id', -1)
        operator = request.POST.get('_operator', -1)
        print('event_id = ',event_id)
        print('inventory_id = ',inventory_id)
        event_type = request.POST.get('_event', -1)
        event_date = request.POST.get('_date', -1)
        print('eventdate =',event_date)
        locationname = request.POST.get('_site', -1)
        mr = request.POST.get('_mr', -1)
        print('mr = ',mr)
        rma = request.POST.get('_rma', -1)
        print('rma = ',rma)
        comment = request.POST.get('_comments', -1)
        print(comment)
        save = request.POST.get('_save', -1)
        print(save)
        update = request.POST.get('_update', -1)
        print(update)
        delete = request.POST.get('_delete', -1)
        print(delete)
        print('event_id = ',event_id)
        Events.objects.filter(Events.id == event_id).delete()
        print('event_id = ',event_id)
        '''
        if not save==None:
            try:
                #save new event
                if comment=="'\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t'" or comment=='' or comment==-1:
                    comment="New event",event_id," created"
                
                Events.objects.create(event_type=event_type, event_date=event_date, operator=operator, comment=comment, locationname=locationname,
                      mr=mr, rma=rma, inventory_id=inventory_id)
                
                #update item	
                Inventory.objects.filter(Inventory.id==inventory_id).update({'description': comment,'locationname':locationname,'update_by':operator,'last_update':timestamp,})
            except IOError as e:
                print ("Events Save Failure ", e)	
        elif not update==-1: 
            try:
                print('event date',event_date)
                if comment=="'\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t'" or comment=='' or comment==-1:
                    comment="Event",event_id," updated"
                
                print('event date',event_date)
                
                #update existing event
                Events.objects.filter(Events.id == event_id).update({'event_type': event_type,'event_date':event_date,'locationname':locationname,'update_by':operator,'operator':operator,
                        'comment':comment,'locationname':locationname,'mr':mr,'rma':rma})
                #update item	
                Inventory.objects.filter(Inventory.id == inventory_id).update({'description': comment,'locationname':locationname,'update_by':operator,'last_update':timestamp})
            except IOError as e:
                print ("Events Update Failure ", e)	
        elif not delete==-1: 
            try:
                if comment=="'\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t'" or comment=='' or comment==-1:
                    comment="Event",event_id," deleted"
                #delete existing event	
                Events.objects.filter(Events.id == event_id).delete()
                #update item	
                Inventory.objects.filter(Inventory.id == inventory_id).update({'description': comment,'locationname':locationname,'update_by':operator,'last_update':timestamp})
            except IOError as e:
                print ("Events Update Failure ", e)
        '''                
        return render (request,"inventory/item.html",{"active_inv":active_inv, "image_file":image_file,"event_list":event_list,
                    "today":date.today(), "locations_list":locations_list, "shelf_list":shelves_list,'event':event})

def items(request):
    desc_list = []
    models_list = []
    locations_list = []
    shelves_list = [] 
    if request.method == 'POST':
        timestamp = date.today()
        print(timestamp)
        description = request.POST.get('_desc', -1)
        print(description)
        category = request.POST.get('_cat', -1)
        print(category)
        status = request.POST.get('_stat', -1)
        print(status)
        model = request.POST.get('_model', -1)
        print(model)
        purchase_order = request.POST.get('_po', -1)
        print(purchase_order)
        serial_number = request.POST.get('_sn', -1)
        print(serial_number)
        quantity = request.POST.get('_Qn', -1)
        print(quantity)
        shipped_date = request.POST.get('_shipped', -1)
        print(shipped_date)
        recieved_date = request.POST.get('_recieved', -1)
        print(recieved_date)
        activestr = request.POST.get('_active', -1)
        if activestr =='True' or activestr=='true':
            active=True
        elif activestr =='False' or activestr =='false':
            active=False
        else:
            active=True
        print(active)
        locationname = request.POST.get('_site', -1)
        print(locationname)
        shelf = request.POST.get('_shelf', -1)
        print(shelf)
        remarks = request.POST.get('_remarks', -1)
        print(remarks)
        try:
            # Add new Inventory item
            Inventory.objects.create(serial_number=serial_number, modelname=model,description=description, locationname=locationname, 
            shelf=shelf, category=category, status=status, quantity=quantity, remarks= remarks, purchase_order=purchase_order,
            recieved_date=recieved_date, shipped_date=shipped_date, active=active, last_update=last_update, update_by=update_by, 
            model_id=model_id, location_id=location_id, shelf_id=shelf_id)
        except IOError as e:
            print ("Inventory Save Failure ", e)
        return HttpResponseRedirect(reverse('inventory:inven'))
    try:
        desc_list = Model.objects.order_by('description').values_list('description', flat=True).distinct()
        models_list = Model.objects.order_by('model').values_list('model', flat=True).distinct()
        locations_list = Location.objects.order_by('name').values_list('name', flat=True).distinct()
        shelves_list = Location.objects.order_by('shelf').values_list('shelf', flat=True).distinct()
    except IOError as e:
         print ("Lists load Failure ", e)	
    return render (request,"inventory/items.html", {"desc_list":desc_list, "models_list":models_list,"locations_list":locations_list, "shelves_list":shelves_list, 'today':timestamp})

def item(request):
    locations_list = []
    shelves_list = []
    event_list = []
    event = 'n/a'
    #Get locationname
    try:
        event_id = request.GET.get('event_id', -1)
        print('event_id = ',event_id)
        if not event_id==-1:
            event = Events.objects.filter(id=event_id)
            event=event[0]
        
        print(event)
        inventory_id = request.GET.get('inventory_id', -1)
        print('inventory_id = ',inventory_id)
        active_inv = Inventory.objects.filter(id=inventory_id)
        active_inv = active_inv[0]
        print('active_inv = ',active_inv)
        mname = active_inv.modelname
        print('model name =',mname)
        model = Model.objects.filter(model__contains=mname)
        model = model[0]
        print('model=',model)
        print(model.image_file)
        image_file = model.image_file
        if image_file == None:
            image_file = 'inventory/images/inv1.jpg'
        print(image_file)

        locations_list = Location.objects.order_by('name').values_list('name', flat=True).distinct()
        shelves_list  = Location.objects.order_by('shelf').values_list('shelf', flat=True).distinct()
        event_list  = Events.objects.filter(inventory_id=inventory_id).all()
    except IOError as e:
        print ("Lists load Failure ", e)	
    return render (request,"inventory/item.html",{"active_inv":active_inv, "image_file":image_file,"event_list":event_list,
                    "today":date.today(), "locations_list":locations_list, "shelf_list":shelves_list,'event':event})
					
 

#https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/ 
def upload_file(request):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return HttpResponseRedirect(reverse('uploaded_file',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
