from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .forms import EquipmentForm, ModelsForm
from datetime import date
from django.urls import reverse,  reverse_lazy
from django.urls import reverse
from django.views import View
from equipment.models import Model
from datetime import date, datetime
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import datetime
model_id = 0

class EquipmentView(View):
    form_class = EquipmentForm
    template_name = "index.html"
    success_url = reverse_lazy('equipment:equipment')
    contSuccess = 0
    
    def get(self, *args, **kwargs):
        form = self.form_class()
        try:
            models = Model.objects.all()
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"equipment/index.html",{"form": form, "models": models, "index_type":"EQUIPMENT"})
	   	
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
        return render (self.request,"equipment/index.html",{"form": form, "models": models, "index_type":"EQUIPMENT"})

class ModelView(View):
    form_class = ModelsForm
    template_name = "model.html"
    success_url = reverse_lazy('equipment:model')
   
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
        return render (self.request,"equipment/index.html",{"form": form, "models": models, "model": mod,  "index_type":"EQUIPMENT"})
        
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
        return render (self.request,"equipment/index.html",{"form": form, "models": models, "index_type":"EQUIPMENT"})

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
                uploaded_file_url = '/tcli/media/inv1.jpg'
            print('uploaded_file_url =',uploaded_file_url)
        except IOError as e:
            print ("load model Failure ", e)
            print('error = ',e) 
        return render(request,"equipment/model.html",{"models": models, "mod": mod, "uploaded_file_url":uploaded_file_url,  "index_type":"Model"})
        
def newmodel(request):
        models = []
        success = True 
        try:	
            mod = -1
            models=Model.objects.all()
            image_file = 'inv1.jpg'
            uploaded_file_url = '/tcli/media/inv1.jpg'
                       
        except IOError as e:
            print ("load model Failure ", e)
            print('error = ',e) 
        return render(request,"equipment/model.html",{"models": models, "mod": mod, "uploaded_file_url":uploaded_file_url, "image_file":image_file,  "index_type":"Model"})

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
    return render(request, 'equipment/images.html', {'form' : form}) 
   
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
            uploaded_file_url='/tcli/media/inv1.jpg' 
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