from django import forms
import json
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .forms import InventoryForm, EquipmentForm, ModelsForm, LocationForm
from datetime import date
from django.urls import reverse, reverse_lazy
from inventory.models import Inventory, Events, Location, Model
from django.views import View
import datetime
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
model_id = 0
site_id = 0

# Create your views here.
class InventoryView(View):
    '''
    #~~~~~~~~~~~Load Item database from csv. must put this somewhere else later"
    import csv
    timestamp  = date.today()  
    import csv
    timestamp  = date.today()
    CSV_PATH = 'items.csv'
    print('csv = ',CSV_PATH)

    contSuccess = 0
    # Remove all data from Table
    #Inventory.objects.all().delete()
    f = open(CSV_PATH)
    reader = csv.reader(f)
    print('reader = ',reader)

    for category, shelf, modelname, serial_number, description, locationname,  status, remarks,last_update,update_by in reader:
        Inventory.objects.create(category=category, shelf=shelf, modelname=modelname, serial_number=serial_number, description=description, locationname=locationname, 
         status=status, remarks=remarks, last_update=datetime.datetime.strptime(last_update, '%m/%d/%Y'), update_by=update_by)
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ') 
    '''
    '''
    #~~~~~~~~~~~Load Events database from csv. must put this somewhere else later"
    import csv
    timestamp  = date.today()      
    CSV_PATH = 'events.csv'
    print('csv = ',CSV_PATH)

    contSuccess = 0

    # Remove all data from Table
    Events.objects.all().delete()

    f = open(CSV_PATH)
    reader = csv.reader(f)
    print('reader = ',reader)
    for event_type, event_date, operator, comment, inventory_id, locationname, rma, rtv, mr, in reader:
        print('event date=',event_date)
        Events.objects.create(event_type=event_type, event_date=datetime.datetime.strptime(event_date, '%m/%d/%Y'), operator=operator,comment=comment, locationname=locationname, mr=mr, rtv =rtv, rma =rma, inventory_id=inventory_id)
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')
    
    #~~~~~~~~~~~Load Events database from csv. must put this somewhere else later"   
    '''
    '''
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
    '''
    #load_iventory_csv(True)
    #load_events_csv(True)
    form_class = InventoryForm
    template_name = "index.html"
    success_url = reverse_lazy('inventory:inv')
    def get(self, *args, **kwargs):
        form = self.form_class()
        try:
            
            description=-1
            category=-1
            model=-1
            status=-1
            locationname=-1
            shelf=-1
            search=-1
            
            print("in GET")
            desc_list = Inventory.objects.order_by('description').values_list('description', flat=True).distinct()
            models_list = Inventory.objects.order_by('modelname').values_list('modelname', flat=True).distinct()
            categorys_list = Inventory.objects.order_by('category').values_list('category', flat=True).distinct()
            status_list = Inventory.objects.order_by('status').values_list('status', flat=True).distinct()
            locations_list = Inventory.objects.order_by('locationname').values_list('locationname', flat=True).distinct()
            shelves_list = Inventory.objects.order_by('shelf').values_list('shelf', flat=True).distinct()
            inv = Inventory.objects.all()
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"inventory/index.html",{"form": form, "inventory": inv, "desc_list":desc_list, "status_list":status_list,
           "models_list":models_list, "locations_list":locations_list, "shelves_list":shelves_list,"categorys_list":categorys_list, "index_type":"INVENTORY",
           'description':description,'model':model,'status':status, 'category':category, 'locationname':locationname, 'shelf':shelf,'search':search})
    
    def post(self, request, *args, **kwargs):
        try: 
            #print("in POST")
            json_data = []
            inv_list = []
            inv = []
            form = self.form_class()
            #print('request =',request)
            model = request.POST.get('_model', -1)
            #print('model = ',model)
            description = request.POST.get('_desc', -1)
            #print('description = ',description)
            status = request.POST.get('_status', -1)
            #print('status =',status)
            category = request.POST.get('_category', -1)
            #print('category =',category)
            locationname = request.POST.get('_site', -1)
            #print('locationname =',locationname)
            shelf = request.POST.get('_shelf', -1)
            #print('shelf =',shelf)
            select = request.POST.get('sel', -1)
            #print('select =',select)
            search = request.POST.get('search', -1)
            #print('search =',search)
            print_report = request.POST.get('monthly_report', -1)
            #print('print_report =',print_report)
            success = True
            
            

            desc_list = Inventory.objects.order_by('description').values_list('description', flat=True).distinct()
            models_list = Inventory.objects.order_by('modelname').values_list('modelname', flat=True).distinct()
            categorys_list = Inventory.objects.order_by('category').values_list('category', flat=True).distinct()
            status_list = Inventory.objects.order_by('status').values_list('status', flat=True).distinct()
            locations_list = Inventory.objects.order_by('locationname').values_list('locationname', flat=True).distinct()
            shelves_list = Inventory.objects.order_by('shelf').values_list('shelf', flat=True).distinct()
            if not search ==-1:
                inv_list = Inventory.objects.filter(description__icontains=search) | Inventory.objects.filter(modelname__icontains=search) | Inventory.objects.filter(status__icontains=search) | Inventory.objects.filter(category__icontains=search) | Inventory.objects.filter(locationname__icontains=search) | Inventory.objects.filter(serial_number__contains=search) | Inventory.objects.filter(shelf__icontains=search).all()
            elif description == "select menu" and model == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":
                inv_list = Inventory.objects.all()
            elif not category =="select menu": 
                if description == "select menu" and model == "select menu" and status == "select menu" and locationname == "select menu" and  shelf == "select":#category only 
                    inv_list = Inventory.objects.filter(category=category).all()
                if not model == "select menu" and status == "select menu" and locationname == "select menu" and  shelf == "select":  #category &  model
                    inv_list = Inventory.objects.filter(category=category, modelname__contains=model).all()  
                if not model == "select menu" and not status == "select menu" and locationname == "select menu" and  shelf == "select":  #category & status & model & description
                    inv_list = Inventory.objects.filter(category=category, modelname__contains=model, status__contains=status).all()  
                if not model == "select menu" and not status == "select menu" and not locationname == "select menu" and  shelf == "select": #category & status & model & description
                    inv_list = Inventory.objects.filter(category=category, modelname__contains=model, status__contains=status, locationname__contains=locationname).all() 
                if not model == "select menu" and not status == "select menu" and not locationname == "select menu" and not shelf == "select": #category & status & model & description &  cat
                    iinv_list = Inventory.objects.filter(category=category, modelname__contains=model, status__contains=status, locationname__contains=locationname, shelf__contains=shelf).all() 
                if not model == "select menu" and not status == "select menu" and not locationname == "select menu" and not shelf == "select" and not description  == "select menu" : #category & status & model & description &  cat
                    iinv_list = Inventory.objects.filter(category=category, modelname__contains=model, status__contains=status, locationname__contains=locationname, shelf__contains=shelf, description__icontains=description).all() 
            elif not model =="select menu": 
                if description == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and shelf == "select":#model only 
                    inv_list = Inventory.objects.filter(modelname__contains=model).all()
                if not category == "select menu" and status == "select menu" and description  == "select menu" and locationname == "select menu" and shelf == "select":  #model & description 
                    inv_list = Inventory.objects.filter(modelname__icontains=model, category_icontains=category ).all()  
                if not category == "select menu" and not status == "select menu" and description  == "select menu" and locationname == "select menu" and shelf == "select":  #model & description &  status 
                    inv_list = Inventory.objects.filter(modelname__icontains=model,category=category, status__contains=status).all()  
                if not category == "select menu" and not status == "select menu" and not description  == "select menu" and locationname == "select menu" and shelf == "select":    #model &  status 
                    inv_list = Inventory.objects.filter(modelname__icontains=model,category=category, status__contains=status, description__icontains=description).all()  
                if not category == "select menu" and not status == "select menu" and not description  == "select menu" and not locationname == "select menu" and shelf == "select": #model & description &   status &  cat
                    inv_list = Inventory.objects.filter(modelname__icontains=model,category=category, status__contains=status,description__icontains=description,locationname__icontains=locationname).all()  
                if not category == "select menu" and not status == "select menu" and not description  == "select menu" and not locationname == "select menu" and shelf == "select": #model & description &  status &  cat' loc
                    inv_list = Inventory.objects.filter(dmodelname__icontains=model,category=category, status__contains=status, description__icontains=description,locationname__icontains=locationname).all() 
                if not category == "select menu" and not status == "select menu" and not description  == "select menu" and not locationname == "select menu" and not shelf == "select": #model & description &  status &  cat' loc &  shelf
                    inv_list = Inventory.objects.filter(modelname__icontains=model,category_icontains=category, status__contains=status, description__icontains=description, locationname__icontains=locationname, shelf__contains=shelf).all()     
            elif not status =="select menu": 
                if description == "select menu" and model == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":#status only 
                    inv_list = Inventory.objects.filter(status__contains=status).all()
                if not model == "select menu" and not status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #status &  model
                    inv_list = Inventory.objects.filter(status__contains=status, modelname__contains=model).all()  
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and locationname == "select menu" and  shelf == "select":  #status & description
                    inv_list = Inventory.objects.filter(status__contains=status, modelname__contains=model,category=category).all()       
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and  shelf == "select":  #status & model & description
                    inv_list = Inventory.objects.filter(status__contains=status, modelname__contains=model,category=category, locationname__icontains=locationname).all()   
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and  shelf == "select": #status & model & description &  cat
                    inv_list = Inventory.objects.filter(status__contains=status, modelname__contains=model,category=category, locationname__icontains=locationname).all()   
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and not shelf == "select": #status & model & description &  cat' loc
                    inv_list = Inventory.objects.filter(status__contains=status, modelname__contains=model,category=category, locationname__icontains=locationname, shelf__contains=shelf).all()   
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and not shelf == "select" and not description  == "select menu" : #status &  model & description &  cat' loc &  shelf
                    inv_list = Inventory.objects.filter(status__contains=status, modelname__contains=model,category=category, locationname__icontains=locationname, shelf__contains=shelf, description__icontains=description).all()       
            elif not locationname =="select menu": 
                if description == "select menu" and model == "select menu" and status == "select menu" and category == "select menu" and  shelf == "select":#locationname only 
                    inv_list = Inventory.objects.filter(locationname__contains= locationname).all()
                if not shelf == "select menu" and status == "select menu" and category == "select menu" and category == "select menu" and  model == "select":  #locationname &  model
                    inv_list = Inventory.objects.filter(locationname__contains=locationname, shelf__contains=shelf).all()  
                if not shelf == "select menu" and not status == "select menu" and category == "select menu" and category == "select menu" and  shelf == "select":  #locationname & status & model & description
                    inv_list = Inventory.objects.filter(locationname__contains=locationname, shelf__contains=shelf,status__contains=status).all()  
                if not shelf == "select menu" and not status == "select menu" and not category == "select menu" and category == "select menu" and  shelf == "select": #locationname & status & model & description &  cat
                    inv_list = Inventory.objects.filter(locationname__contains=locationname,shelf__contains=shelf, status__contains=status, category__contains=category).all() 
                if not shelf == "select menu" and not status == "select menu" and not locationname == "select menu" and not category == "select menu" and  shelf == "select": #locationname & status & model & description &  cat
                    inv_list = Inventory.objects.filter(locationname__contains=locationname, shelf__contains=shelf, description__contains=description, status__contains=status, category=category).all() 
                if not shelf == "select menu" and not status == "select menu" and not category == "select menu" and not category == "select menu" and not shelf == "select" and not modelname == "select": #locationname & status &  model & description &  cat &  shelf
                    inv_list = Inventory.objects.filter(locationname__contains=locationname, shelf__contains=shelf, description__contains=description, status__contains=status, category=category, modelname__contains=model).all()     
            elif not shelf =="select": 
                if description == "select menu" and model == "select menu" and status == "select menu" and category == "select menu" and  locationname == "select menu":#locationname only 
                    inv_list = Inventory.objects.filter(shelf__contains=shelf).all()
                if not locationname == "select menu" and status == "select menu" and category == "select menu" and category == "select menu" and model == "select menu":  #locationname &  model
                    inv_list = Inventory.objects.filter(shelf__contains=shelf, locationname__contains=locationname).all()  
                if not locationname == "select menu" and not status == "select menu" and  category == "select menu" and category == "select menu" and model == "select menu":  #locationname & status & model & description
                    inv_list = Inventory.objects.filter(shelf__contains=shelf, locationname__contains=locationname, status__contains=status).all()  
                if not locationname == "select menu" and not status == "select menu" and not category == "select menu" and category == "select menu" and model == "select menu": #locationname & status & model & description &  cat
                    inv_list = Inventory.objects.filter(shelf__contains=shelf, locationname__contains=locationname, category__contains=category, status__contains=status).all() 
                if not locationname == "select menu" and not status == "select menu" and not category == "select menu" and not category == "select menu" and locationname == "select menu": #locationname & status & model & description &  cat
                    inv_list = Inventory.objects.filter(shelf__contains=shelf, locationname__contains=v, status__contains=status, category__contains=category).all() 
                if not locationname == "select menu" and not status == "select menu" and not category == "select menu" and not category == "select menu" and not model == "select menu": #locationname & status &  model & description &  cat &  shelf
                    inv_list = Inventory.objects.filter(shelf__contains=shelf, locationname__contains=locationname, description__contains=desc, status__contains=status, category__contains=category, modelname__contains=model).all()     
            elif not description =="select menu": 
                if model == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select": #All
                    inv_list = Inventory.objects.filter(description__contains=description).all()
                if not model == "select menu" and status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #description, model 
                    inv_list = Inventory.objects.filter(description__contains=description, modelname__contains=model).all()  
                if model == "select menu" and not status == "select menu" and category == "select menu" and locationname == "select menu" and  shelf == "select":  #description&status 
                    inv_list = Inventory.objects.filter(description__contains=description, modelname__contains=model, status__contains=status).all()  
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and locationname == "select menu" and  shelf == "select": #description &  model, status, cat
                    inv_list = Inventory.objects.filter(description__contains=description, modelname__contains=model, status__contains=status,ategory__contains=category).all() 
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and  shelf == "select": #description, model, status, cat' loc
                    inv_list = Inventory.objects.filter(description__contains=description, modelname__contains=model, status__contains=status, category=category, locationname__contains=locationname).all() 
                if not model == "select menu" and not status == "select menu" and not category == "select menu" and not locationname == "select menu" and not shelf == "select": #description &  model &  status &  cat' loc &  shelf
                    inv_list = Inventory.objects.filter(description__contains=description, modelname__contains=model, status__contains=status, category=category, locationname__contains=locationname, shelf__contains=shelf).all()     
            else:
                inv_list ==None
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        #print('inv_list',inv_list)
        return render (self.request,"inventory/index.html",{"form": form, "inventory": inv_list, "desc_list":desc_list, "status_list":status_list,
           "models_list":models_list, "locations_list":locations_list, "shelves_list":shelves_list,"categorys_list":categorys_list, "index_type":"INVENTORY",
           'description':description,'model':model,'status':status, 'category':category, 'locationname':locationname, 'shelf':shelf,'search':search})
                
        
# Create your views here.
class SearchView(View):
    template_name = "search.html"
    print('in search view')
    def get(self, *args, **kwargs):
        form = self.form_class()
        #print('we are here')
        try:
            desc_list = Model.objects.order_by('description').values_list('description', flat=True).distinct()
            models_list = Inventory.objects.order_by('modelname').values_list('modelname', flat=True).distinct()
            categorys_list = Inventory.objects.order_by('category').values_list('category', flat=True).distinct()
            status_list = Inventory.objects.order_by('status').values_list('status', flat=True).distinct()
            locations_list = Inventory.objects.order_by('locationname').values_list('locationname', flat=True).distinct()
            shelves_list = Inventory.objects.order_by('shelf').values_list('shelf', flat=True).distinct()
            inv = Inventory.objects.all()
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"inventory/index.html",{"form": form, "inventory": inv, "desc_list":desc_list, "status_list":status_list,
           "models_list":models_list, "locations_list":locations_list, "shelves_list":shelves_list,"categorys_list":categorys_list, "index_type":"INVENTORY"})
    
    def post(self, *args, **kwargs):
        form = self.form_class()
        #print(form)
        #print('we are here')
        
   
def load_iventory_csv(delete):
    #~~~~~~~~~~~Load Item database from csv. must put this somewhere else later"
    import csv
    timestamp  = date.today()
    CSV_PATH = 'items.csv'
    #print('csv = ',CSV_PATH)

    contSuccess = 0
    # Remove all data from Table
    if delete:
        Inventory.objects.all().delete()
    f = open(CSV_PATH)
    reader = csv.reader(f)
    print('reader = ',reader)
    for category, shelf, modelname, serial_number, description, locationname,  status, remarks, site_quantity, field_quantity, repair_quantity,last_update, update_by in reader:
        Inventory.objects.create(shelf=shelf,serial_number=serial_number, modelname=modelname, description=description, locationname=locationname,
        category=category,status=status, site_quantity=site_quantity, field_quantity=field_quantity,repair_quantity=repair_quantity, remarks=remarks, last_update=datetime.datetime.strptime(last_update, '%m/%d/%Y'), update_by=update_by)
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')
    
def load_events_csv(delete):
    #~~~~~~~~~~~Load Item database from csv. must put this somewhere else later"
    import csv
    timestamp  = date.today()      
    #~~~~~~~~~~~Load Events database from csv. must put this somewhere else later"
    CSV_PATH = 'events.csv'
    #print('csv = ',CSV_PATH)

    contSuccess = 0
    
    # Remove all data from Table
    if delete:
        Events.objects.all().delete()

    f = open(CSV_PATH)
    reader = csv.reader(f)
    print('reader = ',reader)
    for event_type, event_date, operator, comment,locationname, inventory_id, rma, rtv, mr, in reader:
        Events.objects.create(event_type=event_type, event_date=datetime.datetime.strptime(event_date, '%m/%d/%Y'), operator=operator,comment=comment, locationname=locationname, mr=mr, rtv =rtv, rma =rma, inventory_id=inventory_id)
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')
    
    #~~~~~~~~~~~Load Events database from csv. must put this somewhere else later"   
    

def update_inv(request):
    if request.method == 'POST':
        update_inv = request.POST.get('update_inv', -1)
        inventory_id = request.POST.get('i_id', -1)
        del_inv = request.POST.get('del_inv', -1)
        operator = request.POST.get('_operator', -1)
        event = 'n/a'
        #print('inventory_id =',inventory_id)
        active_inv = Inventory.objects.filter(id=inventory_id)
        #print(active_inv)
        active_inv = active_inv[0]
        #print(active_inv.description)
        mname = active_inv.modelname
        model = Model.objects.filter(model__contains=mname)
        model = model[0]
        image_file = model.image_file
        if image_file == None:
            image_file = 'inventory/images/inv1.jpg'
        #print(image_file)
        locations_list = Location.objects.order_by('name').values_list('name', flat=True).distinct()
        shelves_list = Location.objects.order_by('shelf').values_list('shelf', flat=True).distinct()
        categorys_list = Inventory.objects.order_by('category').values_list('category', flat=True).distinct()
        event_list = Events.objects.filter(inventory_id=inventory_id).all()
        models_list = Model.objects.order_by('model').values_list('model', flat=True).distinct()

        #print('del_inv =',del_inv)
        #print('update_inv =',update_inv)

        if not del_inv==-1:
            try:
               #update item	
                Inventory.objects.filter(id=inventory_id).delete()
                print('delete complete')
            except IOError as e:
                print ("Events Save Failure ", e)
            return HttpResponseRedirect(reverse('inventory:inven'))
        elif not update_inv==-1:
            return render (request,"inventory/items.html",{"today":date.today(), "locations_list":locations_list, "models_list":models_list, 'active_inv':active_inv})
    return render (request,"inventory/item.html",{"active_inv":active_inv, "image_file":image_file,"event_list":event_list,
                    "today":date.today(), "locations_list":locations_list, "shelf_list":shelves_list,'event':event,'active_operator':request.user})
    
     
                
                
def save_event(request):
    if request.method == 'POST':
        timestamp = date.today()
        update_inv = request.POST.get('update_inv', -1)
        del_inv = request.POST.get('del_inv', -1)
        event_id = request.POST.get('e_id', -1)
        inventory_id = request.POST.get('i_id', -1)
        operator = request.POST.get('_operator', -1)
        event_type = request.POST.get('_event', -1)
        event_date = request.POST.get('_date', -1)
        locationname = request.POST.get('_site', -1)
        mr = request.POST.get('_mr', -1)
        rtv = request.POST.get('_rtv', -1)
        rma = request.POST.get('_rma', -1)
        comment = request.POST.get('_comments', -1)
        save = request.POST.get('_save', -1)
        update = request.POST.get('_update', -1)
        delete = request.POST.get('_delete', -1)
        locations_list = Location.objects.order_by('name').values_list('name', flat=True).distinct()
        shelves_list = Location.objects.order_by('shelf').values_list('shelf', flat=True).distinct()
        event_list = Events.objects.filter(inventory_id=inventory_id).all()
        models_list = Model.objects.order_by('model').values_list('model', flat=True).distinct()
        event = 'n/a'
        active_inv = Inventory.objects.filter(id=inventory_id)
        active_inv = active_inv[0]
        mname = active_inv.modelname
        model = Model.objects.filter(model__contains=mname)
        model = model[0]
        image_file = model.image_file

                 
        if not del_inv==-1:
            try:
               #update item	
                Inventory.objects.filter(id=inventory_id).delete()
                print('delete complete')
            except IOError as e:
                print ("Events Save Failure ", e)
            return HttpResponseRedirect(reverse('inventory:inven'))
        elif not update_inv==-1:
            return render (request,"inventory/items.html",{"today":date.today(), "locations_list":locations_list, "models_list":models_list, "shelf_list":shelves_list,'active_inv':active_inv})
        elif not save==-1:
            try:
                #save new event
                if comment=="'\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t'" or comment=='' or comment==-1:
                    comment="New event",event_id," created"
                
                Events.objects.create(event_type=event_type, event_date=event_date, operator=operator, comment=comment, locationname=locationname,mr=mr, rma=rma,rtv=rtv, inventory_id=inventory_id)
                
                #update item	
                Inventory.objects.filter(id=inventory_id).update(remarks=comment,locationname=locationname,update_by=operator,last_update=timestamp)
            except IOError as e:
                print ("Events Save Failure ", e)	
        elif not update==-1: 
            try:
                print('event date',event_date)
                if comment=="'\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t'" or comment=='' or comment==-1:
                    comment="Event",event_id," updated"
                
                print('event date',event_date)
                
                #update existing event
                Events.objects.filter(id=event_id).update(event_type=event_type,event_date=event_date,locationname=locationname,operator=operator,
                        comment=comment,mr=mr,rma=rma)
                #update item	
                Inventory.objects.filter(id=inventory_id).update(remarks=comment,locationname=locationname,update_by=operator,last_update=timestamp)
            except IOError as e:
                print ("Events Update Failure ", e)	
        elif not delete==-1: 
            try:
                if comment=="'\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t'" or comment=='' or comment==-1:
                    comment="Event",event_id," deleted"
                #delete existing event	
                Events.objects.filter(id=event_id).delete()
				
                #update item	
                Inventory.objects.filter(id=inventory_id).update(remarks=comment,locationname=locationname,update_by=operator,last_update=timestamp)
            except IOError as e:
                print ("Events Update Failure ", e)
                
        
        if image_file == None:
            image_file = 'inventory/images/inv1.jpg'
        #print(image_file)

        #print('operator=',operator)
        return render (request,"inventory/item.html",{"active_inv":active_inv, "image_file":image_file,"event_list":event_list,
                    "today":date.today(), "locations_list":locations_list, "shelf_list":shelves_list,'event':event,'active_operator':operator})

def items(request):
    desc_list = []
    models_list = []
    locations_list = []
    shelves_list = [] 
    timestamp = date.today()
    operator = request.user
    #print(timestamp)
    if request.method == 'POST':
        inventory_id = request.POST.get('inventory_id', -1)
        #print(inventory_id)
        description = request.POST.get('_desc', -1)
        #print('description =',description)
        category = request.POST.get('_cat', -1)
        #print('category=',category)
        status = request.POST.get('_stat', -1)
        #print(status)
        model = request.POST.get('_model', -1)
        #print('model=',model)
        purchase_order = request.POST.get('_po', -1)
        #print(purchase_order)
        serial_number = request.POST.get('_sn', -1)
        #print('serial_number=',serial_number)
        activestr = request.POST.get('_active', -1)
        if activestr =='True' or activestr=='true':
            active=True
        elif activestr =='False' or activestr =='false':
            active=False
        else:
            active=True
        #print(active)
        location = request.POST.get('_site', -1)
        #print('location =',location)
        shelf = request.POST.get('_shelf', -1)
        #print('shelf=',shelf)
        remarks = request.POST.get('_remarks', -1)
        #print(remarks)
        model_id = Model.objects.filter(model__contains=model)
        #print('model_id=',model_id)
        model_id=model_id[0].id
        #print('model_id=',model_id)
        
        location_id = Location.objects.filter(name=location)
        location_id=location_id[0].id
        #print('location_id=',location_id)
        shelf_id = Location.objects.filter(name=shelf)
        #shelf_id=shelf_id[0].id
        #print('shelf_id=',shelf_id)
        save = request.POST.get('_save', -1)
        #print('save',save)
        update = request.POST.get('_update', -1)
        #print('update',update)
        operator = request.POST.get('_operator', -1)
        if operator==-1:
            operator = str(request.user)
        #print('operator',operator)
        try:
            if not save ==-1:
                # Add new Inventory item
                Inventory.objects.create(serial_number=serial_number, modelname=model,description=description, locationname=location, shelf=shelf, category=category,
                         model_id=model_id, status=status,remarks=remarks, purchase_order=purchase_order, active=activestr, last_update=timestamp, update_by=operator)

                Events.objects.create(event_type="ADD NEW", event_date=timestamp, operator=operator, comment="New Inventory Item", locationname=location, inventory_id=inventory_id)		
						
            elif not update==-1:
                # Add new Inventory item
                #print('inventory_id=',inventory_id)
                Inventory.objects.filter(id=inventory_id).update(serial_number=serial_number, modelname=model,description=description, locationname=location, shelf=shelf, category=category,
                          model_id=model_id, status=status,remarks=remarks, purchase_order=purchase_order, active=activestr, last_update=timestamp, update_by=operator)
                        
                Events.objects.create(event_type="UPDATE ITEM", event_date=timestamp, operator=operator, comment=remarks, locationname=location, inventory_id=inventory_id)	
                
            HttpResponseRedirect(reverse('inventory:inven'))
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
    return render (request,"inventory/items.html",{"today":date.today(), "locations_list":locations_list, "models_list":models_list, "shelf_list":shelves_list,'active_operator':operator})

def item(request):
    locations_list = []
    shelves_list = []
    event_list = []
    event = 'n/a'
    uploaded_file_url = ""
    #Get locationname
    try:
        event_id = request.GET.get('event_id', -1)
        #print('event_id = ',event_id)
        if not event_id==-1:
            event = Events.objects.filter(id=event_id)
            event=event[0]
        
        #print(event)
        inventory_id = request.GET.get('inventory_id', -1)
        #print('inventory_id = ',inventory_id)
        active_inv = Inventory.objects.filter(id=inventory_id)
        active_inv = active_inv[0]
        #print('active_inv = ',active_inv)
        mname = active_inv.modelname
        #print('model name =',mname)
        model = Model.objects.filter(model__icontains=mname)
        #print('model=',model)
        if Model.objects.filter(model__icontains=mname).exists():
            model = model[0]
            uploaded_file_url=model.photo
        #print('model=',model)
        if uploaded_file_url==None or uploaded_file_url =="":
            uploaded_file_url = '/tcli/media/inv1.jpg'
        #print('uploaded_file_url =',uploaded_file_url)

        locations_list = Location.objects.order_by('name').values_list('name', flat=True).distinct()
        shelves_list = Location.objects.order_by('shelf').values_list('shelf', flat=True).distinct()
        event_list = Events.objects.filter(inventory_id=inventory_id).all()
        #print('event_list = ',event_list)
        operator=request.user
        #print('operator = ',operator)        
    except IOError as e:
        print ("Lists load Failure ", e)	
    return render (request,"inventory/item.html",{"active_inv":active_inv, "uploaded_file_url":uploaded_file_url,"event_list":event_list,
                    "today":date.today(), "locations_list":locations_list, "shelf_list":shelves_list,'event':event,'active_operator':operator})
					
 
def report(request):
    locations_list = []
    shelves_list = []
    event_list = []
    event = 'n/a'
    uploaded_file_url = ""
    operator = str(request.user)
    #Get locationname
    try:
        inventory_id = request.GET.get('inventory_id', -1)
        #print('inventory_id = ',inventory_id)
        active_inv = Inventory.objects.filter(id=inventory_id)
        active_inv = active_inv[0]
        #print('active_inv = ',active_inv)
        mname = active_inv.modelname
        #print('model name =',mname)
        model = Model.objects.filter(model__icontains=mname)
        if Model.objects.filter(model__icontains=mname).exists():
            model = model[0]
            uploaded_file_url=model.photo
        #print('model=',model)
        if uploaded_file_url==None or uploaded_file_url =="":
            uploaded_file_url = '/tcli/media/inv1.jpg'
        #print('uploaded_file_url =',uploaded_file_url)
        #print('model=',model)
        #print(model.image_file)
        image_file = model.image_file
        if image_file == None:
            image_file = 'inventory/images/model.jpg'
        #print(image_file)
        event_list = Events.objects.filter(inventory_id=inventory_id).all()
        #print('event_list = ',event_list)
        operator=request.user
        #print('operator = ',operator)        
    except IOError as e:
        print ("Lists load Failure ", e)	
    return render (request,"inventory/report.html",{"active_inv":active_inv, "uploaded_file_url":uploaded_file_url,"event_list":event_list,
                    "today":date.today(),'event':event,'active_operator':operator})
                    

def inv_report(request):
    inv_list = []
    models_list = []
    model_list = []
    curr_quan = []
    field_quan = []
    repair_quan = []
    missing_quan = []
    #Get locationname
    json_data = []
    inv_list = []
    inv = []
    
    operator = str(request.user)
    model = request.GET.get('model', -1)
    #print('model = ',model)
    category = request.GET.get('category', -1)
    #print('category = ',category)
    success = True
    if category =='select menu' and model =='select menu' :
        inv_list = Inventory.objects.all()
        model_list = Inventory.objects.order_by('modelname').values_list('modelname', flat=True).distinct()
        category ='All categorys'
    elif not category =='select menu' and model =='select menu' :
        inv_list = Inventory.objects.filter(category=category).all()
        model_list = Inventory.objects.filter(category=category).order_by('modelname').values_list('modelname', flat=True).distinct()
    elif not category =='select menu' and not model =='select menu' :
        inv_list = Inventory.objects.filter(category=category,modelname=model).all()
        model_list = Inventory.objects.filter(category=category,modelname=model).order_by('modelname').values_list('modelname', flat=True).distinct()
    
    model_lists = []
    lists =[]
    for model in model_list:
        total_quan=Inventory.objects.filter(modelname=model).count()
        house_quan=Inventory.objects.filter(modelname=model).filter(status__icontains='In-House').count()
        field_quan=Inventory.objects.filter(modelname=model).filter(status__icontains='On-Site').count()
        repair_quan=Inventory.objects.filter(modelname=model).filter(status__icontains='In-Repair').count()
        missing_quan=Inventory.objects.filter(modelname=model).filter(status__icontains='In-Repair').count()
        list = {'modelname':model,'total_quan': total_quan, 'house_quan':house_quan,'field_quan':field_quan,'repair_quan':repair_quan,'missing_quan':missing_quan}
        lists = json.dumps(list)
        model_lists.append(lists)
        model_lists = ListAsQuerySet(model_lists, model='Post')
    
    print('model_list = ', model_lists) 
    print('inv_list = ',inv_list)
    desc_list = Model.objects.order_by('description').values_list('description', flat=True).distinct()
    locations_list = Location.objects.order_by('name').values_list('name', flat=True).distinct()
    shelves_list = Location.objects.order_by('shelf').values_list('shelf', flat=True).distinct()
    
        
   
    return render (request,"inventory/inv_report.html",{"inv_list":inv_list, "category":category, "models_list":model_list, "curr_quan":curr_quan, "field_quan":field_quan, 
                    "repair_quan":repair_quan, "missing_quan":missing_quan, "today":date.today(),'active_operator':operator})
					


def to_json(lst,columns):
    keys = []
    for d in lst:
       keys.append((columns,d))
    data = json.dumps(keys)
    return data
    
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
    
class ListAsQuerySet(list):

    def __init__(self, *args, model, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self  # filter ignoring, but you can impl custom filter

    def order_by(self, *args, **kwargs):
        return self
        
class LocationView(View):
    form_class = LocationForm
    template_name = "index2.html"
    success_url = reverse_lazy('inventory:location')
    
    def get(self, *args, **kwargs):
        form = self.form_class()
        try:
            locations = Location.objects.all()
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"inventory/index2.html",{"form": form, "inventory":locations, "index_type":"SIGNIN", "UserN":self.request.user, "index_type":"SITE LOCATIONS"})
        
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            timestamp = date.today()
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
            inventory_id = None
            active=True
            try:        
               Location.objects.create(name=name, address=address, city=city, state=state, zip_code=zip_code, phone=phone, email=email, website=website,
                        active=active, inventory_id=inventory_id, created_on=timestamp, last_entry=timestamp, lat=lat, lng=lng)
            except IOError as e:
                print ("location Save Failure ", e)	
        return render (self.request,"inventory/index.html",{"index_type":"SIGNIN", "UserN":self.request.user, "index_type":"SITE LOCATIONS"})

def save_csv(delete):               
    #~~~~~~~~~~~Load location database from csv. must put this somewhere else later"
    import csv
    timestamp  = date.today()
    CSV_PATH = 'inventory.csv'
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
    return render(request,"inventory/site.html",{"sites": sites, "site": site, "lat":lat, "lng":lng, "index_type":"Model"})
	
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
    
class EquipmentView(View):
    form_class = EquipmentForm
    template_name = "index.html"
    success_url = reverse_lazy('inventory:equipment')
    contSuccess = 0
    
    def get(self, *args, **kwargs):
        form = self.form_class()
        try:
            models = Model.objects.all()
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"inventory/index.html",{"form": form, "models": models, "index_type":"EQUIPMENT"})
	   	
    def post(self, request, *args, **kwargs):
        form = self.form_class()
        search = request.POST.get('search', -1)
        print('search =',search)
        success = True
        if not search ==-1:
            models = Model.objects.filter(description__icontains=search) | Model.objects.filter(category__icontains=search) | Model.objects.filter(band__icontains=search) | Model.objects.filter(vendor__icontains=search) | Model.objects.filter(model__icontains=search) | Model.objects.filter(status__contains=search).all()
            if not models:
                models = Model.objects.all()
        else:
            models = Model.objects.all()
        return render (self.request,"inventory/index.html",{"form": form, "models": models, "index_type":"EQUIPMENT"})

class ModelView(View):
    form_class = ModelsForm
    template_name = "model.html"
    success_url = reverse_lazy('inventoryt:model')
   
    slug = None
    def get_object(self, queryset=None):
        self.slug = self.kwargs.get('slug', None)
        print('slug = ',self.slug)
        mod= []
        models= []
        
    def get(self, *args, **kwargs):
        form = self.form_class()
        try:
            models = Model.objects.all()
            mod = Model.objects.filter(id=self.slug).all()
            print(models)
            print(mod)
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"inventory/index.html",{"form": form, "models": models, "model": mod,  "index_type":"EQUIPMENT"})
        
    def post(self, *args, **kwargs):
        timestamp = date.today()
        band = request.POST.POST('_band',-1)
        category = request.POST.get('_category',-1)
        description = request.POST.get('_desc',-1)
        model = request.POSTget('_model',-1)
        vendor= request.POST.get('_vendor',-1)
        active = True
        image_file = request.POST.get('fileupload',-1)
        comments = request.POST.get('_comments',-1)
        model_id = request.POST.get('m_id',-1)
        save = request.POST.get('_save',-1)
        update = request.POST.get('_update',-1)
        delete = request.POST.get('_delete',-1)
        
        if not save==None:	
            try:		
                Model.objects.create(description=description, category=category, band=band, vendor=vendor, model=model, 
                        comments=comments, image_file=image_file, status=active, last_update=timestamp)
            except IOError as e:
                success = False
                print ("Models Save Failure ", e)
        elif not update==None: 
            try:
                #update existing event
                Model.objects.filter(id=model_id).update({'description': description,'category':category,'band=':band,
                    'model':model,'comment':comment,'locationname':locationname,'image_file':image_file,'vendor':vendor,'active':active,'last_update':last_update})
            except IOError as e:
                print ("Models Update Failure ", e)	
        elif not delete==None: 
            try:
                Model.objects.filter(id=model_id).delete()
            except IOError as e:
                print ("Models Delete Failure ", e)		
        return render (self.request,"inventory/index.html",{"form": form, "models": models, "index_type":"EQUIPMENT"})

def loadmodel(request, model_id):
        models = []
        mod = []
        print('we are here')
        # cast the request inventory_id from string to integer type.
        model_id = int(model_id)
        success = True 
        try:	
            models=Model.objects.all()
            mod=Model.objects.filter(id=model_id)
            mod=mod[0]
            print('mod.image_file',mod.image_file)
            uploaded_file_url=mod.photo
            if uploaded_file_url==None or uploaded_file_url =="":
                uploaded_file_url = '/simba/media/inv1.jpg'
            print('uploaded_file_url =',uploaded_file_url)
        except IOError as e:
            print ("load model Failure ", e)
            print('error = ',e) 
        return render(request,"inventory/model.html",{"models": models, "mod": mod, "uploaded_file_url":uploaded_file_url,  "index_type":"Model"})
        
def newmodel(request):
        models = []
        success = True 
        try:	
            mod = -1
            models=Model.objects.all()
            image_file = 'inv1.jpg'
            uploaded_file_url = '/simba/media/inv1.jpg'
                       
        except IOError as e:
            print ("load model Failure ", e)
            print('error = ',e) 
        return render(request,"inventory/model.html",{"models": models, "mod": mod, "uploaded_file_url":uploaded_file_url, "image_file":image_file,  "index_type":"Model"})

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
        #file_path = media_folder+image_file
        #image_file = media_folder + imagefile
        
        #os.rename(file_path,image_file)
       
        if form.is_valid(): 
            form.save() 
    else: 
        form = ModelsForm()
        imagefile = request.POST.get('photo',-1)
        #print('imagefile =',imagefile)
    return render(request, 'inventory/images.html', {'form' : form}) 
   
def loadEquipment():
    import csv
    contSuccess = 0
    CSV_PATH = 'models.csv'
    print('csv = ',CSV_PATH)
    
    # Remove all data from Table
    Model.objects.all().delete()

    f = open(CSV_PATH)
    reader = csv.reader(f)
    print('reader = ',reader)
    for description, category, band, vendor, model, comments, image_file, status, last_update in reader:
        print(description)
        print (band)
        print(vendor)
        print(model)
        print(comments)
        print(image_file)
        print(status)
        print(last_update)
        Model.objects.create(description=description, category=category, band=band, vendor=vendor, model=model, comments=comments, image_file=image_file, status=status, last_update=datetime.datetime.strptime(last_update, '%m/%d/%Y'))
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')
 

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
            uploaded_file_url='/simba/media/inv1.jpg' 
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
        return render(request,"inventory/model.html",{"models": models, "mod": mod, "image_file":image_file, 'uploaded_file_url':uploaded_file_url,  "index_type":"Model"})
