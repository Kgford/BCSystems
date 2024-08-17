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
    CONTRACTOR = 'Contractor'
    TERMINATED='Terminated'
    STATUS_CHOICES =(
        (REGULAR, 'Regular'),
        (EXEMPT, 'Exempt'),
        (PART_TIME, 'Part Time'),
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
    shift = models.IntegerField(db_column='shift ', blank=True, null=True)  # Field name made lowercase.
    hours = models.DecimalField(db_column='hours', max_digits=4, decimal_places=1,default = 40)  # Field name made lowercase.
    phone = models.CharField("phone",max_length=50, blank=True)
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
    portfolio_site = models.URLField(blank=True)
    salaried= models.DecimalField('salaried',max_digits=10, decimal_places=2, default=0.0)
    hourly= models.DecimalField('hourly',max_digits=5, decimal_places=2, default=0.0)
    active = models.BooleanField("active",unique=False,null=True,default=True)
    ticket_list = models.BooleanField("ticket_list",unique=False,null=True,default=True)
    ci_list = models.BooleanField("ci_list",unique=False,null=True,default=True)
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
    def __str__(self):
        return "%s%s %s%s %s%s %s%s" % ('User ', self.user, 'year ', self.year, 'week ', self.week, 'weekday ', self.weekday)
    