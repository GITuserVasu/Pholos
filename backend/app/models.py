from django.db import models
from django.utils import timezone
#from django.contrib.gis.db import models

# Create your models here

class whole_data(models.Model):
    id = models.BigAutoField(primary_key=True)
    case_id = models.CharField(max_length=255,null=True)
    data = models.TextField(null=True)
    fileName = models.CharField(max_length=255,null=True)
    orgid = models.CharField(max_length=255,null=True)

class Case_Detiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=255,null=True)
    fileName = models.CharField(max_length=255,null=True)
    XfileName = models.CharField(max_length=255,null=True)
    CULfileName = models.CharField(max_length=255,null=True)
    orgid = models.CharField(max_length=255,null=True)
    username = models.CharField(max_length=255,null=True)
    projectType = models.CharField(max_length=255,null=True)
    projectName = models.CharField(max_length=255,null=True)
    folderType = models.CharField(max_length=255,null=True)
    folderName = models.CharField(max_length=255,null=True)
    ocrType = models.CharField(max_length=255,null=True)
    targetfiles = models.CharField(max_length=255,null=True)
    CreatedDate = models.DateTimeField(default=timezone.now)
    empOrgid = models.CharField(max_length=255, null=True)
    searchtextwords = models.CharField(max_length=255, blank=True)
    selectedholosproduct = models.CharField(max_length=255, blank=True)
    nyers = models.CharField(max_length=255, blank=True)
    subblocksize = models.CharField(max_length=255, blank=True)
    analogyear = models.CharField(max_length=255, blank=True)
    plantdensity = models.CharField(max_length=255, blank=True)
    plantingmethod = models.CharField(max_length=255, blank=True)
    farmid = models.CharField(max_length=255, blank=True)
    farmname = models.CharField(max_length=255, blank=True)
    plantingdate = models.CharField(max_length=255, blank=True)
    class Meta:
      get_latest_by = 'id'
class Registration(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True)
    email = models.CharField(max_length=255,null=True)
    password = models.CharField(max_length=255,null=True)
    bName = models.CharField(max_length=255,null=True)
    city = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=255,null=True)
    country = models.CharField(max_length=255,null=True)
    domain = models.CharField(max_length=255,null=True)
    orgid = models.CharField(max_length=255,null=True)
    packegStatus = models.CharField(max_length=255,null=True)
    CreatedDate = models.DateTimeField(default=timezone.now)
class file_details(models.Model):
    id = models.BigAutoField(primary_key=True)
    filename = models.CharField(max_length=255,null=True)
    filetype = models.CharField(max_length=255,null=True)
    orgid = models.CharField(max_length=255,null=True)
    userid = models.CharField(max_length=255,null=True)
class Set_project_detils(models.Model):
    id = models.BigAutoField(primary_key=True)
    setProjectName = models.CharField(max_length=255,null=True)
    type = models.CharField(max_length=255,null=True)
    orgid = models.CharField(max_length=255,null=True)
class Set_folder_detils(models.Model):
    id = models.BigAutoField(primary_key=True)
    setFolderName = models.CharField(max_length=255,null=True)
    type = models.CharField(max_length=255,null=True)
    project_name = models.CharField(max_length=255,null=True)
    project_type = models.CharField(max_length=255,null=True)
    orgid = models.CharField(max_length=255,null=True)
class summary_details(models.Model):
    id = models.BigAutoField(primary_key=True)
    case_id = models.CharField(max_length=255,null=True)
    summary = models.TextField(max_length=255,null=True)
    orgid = models.CharField(max_length=255,null=True)
    nltksumm = models.TextField(max_length=255,null=True)
    googleT5summ = models.TextField(max_length=255,null=True)
class pdf_table_data(models.Model):
    id = models.BigAutoField(primary_key=True)
    case_id = models.CharField(max_length=255,null=True)
    summary = models.TextField(max_length=255,null=True)
    orgid = models.CharField(max_length=255,null=True)
class contact_form(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True)
    email = models.CharField(max_length=255,null=True)
    msg = models.TextField(max_length=255,null=True)
class TextractJob(models.Model):
    file = models.CharField(max_length=255, blank=True)
    job_id = models.CharField(max_length=255, blank=True)
    caseid = models.CharField(max_length=255, blank=True)
    orgid = models.CharField(max_length=255, blank=True)
    s3loc = models.CharField(max_length=255, blank=True)
    csvpath = models.CharField(max_length=255, blank=True)
    text = models.TextField(max_length=255,null=True)
    key_values = models.TextField(max_length=255,null=True)
    job_id_string = models.TextField(max_length=255,null=True)
    job_status = models.CharField(max_length=255,null=True)
    search_results = models.TextField(max_length=255,null=True)
class pdfcount_details(models.Model):
    id = models.BigAutoField(primary_key=True)
    pages = models.BigIntegerField(default = 0)
    document = models.BigIntegerField(default = 0)
    orgid = models.CharField(max_length=255,null=True)
    class Meta:
      get_latest_by = 'id'

class EmpRegistration(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True)
    email = models.CharField(max_length=255,null=True)
    password = models.TextField(max_length=255,null=True)
    orgid = models.CharField(max_length=255,null=True)
    empOrgid = models.CharField(max_length=255,null=True)
    status = models.CharField(max_length=255,null=True)
    CreatedDate = models.DateTimeField(default=timezone.now)
    # packegStatus = models.CharField(max_length=255,null=True)
    class Meta:
      get_latest_by = 'id'

class AppCodes(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=255,null=True)
    code = models.CharField(max_length=255,null=True)
    description = models.CharField(max_length=255,null=True)
    location = models.TextField(max_length=255,null=True)

class UseCases(models.Model):
    id = models.BigAutoField(primary_key=True)
    industry = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=255,null=True)
    userPersona = models.CharField(max_length=255,null=True)
    process = models.CharField(max_length=255,null=True)
    description = models.TextField(max_length=255,null=True)
    processDiagram = models.CharField(max_length=255,null=True)
    input = models.CharField(max_length=255,null=True)
    sampleInput = models.CharField(max_length=255,null=True)
    output = models.CharField(max_length=255,null=True)
    sampleOutput = models.CharField(max_length=255,null=True)
    videoLink = models.CharField(max_length=255,null=True)
    otherLink = models.CharField(max_length=255,null=True)
    otherCollateral = models.CharField(max_length=255,null=True)

class SearchWords(models.Model):
    id = models.BigAutoField(primary_key=True)
    userid = models.CharField(max_length=255,null=True)
    useremail = models.CharField(max_length=255,null=True)
    project = models.CharField(max_length=255,null=True)
    orgid = models.CharField(max_length=255,null=True)
    empOrgid = models.CharField(max_length=255,null=True)
    folder = models.CharField(max_length=255,null=True)
    searchtitle = models.CharField(max_length=255,null=True)
    searchwords = models.CharField(max_length=255,null=True)
    searchtitlewords = models.CharField(max_length=255,null=True)

class farm_details(models.Model):
    id = models.BigAutoField(primary_key=True)
    farmname = models.CharField(max_length=255,null=True)
    farmdesc = models.TextField(max_length=255,null=True)
    orgid = models.CharField(max_length=255,null=True)
    userid = models.CharField(max_length=255,null=True)
    polygon_coords = models.TextField(max_length=255,null=True)
    farmarea = models.BigIntegerField(default = 0)
    #polygon_coordinates = models.PolygonField(srid=4326, null=True, default = None)

class all_results(models.Model):
    id = models.BigAutoField(primary_key=True)
    orgid = models.CharField(max_length=255,null=True)
    username = models.CharField(max_length=255,null=True)
    projectname = models.CharField(max_length=255,null=True)
    caseid = models.CharField(max_length=255,null=True)
    filetype = models.CharField(max_length=255,null=True)
    fileext = models.CharField(max_length=255,null=True)
    filename = models.CharField(max_length=255,null=True)
    files3loc = models.CharField(max_length=255,null=True)
    reco = models.TextField(max_length=255,null=True)
   