from django.db import models
from django.core.files.base import ContentFile
from django.utils import timezone
from django.conf import settings
# info on remote/local storage
#https://docs.djangoproject.com/en/dev/topics/files/



# Create your models here.
class Model(models.Model):  
    timestamp = timezone.now 
    description = models.CharField("description",max_length=100,null=False,unique=False,default='N/A')  
    category  = models.CharField("category",max_length=50,null=False,unique=False,default='N/A')  # Modem, Switch, Modem Switch, Controller, SC-90 Upgrades
    band = models.CharField("band",max_length=50,null=False,unique=False,default='N/A')  # L-Band, Ku-Band, C-Band, Ka-Band
    vendor = models.CharField("vendor",max_length=50,null=True,unique=False)  
    model = models.CharField("Model",max_length=50,null=False,unique=False)  
    comments = models.CharField("comments",max_length=200,null=True,unique=False)  
    status = models.CharField("status",max_length=50,null=True,unique=False) 
    last_update = models.DateField(default=timestamp)
    inventory_id = models.IntegerField(null=True,unique=False)
    image = models.ImageField(upload_to='equipment/', null=True, blank=True)
    image_width = models.PositiveIntegerField(null=True)
    image_height = models.PositiveIntegerField(null=True)
    
	
    def add_new(self, description, category,band, vendor, model, comments, image, status, last_update):
        self.description = description
        self.category = category
        self.band = band
        self.vendor = vendor
        self.model = model
        self.comments = comments
        self.image_file = image_file
        self.status = status
        self.last_update = last_update
        self.save()	
		
    def serialize(self):
        return {
            'id': self.id, 
            'description': self.description,
            'category': self.category,
            'band': self.band,
            'vendor': self.vendor,
            'model': self.model,
            'comments': self.comments,
            'image_file': self.image_file,
            'status': self.status,
            'last_update': self.last_update,
            'inventory_id': self.inventory_id,
        }  