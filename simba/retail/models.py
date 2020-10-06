from django.db import models

class Retail_BOM(models.Model):
    id = models.AutoField(primary_key=True)
    Item = models.IntegerField(null=True,unique=False)
    InventoryID = models.CharField("inventory id",max_length=255,null=True,unique=False,default='N/A') 
    Material = models.CharField("material",max_length=255,null=True,unique=False,default='N/A') 
    MaterialType = models.CharField("material type",max_length=55,null=True,unique=False,default='N/A')
    MaterialColor = models.CharField("material color",max_length=55,null=True,unique=False,default='N/A') 
    Quantity = models.CharField("quantity",max_length=55,null=True,unique=False,default='N/A') 
    ItemCost = models.CharField("item cost",max_length=55,null=True,unique=False,default='N/A') 
    MaterialSize = models.CharField("material size",max_length=55,null=True,unique=False,default='N/A') 
    QuantityPrice = models.CharField("quantity price",max_length=55,null=True,unique=False,default='N/A') 
    Cost = models.CharField("cost",max_length=55,null=True,unique=False,default='N/A') 
    CostType = models.CharField("cost type",max_length=55,null=True,unique=False,default='N/A') 
    Client = models.CharField("client",max_length=50,null=True,unique=False,default='N/A')
    last_update = models.DateField(null=True)

class Retail_ChargeCodes(models.Model):
    id = models.AutoField(primary_key=True)
    ResourceID = models.CharField("resource id",max_length=100,null=True,unique=False,default='N/A') 
    Customer = models.CharField("customer",max_length=100,null=True,unique=False,default='N/A') 
    ChargeCode = models.CharField("charge code",max_length=100,null=True,unique=False,default='N/A') 
    Products_Services = models.CharField("products services",max_length=100,null=True,unique=False,default='N/A') 
    ChargeDate = models.CharField("charge date",max_length=100,null=True,unique=False,default='N/A') 
    Client = models.CharField("client",max_length=100,null=True,unique=False,default='N/A') 
    last_update = models.DateField(null=True)

class Retail_ClassCodes(models.Model):
    id = models.AutoField(primary_key=True)
    ClassCode = models.CharField("class code",max_length=50,null=True,unique=False,default='N/A') 
    InventoryClass = models.CharField("inv class",max_length=50,null=True,unique=False,default='N/A') 
    Client = models.CharField("client",max_length=50,null=True,unique=False,default='N/A') 
    last_update = models.DateField(null=True)
    
class Retail_ColorCodes(models.Model):
    id = models.AutoField(primary_key=True)
    ColorCode = models.CharField("class code",max_length=50,null=True,unique=False,default='N/A') 
    Color = models.CharField("inv class",max_length=50,null=True,unique=False,default='N/A') 
    Client = models.CharField("client",max_length=50,null=True,unique=False,default='N/A') 
    last_update = models.DateField(null=True)
    
class Retail_SizeCodes(models.Model):
    id = models.AutoField(primary_key=True)
    SizeCode = models.CharField("class code",max_length=50,null=True,unique=False,default='N/A') 
    InventorySize = models.CharField("inv size",max_length=50,null=True,unique=False,default='N/A') 
    Client = models.CharField("client",max_length=50,null=True,unique=False,default='N/A') 
    last_update = models.DateField(null=True)
    
class Retail_TypeCodes(models.Model):
    id = models.AutoField(primary_key=True)
    TypeCode = models.CharField("type code",max_length=50,null=True,unique=False,default='N/A') 
    InventoryType = models.CharField("inv type",max_length=50,null=True,unique=False,default='N/A') 
    Client = models.CharField("client",max_length=50,null=True,unique=False,default='N/A') 
    last_update = models.DateField(null=True)
    
class Retail_CompanyInfo(models.Model):
    id = models.AutoField(primary_key=True)
    CompanyName = models.CharField("company name",max_length=50,null=True,unique=False,default='N/A') 
    StreetAddress = models.CharField("street address",max_length=50,null=True,unique=False,default='N/A') 
    City = models.CharField("city",max_length=50,null=True,unique=False,default='N/A') 
    State = models.CharField("state",max_length=50,null=True,unique=False,default='N/A') 
    ZipCode = models.CharField("zip code",max_length=50,null=True,unique=False,default='N/A') 
    PhoneNumber = models.CharField("phone number",max_length=50,null=True,unique=False,default='N/A') 
    EmailAddress = models.CharField("email address",max_length=255,null=True,unique=False,default='N/A') 
    WebSite = models.CharField("web site",max_length=255,null=True,unique=False,default='N/A')
    TaxIDNumber = models.CharField("tax id",max_length=50,null=True,unique=False,default='N/A')
    CompanyType = models.CharField("company type",max_length=50,null=True,unique=False,default='N/A')
    CompanyDescription = models.CharField("company descrition",max_length=50,null=True,unique=False,default='N/A')
    Instagram = models.CharField("instagram",max_length=50,null=True,unique=False,default='N/A')
    Facebook = models.CharField("facebook",max_length=50,null=True,unique=False,default='N/A')
    snapchat = models.CharField("snapchat",max_length=50,null=True,unique=False,default='N/A')
    Twitter = models.CharField("twitter",max_length=50,null=True,unique=False,default='N/A')
    SendEAlerts = models.BooleanField("alerts",unique=False,null=True,default=True)
    Client = models.CharField("client",max_length=255,null=True,unique=False,default='N/A')
    PrimaryCompany = models.BooleanField("primary company",unique=False,null=True,default=True)

class Retail_Customers(models.Model):
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
	backup_index = models.IntegerField(null=True,unique=False)

class Retail_Expenses(models.Model):
	id = models.AutoField(primary_key=True)
	VendorID = models.CharField("vendor id",max_length=50,null=True,unique=False,default='N/A') 
	ExpenseType = models.CharField("expense type",max_length=50,null=True,unique=False,default='N/A') 
	ExpenseDescription = models.CharField("expense desc",max_length=355,null=True,unique=False,default='N/A') 
	SaleDate = models.CharField("sale date",max_length=50,null=True,unique=False,default='N/A') 
	Item = models.CharField("item",max_length=50,null=True,unique=False,default='N/A') 
	ItemDescription = models.CharField("item desc",max_length=355,null=True,unique=False,default='N/A') 
	Quantity = models.CharField("quantity",max_length=50,null=True,unique=False,default='N/A') 
	ItemCost = models.CharField("item cost",max_length=50,null=True,unique=False,default='N/A') 
	TotalCost = models.CharField("total cost",max_length=50,null=True,unique=False,default='N/A') 
	ReOccurringExpenses = models.CharField("reoccuring expenses",max_length=255,null=True,unique=False,default='N/A') 
	ReOccurringInterval = models.CharField("reoccuring interval",max_length=255,null=True,unique=False,default='N/A') 
	Client = models.CharField("client",max_length=255,null=True,unique=False,default='N/A') 
	InvoiceID = models.CharField("invoiceID",max_length=255,null=True,unique=False,default='N/A') 
	StaffID = models.CharField("staff id",max_length=50,null=True,unique=False,default='N/A') 
	last_update = models.DateField(null=True) 
	backup_index = models.IntegerField(null=True,unique=False)
    
class Retail_Images(models.Model):
	id = models.AutoField(primary_key=True)
	InventoryID = models.CharField("inventory id",max_length=255,null=True,unique=False,default='N/A')
	ImageName = models.CharField("image name",max_length=255,null=True,unique=False,default='N/A')
	PIC = models.ImageField("pic",null=True,unique=False,default='N/A')
	Client = models.CharField("client",max_length=50,null=True,unique=False,default='N/A')
	last_update = models.DateField(null=True) 
	backup_index = models.IntegerField(null=True,unique=False)
    
class Retail_Inventory(models.Model):
	id = models.AutoField(primary_key=True)
	InventoryNumber = models.CharField("inventory num",max_length=55,null=True,unique=False,default='N/A') 
	InventoryID = models.CharField("inventory id",max_length=55,null=True,unique=False,default='N/A') 
	InventoryClass = models.CharField("inventory class",max_length=55,null=True,unique=False,default='N/A') 
	InventoryType = models.CharField("inventory type",max_length=55,null=True,unique=False,default='N/A') 
	ItemName = models.CharField("item name",max_length=255,null=True,unique=False,default='N/A') 
	ItemDescription = models.CharField("item description",max_length=255,null=True,unique=False,default='N/A') 
	ItemCost = models.DecimalField("item cost",max_digits=10, decimal_places=2,null=True,unique=False) 
	RetailCost = models.DecimalField("retail cost",max_digits=10, decimal_places=2,null=True,unique=False) 
	WholeSaleCost = models.DecimalField("wholesale cost",max_digits=10, decimal_places=2,null=True,unique=False) 
	NumberSold = models.IntegerField(null=True,unique=False)
	InStock = models.IntegerField(null=True,unique=False)
	Image = models.CharField("image",max_length=255,null=True,unique=False,default='N/A')
	InventorySizeDIM = models.CharField("inventory size",max_length=55,null=True,unique=False,default='N/A')
	InventorySize = models.CharField("vendor id",max_length=55,null=True,unique=False,default='N/A')
	InventoryColor = models.CharField("vendor id",max_length=55,null=True,unique=False,default='N/A')
	NumberOrdered = models.IntegerField(null=True,unique=False)
	Markup = models.FloatField("vendor id",null=True,unique=False) 
	WholesaleMarkup = models.FloatField("vendor id",null=True,unique=False) 
	Client = models.CharField("client",max_length=50,null=True,unique=False,default='N/A')
	last_update = models.DateField(null=True)
	backup_index = models.IntegerField(null=True,unique=False)

class Retail_Invoice(models.Model):
	id = models.AutoField(primary_key=True)
	InvoiceID = models.IntegerField(null=True,unique=False)
	ResourceID = models.IntegerField(null=True,unique=False)
	CustomerID = models.IntegerField(null=True,unique=False)
	ResourceName = models.CharField("resource name",max_length=100,null=True,unique=False,default='N/A')
	ResourceType = models.CharField("resource type",max_length=100,null=True,unique=False,default='N/A')
	ResourceDept = models.CharField("resource dept",max_length=100,null=True,unique=False,default='N/A')
	InvoiceDate = models.DateField(null=True)
	ChargeCode = models.CharField("charge code",max_length=100,null=True,unique=False,default='N/A')
	Quantity = models.FloatField("quantity",null=True,unique=False) 
	Rate = models.FloatField("rate",null=True,unique=False) 
	Total = models.FloatField("total",null=True,unique=False) 
	Client = models.CharField("client",max_length=50,null=True,unique=False,default='N/A')
	StaffID = models.CharField("staff id",max_length=50,null=True,unique=False,default='N/A')
	last_update = models.DateField(null=True)
	backup_index = models.IntegerField(null=True,unique=False)

class Retail_InvoiceID(models.Model):
	id = models.AutoField(primary_key=True)
	InvoiceReference = models.CharField("invoice ref",max_length=50,null=True,unique=False,default='N/A')
	Customer = models.CharField("customer",max_length=50,null=True,unique=False,default='N/A')
	InvoiceDate = models.DateField(null=True)
	Paid = models.BooleanField("paid",unique=False,null=True,default=True)
	Client = models.CharField("client",max_length=50,null=True,unique=False,default='N/A')
	last_update = models.DateField(null=True)
	backup_index = models.IntegerField(null=True,unique=False)

class Retail_Materials(models.Model):
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
	backup_index = models.IntegerField(null=True,unique=False)
     
class Retail_Orders(models.Model):
	id = models.AutoField(primary_key=True)
	CustomerID = models.CharField("CustomerID",max_length=50,null=True,unique=False,default='N/A')
	SalesAssociateID = models.CharField("SalesAssociateID",max_length=50,null=True,unique=False,default='N/A')
	OrderDate = models.DateField(null=True)
	ItemName = models.CharField("ItemName",max_length=50,null=True,unique=False,default='N/A')
	ItemDescription = models.CharField("ItemDescription",max_length=255,null=True,unique=False,default='N/A')
	InventoryID = models.CharField("InventoryID",max_length=100,null=True,unique=False,default='N/A')
	Quantity = models.IntegerField(null=True,unique=False)
	ItemCharge = models.DecimalField("ItemCharge",max_digits=10, decimal_places=2,null=True,unique=False) 
	ShippingCharge = models.DecimalField("ShippingCharge",max_digits=10, decimal_places=2,null=True,unique=False) 
	SalesTax = models.DecimalField("retail cost",max_digits=10, decimal_places=2,null=True,unique=False) 
	CustomerType = models.CharField("CustomerType",max_length=50,null=True,unique=False,default='N/A')
	TransationID = models.CharField("TransationID",max_length=50,null=True,unique=False,default='N/A')
	Location = models.CharField("Location",max_length=150,null=True,unique=False,default='N/A')
	TaxID = models.CharField("TaxID",max_length=50,null=True,unique=False,default='N/A')
	ItemCost = models.DecimalField("ItemCost",max_digits=10, decimal_places=2,null=True,unique=False) 
	MarkupPercent = models.DecimalField("MarkupPercent",max_digits=10, decimal_places=2,null=True,unique=False) 
	LocalSalesTax = models.DecimalField("LocalSalesTax",max_digits=10, decimal_places=2,null=True,unique=False) 
	ItemDiscount = models.DecimalField("ItemDiscount",max_digits=10, decimal_places=2,null=True,unique=False) 
	TotalDiscount = models.DecimalField("TotalDiscount",max_digits=10, decimal_places=2,null=True,unique=False) 
	Deposit = models.DecimalField("Deposit",null=True,max_digits=10, decimal_places=2,unique=False) 
	Client = models.CharField("Client",max_length=50,null=True,unique=False,default='N/A')
	last_update = models.DateField(null=True)
	backup_index = models.IntegerField(null=True,unique=False)
    
class Retail_PO(models.Model):
	id = models.AutoField(primary_key=True)
	VendorID = models.CharField("VendorID",max_length=50,null=True,unique=False,default='N/A') 
	MaterialType = models.CharField("MaterialType",max_length=255,null=True,unique=False,default='N/A')
	Color = models.CharField("Color",max_length=50,null=True,unique=False,default='N/A') 
	Material = models.CharField("Material",max_length=50,null=True,unique=False,default='N/A') 
	MaterialSize = models.CharField("MaterialSize",max_length=50,null=True,unique=False,default='N/A') 
	Cost = models.CharField("Cost",max_length=50,null=True,unique=False,default='N/A') 
	Total = models.CharField("Total",max_length=50,null=True,unique=False,default='N/A') 
	PurchaseOrderID = models.CharField("PurchaseOrderID",max_length=50,null=True,unique=False,default='N/A') 
	Client = models.CharField("ItemDescription",max_length=50,null=True,unique=False,default='N/A')
	last_update = models.DateField(null=True)
	Retail_backup_index = models.IntegerField(null=True,unique=False)
    
class Retail_POID(models.Model):
	id = models.AutoField(primary_key=True)
	VendorID = models.CharField("VendorID",max_length=50,null=True,unique=False,default='N/A')
	PODate = models.DateField(null=True)
	Client = models.CharField("client",max_length=50,null=True,unique=False,default='N/A')
	last_update = models.DateField(null=True)   
	backup_index = models.IntegerField(null=True,unique=False)	
   
class Retail_Quote(models.Model):
	id = models.AutoField(primary_key=True)
	InvoiceID = models.IntegerField(null=True,unique=False)
	ResourceID = models.IntegerField(null=True,unique=False)
	CustomerID = models.IntegerField(null=True,unique=False)
	ResourceName = models.CharField("resource name",max_length=100,null=True,unique=False,default='N/A')
	ResourceType = models.CharField("resource type",max_length=100,null=True,unique=False,default='N/A')
	ResourceDept = models.CharField("resource dept",max_length=100,null=True,unique=False,default='N/A')
	InvoiceDate = models.DateField(null=True)
	ChargeCode = models.CharField("charge code",max_length=100,null=True,unique=False,default='N/A')
	Quantity = models.FloatField("quantity",null=True,unique=False) 
	Rate = models.FloatField("rate",null=True,unique=False) 
	Total = models.FloatField("total",null=True,unique=False) 
	Client = models.CharField("client",max_length=50,null=True,unique=False,default='N/A')
	StaffID = models.CharField("staff id",max_length=50,null=True,unique=False,default='N/A')
	last_update = models.DateField(null=True)  
	backup_index = models.IntegerField(null=True,unique=False)

class Retail_QuoteID(models.Model):
    id = models.AutoField(primary_key=True)
    InvoiceReference = models.CharField("invoice ref",max_length=50,null=True,unique=False,default='N/A')
    Customer = models.CharField("customer",max_length=50,null=True,unique=False,default='N/A')
    InvoiceDate = models.DateField(null=True)
    Paid = models.BooleanField("paid",unique=False,null=True,default=True)
    Client = models.CharField("client",max_length=50,null=True,unique=False,default='N/A')
    last_update = models.DateField(null=True)   
    backup_index = models.IntegerField(null=True,unique=False)
	
class Retail_SalesTransation(models.Model):
	id = models.AutoField(primary_key=True)
	CustomerID = models.IntegerField(null=True,unique=False)
	SalesAssociateID = models.IntegerField(null=True,unique=False)
	Location = models.CharField("VendorID",max_length=50,null=True,unique=False,default='N/A')
	SaleDate = models.DateField(null=True)
	Client = models.CharField("client",max_length=50,null=True,unique=False,default='N/A')
	last_update = models.DateField(null=True) 
	backup_index = models.IntegerField(null=True,unique=False)
	
class Retail_Vendors(models.Model):
	id = models.AutoField(primary_key=True)
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
	backup_index = models.IntegerField(null=True,unique=False)

class Retail_ZipCode(models.Model):
	id = models.AutoField(primary_key=True)
	ZipCode = models.CharField("ZipCode",max_length=50,null=True,unique=False,default='N/A')
	PlaceName = models.CharField("PlaceName",max_length=50,null=True,unique=False,default='N/A')
	StateAbreviation = models.CharField("StateAbreviation",max_length=50,null=True,unique=False,default='N/A')
	County = models.CharField("County",max_length=50,null=True,unique=False,default='N/A')
	Latitude = models.CharField("Latitude",max_length=50,null=True,unique=False,default='N/A')
	Longitude = models.CharField("Longitude",max_length=50,null=True,unique=False,default='N/A')
	StateTax = models.DecimalField("StateTax",max_digits=10, decimal_places=2,null=True,unique=False)
	LocalTax = models.DecimalField("LocalTax",max_digits=10, decimal_places=2,null=True,unique=False)
	TotalTax = models.DecimalField("TotalTax",max_digits=10, decimal_places=2,null=True,unique=False)
	FiscalDate = models.DateField(null=True) 
	
 
    
    
    
    
    
    
    
    














    