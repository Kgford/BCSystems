from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from datetime import date
from django.urls import reverse
from equipment.models import Model
from datetime import date, datetime

# Create your Equipment views here.
def searchmodel(request):
    mod= []
    success = True 
    models = None    
    try:
        models = Model.objects.all()
    except IOError as e:
        success = False
        print ("Models load Failure ", e)
    if models == None:
        success = False
    else:
        mod=[e.serialize() for e in models]
    return jsonify({"success": success, "model_list": mod})

def loadmodel(request):
    model_id = request.POST['model_id']
    mod = []
    success = True 
    events= None 
    print('model_id =',model_id)
    try:	
        model = Model.get(Model.id==model_id)
    except IOError as e:
        success = False
        print ("Eventss Load Failure ", e)
    if model == None:
        success = False
    else:
        mod=[e.serialize() for e in model]
    print(model)
    return jsonify({"success": success, "model_list": env})


def index(request):
    if request.method == 'POST':
        timestamp = date.today()
        band = request.POST['_band']
        category = request.POST['_category']
        description = request.POST['_desc']
        model = request.POST['_model']
        vendor= request.POST['_vendor']
        active = True
        image_file = request.POST['fileupload']
        comments = request.POST['_comments']
        model_id = request.POST['m_id']
        save = request.POST['_save']
        update = request.POST['_update']
        delete = request.POST['_delete']
        
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
                Model.objects.filter(Model.id == model_id).update({'description': description,'category':category,'band=':band,
					'model':model,'comment':comment,'locationname':locationname,'image_file':image_file,'vendor':vendor,'active':active,'last_update':last_update})
            except IOError as e:
                print ("Models Update Failure ", e)	
        elif not delete==None: 
            try:
                Model.objects.filter(Model.id == model_id).delete()
            except IOError as e:
                print ("Models Delete Failure ", e)
    '''                
    #~~~~~~~~~~~Load equpment database from csv. must put this somewhere else later"
    import csv
    timestamp  = date.today()
    CSV_PATH = 'models.csv'
    print('csv = ',CSV_PATH)

    contSuccess = 0
    # Remove all data from Table
    Model.objects.all().delete()

    f = open(CSV_PATH)
    timestamp  = date.today()
    reader = csv.reader(f)
    print('reader = ',reader)
    for description, category, band, model, vendor, status, last_update in reader:
        Model.objects.create(description=description, category=category, band=band, model=model,vendor=vendor,status=status,last_update=timestamp)
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')
    #~~~~~~~~~~~Load equpment database from csv. must put this somewhere else later"
    '''
    return render(request, "equipment/index.html",{"index_type":"EQUIPMENT"})
