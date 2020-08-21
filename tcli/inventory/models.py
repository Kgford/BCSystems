from django.db import models

# Create your Inventory models here.
class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    serial_number = models.CharField("serial number",max_length=50,null=False,unique=False,default='N/A')  
    modelname = models.CharField("modelname",max_length=50,null=False,unique=False,default='N/A')  
    description = models.CharField("description",max_length=200,null=False,unique=False,default='N/A')  
    locationname = models.CharField("locationname",max_length=100,null=False,unique=False,default='N/A')  
    shelf = models.CharField("shelf",max_length=10,null=False,unique=False,default='N/A')  
    category = models.CharField("category",max_length=50,null=False,unique=False,default='N/A')   #GDC Spares, Critical Spares, SC-90 Upgrades
    status = models.CharField("status",max_length=50,null=False,unique=False,default='N/A')  #In-House, In-Field, In-Test, Out-Repair
    quantity = models.IntegerField(null=True,unique=False,default=0)
    remarks = models.CharField("remarks",max_length=500,null=True,unique=False,default='N/A')  
    purchase_order = models.CharField("purchase_order",max_length=40,null=False,unique=False,default='N/A')  
    recieved_date = models.DateField(null=True)
    shipped_date = models.DateField(null=True)
    active = models.BooleanField("active",unique=False,null=True,default=True)
    last_update = models.DateField(null=True)
    update_by = models.CharField("update_by",max_length=50,null=False,unique=False,default='N/A')  
    model_id = models.IntegerField(null=True,unique=False)
    location_id = models.IntegerField(null=True,unique=False)
    shelf_id = models.IntegerField(null=True,unique=False)
    
           
    def get_absolute_url(self):
        return reverse('inventory-detail', kwargs={'pk': self.pk})
    
    def add_new(self, serial_number, model,description, locationname, shelf, category, status, quantity , remarks,purchase_order,
				recieved_date, shipped_date, active, last_update, update_by, model_id, locationname_id, shelf_id):
        self.serial_number = serial_number
        self.model = model
        self.description = description
        self.locationname = locationname
        self.shelf = shelf
        self.category = category
        self.status = status
        self.quantity  = quantity 
        self.remarks = remarks
        self.purchase_order = purchase_order
        self.recieved_date = recieved_date
        self.shipped_date = shipped_date
        self.active = active
        self.last_update = last_update
        self.update_by = update_by
        self.model_id = model_id
        self.locationname_id = locationname_id
        self.shelf_id = shelf_id
        self.save()	
    
    def serialize(self):
        return {
            'id': self.id, 
            'serial_number': self.serial_number,
            'category': self.category,
            'description':self.description,
            'model':self.model,
            'locationname':self.locationname,
			'shelf':self.shelf,
            'status': self.status,
            'quantity': self.quantity,
            'remarks': self.remarks,
            'purchase_order': self.purchase_order,
            'recieved_date': self.recieved_date,
            'shipped_date': self.shipped_date,
            'active': self.active,
            'last_update': self.last_update,
            'model_id': self.model_id,
            'locationname_id': self.locationname_id,
            'shelf_id': self.shelf_id,
            'image': self.image,
        }
        
    def add_event(self, type, date, comment):
        r = Event(event_type=type,event_date=event_date, operator=operator, comment=comment, locationname=self.locationname,mr=mr, rma=rma, inventorys_id=self.id)
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
    rma = models.CharField("Item Serial number",max_length=20,null=False,unique=False,default='N/A')  
    inventory_id = models.IntegerField(null=True,unique=False)
	
    def add_new(self, event_type, event_date,operator, comment, locationname, mr, rma, inventorys_id):
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
        
        
 			
 
