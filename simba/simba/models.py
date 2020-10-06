from django.db import models

class Customers(models.Model):
    id = models.AutoField(primary_key=True)
    FirstName = models.CharField("First Name",max_length=255,null=True,unique=False,default='N/A') 
    LastName = models.CharField("last name",max_length=255,null=True,unique=False,default='N/A') 
    StreetAddress = models.CharField("street address",max_length=255,null=True,unique=False,default='N/A') 
    City = models.CharField("city",max_length=255,null=True,unique=False,default='N/A') 
    State = models.CharField("state",max_length=50,null=True,unique=False,default='N/A')  
    ZipCode = models.CharField("zip code",max_length=50,null=True,unique=False,default='N/A')  
    PhoneNumber = models.CharField("phone number",max_length=50,null=True,unique=False,default='N/A')  
    EmailAddress = models.CharField("email",max_length=255,null=True,unique=False,default='N/A')  
    CustomerType = models.CharField("customer type",max_length=255,null=True,unique=False,default='N/A')  
    TaxIDNumber = models.CharField("tax id",max_length=50,null=True,unique=False,default='N/A') 
    ShipStreet = models.CharField("ship street",max_length=100,null=True,unique=False,default='N/A')  
    ShipCity = models.CharField("ship city",max_length=50,null=True,unique=False,default='N/A')  
    ShipState = models.CharField("shipstate",max_length=50,null=True,unique=False,default='N/A')  
    ShipZip = models.CharField("ship zip",max_length=50,null=True,unique=False,default='N/A')      
    Unsubscribe = models.BooleanField("active",unique=False,null=True,default=True)
    ProfitabilityScale = models.CharField("ship zip",max_length=50,null=True,unique=False,default='N/A') 
    Business = models.CharField("ship zip",max_length=50,null=True,unique=False,default='N/A') 
    BusinessName = models.CharField("ship zip",max_length=255,null=True,unique=False,default='N/A') 
    Client = models.CharField("ship zip",max_length=50,null=True,unique=False,default='N/A')
    last_update = models.DateField(null=True)    
    
    
class ErrorLog(models.Model):
    id = models.AutoField(primary_key=True)
    CompanyName = models.CharField("company name",max_length=255,null=True,unique=False,default='N/A') 
    DateTime = models.DateField(null=True)
    SoftwareVersion = models.CharField("version",max_length=255,null=True,unique=False,default='N/A') 
    SoftwareKey = models.CharField("key",max_length=255,null=True,unique=False,default='N/A') 
    ErrorFunction = models.CharField("error function",max_length=255,null=True,unique=False,default='N/A') 
    ErrorCode = models.CharField("error code",max_length=255,null=True,unique=False,default='N/A') 
    Operator = models.CharField("operator",max_length=255,null=True,unique=False,default='N/A') 
    ConnectionType = models.CharField("connection type",max_length=255,null=True,unique=False,default='N/A') 
    SignalStrength = models.CharField("signal strengeh",max_length=255,null=True,unique=False,default='N/A') 
    WifiAccount = models.CharField("wifi",max_length=255,null=True,unique=False,default='N/A') 
    Secure = models.BooleanField("secure",unique=False,null=True,default=True)
    
    
class esnecil(models.Model):
    id = models.AutoField(primary_key=True)
    LLc = models.CharField("llc",max_length=255,null=True,unique=False,default='N/A') 
    Status = models.CharField("status",max_length=255,null=True,unique=False,default='N/A')
    Ins = models.CharField("ins",max_length=255,null=True,unique=False,default='N/A')
    AcK = models.IntegerField(null=True,unique=False)
    AcC = models.CharField("acc",max_length=255,null=True,unique=False,default='N/A')
    DataSource = models.CharField("data source",max_length=255,null=True,unique=False,default='N/A')
    InitialCatalog = models.CharField("initial catalog",max_length=255,null=True,unique=False,default='N/A')
    UserID = models.CharField("user id",max_length=255,null=True,unique=False,default='N/A')
    PW = models.CharField("pw",max_length=255,null=True,unique=False,default='N/A')
    CustomerName = models.CharField("customer Name",max_length=255,null=True,unique=False,default='N/A')
    last_update = models.DateField(null=True)  
    
class sedoc(models.Model):
    id = models.AutoField(primary_key=True)
    CID = models.IntegerField(null=True,unique=False)
    UNum = models.IntegerField(null=True,unique=False)
    ALeng = models.IntegerField(null=True,unique=False)
    ATyp = models.CharField("atyp",max_length=50,null=True,unique=False,default='N/A')
    RDesk = models.BooleanField("rdesk",unique=False,null=True,default=True)
    RData = models.BooleanField("rdata",unique=False,null=True,default=True)
    AC = models.CharField("ac",max_length=255,null=True,unique=False,default='N/A')
    ADate = models.CharField("adate",max_length=50,null=True,unique=False,default='N/A')
    SRev = models.CharField("srev",max_length=255,null=True,unique=False,default='N/A')
    DataSource = models.CharField("data source",max_length=50,null=True,unique=False,default='N/A')
    InitialCatalog = models.CharField("initial catalog",max_length=50,null=True,unique=False,default='N/A')
    UserID = models.CharField("user id",max_length=50,null=True,unique=False,default='N/A')
    PW = models.CharField("pw",max_length=50,null=True,unique=False,default='N/A')
    dilav = models.BooleanField("dilav",unique=False,null=True,default=True)
    ActivatedUsers = models.BooleanField("active",unique=False,null=True,default=True)
    last_update = models.DateField(null=True)  
    
class Vendors(models.Model):
    id = models.AutoField(primary_key=True)
    SimbaCustomer = models.CharField("simba customer",max_length=255,null=True,unique=False,default='N/A')
    CompanyName = models.CharField("company name",max_length=255,null=True,unique=False,default='N/A')
    StreetAddress = models.CharField("street address",max_length=255,null=True,unique=False,default='N/A')
    City = models.CharField("city",max_length=255,null=True,unique=False,default='N/A')
    State = models.CharField("state",max_length=50,null=True,unique=False,default='N/A')
    ZipCode = models.CharField("zip code",max_length=50,null=True,unique=False,default='N/A')
    PhoneNumber = models.CharField("phone number",max_length=50,null=True,unique=False,default='N/A')
    EmailAddress = models.CharField("email",max_length=255,null=True,unique=False,default='N/A')
    TaxIDNumber = models.CharField("tax id",max_length=50,null=True,unique=False,default='N/A')
    Fax = models.CharField("Fax",max_length=50,null=True,unique=False,default='N/A')
    Client = models.CharField("client",max_length=50,null=True,unique=False,default='N/A')
    last_update = models.DateField(null=True) 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    