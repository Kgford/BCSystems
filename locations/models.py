from django.db import models
from inventory.models import Inventory

# Create your locaions models here.
class Location(models.Model):   
    id = models.AutoField(primary_key=True)
    name = models.CharField("location name",max_length=100,null=False,unique=True)
    address = models.CharField("location address",max_length=100,null=False,unique=False,default='N/A')    	
    city = models.CharField("location city",max_length=50,null=False,unique=False,default='N/A')                           
    state = models.CharField("location state",max_length=25,null=False,unique=False,default='N/A')    
    zip_code = models.CharField("location state",max_length=25,null=False,unique=False,default='N/A')   
    phone = models.CharField("location Phone Number",max_length=15,null=False,unique=False,default='N/A')      
    email = models.CharField("location Phone Number",max_length=50,null=False,unique=False,default='N/A')   
    website = models.CharField("location Phone Number",max_length=60,null=False,unique=False,default='N/A') 
    active = models.BooleanField("location active",unique=False,null =True,default=True)
    image_file = models.CharField("location image",max_length=50,null=True,unique=False)   
    created_on = models.DateField()
    last_entry = models.DateField()
    inventory_id = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True)
    lat = models.FloatField("location Latitude",null=True,unique=False)
    lng = models.FloatField("location Longitude",null=True,unique=False)
    shelf = models.CharField("shelf",max_length=25,null=False,unique=False,default='N/A')   
    
    def add_new(self, name, address, city, state, phone, email, website, active, inventory_id, create_date, log_date, lat, lng):
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.phone = phone
        self.email = email
        self.website = website
        self.active = active
        self.inventory_id = inventory_id
        self.created_on = create_date
        self.last_entry = log_date
        self.lat = lat
        self.lng = lng
        self.save()	
	
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'phone': self.phone,
            'email': self.email,
            'website': self.website,
            'active': self.active,
            'image_file': self.image_file,
            'created_on': self.created_on,
            'last_entry': self.last_entry,
            'inventory_id': self.inventory_id
        }

