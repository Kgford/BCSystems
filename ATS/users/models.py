from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserProfileInfo(models.Model):
    USER='User'
    SUPERVISOR='Supervisor'
    MANAGER='Manager'
    OWNER='Owner'
    ENGINEER='Engineer'
    PRESIDENT='President'
    VICE_PRESIDENT='Vice President'
    CONTROLLER='Controller'
    TEST_ENGINEER='Test_Engineer'
    SOFTWARE_ENGINEER='Software_Engineer'
    MECHANICAL_ENGINEER='Mechaical_Engineer'
    TECHNICIAN='Technician'
    TESTER='Tester'
    PREP_OPERATOR='Prep_Operator'
    DESIGNER='Designer'
    DRAFTSMAN='Draftsman'
    MECHANICAL_ASSEMBLER='Mechanical_Assembler'
    ELECTRICAL_ASSEMBLER='Electrical_Assembler'
    OPERATOR='Operator'
    CONTRACTOR='Contractor'
    MANAGED_SERVICES_PROVIDER='Managed_Services_Provider'
    IT='IT'
    DEVELOPER='Developer'
    MARKETING='Marketing'
    COSTING='Costing'
    SALES='Sales'
    SOCIAL_MEDIA='Social_Media'
    WEB_MONITOR='Web_Monitor'
    HELP_DESK='Help_Desk'
    SECURITY='Security'
    REGULAR = 'Regular'
    EXEMPT = 'Exempt'
    PART_TIME = 'Part Time'
    TEMP = 'Temp'
    CONTRACTOR = 'Contractor'
    TERMINATED='Terminated'
    NONE='None'
    WHITE='White'
    YELLOW='Yellow'
    GREEN='Green'
    BLACK='Black'
    STATUS_CHOICES =(
        (REGULAR, 'Regular'),
        (EXEMPT, 'Exempt'),
        (PART_TIME, 'Part Time'),
        (TEMP, 'Temp'),
        (CONTRACTOR, 'Contractor'),
        (TERMINATED, 'Terminated'),
    )
    
    ROLE_CHOICES = (
        (USER, 'User'),
        (PRESIDENT, 'President'),
        (VICE_PRESIDENT, 'Vice President'),
        (CONTROLLER, 'Controller'),
        (SUPERVISOR, 'Supervisor'),
        (MANAGER, 'Manager'),
        (OWNER, 'Owner'),
        (ENGINEER, 'Engineer'),
        (TEST_ENGINEER, 'Test_Engineer'),
        (SOFTWARE_ENGINEER, 'Software_Engineer'),
        (MECHANICAL_ENGINEER, 'Mechaical_Engineer'),
        (TECHNICIAN, 'Technician'),
        (TESTER, 'Tester'),
        (PREP_OPERATOR, 'Prep_Operator'),
        (DESIGNER, 'Designer'),
        (DRAFTSMAN, 'Draftsman'),
        (MECHANICAL_ASSEMBLER, 'Mechanical_Assembler'),
        (ELECTRICAL_ASSEMBLER, 'Electrical_Assembler'),
        (OPERATOR, 'Operator'),
        (CONTRACTOR, 'Contractor'),
        (MANAGED_SERVICES_PROVIDER, 'Managed_Services_Provider'),
        (IT, 'IT'),
        (DEVELOPER, 'Developer'),
        (MARKETING, 'Marketing'),
        (COSTING, 'Costing'),
        (SALES, 'Sales'),
        (SOCIAL_MEDIA, 'Social_Media'),
        (WEB_MONITOR, 'Web_Monitor'),
        (HELP_DESK, 'Help_Desk'),
        (SECURITY, 'Security'),
    )
    
    LEAN_CHOICES = (
    (NONE, 'None'),
    (WHITE, 'White'),
    (YELLOW, 'Yellow'),
    (GREEN, 'Green'),
    (BLACK, 'Black'),
    )
    
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    employee_code = models.CharField(db_column='Employee_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    active_group = models.CharField("active_group",max_length=50, blank=True)
    reports_to = models.CharField("reports_to",max_length=50, blank=True)
    department_code = models.CharField("department_code",max_length=10,null=True, blank=True,default = "0")
    employee_number = models.CharField("employee_number",max_length=10,null=True, blank=True,default = "0")
    status = models.CharField("status",choices=STATUS_CHOICES,max_length=50, blank=True)
    shift = models.IntegerField(db_column='shift ', blank=True, null=True)  # Field name made lowercase.
    shift_start = models.TimeField("shift_start",null=True, blank=True)
    shift_end = models.TimeField("shift_end ",null=True, blank=True)
    hours = models.DecimalField(db_column='hours', max_digits=4, decimal_places=1,default = 40)  # Field name made lowercase.
    phone = models.CharField(max_length=50, blank=True)
    personal_phone = models.CharField("personal_phone",max_length=50, blank=True)
    email = models.CharField("email",max_length=50, blank=True)
    personal_email = models.CharField("personal_email",max_length=50, blank=True)
    address = models.CharField("address",max_length=60, blank=True)
    address_line2 = models.CharField("address_line2",max_length=20, null=True, blank=True)
    ip_address = models.CharField("ip_address",max_length=60, blank=True)
    city = models.CharField("city",max_length=60, blank=True)
    state = models.CharField("state",max_length=10, blank=True)
    zip = models.CharField("zip",max_length=30, blank=True)
    birthdate = models.DateField("birthdate",null=True, blank=True)
    hire_date = models.DateField("hire_date",null=True, blank=True)
    wage_change_date = models.DateField("wage_change_date",null=True, blank=True)
    last_review_date = models.DateField("last_review_date",null=True, blank=True)
    last_training_date = models.DateField("last_training_date",null=True, blank=True)
    termination_date = models.DateField("termination_date",null=True, blank=True)
    lean_status = models.CharField("lean_status",choices=LEAN_CHOICES,max_length=30, blank=True,default = "None")
    portfolio_site = models.URLField(blank=True)
    salaried= models.DecimalField('salaried',max_digits=10, decimal_places=2, default=0.0)
    hourly= models.DecimalField('hourly',max_digits=5, decimal_places=2, default=0.0)
    active = models.BooleanField("active",unique=False,null=True,default=True)
    ticket_list = models.BooleanField("ticket_list",unique=False,null=True,default=True)
    ci_list = models.BooleanField("ci_list",unique=False,null=True,default=True)
    gemba_team = models.BooleanField("gemba_team",unique=False,null=True,default=False)
    paychex = models.BooleanField("paychex",unique=False,null=True,default=True)
    contact_name = models.CharField("contact_relationship",max_length=50, blank=True)
    contact_relationship = models.CharField("contact_relationship",max_length=50, blank=True)
    contact_address = models.CharField("contact_address",max_length=60, blank=True)
    contact_address_line2 = models.CharField("contact_address_line2",max_length=60, blank=True)
    contact_city = models.CharField("contact_city",max_length=60, blank=True)
    contact_state = models.CharField("contact_state",max_length=60, blank=True)
    contact_zip = models.CharField("contact_zip",max_length=30, blank=True)
    contact_phone = models.CharField("contact_phone",max_length=50, blank=True)
    contact_cell_phone = models.CharField("contact_cell_phone",max_length=50, blank=True)
    contact_email = models.CharField("contact_email",max_length=50, blank=True)
    contact_personal_email = models.CharField("contact_personal_email",max_length=50, blank=True)
    qrcode = models.ImageField(upload_to='qrcodes/', null=True, blank=True)
    role = models.CharField("role",choices=ROLE_CHOICES, max_length=50, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    alerts_manager = models.BooleanField("alerts_manager",unique=False,null=True,default=False)
    alerts_help_desk = models.BooleanField("alerts_help_desk",unique=False,null=True,default=False)
    alerts_marketing = models.BooleanField("alerts_marketing",unique=False,null=True,default=False)
    alerts_social_media = models.BooleanField("alerts_social_media",unique=False,null=True,default=False)
    alerts_web_monitor = models.BooleanField("alerts_web_monitor",unique=False,null=True,default=False)
    alerts_sales = models.BooleanField("alerts_sales",unique=False,null=True,default=False)
    alerts_developer = models.BooleanField("alerts_developer",unique=False,null=True,default=False)
    alerts_security = models.BooleanField("alerts_security",unique=False,null=True,default=False)
    alerts_accounting = models.BooleanField("alerts_accounting",unique=False,null=True,default=False)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfileInfo.objects.create(user=instance)
    instance.userprofileinfo.save()
     

def __str__(self):
    return self.user.username
    
    
class Globals(models.Model):
    last_user = models.CharField(db_column='last_user', max_length=50) 
    
    
class PTOAccrualsTotal(models.Model):
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wednesday = 'Wednesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'
    Sunday ='Sunday'
    
    CHOICES = (
        (Monday, 'Monday'),
        (Tuesday, 'Tuesday'),
        (Wednesday, 'Wednesday'),
        (Thursday, 'Thursday'),
        (Friday, 'Friday'),
        (Saturday, 'Saturday'),
        (Sunday, 'Sunday'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    year = models.IntegerField("year",null=False,default = 2014)
    month = models.IntegerField("month",null=False,default = 1)
    week = models.IntegerField("month",null=False,default = 1)
    weekday = models.CharField("weekday",choices=CHOICES, max_length=50, null=True, blank=True)
    holiday = models.DecimalField('holiday',max_digits=10, decimal_places=2, default=0.0)
    vacation = models.DecimalField('vacation',max_digits=10, decimal_places=2, default=0.0)
    personal = models.DecimalField('personal',max_digits=10, decimal_places=2, default=0.0)
    unpaid_pto = models.DecimalField('unpaid_pto',max_digits=10, decimal_places=2, default=0.0)
    disability = models.DecimalField('disability',max_digits=10, decimal_places=2, default=0.0)
    family_leave = models.DecimalField('family_leave',max_digits=10, decimal_places=2, default=0.0)
    bereavement = models.DecimalField('bereavement',max_digits=10, decimal_places=2, default=0.0)
    military = models.DecimalField('military',max_digits=10, decimal_places=2, default=0.0)
    voting_leave = models.DecimalField('voting_leave',max_digits=10, decimal_places=2, default=0.0)
    jury_duty = models.DecimalField('jury_duty',max_digits=10, decimal_places=2, default=0.0)
    other = models.DecimalField('other',max_digits=10, decimal_places=2, default=0.0)
    def __str__(self):
        return "%s%s %s%s %s%s" % ('User ', self.user, 'year ', self.year, 'monthe ', self.month)
    


class PTOAccruals(models.Model):
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wednesday = 'Wednesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'
    Sunday ='Sunday'
    CHOICES = (
        (Monday, 'Monday'),
        (Tuesday, 'Tuesday'),
        (Wednesday, 'Wednesday'),
        (Thursday, 'Thursday'),
        (Friday, 'Friday'),
        (Saturday, 'Saturday'),
        (Sunday, 'Sunday'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    year = models.IntegerField("year",null=False,default = 2014)
    month = models.IntegerField("month",null=False,default = 1)
    week = models.IntegerField("week",null=False,default = 1)
    weekday = models.CharField("weekday",choices=CHOICES, max_length=50, null=True, blank=True)
    holiday = models.DecimalField('holiday',max_digits=10, decimal_places=2, default=0.0)
    vacation = models.DecimalField('vacation',max_digits=10, decimal_places=2, default=0.0)
    personal = models.DecimalField('personal',max_digits=10, decimal_places=2, default=0.0)
    unpaid_pto = models.DecimalField('unpaid_pto',max_digits=10, decimal_places=2, default=0.0)
    disability = models.DecimalField('disability',max_digits=10, decimal_places=2, default=0.0)
    family_leave = models.DecimalField('family_leave',max_digits=10, decimal_places=2, default=0.0)
    bereavement = models.DecimalField('bereavement',max_digits=10, decimal_places=2, default=0.0)
    military = models.DecimalField('military',max_digits=10, decimal_places=2, default=0.0)
    voting_leave = models.DecimalField('voting_leave',max_digits=10, decimal_places=2, default=0.0)
    jury_duty = models.DecimalField('jury_duty',max_digits=10, decimal_places=2, default=0.0)
    other = models.DecimalField('other',max_digits=10, decimal_places=2, default=0.0)
    pto_adjustment = models.DecimalField('pto_adjustment',max_digits=10, decimal_places=2, default=0.0)
    def __str__(self):
        return "%s%s %s%s %s%s %s%s" % ('User ', self.user, 'year ', self.year, 'week ', self.week, 'weekday ', self.weekday)
        
        
class EmployeeCode(models.Model):
    company_code = models.CharField(db_column='Company_Code', max_length=20)  # Field name made lowercase.
    employee_code_id = models.AutoField(db_column='Employee_Code_ID', primary_key=True)  # Field name made lowercase.
    employee_code = models.CharField(db_column='Employee_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    employee_number = models.IntegerField(db_column='Employee_Number', blank=True, null=True)  # Field name made lowercase.
    employee_name = models.CharField(db_column='Employee_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    shift_code = models.CharField(db_column='Shift_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hire_date = models.DateTimeField(db_column='Hire_Date', blank=True, null=True)  # Field name made lowercase.
    termination_date = models.DateTimeField(db_column='Termination_Date', blank=True, null=True)  # Field name made lowercase.
    last_review_date = models.DateTimeField(db_column='Last_Review_Date', blank=True, null=True)  # Field name made lowercase.
    next_review_date = models.DateTimeField(db_column='Next_Review_Date', blank=True, null=True)  # Field name made lowercase.
    phone_number = models.CharField(db_column='Phone_Number', max_length=30, blank=True, null=True)  # Field name made lowercase.
    social_security_number = models.CharField(db_column='Social_Security_Number', max_length=11, blank=True, null=True)  # Field name made lowercase.
    payroll_code = models.CharField(db_column='Payroll_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    department_code = models.CharField(db_column='Department_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    shift_begin_time = models.DateTimeField(db_column='Shift_Begin_Time', blank=True, null=True)  # Field name made lowercase.
    shift_end_time = models.DateTimeField(db_column='Shift_End_Time', blank=True, null=True)  # Field name made lowercase.
    ot_method = models.CharField(db_column='OT_Method', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ot_threshold_hours = models.DecimalField(db_column='OT_Threshold_Hours', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    ot_factor = models.DecimalField(db_column='OT_Factor', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    work_sunday = models.BooleanField(db_column='Work_Sunday', blank=True, null=True)  # Field name made lowercase.
    work_monday = models.BooleanField(db_column='Work_Monday', blank=True, null=True)  # Field name made lowercase.
    work_tuesday = models.BooleanField(db_column='Work_Tuesday', blank=True, null=True)  # Field name made lowercase.
    work_wednesday = models.BooleanField(db_column='Work_Wednesday', blank=True, null=True)  # Field name made lowercase.
    work_thursday = models.BooleanField(db_column='Work_Thursday', blank=True, null=True)  # Field name made lowercase.
    work_friday = models.BooleanField(db_column='Work_Friday', blank=True, null=True)  # Field name made lowercase.
    work_saturday = models.BooleanField(db_column='Work_Saturday', blank=True, null=True)  # Field name made lowercase.
    active = models.BooleanField(db_column='Active', blank=True, null=True)  # Field name made lowercase.
    apply_auto_break = models.BooleanField(db_column='Apply_Auto_Break', blank=True, null=True)  # Field name made lowercase.
    image_filename = models.CharField(db_column='Image_Filename', max_length=255, blank=True, null=True)  # Field name made lowercase.
    allow_batch_at_clock = models.BooleanField(db_column='Allow_Batch_At_Clock', blank=True, null=True)  # Field name made lowercase.
    user_code = models.CharField(db_column='User_Code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=50, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.DecimalField(db_column='User_Currency1', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.DecimalField(db_column='User_Currency2', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.DecimalField(db_column='User_Number1', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.DecimalField(db_column='User_Number2', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.DecimalField(db_column='User_Number3', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.DecimalField(db_column='User_Number4', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase.
    template_name = models.CharField(db_column='Template_Name', max_length=20, blank=True, null=True)  # Field name made lowercase.
    template_description = models.CharField(db_column='Template_Description', max_length=50, blank=True, null=True)  # Field name made lowercase.
    default_template = models.BooleanField(db_column='Default_Template', blank=True, null=True)  # Field name made lowercase.
    exported = models.BooleanField(db_column='Exported', blank=True, null=True)  # Field name made lowercase.
    attendance_code = models.CharField(db_column='Attendance_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    entered_date = models.DateTimeField(db_column='Entered_Date', blank=True, null=True)  # Field name made lowercase.
    entered_by = models.CharField(db_column='Entered_By', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ot_calculator = models.CharField(db_column='OT_Calculator', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fax_number = models.CharField(db_column='Fax_Number', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mobile_phone_number = models.CharField(db_column='Mobile_Phone_Number', max_length=30, blank=True, null=True)  # Field name made lowercase.
    email_address = models.CharField(db_column='Email_Address', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mobile_email_address = models.CharField(db_column='Mobile_Email_Address', max_length=50, blank=True, null=True)  # Field name made lowercase.
    allow_start_job_on_closed_jobs = models.BooleanField(db_column='Allow_Start_Job_On_Closed_Jobs', blank=True, null=True)  # Field name made lowercase.
    allow_clock_in_at_clock = models.BooleanField(db_column='Allow_Clock_In_At_Clock', blank=True, null=True)  # Field name made lowercase.
    allow_transaction_during_autobreak = models.BooleanField(db_column='Allow_Transaction_During_Autobreak', blank=True, null=True)  # Field name made lowercase.
    holiday_shift_code = models.CharField(db_column='Holiday_Shift_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    geo_fence_method = models.CharField(db_column='Geo_Fence_Method', max_length=20, blank=True, null=True)  # Field name made lowercase.
    warehouse_code = models.CharField(db_column='Warehouse_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    geo_fence_radius = models.IntegerField(db_column='Geo_Fence_Radius', blank=True, null=True)  # Field name made lowercase.
    network_name = models.CharField(db_column='Network_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    workflow_hold = models.BooleanField(db_column='Workflow_Hold', blank=True, null=True)  # Field name made lowercase.
    workflow_hold_reason = models.TextField(db_column='Workflow_Hold_Reason', blank=True, null=True)  # Field name made lowercase.
    workflow_hold_date = models.DateTimeField(db_column='Workflow_Hold_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EmployeeCode'
              
        
class AttendanceDetail(models.Model):
    company_code = models.CharField(db_column='Company_Code', max_length=20)  # Field name made lowercase.
    attendance_detail_id = models.AutoField(db_column='Attendance_Detail_ID', primary_key=True)  # Field name made lowercase.
    attendance_header_id = models.IntegerField(db_column='Attendance_Header_ID', blank=True, null=True)  # Field name made lowercase.
    actual_clock_in = models.DateTimeField(db_column='Actual_Clock_In', blank=True, null=True)  # Field name made lowercase.
    actual_clock_out = models.DateTimeField(db_column='Actual_Clock_Out', blank=True, null=True)  # Field name made lowercase.
    adjusted_clock_in = models.DateTimeField(db_column='Adjusted_Clock_In', blank=True, null=True)  # Field name made lowercase.
    adjusted_clock_out = models.DateTimeField(db_column='Adjusted_Clock_Out', blank=True, null=True)  # Field name made lowercase.
    actual_hours = models.DecimalField(db_column='Actual_Hours', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    adjusted_hours = models.DecimalField(db_column='Adjusted_Hours', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    attendance_code = models.CharField(db_column='Attendance_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    payroll_code = models.CharField(db_column='Payroll_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    payroll_rate = models.DecimalField(db_column='Payroll_Rate', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    gl_account = models.CharField(db_column='GL_Account', max_length=20, blank=True, null=True)  # Field name made lowercase.
    overtime = models.BooleanField(db_column='Overtime', blank=True, null=True)  # Field name made lowercase.
    shift_code = models.CharField(db_column='Shift_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    holiday = models.BooleanField(db_column='Holiday', blank=True, null=True)  # Field name made lowercase.
    created_by = models.CharField(db_column='Created_By', max_length=20, blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    ot_calculation_flag = models.CharField(db_column='OT_Calculation_Flag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    collection_terminal_number = models.SmallIntegerField(db_column='Collection_Terminal_Number', blank=True, null=True)  # Field name made lowercase.
    payroll_amount = models.DecimalField(db_column='Payroll_Amount', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    break_hours = models.DecimalField(db_column='Break_Hours', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    break_code = models.CharField(db_column='Break_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    paid_break = models.BooleanField(db_column='Paid_Break', blank=True, null=True)  # Field name made lowercase.
    employee_code_id = models.IntegerField(db_column='Employee_Code_ID', blank=True, null=True)  # Field name made lowercase.
    company_code_id = models.IntegerField(db_column='Company_Code_ID', blank=True, null=True)  # Field name made lowercase.
    ot_factor = models.DecimalField(db_column='OT_Factor', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    run_splitters = models.BooleanField(db_column='Run_Splitters', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Attendance_Detail'


class AttendanceHeader(models.Model):
    company_code = models.CharField(db_column='Company_Code', max_length=20)  # Field name made lowercase.
    attendance_header_id = models.AutoField(db_column='Attendance_Header_ID', primary_key=True)  # Field name made lowercase.
    employee_code = models.CharField(db_column='Employee_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    employee_name = models.CharField(db_column='Employee_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ticket_date = models.DateTimeField(db_column='Ticket_Date', blank=True, null=True)  # Field name made lowercase.
    pay_period_code = models.CharField(db_column='Pay_Period_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    exported = models.BooleanField(db_column='Exported', blank=True, null=True)  # Field name made lowercase.
    template_name = models.CharField(db_column='Template_Name', max_length=20, blank=True, null=True)  # Field name made lowercase.
    template_description = models.CharField(db_column='Template_Description', max_length=50, blank=True, null=True)  # Field name made lowercase.
    default_template = models.BooleanField(db_column='Default_Template', blank=True, null=True)  # Field name made lowercase.
    total_actual_hours = models.DecimalField(db_column='Total_Actual_Hours', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    total_adjusted_hours = models.DecimalField(db_column='Total_Adjusted_Hours', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    total_break_hours = models.DecimalField(db_column='Total_Break_Hours', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    total_man_hours = models.DecimalField(db_column='Total_Man_Hours', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    total_machine_hours = models.DecimalField(db_column='Total_Machine_Hours', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    total_payroll_amount = models.DecimalField(db_column='Total_Payroll_Amount', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    total_labor_amount = models.DecimalField(db_column='Total_Labor_Amount', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    total_burden_amount = models.DecimalField(db_column='Total_Burden_Amount', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    total_time_and_material_amount = models.DecimalField(db_column='Total_Time_And_Material_Amount', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    total_pieces_good = models.DecimalField(db_column='Total_Pieces_Good', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    total_pieces_scrapped = models.DecimalField(db_column='Total_Pieces_Scrapped', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=50, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.DecimalField(db_column='User_Currency1', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.DecimalField(db_column='User_Currency2', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.DecimalField(db_column='User_Number1', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.DecimalField(db_column='User_Number2', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.DecimalField(db_column='User_Number3', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.DecimalField(db_column='User_Number4', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase.
    attendance_header_code = models.CharField(db_column='Attendance_Header_Code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    source_attendance_header_code = models.CharField(db_column='Source_Attendance_Header_Code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    employee_code_id = models.IntegerField(db_column='Employee_Code_ID', blank=True, null=True)  # Field name made lowercase.
    company_code_id = models.IntegerField(db_column='Company_Code_ID', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    entered_date = models.DateTimeField(db_column='Entered_Date', blank=True, null=True)  # Field name made lowercase.
    entered_by = models.CharField(db_column='Entered_By', max_length=50, blank=True, null=True)  # Field name made lowercase.
    total_pieces_reported = models.DecimalField(db_column='Total_Pieces_Reported', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    total_pieces_suspect = models.DecimalField(db_column='Total_Pieces_Suspect', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    total_pieces_to_repair = models.DecimalField(db_column='Total_Pieces_To_Repair', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    total_pieces_to_remake = models.DecimalField(db_column='Total_Pieces_To_Remake', max_digits=18, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    employee_number = models.IntegerField(db_column='Employee_Number', blank=True, null=True)  # Field name made lowercase.
    department_code = models.CharField(db_column='Department_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    workflow_hold = models.BooleanField(db_column='Workflow_Hold', blank=True, null=True)  # Field name made lowercase.
    workflow_hold_reason = models.TextField(db_column='Workflow_Hold_Reason', blank=True, null=True)  # Field name made lowercase.
    workflow_hold_date = models.DateTimeField(db_column='Workflow_Hold_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Attendance_Header'
     
