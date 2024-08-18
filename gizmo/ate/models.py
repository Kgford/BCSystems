from django.db import models

class Specifications(models.Model):
    id = models.AutoField(primary_key=True)
    spec_type = models.CharField("comments",max_length=50,null=True,unique=False,default='N/A')  
    job_number = models.CharField("job",max_length=20,null=False,unique=False,default='N/A')  
    part_number = models.CharField("part",max_length=20,null=False,unique=False,default='N/A')  
    title = models.CharField("update_by",max_length=50,null=False,unique=False,default='N/A')  
    quantity = models.IntegerField(blank=True, null=True)
    spec_start_freq = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    spec_stop_freq = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    cutoff_freq = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    output_port_number = models.IntegerField(blank=True, null=True)
    vswr = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    insertion_loss = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    isolation = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    isolation2_freq = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    amplitude_balance = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    coupling = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    coup_plus_minus = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    directivity = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    phase_balance = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    coupled_flatness = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15) #index20
    power = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15) #index21
    temperature = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15) #index21
    offset1 = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    offset2 = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    offset3 = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    offset4 = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    offset5 = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    test1 = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    test2 = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    test3 = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    test4 = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    test5 = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    active = models.BooleanField("active",unique=False,null=True,default=True)
    last_update = models.DateField(null=True)  

    def __str__(self):
        return self.job

class Trace(models.Model):
	id = models.AutoField(primary_key=True)
	test_id = models.CharField("test_id",max_length=50,null=True,unique=False,default='N/A') 
	job_number = models.CharField("job_number",max_length=50,null=True,unique=False,default='N/A') 
	title = models.CharField("title",max_length=50,null=True,unique=False,default='N/A') 
	serial_number = models.CharField("serial_number",max_length=50,null=True,unique=False,default='N/A') 
	workstation = models.CharField("workstation",max_length=50,null=True,unique=False,default='N/A') 
	points = models.CharField("points",max_length=50,null=True,unique=False,default='N/A') 
	active_date = models.DateField(null=True)  
	cal_date = models.DateField(null=True) 
	cal_due = models.DateField(null=True) 
	prog_title = models.CharField("prog_title",max_length=50,null=True,unique=False,default='N/A') 
	prog_version = models.CharField("prog_version",max_length=50,null=True,unique=False,default='N/A') 
	x_title = models.CharField("x_title",max_length=50,null=True,unique=False,default='N/A') 
	y_title = models.CharField("y_title",max_length=50,null=True,unique=False,default='N/A') 
	x_array_str = models.CharField("x_array_str",max_length=500,null=True,unique=False,default='N/A') 
	y_array_str = models.CharField("y_array_str",max_length=500,null=True,unique=False,default='N/A') 
	active = models.BooleanField("active",unique=False,null=True,default=True)
	last_update = models.DateField(null=True) 
	
class Trace_points(models.Model):
    id = models.AutoField(primary_key=True)
    trace_id = models.IntegerField(blank=True, null=True)
    idx = models.IntegerField(blank=True, null=True)
    x_data = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    y_data = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    coef_cal = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
	
class Testdata(models.Model):
    id = models.AutoField(primary_key=True)
    spec_id = models.CharField("spec_id",max_length=50,null=False,unique=False,default='N/A')
    job_number = models.CharField("job_number",max_length=50,null=False,unique=True,default='N/A')  
    part_number = models.CharField("part_numbe",max_length=50,null=False,unique=True,default='N/A')  
    serial_number = models.CharField("serial_number",max_length=50,null=True,unique=False,default='N/A') 
    workstation = models.CharField("workstation",max_length=50,null=True,unique=False,default='N/A')
    insertion_loss = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    return_loss = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15) 
    coupling = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    isolation = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    directivity = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    amplitude_balance = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    coupling_flatness = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    phase_balance = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    failure_log = models.CharField("failure_log",max_length=150,null=True,unique=False,default='N/A')
    last_update = models.DateField(null=True)
    
class PortConfig(models.Model):
    id = models.AutoField(primary_key=True)
    job_number = models.CharField("job_number",max_length=50,null=False,unique=True,default='N/A')  
    part_number = models.CharField("part_numbe",max_length=50,null=False,unique=True,default='N/A')  	
    j1j1 = models.CharField("j1j1",max_length=50,null=True,unique=False,default='N/A')
    j1j2 = models.CharField("j1j2",max_length=50,null=True,unique=False,default='N/A')
    j1j3 = models.CharField("j1j3",max_length=50,null=True,unique=False,default='N/A')
    j1j4 = models.CharField("j1j4",max_length=50,null=True,unique=False,default='N/A')
    j1j5 = models.CharField("j1j5",max_length=50,null=True,unique=False,default='N/A')
    j2j1 = models.CharField("j2j1",max_length=50,null=True,unique=False,default='N/A')
    j2j2 = models.CharField("j2j2",max_length=50,null=True,unique=False,default='N/A')
    j3j3 = models.CharField("j3j3",max_length=50,null=True,unique=False,default='N/A')
    j4j4 = models.CharField("j4j4",max_length=50,null=True,unique=False,default='N/A')
    j3j1 = models.CharField("j3j1",max_length=50,null=True,unique=False,default='N/A')
    j3j2 = models.CharField("j3j2",max_length=50,null=True,unique=False,default='N/A')
    j3j3 = models.CharField("j3j3",max_length=50,null=True,unique=False,default='N/A')
    j3j4 = models.CharField("j4j4",max_length=50,null=True,unique=False,default='N/A')
    j4j1 = models.CharField("j1j1",max_length=50,null=True,unique=False,default='N/A')
    j4j2 = models.CharField("j1j2",max_length=50,null=True,unique=False,default='N/A')
    j4j3 = models.CharField("j1j3",max_length=50,null=True,unique=False,default='N/A')
    j4j4 = models.CharField("j1j4",max_length=50,null=True,unique=False,default='N/A')
 

class Devices(models.Model):
    id = models.AutoField(primary_key=True)
    string_name = models.CharField("string_name",max_length=100,null=False,unique=True,default='N/A')  
    string = models.CharField("string",max_length=100,null=False,unique=True,default='N/A')  
 
  
class Devices(models.Model):
    id = models.AutoField(primary_key=True)
    dev_name = models.CharField("dev_name",max_length=100,null=False,unique=True,default='N/A')  
    manufacturer = models.CharField("manufacturer",max_length=100,null=False,unique=True,default='N/A')  	
    dev_type = models.CharField("dev_type",max_length=100,null=False,unique=False,default='N/A')
    default_addr = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    timeout_ms = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15)
    term = models.CharField("manufacturer",max_length=100,null=False,unique=True,default='N/A')  	
    termout = models.CharField("dev_type",max_length=100,null=False,unique=False,default='N/A')
    eoi = models.BooleanField (default=False)
    idn_response = models.CharField("idn_response",max_length=100,null=False,unique=True,default='N/A')  	
    notes = models.CharField("notes",max_length=100,null=False,unique=False,default='N/A')
    manual = models.BooleanField(default=False)
    safe_command = models.CharField("safe_command",max_length=100,null=False,unique=True,default='N/A')  	
    safe_response = models.CharField("safe_response",max_length=100,null=False,unique=False,default='N/A')
    

    
class Workstation(models.Model):
    id = models.AutoField(primary_key=True)
    computer_name = models.CharField("computer_name",max_length=50,null=True,unique=False,default='N/A') 
    workstation_name = models.CharField("workstation_name",max_length=50,null=True,unique=False,default='N/A') 
    vna_type = models.CharField("workstation_name",max_length=50,null=True,unique=False,default='N/A')
    operator = models.CharField("operator",max_length=50,null=True,unique=False,default='N/A') 
    vna_freq = models.DecimalField(blank=True, null=True,decimal_places=4,max_digits=15) #index5
    password = models.CharField("last_user",max_length=100,null=True,unique=False,default='N/A') 
	
	
	
class Effeciency(models.Model):
    id = models.AutoField(primary_key=True)
    workstation = models.CharField("workstation",max_length=50,null=True,unique=False,default='N/A') 
    job_number = models.CharField("job_number",max_length=20,null=False,unique=True,default='N/A')  
    part_number = models.CharField("part_number",max_length=20,null=False,unique=True,default='N/A') 
    operator = models.CharField("operator",max_length=50,null=True,unique=False,default='N/A') 
    active_date = models.DateField(null=True)      
    total_uuts = models.IntegerField(blank=True, null=True)
    complete_uuts = models.IntegerField(blank=True, null=True)
    effeciency_status = models.CharField("effeciency_status",max_length=50,null=True,unique=False,default='N/A') 
    run_status = models.CharField("run_status",max_length=50,null=True,unique=False,default='N/A')   


class Logger(models.Model):
	id = models.AutoField(primary_key=True)
	log_type = models.CharField("log_type",max_length=100,null=True,unique=False)  
	log = models.CharField("log",max_length=1024,null=True,unique=False)  
	
	def __str__(self):
		return self.log