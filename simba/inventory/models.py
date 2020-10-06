from django.db import models
from django.core.files.base import ContentFile
from django.utils import timezone
from django.conf import settings

# Create your Inventory models here.
class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    serial_number = models.CharField("serial number",max_length=50,null=True,unique=False,default='N/A')  
    modelname = models.CharField("modelname",max_length=50,null=True,unique=False,default='N/A')  
    description = models.CharField("description",max_length=200,null=True, unique=False,default='N/A')  
    locationname = models.CharField("locationname",max_length=100,null=False,unique=False,default='N/A')  
    shelf = models.CharField("shelf",max_length=10,null=True,unique=False,default='N/A')  
    category = models.CharField("category",max_length=50,null=True,unique=False,default='N/A')   #GDC Spares, Critical Spares, SC-90 Upgrades
    status = models.CharField("status",max_length=50,null=True,unique=False,default='N/A')  #In-House, In-Field, In-Test, Out-Repair
    remarks = models.CharField("remarks",max_length=500,null=True,unique=False,default='N/A')  
    purchase_order = models.CharField("purchase_order",max_length=40,null=False,unique=False,default='N/A')  
    active = models.BooleanField("active",unique=False,null=True,default=True)
    last_update = models.DateField(null=True)
    update_by = models.CharField("update_by",max_length=50,null=False,unique=False,default='N/A')  
    model_id = models.IntegerField(null=True,unique=False)
    location_id = models.IntegerField(null=True,unique=False)
    shelf_id = models.IntegerField(null=True,unique=False)

    def serialize(self):
        return {
        'id': self.id, 
        'serial_number': self.serial_number,
        'category': self.category,
        'description':self.description,
        'model':self.modelname,
        'locationname':self.locationname,
        'shelf':self.shelf,
        'status': self.status,
        'remarks': self.remarks,
        'purchase_order': self.purchase_order,
        'active': self.active,
        'last_update': self.last_update,
        'model_id': self.model_id,
        'locationname_id': self.locationname_id,
        'shelf_id': self.shelf_id,
        'image': self.image,
        }
        
    def add_event(self, type, date, comment):
        r = Event(event_type=type,event_date=event_date, operator=operator, comment=comment, locationname=self.locationname,mr=mr, rma=rma, inventory_id=self.id)
        self.add(r)
        self.commit()
		
    def add_shelf(self):
        r = Mr(name=self.description,locationname=self.locationname,inventory_id=self.id)
        self.add(r)
        self.commit()
  		
class Shelf(models.Model):   
    __tablename__ = 'shelf'
    __table_args__ = {'extend_existing': True}
    id = models.AutoField(primary_key=True)
    name = models.CharField("Item Serial number",max_length=20,null=False,unique=False,default='N/A')  
    locationname = models.CharField("Item Serial number",max_length=100,null=False,unique=False,default='N/A')  
    locationname_id = models.IntegerField(null=True,unique=False)
    #inventory_id = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'locationname_id': locationname_id.category,
            'inventory_id': inventory_id
        }

class Events(models.Model):
    """User account event."""
    __tablename__ = 'event'
    __table_args__ = {'extend_existing': True}
    id = models.AutoField(primary_key=True)
    event_type = models.CharField("Item Serial number",max_length=20,null=False,unique=False,default='N/A')  
    event_date = models.DateField(null=True)
    operator = models.CharField("Item Serial number",max_length=50,null=False,unique=False,default='N/A')  
    comment = models.CharField("Item Serial number",max_length=500,null=False,unique=False,default='N/A')  
    locationname = models.CharField("Item Serial number",max_length=50,null=False,unique=False,default='N/A')  
    mr = models.CharField("Item Serial number",max_length=20,null=False,unique=False,default='N/A')  
    rtv = models.CharField("Item Serial number",max_length=20,null=False,unique=False,default='N/A')  
    rma = models.CharField("Item Serial number",max_length=20,null=False,unique=False,default='N/A')  
    inventory_id = models.IntegerField(null=True,unique=False)
	
    def add_new(self, event_type, event_date,operator, comment, locationname, mr, rma, inventory_id):
        self.event_type = event_type
        self.event_date = event_date
        self.operator = operator
        self.comment = comment
        self.locationname = locationname
        self.mr = mr
        self.rma = rma
        self.inventory_id = inventory_id
        self.save()	
		
    def serialize(self):
        return {
            'id': self.id, 
            'event_type': self.event_type,
            'event_date': self.event_date,
            'operator': self.operator,
            'comment': self.comment,
            'locationname': self.locationname,
			'mr': self.mr,
			'rma': self.rma,
			'inventory_id': self.inventory_id
        } 


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

class Location(models.Model):   
    id = models.AutoField(primary_key=True)
    name = models.CharField("name",max_length=100,null=False,unique=True)
    address = models.CharField("address",max_length=100,null=False,unique=False,default='N/A')    	
    city = models.CharField("city",max_length=50,null=False,unique=False,default='N/A')                           
    state = models.CharField("state",max_length=25,null=False,unique=False,default='N/A')    
    zip_code = models.CharField("zip_code",max_length=25,null=False,unique=False,default='N/A')   
    phone = models.CharField("Phone",max_length=15,null=False,unique=False,default='N/A')      
    email = models.CharField("email",max_length=50,null=False,unique=False,default='N/A')   
    website = models.CharField("website",max_length=60,null=False,unique=False,default='N/A') 
    active = models.BooleanField("active",unique=False,null =True,default=True)
    image_file = models.CharField("image",max_length=50,null=True,unique=False)   
    created_on = models.DateField()
    last_entry = models.DateField()
    inventory_id  = models.IntegerField(null=True,unique=False)
    lat = models.FloatField("lat",null=True,unique=False)
    lng = models.FloatField("lng",null=True,unique=False)
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

class Materials(models.Model):
    id = models.AutoField(primary_key=True)
    VendorID = models.CharField("vendor id",max_length=50,null=True,unique=False,default='N/A')
    MaterialType = models.CharField("material type",max_length=255,null=True,unique=False,default='N/A')
    Color = models.CharField("color",max_length=50,null=True,unique=False,default='N/A')
    Material = models.CharField("material",max_length=255,null=True,unique=False,default='N/A')
    MaterialSize = models.CharField("material size",max_length=50,null=True,unique=False,default='N/A')
    QuantityPrice = models.CharField("quantity price",max_length=50,null=True,unique=False,default='N/A')
    Cost = models.CharField("cost",max_length=50,null=True,unique=False,default='N/A')
    CostType = models.CharField("cost type",max_length=50,null=True,unique=False,default='N/A')
    Client = models.CharField("client",max_length=50,null=True,unique=False,default='N/A')
    Active = models.BooleanField("Active",unique=False,null=True,default=True)
    ChargeID = models.CharField("charge id",max_length=50,null=True,unique=False,default='N/A')
    InvoiceID = models.CharField("invoice id",max_length=255,null=True,unique=False,default='N/A')
    CustomerID = models.CharField("customer id",max_length=50,null=True,unique=False,default='N/A')
    MaterialDate = models.DateField(null=True)
    last_update = models.DateField(null=True)        