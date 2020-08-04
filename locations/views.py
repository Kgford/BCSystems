from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from datetime import date
from django.urls import reverse
from locations.models import Location
from inventory.models import Inventory, Events

# Create your views here.
def index(request):
    if request.method == 'POST':
        timestamp = date.today()
        name = request.POST['_name']
        address = request.POST['_addr']
        city = request.POST['_city']
        state = request.POST['_state']
        zipcode = request.POST['_zip']
        phone = request.POST['_phone']
        lat = request.POST['_lat']
        lng = request.POST['_lng']
        email = request.POST['_email']
        website = request.POST['_web']
        inventory_id = None
        active=True
        try:        
           Location.objects.create(name=name, address=address, city=city, state=state, zip_code=zip_code, phone=phone, email=email, website=website,
                    active=active, inventory_id=inventory_id, created_on=timestamp, last_entry=timestamp, lat=lat, lng=lng)
        except IOError as e:
            print ("location Save Failure ", e)	

    '''               
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
    
    #~~~~~~~~~~~Load equpment database from csv. must put this somewhere else later"
    '''          
    return render (request,"locations/index.html",{"index_type":"SIGNIN", "UserN":request.user})
	
def site(request,location_id):
    #Get locationname
    active_site = location.get(location.id==location_id)
    #lat = 40.815320
    #lng = -73.237710
    return render_template("site.html",active_site=active_site)
	
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
