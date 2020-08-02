from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from datetime import date
from django.urls import reverse
from equipment.models import Model
from locations.models import location
from inventory.models import Inventory, Events

# Create your views here.
def index(request):
    desc_list = []
    models_list = []
    locations_list = []
    shelves_list = []
    try:
        desc_list = Model.objects.order_by('description').values_list('description', flat=True).distinct()
        print(desc_list)
        models_list = Model.objects.order_by('model').values_list('model', flat=True).distinct()
        print(models_list)
        locations_list = location.objects.order_by('name').values_list('name', flat=True).distinct()
        print(locations_list)
        shelves_list  = location.objects.order_by('shelf').values_list('shelf', flat=True).distinct()
    except IOError as e:
        print ("Lists load Failure ", e)
        print('error = ',e)        
    return render (request,"inventory/index.html",{"desc_list":desc_list, "models_list":models_list, "locations_list":locations_list, "shelves_list":shelves_list,"index_type":"INVENTORY"})


def searchevents(request,inventory_id):
    env = []
    success = True 
    events= None  
    
    try:	
        events = Events.objects.filter(Events.inventory_id==inventory_id).all()
    except IOError as e:
        success = False
        print ("Events load Failure ", e)
    if events == None:
        success = False
    else:
        env=[e.serialize() for e in events]
    return jsonify({"success": success, "event_list": env})

def loadevent(request):
    event_id = request.form['event_id']
    env = []
    success = True 
    events= None 
    try:	
        events = Events.objects.get(Events.id==event_id)
    except IOError as e:
        success = False
        print ("Events load Failure ", e)
    if events == None:
        success = False
    else:
        env=[e.serialize() for e in events]
    return jsonify({"success": success, "event_list": env})
    
    
def save_event(request):
    timestamp = date.today()
    event_id = request.POST['e_id']
    inventory_id = request.POST['i_id'] 
    operator = request.POST['_operator']
    print('event_id = ',event_id)
    print('inventory_id = ',inventory_id)
    event_type = request.POST['_event']
    event_date = request.POST['_date']
    locationname = request.POST['_loc']
    mr = request.POST['_mr']
    print('mr = ',mr)
    rma = request.POST['_rma']
    print('rma = ',rma)
    comment = request.POST['_comments']
    print(comment)
    save = request.POST['_save']
    update = request.POST['_update']
    delete = request.POST['_delete']
    if not save==None:
        try:
			#save new event
            Events.add_new(self, event_type, event_date,operator, comment, locationname, mr, rma, inventory_id)
            
			#update item	
            Inventory.objects.filter(Inventory.id == inventory_id).update({'description': comment,'locationname':locationname,'update_by':operator,'last_update':timestamp,})
        except IOError as e:
            print ("Events Save Failure ", e)	
    elif not update==None: 
        try:
			#update existing event
            Events.objects.filter(Events.id == event_id).update({'event_type': event_type,'locationname':event_date,'update_by':operator,'operator':operator,
					'comment':comment,'locationname':locationname,'mr':mr,'rma':rma})
        except IOError as e:
            print ("Events Update Failure ", e)	
    elif not delete==None: 
        try:
            Events.objects.filter(Events.id == event_id).delete()
        except IOError as e:
            print ("Events Update Failure ", e)	
    return HttpResponseRedirect(reverse('inventory/item/'+str(inventory_id)))
	    
def items(request):
    desc_list = []
    models_list = []
    locations_list = []
    shelves_list = []
    if request.method == 'POST':
        timestamp = date.today()
        print(timestamp)
        description = request.POST['_desc']
        print(description)
        category = request.POST['_cat']
        print(category)
        status = request.POST['_stat']
        print(status)
        model = request.POST['_model']
        print(model)
        purchase_order = request.POST['_po']
        print(purchase_order)
        serial_number = request.POST['_sn']
        print(serial_number)
        quantity = request.POST['_Qn']
        print(quantity)
        shipped_date = request.POST['_shipped']
        print(shipped_date)
        recieved_date = request.POST['_recieved']
        print(recieved_date)
        activestr = request.POST['_active']
        if activestr =='True' or activestr=='true':
            active=True
        elif activestr =='False' or activestr =='false':
            active=False
        else:
            active=True
        print(active)
        locationname = request.POST['_site']
        print(locationname)
        shelf = request.POST['_shelf']
        print(shelf)
        remarks = request.POST['_remarks']
        print(remarks)
        try:
            # Add new Inventory item
            Inventory.add_new(serial_number, model,description, locationname, shelf, category, status, quantity, remarks, purchase_order,
				 recieved_date, shipped_date, active, last_update, update_by, model_id, location_id, shelf_id)
        except IOError as e:
            print ("Inventory Save Failure ", e)
        return HttpResponseRedirect(reverse('inventory:index'))
    try:
        desc_list = Model.objects.order_by('description').values_list('description', flat=True).distinct()
        models_list = Model.objects.order_by('model').values_list('model', flat=True).distinct()
        locations_list = location.objects.order_by('name').values_list('name', flat=True).distinct()
        shelves_list = Shelf.objects.order_by('name').values_list('name', flat=True).distinct()
    except IOError as e:
         print ("Lists load Failure ", e)	
    return render (request,"locations/items.html", {"desc_list":desc_list, "models_list":models_list,"locationnames_list":locationnames_list, "shelves_list":shelves_list})
	
def item(request,inventory_id):
    locations_list = []
    shelves_list = []
	#Get locationname
    active_inv = Inventory.objects.get(Inventory.id==inventory_id)
    model = Model.objects.get(Model.model__contains==active_inv.model)
    image_file = 'assets/images/',model.image_file
    print(image_file)
    if image_file == None:
	    image_file = 'assets/images/inv1.jpg'
    try:
        locations_list = location.objects.order_by('name').values_list('name', flat=True).distinct()
        shelves_list  = Shelf.objects.order_by('name').values_list('name', flat=True).distinct()
    except IOError as e:
        session.rollback()
        print ("Lists load Failure ", e)	
    return render (request,"item.html",{"active_inv":active_inv, "image_file":image_file, "today":date.today(), "locations_list":locations_list, "shelf_list":shelves_list})
    
 
def search(request):
    json_data = []
    inv_list = []
    inv = []
    desc = request.POST['desc']
    print('desc = ',desc)
    model = request.POST['model']
    print('model = ',model)
    status = request.POST['status']
    print('status =',status)
    category = request.POST['category']
    print('cat =',category)
    locationname = request.POST['locationname']
    print('loc =',locationname)
    shelf = request.POST['shelf']
    print('shelf =',shelf)
    select = request.POST['sel']
    print('select =',select)
    success = True  
    try:
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
    
def searchall(request):
    json_data = []
    inv_list = []
    search = request.POST['search']
    print(search)
    success = True 
    try:	
        inv_list = inventory.objects.filter(Inventory.description__contains == search | Inventory.modelname__contains == search | 
					Inventory.status__contains == search | Inventory.category__contains == search | Inventory.locationname__contains == search | Inventory.shelf__contains == search)
        desc=inv_list.locations.name           
        if inv_list == None:
            success = False
        else:
            inv=[e.serialize() for e in inv_list]
            return jsonify({"success": success, "inv_list": inv})
    except IOError as e:
        success = False
        print ("Inventory load Failure ", e)
        return jsonify({"success": success, "inv_list": inv})

	

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