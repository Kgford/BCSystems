def load_csv(delete):
    #~~~~~~~~~~~Load equpment database from csv."
    import csv
    timestamp  = date.today()
    CSV_PATH = 'models.csv'
    print('csv = ',CSV_PATH)

    contSuccess = 0
    # Remove all data from Table
    if delete:
        Model.objects.all().delete()

    f = open(CSV_PATH)
    timestamp  = date.today()
    reader = csv.reader(f)
    print('reader = ',reader)
    for description, category, band, vendor, model,  status, last_update in reader:
        Model.objects.create(description=description, category=category, band=band, model=model,vendor=vendor,status=status,last_update=timestamp)
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')
  