from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
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
from django.contrib.auth.decorators import login_required
model_id = 0

class EquipmentView(View):
    form_class = EquipmentForm
    template_name = "index.html"
    success_url = reverse_lazy('equipment:equipment')
    def get(self, *args, **kwargs):
        form = self.form_class()
        try:
            models = Model.objects.all()
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"equipment/index.html",{"form": form, "models": models, "index_type":"EQUIPMENT"})
	   	
    def post(self, request, *args, **kwargs):
        timestamp = date.today()
        band = request.GET.get['_band']
        category = request.GET.get['_category']
        description = request.GET.get['_desc']
        model = request.GET.get['_model']
        vendor= request.GET.get['_vendor']
        active = True
        image_file = request.GET.get['fileupload']
        comments = request.GET.get['_comments']
        model_id = request.GET.get['m_id']
        save = request.GET.get['_save']
        update = request.GET.get['_update']
        delete = request.GET.get['_delete']
        
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
            mod = Model.objects.filter(Model.id == self.slug).all()
            print(models)
            print(mod)
        except IOError as e:
            print ("Lists load Failure ", e)
            print('error = ',e) 
        return render (self.request,"equipment/index.html",{"form": form, "models": models, "model": mod,  "index_type":"EQUIPMENT"})
        
    def post(self, *args, **kwargs):
        timestamp = date.today()
        band = request.GET.get['_band']
        category = request.GET.get['_category']
        description = request.GET.get['_desc']
        model = request.GET.get['_model']
        vendor= request.GET.get['_vendor']
        active = True
        image_file = request.GET.get['fileupload']
        comments = request.GET.get['_comments']
        self.slug = request.GET.get['m_id']
        save = request.GET.get['_save']
        update = request.GET.get['_update']
        delete = request.GET.get['_delete']
        
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
                Model.objects.filter(Model.id == self.slug).update({'description': description,'category':category,'band=':band,
                    'model':model,'comment':comment,'locationname':locationname,'image_file':image_file,'vendor':vendor,'active':active,'last_update':last_update})
            except IOError as e:
                print ("Models Update Failure ", e)	
        elif not delete==None: 
            try:
                Model.objects.filter(Model.id == self.slug).delete()
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
            models = Model.objects.all()
            for mod1 in models:
                if mod1.id ==model_id:
                    mod = mod1
                    break
            print(mod.image_file)
            if mod.image_file==None:
                image_file = 'equipment/images/inv1.jpg'
            else:
                image_file = 'equipment/images/', mod.image_file
                    
            print('desc =',mod.description)
            
        except IOError as e:
            print ("load model Failure ", e)
            print('error = ',e) 
        return render(request,"equipment/model.html",{"models": models, "mod": mod, "image_file":image_file,  "index_type":"Model"})

@login_required
def savemodel(request):
    if request.method == 'POST':
        timestamp = date.today()
        band = request.GET.get['_band']
        print(band)
        category = request.GET.get['_category']
        description = request.GET.get['_desc']
        model = request.GET.get['_model']
        vendor= request.GET.get['_vendor']
        active = True
        image_file = request.GET.get['fileupload']
        comments = request.GET.get['_comments']
        self.slug = request.GET.get['m_id']
        save = request.GET.get['_save']
        update = request.GET.get['_update']
        delete = request.GET.get['_delete']
        
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
                Model.objects.filter(Model.id == self.slug).update({'description': description,'category':category,'band=':band,
                    'model':model,'comment':comment,'locationname':locationname,'image_file':image_file,'vendor':vendor,'active':active,'last_update':last_update})
            except IOError as e:
                print ("Models Update Failure ", e)	
        elif not delete==None: 
            try:
                Model.objects.filter(Model.id == self.slug).delete()
            except IOError as e:
                print ("Models Delete Failure ", e)		
        return render(request,"equipment/model.html",{"models": models, "mod": mod, "image_file":image_file,  "index_type":"Model"})