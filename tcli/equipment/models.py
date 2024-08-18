from django.db import models
from django.core.files.base import ContentFile
from django.utils import timezone
from django.conf import settings
# info on remote/local storage
#https://docs.djangoproject.com/en/dev/topics/files/



# Create your models here.
class Model(models.Model):  
    timestamp = timezone.now 
    id = models.AutoField(primary_key=True)
    description = models.CharField("description",max_length=100,null=False,unique=False,default='N/A')  
    category  = models.CharField("category",max_length=50,null=False,unique=False,default='N/A')  # Modem, Switch, Modem Switch, Controller, SC-90 Upgrades
    band = models.CharField("band",max_length=50,null=False,unique=False,default='N/A')  # L-Band, Ku-Band, C-Band, Ka-Band
    vendor = models.CharField("vendor",max_length=50,null=True,unique=False)  
    model = models.CharField("Model",max_length=50,null=False,unique=False)  
    comments = models.CharField("comments",max_length=200,null=True,unique=False)  
    image_file = models.CharField("Image_file",max_length=20,null=True,unique=False) 
    status = models.CharField("status",max_length=50,null=True,unique=False) 
    last_update = models.DateField(default=timestamp)
    inventory_id = models.IntegerField(null=True,unique=False)
    photo= models.ImageField(upload_to='media/', blank=True)
        
    def __str__(self):
        return self.description
        
    def get_absolute_url(self):
        return reverse('model', kwargs={'slug': self.id})
		
       
    
	
    def add_new(self, description, category,band, vendor, model, comments, image_file, status, last_update):
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