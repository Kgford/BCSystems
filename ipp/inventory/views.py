from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from .forms import InventoryForm
from datetime import date, datetime
from django.urls import reverse, reverse_lazy
from inventory.models import Inventory
from django.views import View
import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
class InventoryView(View):
    #~~~~~~~~~~~Load Item database from csv. must put this somewhere else later"
    import csv
    #timestamp  = date.today()
    CSV_PATH = 'C:\src\ipp\inventory\inventory.csv'
    print('csv = ',CSV_PATH)

    contSuccess = 0
    # Remove all data from Table
            
    form_class = InventoryForm
    template_name = "index.html"
    success_url = reverse_lazy('inventory:inv')
    def get(self, *args, **kwargs):
        form = self.form_class()
        try:
            part_number=-1
            unit=-1
            bins=-1
            description=-1
            vendor=-1
            customer=-1
            search=-1
            timestamp = datetime.datetime.today() 
            year = timestamp.year
            month_num= timestamp.month
            print('year =',year)
            months = {'1': "Jan", '2': "Feb",  '3': "March", '4': 'April', '5': "May", '6': "Jun", '7': "Jul", '8': "Aug", '9': "Sept", '10': "Oct", '11': "Nov", '12': "Dec"}
            month = months[str(month_num)]
            print('month =',month)
            parts_list = Inventory.objects.order_by('part_number').values_list('part_number', flat=True).distinct()
            description_list = Inventory.objects.order_by('description').values_list('description', flat=True).distinct()
            vendor_list = Inventory.objects.order_by('vendor').values_list('vendor', flat=True).distinct()
            inv = Inventory.objects.all()
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"inventory/index.html",{"form": form, "inventory": inv, "parts_list":parts_list,
           "description_list":description_list, "vendor_list":vendor_list, "index_type":"INVENTORY",
           'description':description,'part_number':part_number,'vendor':vendor,'search':search,'year':year,'month':month})
    
    def post(self, request, *args, **kwargs):
        try: 
            print("in POST")
            json_data = []
            inv_list = []
            inv = []
            form = self.form_class()
            print('request =',request)
            part_number = request.POST.get('_part', -1)
            print('part_number = ',part_number)
            description = request.POST.get('_desc', -1)
            print('description = ',description)
            year = request.POST.get('_year', -1)
            print('year =',year)
            monthstr = request.POST.get('_month', -1)
            print('monthstr =',monthstr)
            if monthstr==-1:
                month = "all months"
            elif not monthstr=="all months":
                months = {"Jan": "1", "Feb": "2",  "March": "3", 'April': "4", "May": "5", "Jun": "6", "Jul": "7", "Aug": "8", "Sept": "9", "Oct": "10", "Nov": "11", "Dec": "12"}
                month = months[monthstr]
                print(month)
            else:
                month = "all months"
            vendor = request.POST.get('_vendor', -1)
            print('vendor =',vendor)
            search = request.POST.get('search', -1)
            print('search =',search)
            success = True

            #p = Inventory.objects.filter(timestamp__year='2014').filter(timestamp__month='1')
            #p = Inventory.objects.filter(timestamp__range=(start_date, end_date))
            #p = Inventory.objects.filter(Q(created_at__gte=from_date)&Q(created_at__lte=to_date))
            #gte means greater than equal
            #lte means less than equal

            parts_list = Inventory.objects.order_by('part_number').values_list('part_number', flat=True).distinct()
            description_list = Inventory.objects.order_by('description').values_list('description', flat=True).distinct()
            vendor_list = Inventory.objects.order_by('vendor').values_list('vendor', flat=True).distinct()
            if not search ==-1:
                inv_list = Inventory.objects.filter(description__icontains=search) | Inventory.objects.filter(part_number__icontains=search) | Inventory.objects.filter(vendor__icontains=search) | Inventory.objects.filter(customer__icontains=search) | Inventory.objects.filter(gl_code__icontains=search) | Inventory.objects.filter(prod_code__icontains=search) | Inventory.objects.filter(gl_code__icontains=search).all()
            elif month == "all months" and year == "all years" and description == "all descriptions" and part_number == "all parts"  and vendor == "all vendors" :
                inv_list = Inventory.objects.all()
            elif not description =="all descriptions": 
                if month == "all months" and year == "all years" and part_number == "all parts"  and vendor == "all vendors": #All
                    inv_list = Inventory.objects.filter(description__contains=description).all()
                    print(inv_list)
                if not month == "all months" and year == "all years" and part_number == "all parts"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(description__contains=description).filter(timestamp__month=month).all()  
                if not month == "all months" and not year == "all years" and part_number == "all parts"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(description__contains=description).filter(timestamp__month=month).filter(timestamp__year=year).all()  
                if not month == "all months" and not year == "all years" and not part_number == "all parts"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(description__contains=description).filter(timestamp__month=month).filter(timestamp__year=year).filter(part_number__contains=part_number).all()  
                if not month == "all months" and not year == "all years" and not part_number == "all parts"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(description__contains=description).filter(timestamp__month=month).filter(timestamp__year=year).filter(part_number__contains=part_number).filter(vendor__contains=vendor).all()
            elif not part_number =="all parts": 
                if month== "all months" and year == "all years" and description == "all descriptions"  and vendor == "all vendors": #All
                    inv_list = Inventory.objects.filter(part_number__contains=part_number).all()
                if not month == "all months" and year == "all years" and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(part_number__contains=part_number).filter(timestamp__month=month).all()  
                if not month == "all months" and not year == "all years"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(part_number__contains=part_number).filter(timestamp__month=month).filter(timestamp__year=year).all()  
                if not month == "all months" and not year == "all years" and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(part_number__contains=part_number).filter(timestamp__month=month).filter(timestamp__year=year).filter(description__contains=description).all()  
                if not month == "all months" and not year == "all years"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(part_number__contains=part_number).filter(timestamp__month=month).filter(timestamp__year=year).filter(description__contains=description).filter(vendor__contains=vendor).all()
                print(inv_list)
            elif not vendor =="all vendors": 
                if year == "all years" and description == "all descriptions"  and part_number =="all parts" : #All
                    inv_list = Inventory.objects.filter(vendor__contains=vendor).all()
                if not month == "all months" and year == "all years" and part_number =="all parts"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(vendor__contains=vendor).filter(timestamp__month=month).all()  
                if not month == "all months" and not year == "all years" and part_number =="all parts"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(vendor__contains=vendor).filter(timestamp__month=month).filter(timestamp__year=year).all()  
                if not month == "all months" and not year == "all years" and not part_number =="all parts"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(vendor__contains=vendor).filter(timestamp__month=month).filter(timestamp__year=year).filter(description__contains=description).all()  
                if not month == "all months" and not year == "all years" and not part_number =="all parts"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(vendor__contains=vendor).filter(timestamp__month=month).filter(timestamp__year=year).filter(description__contains=description).filter(vendor__contains=vendor).all()
            elif not month =="all months": 
                if not month == "all months" and year == "all years" and description == "all descriptions"  and vendor == "all vendors" and part_number =="all parts" : #All
                    inv_list = Inventory.objects.filter(timestamp__month__contains=month).all()
                if not month == "all months" and not year == "all years" and part_number =="all parts"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(timestamp__month__contains=month).filter(vendor__contains=vendor).all()  
                if not month == "all months" and not year == "all years" and part_number =="all parts"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(timestamp__month__contains=month).filter(vendor__contains=vendor).filter(timestamp__year=year).all()  
                if not month== "all months" and not year == "all years" and not part_number =="all parts"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(timestamp__month__contains=month).filter(vendor__contains=vendor).filter(timestamp__year=year).filter(description__contains=description).all()  
                if not month== "all months" and not year == "all years" and not part_number =="all parts"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(mtimestamp__month__contains=month).filter(vendor__contains=vendor).filter(timestamp__year=year).filter(description__contains=description).filter(vendor__contains=vendor).all()
            elif not year == "all years": 
                if not year== "all years" and month == "all months" and description == "all descriptions"  and vendor == "all vendors" and part_number =="all parts" : #All
                    inv_list = Inventory.objects.filter(timestamp__year__contains=year).all()
                if not year == "all years" and not month == "all months" and part_number =="all parts"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(timestamp__year__contains=year).filter(timestamp__month=month).all()  
                if not year == "all years"  and not month == "all months" and part_number =="all parts"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(timestamp__year__contains=year).filter(vendor__contains=vendor).filter(timestamp__month=month).all()  
                if not year == "all years"  and not month == "all months" and not part_number =="all parts"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(timestamp__year__containsyear).filter(vendor__contains=vendor).filter(timestamp__month=month).filter(description__contains=description).all()  
                if not year == "all years"  and not month == "all months" and not part_number =="all parts"  and vendor == "all vendors":#description, month
                    inv_list = Inventory.objects.filter(mtimestamp__year__contains=year).filter(vendor__contains=vendor).filter(timestamp__month=month).filter(description__contains=description).filter(vendor__contains=vendor).all()
            else:
                inv_list = None
        except IOError as e:
            inv_list = None
            print ("Lists load Failure ", e)

        print('inv_list',inv_list)
        return render (self.request,"inventory/index.html",{"form": form, "inventory": inv_list, "parts_list":parts_list,
           "description_list":description_list, "vendor_list":vendor_list, "index_type":"INVENTORY",
           'description':description,'part_number':part_number,'vendor':vendor,'search':search,'year':year,'month':month})
                
        
# Create your views here.
class SearchView(View):
    template_name = "search.html"
    print('in search view')
    def get(self, *args, **kwargs):
        form = self.form_class()
        print('we are here')
        try:
            parts_list = Inventory.objects.order_by('part_number').values_list('part_number', flat=True).distinct()
            description_list = Inventory.objects.order_by('description').values_list('description', flat=True).distinct()
            vendor_list = Inventory.objects.order_by('vendor').values_list('vendor', flat=True).distinct()
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
    CSV_PATH = 'C:\src\ipp\inventory\inventory.csv'
    print('csv = ',CSV_PATH)

    contSuccess = 0
    # Remove all data from Table
    #Inventory.objects.all().delete()
    print('deleted Inventory')
    f = open(CSV_PATH)
    reader = csv.reader(f)
    print('reader = ',reader)
    for part_number, unit, bins, description, vendor, customer, gl_code, prod_code, in_process, on_order, reserved, outside, on_hand, cost, cost_total, timestamp, update_by in reader:
                if gl_code =='':
                    gl_code= None
                if in_process =='':
                    in_process= None
                if on_order =='':
                    on_order= None
                if reserved =='':
                    reserved= None
                if outside =='':
                    outside= None    
                if on_hand =='':
                    on_hand= None    
                if cost =='':
                    cost= None    
                if cost_total =='':
                    cost_total= None 
                print('timestamp =',timestamp)
                Inventory.objects.create(part_number=part_number, unit=unit, bins=bins, description=description, vendor=vendor,
                customer=customer, gl_code=gl_code, prod_code=prod_code, in_process=in_process, on_order=on_order, reserved=reserved, outside=outside,
                on_hand=on_hand,cost=cost,cost_total=cost_total, timestamp=datetime.datetime.strptime(timestamp, '%m/%d/%Y'), update_by=update_by)
    print(f'{str(contSuccess)} inserted successfully! ')
    
def update_iventory_csv(delete):
    #~~~~~~~~~~~Load Item database from csv. must put this somewhere else later"
    import csv
    timestamp  = date.today()
    CSV_PATH = 'C:\src\ipp\inventory\inventory.csv'
    print('csv = ',CSV_PATH)

    contSuccess = 0
    f = open(CSV_PATH)
    reader = csv.reader(f)
    print('reader = ',reader)
    for part_number, unit, bins, description, vendor, customer, gl_code, prod_code, in_process, on_order, reserved, outside, on_hand, cost, cost_total, timestamp, update_by in reader:
                if gl_code =='':
                    gl_code= None
                if in_process =='':
                    in_process= None
                if on_order =='':
                    on_order= None
                if reserved =='':
                    reserved= None
                if outside =='':
                    outside= None    
                if on_hand =='':
                    on_hand= None    
                if cost =='':
                    cost= None    
                if cost_total =='':
                    cost_total= None 
                    
                Inventory.objects.create(part_number=part_number, unit=unit, bins=bins, description=description, vendor=vendor,
                customer=customer, gl_code=gl_code, prod_code=prod_code, in_process=in_process, on_order=on_order, reserved=reserved, outside=outside,
                on_hand=on_hand,cost=cost,cost_total=cost_total, timestamp=datetime.datetime.strptime(timestamp, '%m/%d/%Y'), update_by=update_by)
    print(f'{str(contSuccess)} inserted successfully! ')
    
    

def update_inv(request):
    if request.method == 'POST':
        update_inv = request.POST.get('update_inv', -1)
        inventory_id = request.POST.get('i_id', -1)
        del_inv = request.POST.get('del_inv', -1)
        operator = request.POST.get('_operator', -1)
        Locations_list = []
        event = 'n/a'
        print('inventory_id =',inventory_id)
        active_inv = Inventory.objects.filter(id=inventory_id)
        print(active_inv)
        active_inv = active_inv[0]
        print(active_inv.description)
        mname = active_inv.modelname
        model = Model.objects.filter(model__contains=mname)
        model = model[0]
        image_file = model.image_file
        if image_file == None:
            image_file = 'inventory/images/inv1.jpg'
        print(image_file)
        parts_list = Inventory.objects.order_by('part_number').values_list('part_number', flat=True).distinct()
        description_list = Inventory.objects.order_by('description').values_list('description', flat=True).distinct()
        vendor_list = Inventory.objects.order_by('vendor').values_list('vendor', flat=True).distinct()
        print('del_inv =',del_inv)
        print('update_inv =',update_inv)

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
    return render (request,"inventory/item.html",{"active_inv":active_inv, "image_file":image_file,"event_list":event_list,
                    "today":date.today(), "locations_list":locations_list, "shelf_list":shelves_list,'event':event,'active_operator':request.user})
    
     
                
                
def save_event(request):
    if request.method == 'POST':
        Locations_list = []
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
        rma = request.POST.get('_rma', -1)
        comment = request.POST.get('_comments', -1)
        save = request.POST.get('_save', -1)
        update = request.POST.get('_update', -1)
        delete = request.POST.get('_delete', -1)
        parts_list = Inventory.objects.order_by('part_number').values_list('part_number', flat=True).distinct()
        description_list = Inventory.objects.order_by('description').values_list('description', flat=True).distinct()
        vendor_list = Inventory.objects.order_by('vendor').values_list('vendor', flat=True).distinct()
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
                
                Events.objects.create(event_type=event_type, event_date=event_date, operator=operator, comment=comment, locationname=locationname,
                      mr=mr, rma=rma, inventory_id=inventory_id)
                
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
        print(image_file)

        print('operator=',operator)
        return render (request,"inventory/item.html",{"active_inv":active_inv, "image_file":image_file,"event_list":event_list,
                    "today":date.today(), "locations_list":locations_list, "shelf_list":shelves_list,'event':event,'active_operator':operator})

def items(request):
    parts_list = []
    description_list = []
    vendor_list = []
    locations_list = []
    event = 'n/a'
    timestamp = date.today()
    operator = request.user
    print(timestamp)
    if request.method == 'POST':
        inventory_id = request.POST.get('inventory_id', -1)
        print(inventory_id)
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
        location = request.POST.get('_site', -1)
        print(location)
        shelf = request.POST.get('_shelf', -1)
        print(shelf)
        remarks = request.POST.get('_remarks', -1)
        print(remarks)
        model_id = Model.objects.filter(model__contains=model)
        print('model_id=',model_id)
        model_id=model_id[0].id
        print('model_id=',model_id)
        location_id = Location.objects.filter(name=location)
        location_id=location_id[0].id
        print('location_id=',location_id)
        shelf_id = Location.objects.filter(name=shelf)
        #shelf_id=shelf_id[0].id
        #print('shelf_id=',shelf_id)
        save = request.POST.get('_save', -1)
        print('save',save)
        update = request.POST.get('_update', -1)
        print('update',update)
        operator = request.POST.get('_operator', -1)
        if operator==-1:
            operator = request.user
        print('operator',operator)
        try:
            if not save ==-1:
                # Add new Inventory item
                Inventory.objects.create(serial_number=serial_number, modelname=model,description=description, locationname=location, 
                        shelf=shelf, category=category, status=status, quantity=quantity, remarks=remarks, purchase_order=purchase_order,
                        recieved_date=recieved_date, shipped_date=shipped_date, active=activestr, last_update=timestamp, update_by=operator,
                        location_id=location_id, model_id=model_id)
            elif not update==-1:
                # Add new Inventory item
                print('ready to update')
                Inventory.objects.filter(id=inventory_id).update(serial_number=serial_number, modelname=model,description=description, locationname=location, 
                        shelf=shelf, category=category, status=status, quantity=quantity, remarks=remarks, purchase_order=purchase_order,
                        recieved_date=recieved_date, shipped_date=shipped_date, active=activestr, last_update=timestamp, 
                        location_id=location_id, model_id=model_id)
                
            HttpResponseRedirect(reverse('inventory:inven'))
        except IOError as e:
            print ("Inventory Save Failure ", e)
        return HttpResponseRedirect(reverse('inventory:inven'))
    try:
        parts_list = Inventory.objects.order_by('part_number').values_list('part_number', flat=True).distinct()
        description_list = Inventory.objects.order_by('description').values_list('description', flat=True).distinct()
        vendor_list = Inventory.objects.order_by('vendor').values_list('vendor', flat=True).distinct()
        Locations_list = []
    except IOError as e:
         print ("Lists load Failure ", e)	
    return render (request,"inventory/items.html",{"today":date.today(), 'active_operator':operator})

def item(request):
    parts_list = []
    description_list = []
    vendor_list = []
    event = 'n/a'
    #Get locationname
    try:
        
        print(event)
        inventory_id = request.GET.get('inventory_id', -1)
        part_number = request.GET.get('part_number', -1)
        print('part_number = ',part_number)
        active_inv = Inventory.objects.filter(id=inventory_id).all()
        active_inv = active_inv[0]
        print('active_inv = ',active_inv)
        inventory = Inventory.objects.filter(part_number=part_number).all()
        print('inventory = ',inventory)
        operator=request.user
        print('operator = ',operator)        
    except IOError as e:
        print ("Lists load Failure ", e)	
    return render (request,"inventory/item.html",{"active_inv":active_inv, "inventory":inventory})
					
 

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
