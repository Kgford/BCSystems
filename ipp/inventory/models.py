from django.db import models

# Create your Inventory models here.
class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    part_number = models.CharField("serial number",max_length=50,null=True,unique=False,default='N/A')  
    unit = models.CharField("modelname",max_length=10,null=True,unique=False,default='N/A')  
    bins = models.CharField("locationname",max_length=100,null=True,unique=False,default='N/A')  
    description = models.CharField("description",max_length=500,null=True,unique=False,default='N/A')  
    vendor = models.CharField("locationname",max_length=100,null=True,unique=False,default='N/A')  
    customer = models.CharField("locationname",max_length=100,null=True,unique=False,default='N/A')
    gl_code = models.IntegerField(null=True,unique=False)
    prod_code = models.CharField("shelf",max_length=100,null=True,unique=False,default='N/A') 	
    in_process = models.IntegerField(null=True,unique=False)
    on_order = models.IntegerField(null=True,unique=False)
    reserved = models.IntegerField(null=True,unique=False)
    outside = models.FloatField(null=True,unique=False) 
    on_hand = models.IntegerField(null=True,unique=False)
    cost = models.FloatField(null=True,unique=False) 
    cost_total = models.FloatField(null=True,unique=False) 
    timestamp = models.DateField()
    update_by = models.CharField("update_by",max_length=50,null=False,unique=False,default='N/A')  
    
    
    class Meta:
        managed = True
        db_table = 'inventory' 
       
    def serialize(self):
        return {
			'id': self.id, 
			'part_number': part_number,
			'unit': unit,
			'bins': bins,
			'description':self.description,
			'vendor':self.vendor,
			'customer':self.customer,
			'gl_code':self.gl_code,
			'prod_code': self.prod_code,
			'in_process': self.in_process,
			'on_order': self.on_order,
			'reserved': self.reserved,
			'outside': self.outside,
			'on_hand': self.on_hand,
			'cost': self.cost,
			'cost_total': self.cost_total,
			'model_id': self.model_id,
			'last_update': self.last_update,
			'update_by': self.update_by,
        }
