from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from django.utils.timezone import now
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

class Specifications(models.Model): # Basic Specs for all Parts
    spectype = models.CharField(db_column='spectype', max_length=100, blank=True, null=True)  # Field name made lowercase.
    partnumber = models.CharField(db_column='partnumber', max_length=100, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='title', max_length=100, blank=True, null=True)  # Field name made lowercase.
    port_loss = models.FloatField(db_column='port_loss', blank=True, null=True,default=3)  # Field name made lowercase.
    port_phase = models.FloatField(db_column='port_phase', blank=True, null=True,default=0)  # Field name made lowercase.
    port_impediance = models.FloatField(db_column='port_impediance', blank=True, null=True,default=50)  # Field name made lowercase.
    startfreqmhz = models.FloatField(db_column='startfreqmhz', blank=True, null=True,default=0)  # Field name made lowercase.
    stopfreqmhz = models.FloatField(db_column='stopfreqmhz', blank=True, null=True,default=0)  # Field name made lowercase.
    cutofffreqmhz = models.FloatField(db_column='cutofffreqmhz', blank=True, null=True,default=0)  # Field name made lowercase.
    vswr = models.FloatField(db_column='vswr', blank=True, null=True,default=0)  # Field name made lowercase.
    insertionloss = models.FloatField(db_column='insertionloss', blank=True, null=True,default=0)  # Field name made lowercase.
    returnloss = models.FloatField(db_column='returnloss', blank=True, null=True,default=0)  # Field name made lowercase.
    isolation = models.FloatField(db_column='isolation', blank=True, null=True,default=0)  # Field name made lowercase.
    amplitudebalance = models.FloatField(db_column='amplitudebalance', blank=True, null=True,default=0)  # Field name made lowercase.
    coupling = models.FloatField(db_column='coupling', blank=True, null=True,default=0)  # Field name made lowercase.
    coupplusminus = models.FloatField(db_column='coupplusminus', blank=True, null=True,default=0)  # Field name made lowercase.
    coupledflatness = models.FloatField(db_column='coupledflatness', blank=True, null=True,default=0)  # Field name made lowercase.
    directivity = models.FloatField(db_column='directivity', blank=True, null=True,default=0)  # Field name made lowercase.
    phasebalance = models.FloatField(db_column='phasebalance', blank=True, null=True,default=0)  # Field name made lowercase.
    power = models.FloatField(db_column='power', blank=True, null=True,default=0)  # Field name made lowercase.
    temperature = models.FloatField(db_column='temperature', blank=True, null=True,default=0)  # Field name made lowercase.
    points = models.IntegerField(db_column='points',null=False,default = 201)  # Field name made lowercase.
    po = models.CharField(db_column='po', max_length=1000, blank=True, null=True,default='N/A')  # Field name made lowercase.
    pph = models.FloatField(db_column='pph', blank=True, null=True,default=0)  # Field name made lowercase.
    special_config = models.TextField("special_config", blank=True,default='N/A')
    def __str__(self):
        return "%s%s %s%s %s%s" % ('Spec ID ', self.pk, ' Spec Type ',self.spectype, ' Part Number ',self.partnumber)

   
class JobData(models.Model): # Parameters and Specs specific to the Job
    jobnumber = models.CharField(db_column='JobNumber', max_length=100, blank=True, null=True)  # Field name made lowercase.
    partnumber = models.CharField(db_column='PartNumber', max_length=100, blank=True, null=True)  # Field name made lowercase.
    datecode = models.CharField(db_column='datecode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
   
    def __str__(self):
        return "%s%s %s%s %s%s" % ('Data ID ', self.pk, ' Job Number ',self.jobnumber, ' Part Number ',self.partnumber)

class TestData(models.Model):
    jobnumber = models.CharField(db_column='JobNumber', max_length=100, blank=True, null=True)  # Field name made lowercase.
    partnumber = models.CharField(db_column='PartNumber', max_length=100, blank=True, null=True)  # Field name made lowercase.
    artwork = models.CharField(db_column='artwork', max_length=100, blank=True, null=True)  # Field name made lowercase.
    panel = models.CharField(db_column='panel', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sector = models.CharField(db_column='sector', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lot = models.CharField(db_column='lot', max_length=100, blank=True, null=True)  # Field name made lowercase.
    test1_run = models.BooleanField("test1_run",unique=False,null=False,default=True) 
    test2_run = models.BooleanField("test2_run",unique=False,null=False,default=True) 
    test3_run = models.BooleanField("test3_run",unique=False,null=False,default=True) 
    test4_run = models.BooleanField("test4_run",unique=False,null=False,default=True) 
    test5_run = models.BooleanField("test4_run",unique=False,null=False,default=True) 
    def __str__(self):
        return "%s%s %s%s %s%s" % ('Data ID ', self.pk, ' Job Number ',self.jobnumber, ' Part Number ',self.partnumber)


class SpecAttachments(models.Model):
    attachment = models.FileField(upload_to='photos', null=True, blank=True)
    name = models.CharField("name",max_length=255,null=True,unique=False,default='N/A')
    attachment_url = models.CharField("attachment_url",max_length=255,null=True,unique=False,default='N/A')
    this_date = models.CharField("this_date",max_length=20,null=True,unique=False,default='N/A')
    creation_date = models.CharField("this_date",max_length=20,null=True,unique=False,default='N/A')
    spec = models.ForeignKey(Specifications, on_delete=models.CASCADE)
    def __str__(self):
        return "%s%s" % ('Part#', self.spec.partnumber)

class SpecDrawings(models.Model):
    drawing = models.FileField(upload_to='drawings', null=True, blank=True)
    name = models.CharField("name",max_length=255,null=True,unique=False,default='N/A')
    drawing_url = models.CharField("drawing_url",max_length=255,null=True,unique=False,default='N/A')
    this_date = models.CharField("this_date",max_length=20,null=True,unique=False,default='N/A')
    creation_date = models.CharField("this_date",max_length=20,null=True,unique=False,default='N/A')
    spec = models.ForeignKey(Specifications, on_delete=models.CASCADE)
    def __str__(self):
        return "%s%s" % ('Part#', self.spec.partnumber)

class Workstation(models.Model):
    computername = models.CharField(db_column='ComputerName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    workstationname = models.CharField(db_column='WorkstationName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bypass = models.BooleanField("golden_data",unique=False,null=False,default=False) 
    jobnumber = models.CharField(db_column='JobNumber', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fail_percent = models.FloatField(db_column='Coupling', blank=True, null=True)  # Field name made lowercase.
    offset1 = models.FloatField(db_column='Offset1', blank=True, null=True,default=0)  # Field name made lowercase.
    offset2 = models.FloatField(db_column='Offset2', blank=True, null=True,default=0)  # Field name made lowercase.
    offset3 = models.FloatField(db_column='Offset3', blank=True, null=True,default=0)  # Field name made lowercase.
    offset4 = models.FloatField(db_column='Offset4', blank=True, null=True,default=0)  # Field name made lowercase.
    offset5 = models.FloatField(db_column='Offset5', blank=True, null=True,default=0)  # Field name made lowercase.
    spec = models.ForeignKey(Specifications, on_delete=models.CASCADE)
    def __str__(self):
        return "%s%s %s%s" % ('Spec ID#', self.spec.pk,' Part Number ', self.spec.partnumber)

class TestFixture(models.Model):
    fixture = models.CharField(db_column='fixture', max_length=100, blank=True, null=True)  # Field name made lowercase.
    plunger = models.CharField(db_column='plunger', max_length=100, blank=True, null=True)  # Field name made lowercase.
    psi = models.FloatField(db_column='psi', blank=True, null=True)  # Field name made lowercase.
    revision = models.CharField(db_column='revision', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fixture_num = models.IntegerField(db_column='fixture_num', blank=True, null=True)  # Field name made lowercase.
    spec = models.ForeignKey(Specifications, on_delete=models.CASCADE)
    def __str__(self):
        return "%s%s %s%s" % ('Spec ID#', self.spec.pk,' Part Number ', self.spec.partnumber)
       
class FixtureAttachments(models.Model):
    attachment = models.FileField(upload_to='photos', null=True, blank=True)
    name = models.CharField("name",max_length=255,null=True,unique=False,default='N/A')
    attachment_url = models.CharField("attachment_url",max_length=255,null=True,unique=False,default='N/A')
    this_date = models.CharField("this_date",max_length=20,null=True,unique=False,default='N/A')
    fixture = models.ForeignKey(TestFixture, on_delete=models.CASCADE)
    def __str__(self):
        return "%s%s" % ('Part#', self.fixture.spec.partnumber)


class FixtureDrawings(models.Model):
    drawing = models.FileField(upload_to='drawings', null=True, blank=True)
    name = models.CharField("name",max_length=255,null=True,unique=False,default='N/A')
    drawing_url = models.CharField("drawing_url",max_length=255,null=True,unique=False,default='N/A')
    this_date = models.CharField("this_date",max_length=20,null=True,unique=False,default='N/A')
    fixture = models.ForeignKey(TestFixture, on_delete=models.CASCADE)
    def __str__(self):
        return "%s%s" % ('Part#', self.fixture.spec.partnumber)


   

class TestStatus(models.Model):
    start_time = models.TimeField("start_time",blank=True, null=True)
    current_time = models.TimeField("current_time",blank=True, null=True)
    finish_time = models.TimeField("finish_time",blank=True, null=True)
    test1 = models.BooleanField("test1",unique=False,null=False,default=True) 
    test2 = models.BooleanField("test2",unique=False,null=False,default=True) 
    test3 = models.BooleanField("test3",unique=False,null=False,default=True) 
    test4 = models.BooleanField("test4",unique=False,null=False,default=True) 
    test5 = models.BooleanField("test4",unique=False,null=False,default=True) 
    testfail = models.FloatField(db_column='TestFail', blank=True, null=True)  # Field name made lowercase.
    retestfail = models.FloatField(db_column='RetestFail', blank=True, null=True)  # Field name made lowercase.
    failpercent = models.FloatField(db_column='FailPercent', blank=True, null=True)  # Field name made lowercase.
    current_serialnumber = models.CharField(db_column='current_serialnumber', max_length=100, blank=True, null=True)  # Field name made lowercase.
    last_serialnumber = models.CharField(db_column='last_serialnumber', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tested = models.IntegerField(db_column='tested', blank=True, null=True,default=0)  # Field name made lowercase.
    failed = models.IntegerField(db_column='failed', blank=True, null=True,default=0)  # Field name made lowercase.
    job_data = models.ForeignKey(JobData, on_delete=models.CASCADE)
    def __str__(self):
        return "%s%s %s%s %s%s" % ('Data ID#', self.job_data.pk,' Part Number ', self.job_data.partnumber,' Job Number', self.job_data.jobnumber)


class TestLogs(models.Model):
    log = RichTextUploadingField("log", blank=True)
    job_data = models.ForeignKey(JobData, on_delete=models.CASCADE)
    def __str__(self):
        return "%s%s %s%s %s%s" % ('Data ID#', self.job_data.pk,' Part Number ', self.job_data.partnumber,' Job Number', self.job_data.jobnumber)

class TabularData(models.Model):
    serialnumber = models.CharField(db_column='SerialNumber', max_length=100, blank=True, null=True)  # Field name made lowercase.
    artwork_revision = models.CharField(db_column='artwork_revision', max_length=100, blank=True, null=True)  # Field name made lowercase.
    job_data = models.ForeignKey(JobData, on_delete=models.CASCADE)
    def __str__(self):
        return "%s%s %s%s %s%s" % ('Data ID#', self.job_data.pk,' Part Number ', self.job_data.partnumber,' Job Number', self.job_data.jobnumber)

class TraceData(models.Model):
    serialnumber = models.CharField(db_column='SerialNumber', max_length=100, blank=True, null=True)  # Field name made lowercase.
    artwork_revision = models.CharField(db_column='artwork_revision', max_length=100, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='title', max_length=100, blank=True, null=True)  # Field name made lowercase
    xdata = models.TextField(db_column='xdata', blank=True, null=True)  # Field name made lowercase.
    ydata = models.TextField(db_column='ydata', blank=True, null=True)  # Field name made lowercase.
    job_data = models.ForeignKey(JobData, on_delete=models.CASCADE)
    def __str__(self):
        return "%s%s %s%s %s%s" % ('Data ID#', self.job_data.pk,' Part Number ', self.job_data.partnumber,' Job Number', self.test_data.jobnumber)






    
    