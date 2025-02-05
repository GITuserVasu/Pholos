import csv
from http.client import HTTPResponse
import os
import requests
import json
from django.http import HttpResponse

#import pytesseract
from PyPDF2 import PdfFileReader
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from app.models import (
    file_details,
    Case_Detiles,
    Set_folder_detils,
    contact_form,
    summary_details,
    whole_data,
    Registration,
    Set_project_detils,
    pdf_table_data,
    pdfcount_details,
    SearchWords,
    farm_details,
    all_results,
)
from app.serilizer import (
    farm_details_serializers,
    file_details_serializers,
    Case_Detiles_serializers,
    Set_folder_detils_serializers,
    pdf_table_data_serializers,
    summary_detils_serializers,
    whole_data_serializers,
    Registration_serializers,
    Set_project_detils_serializers,
    contact_form_serializers,
    Pdfinfo_details_serializers,
    SearchWords_serializers,
    all_results_serializers,
)
from .functions import handle_uploaded_file
from django.http import JsonResponse
from pdf2image import convert_from_path
from pdf2image import pdfinfo_from_path
from PIL import Image
import subprocess
#import tabula
from tabulate import tabulate
import boto3
from trp import Document
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMultiAlternatives

#from django.contrib.gis.geos import GEOSGeometry

# Create your views here.

#########
""" @csrf_exempt
def prednow(predjson):
    print("In prednow")
    #reportfile = open_reporting_session("","")
    return JsonResponse({"statusCode": 200, "name": "test"}) """
#####


# create s3 bucket n
boto3.setup_default_session(profile_name='holos')
s3session = boto3.Session(profile_name='holos')
s5 = s3session.client('s3')
#s3 = boto3.client("s3", region_name='us-east-1')
s3 = boto3.client("s3", region_name='us-east-2')
#bucket_name = "ocrnlp"
#bucket_name = "user-holos"
bucket_name = "docker-holos-spatial-dssat-trigger-bucket"

# poppler_path_manual = 'C:/Users/Manikanta/Downloads/poppler-0.68.0_x86 (1)/poppler-0.68.0_x86 (1)/poppler-0.68.0/bin'
# tesseract_cmd_path = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
# tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'

poppler_path_manual = "/usr/bin"
tesseract_cmd_path = "/usr/bin/tesseract"
tessdata_dir_config = '--tessdata-dir "/usr/share/tesseract-ocr/4.00/tessdata"'

FilePath = "/var/www/html/devholos/assets/temp"
# FilePath = settings.MEDIA_ROOT
ImgPath = "/var/www/html/ocrApp/assets/temp/images"
# ImgPath = settings.MEDIA_ROOT+'/uplodedFiles/apiImages/'

@csrf_exempt
def make_json(exptJson):
    print("In Make JSON")
    nuline = ""
    comma = ","
    jsondata = JSONParser().parse(exptJson)
    companyID = jsondata["companyID"]
    name = jsondata["UserName"]
    name = name.replace(" ","")
    useremail = jsondata["UserEmailID"]
    simulationname = jsondata["SimulationName"]
    projectname = jsondata["SimulationName"]
    selectedholosproduct = jsondata["SelectedHolosProduct"]
    Xfile_as_string = jsondata["Xfile_as_string"]
    #print("Xfile", Xfile_as_string)
    CULfile_as_string = jsondata["CULfile_as_string"]
    #print("CULfile", CULfile_as_string)
    roiname = jsondata["roiname"]
    subblocksize = str(jsondata["subblocksize"])
    nyers = jsondata["nyers"]
    analogousweatheryear = jsondata["analogyear"]
    tpyear = str(jsondata["tpyear"])
    tpmonth = str(jsondata["tpmonth"])
    tpday = str(jsondata["tpday"])
    planting_method = str(jsondata["plantingmethod"])
    density_plantspersqm = jsondata["plantdensity"]
    baseXfilename = jsondata["Xfilename"]
    CULfilename = jsondata["CULfilename"]
    farm_existing_new = jsondata["farm_existing_new"]
    farmid = jsondata["farmid"]
    X_existing_new = jsondata["X_existing_new"]
    #Xfileid = jsondata["Xfileid"]
    CUL_existing_new = jsondata["CUL_existing_new"]
    #CULfileid = jsondata["CULfileid"]
    ccatmco2 = jsondata["ccatmco2"]
    ccperiod = jsondata["ccperiod"]
    ccmodel = jsondata["ccmodel"]
    ccscenario = jsondata["ccscenario"]
    city = jsondata["city"]
    state = jsondata["state"]
    country = jsondata["country"]

    
    json_version_num = "4.1"

    Xfile_content6 = ""
    if X_existing_new == "existing":
        print("X_existing_new", X_existing_new)
        Xpath = companyID+"/"+name+"/Xfiles/"+baseXfilename
        print(Xpath)
        print(bucket_name)
        try:
            # Download the file from S3
            response = s3.get_object(Bucket=bucket_name, Key=Xpath)

            # Get the file content
            Xfile_content = response['Body'].read()
            Xfile_content0 = str(Xfile_content)
            Xfile_content1 = Xfile_content0.lstrip("b")
            Xfile_content2 = Xfile_content1.lstrip("'")
            Xfile_content3 = Xfile_content2.rstrip("'")
            Xfile_content4 = Xfile_content3.replace("\\r\\n", "\n")
            #print( "Xfile without the \r\n", Xfile_content4)
            Xfile_content5 = Xfile_content4.replace("\n","\\n")
            Xfile_content6 = Xfile_content5.replace("\\x1a","\\u001a")
            #print( "Xfile without the \x1a", Xfile_content6)
            #print(Xfile_content0)
            Xfile_as_string = Xfile_content6
        except Exception as e:
           # Handle any exceptions that may occur during the download
           print("Error in downloading file")
        
        
    CULfile_content4 = ""
    if CUL_existing_new == "existing":
        print(CUL_existing_new)
        CULpath = companyID+"/"+name+"/CULfiles/"+CULfilename
        print(CULpath)
        try:
            # Download the file from S3
            response = s3.get_object(Bucket=bucket_name, Key=CULpath)

            # Get the file content
            CULfile_content = response['Body'].read()
            CULfile_content0 = str(CULfile_content)
            CULfile_content1 = CULfile_content0.lstrip("b")
            CULfile_content2 = CULfile_content1.lstrip("'")
            CULfile_content3 = CULfile_content2.rstrip("'")
            CULfile_content4 = CULfile_content3.replace("\\r", "")
            CULfile_content5 = CULfile_content4.replace("\n","\\n")
            """print(CULfile_content3) """
            CULfile_as_string = CULfile_content5
        except Exception as e:
           # Handle any exceptions that may occur during the download
           print("Error in downloading file")
        
        

    if farm_existing_new == "new":
        origcoordinates = jsondata["Coordinates"]
        coordinates = json.loads(origcoordinates)
    if farm_existing_new == "existing":
        print(farm_existing_new)
        try:
           farm_record = farm_details.objects.get(id=farmid )
        except farm_details.DoesNotExist:
           print("Error in getting farm details")
        origcoordinates = farm_record.polygon_coords
        coordinates = json.loads(origcoordinates)
        print(coordinates)
    # for points in coordinates:
    num_vertices = len(coordinates[0]) -1
    print("num vertices", num_vertices)

    rows = num_vertices + 1 # number of vertices in the polygon
    cols = 2
    coord_array=[[0 for i in range(cols)] for j in range(rows)]
    i = -1
    for list in coordinates:
        #  list.pop(num_vertices)
        for item in list:
            j = 0
            i = i + 1
            for newitem in item:
                coord_array[i][j] = str(newitem)
                print(coord_array[i][j])
                j = j + 1
    
    

    print("In make json")
    print(name, useremail,simulationname, selectedholosproduct)

    json_string = ""
    json_string = json_string + "{"
    json_string = json_string + '"UserID"'+":"
    json_string = json_string + '"' + name +'"'+ comma + nuline
    json_string = json_string + '"_comment"'+":"+ '"CompanyID will be autogenerated; for testing using 999"' + comma + nuline
    json_string = json_string + '"CompanyID"' +":"
    json_string = json_string + '"'+companyID+'"' + comma + nuline
    json_string = json_string + '"ProjectName"' +":"
    json_string = json_string + '"'+projectname+'"' + comma + nuline
    json_string = json_string + '"Blocks"'+": [{"
    json_string = json_string + '"Name"' +":"
    json_string = json_string + '"'+projectname+'"' + comma + nuline
    json_string = json_string + '"Country"' +":"
    json_string = json_string + '"'+country+'"' + comma + nuline
    json_string = json_string + '"State"' +":"
    json_string = json_string + '"'+state+'"' + comma + nuline
    json_string = json_string + '"SelectedHolosProducts"'+":"
    json_string = json_string + "["+'"'+selectedholosproduct+'"'+"]" + comma + nuline
    json_string = json_string + '"_comment"'+":"+ '"*NEW* Array of ROIs, each ROI contains Holos prod info, config of ROI, farming practices, grouping of ROIs (optional), mapping of ROIs or ROI groups to farming practices"'+comma+ nuline
    json_string = json_string + '"ROIs"'+": [{"
    json_string = json_string + '"_comment"'+":"+ '"*NEW* ROI Is New"'+comma + nuline
    json_string = json_string + '"ROIName"'+":"
    json_string = json_string + '"'+roiname+'"' + comma + nuline
    json_string = json_string + '"ROIConfiguration"'+": {"
    json_string = json_string + '"_comment"'+":"+ '"Sample geoJSON - Coimbatore"'+comma + nuline
    json_string = json_string + '"geoJSON"'+": {"
    json_string = json_string + '"type"'+":"+ '"FeatureCollection"'+comma
    json_string = json_string + '"features"'+": [{"
    json_string = json_string + '"type"'+":" + '"Feature"'+ comma
    json_string = json_string + '"geometry"'+": {"
    json_string = json_string + '"type"'+":" + '"Polygon"'+ comma + nuline
    json_string = json_string + '"coordinates"' + ":" +" [[" + nuline
    for i in range(rows):
        if (i == rows-1):
          json_string = json_string + "["+  coord_array[i][0] +   comma +  coord_array[i][1] +"]"
        else: 
          json_string = json_string + "["+  coord_array[i][0] +   comma +  coord_array[i][1] +"]" + comma + nuline
    """ json_string = json_string + "["+ '"' + coord_array[0][0] + '"' +  comma + '"'+ coord_array[0][1]+'"' +"]" + comma + nuline
    json_string = json_string + "["+ '"' + coord_array[1][0] + '"' +  comma + '"'+ coord_array[1][1]+'"'  +"]" + comma + nuline
    json_string = json_string + "["+ '"' + coord_array[2][0] + '"' +  comma + '"'+ coord_array[2][1]+'"'  +"]" + comma + nuline
    json_string = json_string + "["+ '"' + coord_array[3][0] + '"' +  comma + '"'+ coord_array[3][1]+'"'  +"]" + comma + nuline
    json_string = json_string + "["+ '"' + coord_array[4][0] + '"' +  comma + '"'+ coord_array[4][1]+'"'  +"]" + comma + nuline
    json_string = json_string + "["+ '"' + coord_array[5][0] + '"' +  comma + '"'+ coord_array[5][1]+'"'  +"]" + comma + nuline
    json_string = json_string + "["+ '"' + coord_array[6][0] + '"' +  comma + '"'+ coord_array[6][1]+'"'  +"]" + comma + nuline
    json_string = json_string + "["+ '"' + coord_array[7][0] + '"' +  comma + '"'+ coord_array[7][1]+'"'  +"]" """ 
    json_string = json_string + "]]}" + comma
    json_string = json_string + '"properties"' + ":" + '"null"'+comma + nuline
    json_string = json_string + '"id"'+":" +  '"Coimbatore,TamilNadu"' 
    json_string = json_string + "}]}," + nuline
    json_string = json_string + '"SubBlockSize"' +":"
    json_string = json_string +  subblocksize  
    json_string = json_string + "}}]," + nuline
    json_string = json_string + '"HolosProductParams"' + ": [{"
    json_string = json_string + '"'+ selectedholosproduct+'"' +": {"
    if selectedholosproduct == "PRSEASON":
        json_string = json_string + '"NYERS"' +":" 
        json_string = json_string + nyers  + comma + nuline
        json_string = json_string + '"AnalogousWeatherYear"' + ":"
        json_string = json_string +  analogousweatheryear
    if selectedholosproduct == "CLIMCHNG":
        if ccperiod == "baseline":
             json_string = json_string + '"FromYear"' +": 1991" +comma + nuline
             json_string = json_string + '"ToYear"' +": 2020" +comma + nuline
             json_string = json_string + '"WeatherSource"'+":{" + nuline
             json_string = json_string + '"Repo"'+":"+'"NASA"' + nuline
             json_string = json_string + "}" + comma + nuline
             json_string = json_string + '"AtmosCO2"' + ": " + ccatmco2 + nuline
        if ccperiod == "near":
             json_string = json_string + '"FromYear"' +": 2021" +comma + nuline
             json_string = json_string + '"ToYear"' +": 2050" +comma + nuline
             json_string = json_string + '"WeatherSource"'+":{" + nuline
             json_string = json_string + '"Repo"'+":"+'"CMIP6"' + comma + nuline
             json_string = json_string + '"Model"' + ":" + '"'+ ccmodel +'"'+comma + nuline
             json_string = json_string + '"GHGScenarios"'+": " +'"' + ccscenario +'"' + nuline
             json_string = json_string + "}" + comma + nuline
             json_string = json_string + '"AtmosCO2"' + ": " + ccatmco2 + nuline
        if ccperiod == "mid":
             json_string = json_string + '"FromYear"' +": 2051" +comma + nuline
             json_string = json_string + '"ToYear"' +": 2080" +comma + nuline
             json_string = json_string + '"WeatherSource"'+":{" + nuline
             json_string = json_string + '"Repo"'+":"+'"CMIP6"' + comma + nuline
             json_string = json_string + '"Model"' + ":" + '"'+ ccmodel +'"'+comma + nuline
             json_string = json_string + '"GHGScenarios"'+": " +'"' + ccscenario +'"' +  nuline
             json_string = json_string + "}" + comma + nuline
             json_string = json_string + '"AtmosCO2"' + ": " + ccatmco2 + nuline
    
    

    json_string = json_string + "}}]," + nuline
    json_string = json_string + '"CommonParams"'+": {"
    json_string = json_string + '"TargetPlantingYear"'+":"
    json_string = json_string + tpyear + comma + nuline
    json_string = json_string + '"TargetPlantingMonth"'+":"
    json_string = json_string + tpmonth + comma + nuline
    json_string = json_string + '"TargetPlantingDay"' + ": "
    json_string = json_string + tpday + comma + nuline
    json_string = json_string + '"_comment"'+":" + '"*NEW* PlantingMethod and Density_PlantsPerSqM Are New"'+comma + nuline
    json_string = json_string + '"PlantingMethod"' +": "
    json_string = json_string + '"' + planting_method +'"' + comma + nuline
    json_string = json_string + '"Density_PlantsPerSqM"' +":"
    json_string = json_string + density_plantspersqm + comma + nuline
    json_string = json_string + '"BaseXFileName"' +": "
    json_string = json_string + '"'+baseXfilename+'"' + comma + nuline
    json_string = json_string + nuline + '"BaseCul"' +": "
    json_string = json_string + '"' + CULfile_as_string + '"' + comma
    json_string = json_string + '"BaseX"' + ": "
    # json_string = json_string + '"'+"*" +"EXP.DETAILS: Historical X file compliant w DSSAT, for two years, starting 2021  *GENERAL @PEOPLE Geetha&Bhuvana @ADDRESS TNAU @SITE Tanjore  *TREATMENTS                        -------------FACTOR LEVELS------------ @N R O C TNAME.................... CU FL SA IC MP MI MF MR MC MT ME MH SM  1 1 1 0 Tanjavur                   1  1  0  1  1  1  1  0  0  0  0  0  1  2 1 1 0 Tanjavur                   2  1  0  1  1  1  1  0  0  0  0  0  1  3 1 1 0 Tanjavur                   3  1  0  1  1  1  1  0  0  0  0  0  1  4 1 1 0 Tanjavur                   4  1  0  1  1  1  1  0  0  0  0  0  1  5 1 1 0 Tanjavur                   5  1  0  1  1  1  1  0  0  0  0  0  1  *CULTIVARS @C CR INGENO CNAME  1 RI IB0036 BPT5204  2 RI IB0803 ADT45  3 RI IB0806 CO51  4 RI IB0802 ASD16  5 RI IB0805 ADT36  *FIELDS @L ID_FIELD WSTA....  FLSA  FLOB  FLDT  FLDD  FLDS  FLST SLTX  SLDP  ID_SOIL    FLNAME  1 CDZT2201 TNJR8141   -99   -99 DR000   -99   -99   -99 CL     -99  IN04042298 test1 @L ...........XCRD ...........YCRD .....ELEV .............AREA .SLEN .FLWR .SLAS FLHST FHDUR  1             -99             -99       -99               -99   -99   -99   -99   -99   -99  *INITIAL CONDITIONS @C   PCR ICDAT  ICRT  ICND  ICRN  ICRE  ICWD ICRES ICREN ICREP ICRIP ICRID ICNAME  1    RI 21255   -99   -99     1     1   -99   -99   -99   -99   -99   -99 ini1 @C  ICBL  SH2O  SNH4  SNO3  1    10  .301    .2   1.3  1    30  .354    .2   1.3  1    80  .375    .2   1.3  1   100  .418    .2   1.3  1   150   .43    .2   1.3  1   200  .453    .2   1.3  *PLANTING DETAILS @P PDATE EDATE  PPOP  PPOE  PLME  PLDS  PLRS  PLRD  PLDP  PLWT  PAGE  PENV  PLPH  SPRL                        PLNAME  1 21263 21268    33    33     T     H    20    90     3   -99    21    24     3   -99                        Sep21  *IRRIGATION AND WATER MANAGEMENT @I  EFIR  IDEP  ITHR  IEPT  IOFF  IAME  IAMT IRNAME  1     1    30    50   100 GS000 IR001    10 -99 @I IDATE  IROP IRVAL  1     1 IR009   100  1     1 IR008     1  1     1 IR006    25  1     3 IR006    25  1     6 IR006    25  1     9 IR006    25  1    12 IR006    25  1    16 IR006    25  1    20 IR006    25  1    24 IR006    50  1    28 IR006    50  1    32 IR006    50  1    36 IR006    50  1    40 IR006    50  1    44 IR006    50  1    48 IR006    50  1    52 IR006    50  1    54 IR006    50  1    56 IR006    50  1    60 IR006    50  1    64 IR006    50  1    68 IR006    50  1    72 IR006    50  1    76 IR006    50  1    80 IR006    50  1    84 IR006    50  1    88 IR006    50  *FERTILIZERS (INORGANIC) @F FDATE  FMCD  FACD  FDEP  FAMN  FAMP  FAMK  FAMC  FAMO  FOCD FERNAME  1     1 FE005 AP016     1    38     0   -99   -99   -99   -99 ferti  1    35 FE005 AP015     1    38     0   -99   -99   -99   -99 ferti  1    65 FE005 AP015     1    38     0   -99   -99   -99   -99 ferti  1    95 FE005 AP014     1    38     0   -99   -99   -99   -99 ferti  *RESIDUES AND ORGANIC FERTILIZER @R RDATE  RCOD  RAMT  RESN  RESP  RESK  RINP  RDEP  RMET RENAME  1     0 RE003  6000    .5   .25    .5    70     4 AP012 ORGANIC1  *TILLAGE AND ROTATIONS @T TDATE TIMPL  TDEP TNAME  1 21173   -99   -99 -99  *ENVIRONMENT MODIFICATIONS @E ODATE EDAY  ERAD  EMAX  EMIN  ERAIN ECO2  EDEW  EWIND ENVNAME    1 21141 A   0 M 3.6 A   0 A   0 A 0.0 A   0 A   0 A   0   *HARVEST DETAILS @H HDATE  HSTG  HCOM HSIZE   HPC  HBPC HNAME  1 21173 GS000   -99   -99   -99   -99 Rice  *SIMULATION CONTROLS @N GENERAL     NYERS NREPS START SDATE RSEED SNAME.................... SMODEL  1 GE              2     1     S 21255  2150 DEFAULT SIMULATION CONTR  RICER @N OPTIONS     WATER NITRO SYMBI PHOSP POTAS DISES  CHEM  TILL   CO2  1 OP              Y     Y     Y     N     N     N     N     Y     M @N METHODS     WTHER INCON LIGHT EVAPO INFIL PHOTO HYDRO NSWIT MESOM MESEV MESOL  1 ME              M     M     E     R     S     L     R     1     G     S     2 @N MANAGEMENT  PLANT IRRIG FERTI RESID HARVS  1 MA              R     D     D     D     M @N OUTPUTS     FNAME OVVEW SUMRY FROPT GROUT CAOUT WAOUT NIOUT MIOUT DIOUT VBOSE CHOUT OPOUT FMOPT  1 OU              N     Y     Y     1     Y     Y     Y     Y     Y     N     Y     N     Y     A  @  AUTOMATIC MANAGEMENT @N PLANTING    PFRST PLAST PH2OL PH2OU PH2OD PSTMX PSTMN  1 PL          21244 21263    40   100    30    40    10 @N IRRIGATION  IMDEP ITHRL ITHRU IROFF IMETH IRAMT IREFF  1 IR              5    50   100 GS000 IR006    10    .9 @N NITROGEN    NMDEP NMTHR NAMNT NCODE NAOFF  1 NI             30    50    25 FE001 GS000 @N RESIDUES    RIPCN RTIME RIDEP  1 RE            100     1    20 @N HARVEST     HFRST HLAST HPCNP HPCNR  1 HA              0 20173   100     0   "+'"' + comma + nuline
    json_string = json_string + '"' + Xfile_as_string + '"' 
    #json_string = json_string + nuline + '"BaseCul"' +": "
    #json_string = json_string + '"' +"*" +"RICE GENOTYPE COEFFICIENTS: RICER047 MODEL ! @VAR#  VAR-NAME........ EXPNO   ECO#    P1   P2R    P5   P2O    G1    G2    G3 PHINT  THOT TCLDP TCLDF  !    previous !                                        1     2     3     4     5     6     7     8     9    10    11  !     G4    G5  !Introduce temperature-based factors to replace G4 and G5 990001 IRRI ORIGINALS       . IB0001 880.0  52.0 550.0  12.0  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !   1.00   1.0 990002 IRRI RECENT          . IB0001 450.0 149.0 350.0  11.7  68.0 .0230  1.00  83.0  28.0  15.0  15.0  !   1.00   1.0 990003 JAPANESE             . IB0001 220.0  35.0 510.0  12.0  55.0 .0250  1.00  83.0  28.0  15.0  15.0  !   1.00   1.0 990004 N.AMERICAN           . IB0001 318.0 189.0 550.0  12.8  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !   1.00   1.0 !                                                                                                !@VAR#  VAR-NAME........ EXPNO   ECO#    P1   P2R    P5   P2O    G1    G2    G3    G4 PHINT    G5 !990001 IRRI ORIGINALS       . IB0001 880.0  52.0 550.0  12.0  65.0 .0280  1.00  1.00  83.0   1.0 !990002 IRRI RECENT          . IB0001 450.0 149.0 350.0  11.7  68.0 .0230  1.00  1.00  83.0   1.0 !990003 JAPANESE             . IB0001 220.0  35.0 510.0  12.0  55.0 .0250  1.00  1.00  83.0   1.0 !990004 N.AMERICAN           . IB0001 318.0 189.0 550.0  12.8  65.0 .0280  1.00  1.00  83.0   1.0  !US and JF calibrated parameters. THOT = 28/G4, TCLDP and TCLDF = 15.0*G5  !VAR#  VAR-NAME........ EXPNO   ECO#    P1   P2R    P5   P2O    G1    G2    G3 PHINT  THOT TCLDP TCLDF  !     G4    G5 IB0003 IR 36                . IB0001 556.8 53.88 373.4 12.87 68.00 0.023  1.00 83.00  31.3  15.0  15.0  !  0.895   1.0 IB0012 IR 58                . IB0001 254.8 96.44 378.4 10.63 77.03 0.020  1.00 83.00  33.9  15.0  15.0  !  0.825   1.0 IB0020 RD 23                . IB0001 528.6 156.5 387.4 12.64 52.65 0.022  1.00 83.00  29.0  15.0  15.0  !  0.967   1.0 IB0050 PR114                . IB0001 662.5 184.4 503.0 12.38 62.86 0.023  1.00 83.00  25.7  15.0  15.0  !  1.091   1.0 IB0055 Basmati 385          . IB0001 498.3 130.1 420.0 12.90 74.76 0.022  0.53 83.00  30.9  15.0  15.0  !  0.906   1.0 IB0118 IR 72                . IB0001 437.1 61.02 371.8 11.58 77.80 0.026  1.00 83.00  30.4  15.0  15.0  !  0.921   1.0  !Recalibration by Upendra Singh and Job Fugice 2019-04-25 !!VAR#  VAR-NAME........ EXPNO   ECO#    P1   P2R    P5   P2O    G1    G2    G3    G4 PHINT    G5 !IB0003 IR 36                . IB0001 556.8 53.88 373.4 12.87 68.00 0.023  1.00 0.895 83.00   1.0 !IB0012 IR 58                . IB0001 254.8 96.44 378.4 10.63 77.03 0.020  1.00 0.825 83.00   1.0 !IB0020 RD 23                . IB0001 528.6 156.5 387.4 12.64 52.65 0.022  1.00 0.967 83.00   1.0 !IB0050 PR114                . IB0001 662.5 184.4 503.0 12.38 62.86 0.023  1.00 1.091 83.00   1.0 !IB0055 Basmati 385          . IB0001 498.3 130.1 420.0 12.90 74.76 0.022  0.53 0.906 83.00   1.0 !IB0118 IR 72                . IB0001 437.1 61.02 371.8 11.58 77.80 0.026  1.00 0.921 83.00   1.0  !VAR#  VAR-NAME........ EXPNO   ECO#    P1   P2R    P5   P2O    G1    G2    G3 PHINT  THOT TCLDP TCLDF  !    previous !                                        1     2     3     4     5     6     7     8     9    10    11  !    G4    G5  IB0001 IR 8                 . IB0001 880.0  52.0 550.0  12.1  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0002 IR 20                . IB0001 500.0 166.0 500.0  11.2  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0004 IR 43                . IB0001 720.0 120.0 580.0  10.5  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0005 LABELLE              . IB0001 318.0 189.0 550.0  12.8  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0006 MARS                 . IB0001 698.0 134.0 550.0  13.0  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0007 NOVA 66              . IB0001 389.0 155.0 550.0  11.0  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0008 PETA                 . IB0001 420.0 240.0 550.0  11.3  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0009 STARBONNETT          . IB0001 880.0 164.0 550.0  13.0  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0010 UPLRI5               . IB0001 620.0 160.0 380.0  11.5  50.0 .0220  0.60  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0011 UPLRI7               . IB0001 760.0 150.0 450.0  11.7  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0013 SenTaNi (???)        . IB0001 320.0  50.0 550.0  10.0  70.0 .0300  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0014 IR 54                . IB0001 350.0 125.0 520.0  11.5  60.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0015 IR 64                . IB0001 500.0 160.0 450.0  12.0  60.0 .0250  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0016 IR 60(Est)           . IB0001 490.0 100.0 320.0  11.5  75.0 .0275  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0017 IR 66                . IB0001 500.0  50.0 490.0  12.5  62.0 .0265  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0018 IR 72x               . IB0001 400.0 100.0 580.0  12.0  76.0 .0230  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0019 RD 7 (cal.)          . IB0001 603.3 150.0 452.5  11.2  65.0 .0230  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0021 CICA8                . IB0001 700.0 120.0 360.0  11.7  60.0 .0270  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0022 LOW TEMP.SEN         . IB0001 400.0 120.0 420.0  12.0  60.0 .0250  1.00  83.0  35.0  15.0  15.0  !  0.80   1.0 IB0023 LOW TEMP.TOL         . IB0001 400.0 120.0 420.0  12.0  60.0 .0250  1.00  83.0  22.4  15.0  15.0  !  1.25   1.0 IB0024 17 BR11,T.AMAN       . IB0001 740.0 180.0 400.0  10.5  55.0 .0250  1.00  83.0  31.1  15.0  15.0  !  0.90   1.0 IB0025 18 BR22,T.AMAN       . IB0001 650.0 110.0 400.0  12.0  60.0 .0250  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0026 19 BR 3,T.AMAN       . IB0001 650.0 110.0 420.0  12.0  65.0 .0250  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0027 20 BR 3,BORO         . IB0001 650.0  90.0 400.0  13.0  65.0 .0250  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0029 CPIC8                . IB0001 380.0 150.0 300.0  12.8  38.0 .0210  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0030 LEMONT               . IB0001 500.0  50.0 300.0  12.8  60.0 .0207  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0031 RN12                 . IB0001 380.0  50.0 300.0  12.8  40.0 .0199  1.00  83.0  24.3  15.0  15.0  !  1.15   1.0 IB0032 TW                   . IB0001 360.0  50.0 290.0  12.8  55.0 .0210  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0115 IR 64*               . IB0001 540.0 160.0 490.0  12.0  50.0 .0250  1.10  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0116 HEAT SENSITIVE       . IB0001 460.0   5.0 390.0  13.5  62.0 .0250  1.00  83.0  24.3  15.0  15.0  !  1.15   1.0 IB0117 BR14                 . IB0001 560.0 200.0 500.0  11.5  45.0 .0260  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0119 BR11                 . IB0001 825.0 300.0 390.0  11.5  52.0 .0240  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0120 PANT-4               . IB0001 830.0 160.0 300.0  11.4  45.0 .0300  1.00  83.0  35.0  15.0  15.0  !  0.80   1.0 IB0121 JAYA                 . IB0001 830.0 100.0 200.0  11.4  40.0 .0300  1.00  83.0  35.0  15.0  15.0  !  0.80   1.0 IB0122 BPRI10               . IB0001 740.0 200.0 225.0  13.5  40.0 .0230  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 IB0151 ZHENG DAO 9380       . IB0001 400.0 120.0 420.0  13.0  60.0 .0270  1.00  83.0  24.3  15.0  15.0  !  1.15   1.0 IB0200 CL-448               . IB0001 100.0 120.0 250.0  12.0  40.0 .0250  1.00  83.0  22.4  15.0  15.0  !  1.25   1.0 IB0051 KS-282 CRice         . IB0001 290.0  17.0 490.0  13.0  55.0 .0500  1.00  83.0  40.0  15.0  15.0  !  0.70   1.0 IB0052 Basmati-515 FRice    . IB0001 460.0 120.0 512.0  11.0  37.0 .0210  1.00  75.0  34.0  15.0  15.0  !  1.00   1.0 IB0801 ADT43                . IB0001 483.0  53.5 348.0  12.0  55.8 .0240  1.00  83.0  34.0  15.0  15.0  !  0.89   1.0 IB0803 ADT45                . IB0001 450.0  75.0 355.0  12.0  73.0 .0260  1.00  83.0  34.0  15.0  15.0  !  1.00   1.0 IB0806 CO51                 . IB0001 460.0  78.4 360.3  12.0  64.0 .0250  0.60  83.0  34.0  15.0  15.0  !  0.89   1.0 !IB0806 CO51                 . IB0001 460.0  78.4 360.3  12.0  74.0 .0250  1.00  83.0  34.0  15.0  15.0  !  0.89   1.0 IB0802 ASD16                . IB0001 450.0  69.0 350.0  12.0  73.0 .0280  1.00  83.0  34.0  15.0  15.0  !  1.00   1.0 IB0804 CO(R)50              . IB0001 550.0  85.4 315.3  12.0  43.0 .0200  0.85  83.0  30.0  15.0  15.0  !  0.89   1.0 IB0805 CR-1009              . IB0001 483.0 53.50 348.1 12.00 55.80 0.024  1.00  83.0  34.0  15.0  15.0  !  0.89   1.0 IB0036 BPT5204              . IB0001 990.0  60.0 350.0  12.0  49.0 .0220  1.00  83.0  30.4  15.0  15.0  !  0.89   1.0    !chp added revised cultivars from ATTACHAI JINTRAWET (Thailand) - gave new name   !  starting with MC.                                                              !             A low G3 value put more biomass to tillers, thru TILRAT and         !             TPANIWT variables, meaning that more STMWT is needed.               !VAR#  VAR-NAME........ EXPNO   ECO#    P1   P2R    P5   P2O    G1    G2    G3 PHINT  THOT TCLDP TCLDF  !    previous !                                        1     2     3     4     5     6     7     8     9    10    11  !    G4    G5  MC0020 RD 23                . IB0001 310.3 140.0 370.0  11.2  53.0 .0230  0.30  83.0  28.0  15.0  15.0  !  1.00   1.0 TR0001 KDML105              . IB0001 502.3 123.3 386.5  12.7  45.7 .0270  1.00  83.0  29.5  15.0  15.0  !  0.95   1.0 TR0002 NIEW SANPATONG       . IB0001 495.8 128.3 364.2  12.7  40.7 .0277  0.70  83.0  32.9  15.0  15.0  !  0.85   1.0 TR0003 SUPANBURI 60         . IB0001 540.0 154.7 497.0  11.9  77.7 .0280  1.00  83.0  27.2  15.0  15.0  !  1.03   1.0 TR0004 CHAINAT 1            . IB0001 570.0 122.8 334.8  11.9  63.1 .0278  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0 TR0005 DOA 1                . IB0001 388.5  20.0 381.8  12.0  73.8 .0275  1.10  83.0  24.3  15.0  15.0  !  1.15   1.0  ! The cultivar coefficient G5 was added to CSM-CERES-Rice Version 4.7.5 ! v4.7.7 - remove G4 and G5 and introduce THOT, TCLDP, and TCLDF ! ! COEFF    DEFINITIONS ! ======== =========== ! VAR#     Identification code or number for a specific cultivar. ! VAR-NAME Name of cultivar. ! EXPNO    Number of experiments used to estimate cultivar parameters ! ECO#     Ecotype code for this cultivar points to the Ecotype in the ECO !          file (currently not used).  ! P1       Time period (expressed as growing degree days [GDD] in oC-d above a !          base temperature of 9oC) from seedling emergence during which the !          rice plant is not responsive to changes in photoperiod. This period !          is also referred to as the basic vegetative phase of the plant. !          Range: 150-800 oC-d.  !          Calibration: flexible, compare with observed panicle initiation  !          and flowering dates.  ! P2O      Critical photoperiod or the longest day length (in hours) at !          which the development occurs at a maximum rate. At values higher !          than P2O developmental rate is slowed, hence there is delay due !          to longer day lengths.  !          Range 11-13 h. Default 12 h.  !          Calibration: Do not go below 11 unless data are available.   ! P2R      Extent to which phasic development leading to panicle initiation !          is delayed (expressed as GDD in oC-d) for each hour increase in !          photoperiod above P2O.  !          Range 5-300 oC-d.  !          Calibration: Modern rice varieties will have values in  !          the lower range.  ! P5       Time period in GDD oC-d) from beginning of grain filling (3 to !          4 days after flowering) to physiological maturity with a base !          temperature of 9oC.  !          Range 150-850 oC-d.  !          Calibration: Ensure P1, P2O and P2R are correctly calibrated for  !          anthesis data. Then calibrate P5 for observed maturity date.  ! G1       Potential spikelet number coefficient as estimated from the !          number of spikelets per g of main culm dry weight (less leaf !          blades and sheaths plus spikes) at anthesis.  !          Range 50-75 #/g. A typical value is 55 #/g.  ! G2       Single grain weight (g) under ideal growing conditions, i.e. !          nonlimiting light, water, nutrients, and absence of pests !          and diseases. !          Range 0.015-0.030 g. Default 0.025 g. !          Calibration: Very low flexibility.   ! G3       Tillering coefficient (scalar value) relative to IR64 cultivar !          under ideal conditions.  !          Range 0.7-1.3. !          Calibration: A higher tillering cultivar would have a coefficient  !          greater than 1.0.  ! PHINT    Phyllochron Interval (oC-d). Time interval in degree-days for each  !          leaf-tip to appear under non-stressed conditions.   !          Range 55-90 oC-d. Default 83 oC-d. !          Calibration: Recommend to not change unless field data on leaf  !          numbers are available.  ! THOT     Temperature (oC) above which spikelet sterility is affected by  !          high temperature.   !          Range 25-34 oC. Default 28oC.  !          Calibration: recommended to not change unless hot environment !          data are available. Convert old cultivars THOT = 28./G4.  ! TCLDP    Temperature (oC) below which panicle initiation is further delayed  !          (other than P1, P2O and P2R) by low temperature. !          Range 12-18 oC. Default 15oC.  !          Calibration: recommended to not change unless cold environment !          data are available. Convert old cultivars TCLDP = 15.*G5.  ! TCLDF    Temperature (oC) below which spikelet sterility is affected by  !          low temperature. !          Range 10-20 oC. Default 15oC.  !          Calibration: recommended to not change unless cold environment !          data are available. Convert old cultivars TCLDF = 15.*G5.  " +'"' + nuline
    #json_string = json_string + '"' + CULfile_as_string + '"'
    json_string = json_string + "}}]," + nuline
    json_string = json_string + '"Version"' + ":"
    json_string = json_string + json_version_num + comma + nuline
    json_string = json_string + '"UserEmailID"' +": "
    json_string = json_string + '"'+useremail+'"'
    json_string = json_string + "}"

    
    json_path = "/var/www/html/tmp/json_file"
    with open(json_path, mode='w') as f:
         f.write(json_string)
    
    json_string2 = json.dumps(json_string)

    json_string3 = '{"UserID":"Vasu Vijay","_comment":"CompanyID will be autogenerated; for testing using 999","CompanyID":"191629","ProjectName":"320-test7","Blocks": [{"Name":"320-test7","SelectedHolosProducts":["PRSEASON"],"_comment":"*NEW* Array of ROIs, each ROI contains Holos prod info, config of ROI, farming practices, grouping of ROIs (optional), mapping of ROIs or ROI groups to farming practices","ROIs": [{"_comment":"*NEW* ROI Is New","ROIName":"test","ROIConfiguration": {"_comment":"Sample geoJSON - Coimbatore","geoJSON": {"type":"FeatureCollection","features": [{"type":"Feature","geometry": {"type":"Polygon","coordinates": [[[77.02657421147529,11.051931828419981],[77.02773999274739,11.043349047989182],[77.01812232504696,11.043062949894193],[77.01258489179885,11.050501382448275],[77.02657421147529,11.051931828419981]]]},"properties":"null","id":"Coimbatore,TamilNadu"}]},"SubBlockSize":1000000}}],"HolosProductParams": [{"PRSEASON": {"NYERS":1,"AnalogousWeatherYear":2017}}],"CommonParams": {"TargetPlantingYear":2024,"TargetPlantingMonth":3,"TargetPlantingDay": 28,"_comment":"*NEW* PlantingMethod and Density_PlantsPerSqM Are New","PlantingMethod": "dryseed","Density_PlantsPerSqM":5,"BaseXFileName": "JDCH2022.RIX","BaseCul": "*RICE GENOTYPE COEFFICIENTS: RICER047 MODEL\n!\n@VAR#  VAR-NAME........ EXPNO   ECO#    P1   P2R    P5   P2O    G1    G2    G3 PHINT  THOT TCLDP TCLDF  !    previous\n!                                        1     2     3     4     5     6     7     8     9    10    11  !     G4    G5 \n!Introduce temperature-based factors to replace G4 and G5\n990001 IRRI ORIGINALS       . IB0001 880.0  52.0 550.0  12.0  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !   1.00   1.0\n990002 IRRI RECENT          . IB0001 450.0 149.0 350.0  11.7  68.0 .0230  1.00  83.0  28.0  15.0  15.0  !   1.00   1.0\n990003 JAPANESE             . IB0001 220.0  35.0 510.0  12.0  55.0 .0250  1.00  83.0  28.0  15.0  15.0  !   1.00   1.0\n990004 N.AMERICAN           . IB0001 318.0 189.0 550.0  12.8  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !   1.00   1.0\n!                                                                                               \n!@VAR#  VAR-NAME........ EXPNO   ECO#    P1   P2R    P5   P2O    G1    G2    G3    G4 PHINT    G5\n!990001 IRRI ORIGINALS       . IB0001 880.0  52.0 550.0  12.0  65.0 .0280  1.00  1.00  83.0   1.0\n!990002 IRRI RECENT          . IB0001 450.0 149.0 350.0  11.7  68.0 .0230  1.00  1.00  83.0   1.0\n!990003 JAPANESE             . IB0001 220.0  35.0 510.0  12.0  55.0 .0250  1.00  1.00  83.0   1.0\n!990004 N.AMERICAN           . IB0001 318.0 189.0 550.0  12.8  65.0 .0280  1.00  1.00  83.0   1.0\n\n!US and JF calibrated parameters. THOT = 28/G4, TCLDP and TCLDF = 15.0*G5 \n!VAR#  VAR-NAME........ EXPNO   ECO#    P1   P2R    P5   P2O    G1    G2    G3 PHINT  THOT TCLDP TCLDF  !     G4    G5\nIB0003 IR 36                . IB0001 556.8 53.88 373.4 12.87 68.00 0.023  1.00 83.00  31.3  15.0  15.0  !  0.895   1.0\nIB0012 IR 58                . IB0001 254.8 96.44 378.4 10.63 77.03 0.020  1.00 83.00  33.9  15.0  15.0  !  0.825   1.0\nIB0020 RD 23                . IB0001 528.6 156.5 387.4 12.64 52.65 0.022  1.00 83.00  29.0  15.0  15.0  !  0.967   1.0\nIB0050 PR114                . IB0001 662.5 184.4 503.0 12.38 62.86 0.023  1.00 83.00  25.7  15.0  15.0  !  1.091   1.0\nIB0055 Basmati 385          . IB0001 498.3 130.1 420.0 12.90 74.76 0.022  0.53 83.00  30.9  15.0  15.0  !  0.906   1.0\nIB0118 IR 72                . IB0001 437.1 61.02 371.8 11.58 77.80 0.026  1.00 83.00  30.4  15.0  15.0  !  0.921   1.0\n\n!Recalibration by Upendra Singh and Job Fugice 2019-04-25\n!!VAR#  VAR-NAME........ EXPNO   ECO#    P1   P2R    P5   P2O    G1    G2    G3    G4 PHINT    G5\n!IB0003 IR 36                . IB0001 556.8 53.88 373.4 12.87 68.00 0.023  1.00 0.895 83.00   1.0\n!IB0012 IR 58                . IB0001 254.8 96.44 378.4 10.63 77.03 0.020  1.00 0.825 83.00   1.0\n!IB0020 RD 23                . IB0001 528.6 156.5 387.4 12.64 52.65 0.022  1.00 0.967 83.00   1.0\n!IB0050 PR114                . IB0001 662.5 184.4 503.0 12.38 62.86 0.023  1.00 1.091 83.00   1.0\n!IB0055 Basmati 385          . IB0001 498.3 130.1 420.0 12.90 74.76 0.022  0.53 0.906 83.00   1.0\n!IB0118 IR 72                . IB0001 437.1 61.02 371.8 11.58 77.80 0.026  1.00 0.921 83.00   1.0\n\n!VAR#  VAR-NAME........ EXPNO   ECO#    P1   P2R    P5   P2O    G1    G2    G3 PHINT  THOT TCLDP TCLDF  !    previous\n!                                        1     2     3     4     5     6     7     8     9    10    11  !    G4    G5 \nIB0001 IR 8                 . IB0001 880.0  52.0 550.0  12.1  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0002 IR 20                . IB0001 500.0 166.0 500.0  11.2  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0004 IR 43                . IB0001 720.0 120.0 580.0  10.5  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0005 LABELLE              . IB0001 318.0 189.0 550.0  12.8  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0006 MARS                 . IB0001 698.0 134.0 550.0  13.0  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0007 NOVA 66              . IB0001 389.0 155.0 550.0  11.0  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0008 PETA                 . IB0001 420.0 240.0 550.0  11.3  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0009 STARBONNETT          . IB0001 880.0 164.0 550.0  13.0  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0010 UPLRI5               . IB0001 620.0 160.0 380.0  11.5  50.0 .0220  0.60  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0011 UPLRI7               . IB0001 760.0 150.0 450.0  11.7  65.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0013 SenTaNi (???)        . IB0001 320.0  50.0 550.0  10.0  70.0 .0300  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0014 IR 54                . IB0001 350.0 125.0 520.0  11.5  60.0 .0280  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0015 IR 64                . IB0001 500.0 160.0 450.0  12.0  60.0 .0250  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0016 IR 60(Est)           . IB0001 490.0 100.0 320.0  11.5  75.0 .0275  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0017 IR 66                . IB0001 500.0  50.0 490.0  12.5  62.0 .0265  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0018 IR 72x               . IB0001 400.0 100.0 580.0  12.0  76.0 .0230  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0019 RD 7 (cal.)          . IB0001 603.3 150.0 452.5  11.2  65.0 .0230  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0021 CICA8                . IB0001 700.0 120.0 360.0  11.7  60.0 .0270  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0022 LOW TEMP.SEN         . IB0001 400.0 120.0 420.0  12.0  60.0 .0250  1.00  83.0  35.0  15.0  15.0  !  0.80   1.0\nIB0023 LOW TEMP.TOL         . IB0001 400.0 120.0 420.0  12.0  60.0 .0250  1.00  83.0  22.4  15.0  15.0  !  1.25   1.0\nIB0024 17 BR11,T.AMAN       . IB0001 740.0 180.0 400.0  10.5  55.0 .0250  1.00  83.0  31.1  15.0  15.0  !  0.90   1.0\nIB0025 18 BR22,T.AMAN       . IB0001 650.0 110.0 400.0  12.0  60.0 .0250  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0026 19 BR 3,T.AMAN       . IB0001 650.0 110.0 420.0  12.0  65.0 .0250  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0027 20 BR 3,BORO         . IB0001 650.0  90.0 400.0  13.0  65.0 .0250  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0029 CPIC8                . IB0001 380.0 150.0 300.0  12.8  38.0 .0210  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0030 LEMONT               . IB0001 500.0  50.0 300.0  12.8  60.0 .0207  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0031 RN12                 . IB0001 380.0  50.0 300.0  12.8  40.0 .0199  1.00  83.0  24.3  15.0  15.0  !  1.15   1.0\nIB0032 TW                   . IB0001 360.0  50.0 290.0  12.8  55.0 .0210  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0115 IR 64*               . IB0001 540.0 160.0 490.0  12.0  50.0 .0250  1.10  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0116 HEAT SENSITIVE       . IB0001 460.0   5.0 390.0  13.5  62.0 .0250  1.00  83.0  24.3  15.0  15.0  !  1.15   1.0\nIB0117 BR14                 . IB0001 560.0 200.0 500.0  11.5  45.0 .0260  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0119 BR11                 . IB0001 825.0 300.0 390.0  11.5  52.0 .0240  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0120 PANT-4               . IB0001 830.0 160.0 300.0  11.4  45.0 .0300  1.00  83.0  35.0  15.0  15.0  !  0.80   1.0\nIB0121 JAYA                 . IB0001 830.0 100.0 200.0  11.4  40.0 .0300  1.00  83.0  35.0  15.0  15.0  !  0.80   1.0\nIB0122 BPRI10               . IB0001 740.0 200.0 225.0  13.5  40.0 .0230  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nIB0151 ZHENG DAO 9380       . IB0001 400.0 120.0 420.0  13.0  60.0 .0270  1.00  83.0  24.3  15.0  15.0  !  1.15   1.0\nIB0200 CL-448               . IB0001 100.0 120.0 250.0  12.0  40.0 .0250  1.00  83.0  22.4  15.0  15.0  !  1.25   1.0\nIB0051 KS-282 CRice         . IB0001 290.0  17.0 490.0  13.0  55.0 .0500  1.00  83.0  40.0  15.0  15.0  !  0.70   1.0\nIB0052 Basmati-515 FRice    . IB0001 460.0 120.0 512.0  11.0  37.0 .0210  1.00  75.0  34.0  15.0  15.0  !  1.00   1.0\nIB0801 ADT43                . IB0001 483.0  53.5 348.0  12.0  55.8 .0240  1.00  83.0  34.0  15.0  15.0  !  0.89   1.0\nIB0803 ADT45                . IB0001 450.0  75.0 355.0  12.0  73.0 .0260  1.00  83.0  34.0  15.0  15.0  !  1.00   1.0\nIB0806 CO51                 . IB0001 460.0  78.4 360.3  12.0  64.0 .0250  0.60  83.0  34.0  15.0  15.0  !  0.89   1.0\n!IB0806 CO51                 . IB0001 460.0  78.4 360.3  12.0  74.0 .0250  1.00  83.0  34.0  15.0  15.0  !  0.89   1.0\nIB0802 ASD16                . IB0001 450.0  69.0 350.0  12.0  73.0 .0280  1.00  83.0  34.0  15.0  15.0  !  1.00   1.0\nIB0804 CO(R)50              . IB0001 550.0  85.4 315.3  12.0  43.0 .0200  0.85  83.0  30.0  15.0  15.0  !  0.89   1.0\nIB0805 CR-1009              . IB0001 483.0 53.50 348.1 12.00 55.80 0.024  1.00  83.0  34.0  15.0  15.0  !  0.89   1.0\nIB0036 BPT5204              . IB0001 990.0  60.0 350.0  12.0  49.0 .0220  1.00  83.0  30.4  15.0  15.0  !  0.89   1.0\n\n\n\n!chp added revised cultivars from ATTACHAI JINTRAWET (Thailand) - gave new name  \n!  starting with MC.                                                             \n!             A low G3 value put more biomass to tillers, thru TILRAT and        \n!             TPANIWT variables, meaning that more STMWT is needed.              \n!VAR#  VAR-NAME........ EXPNO   ECO#    P1   P2R    P5   P2O    G1    G2    G3 PHINT  THOT TCLDP TCLDF  !    previous\n!                                        1     2     3     4     5     6     7     8     9    10    11  !    G4    G5 \nMC0020 RD 23                . IB0001 310.3 140.0 370.0  11.2  53.0 .0230  0.30  83.0  28.0  15.0  15.0  !  1.00   1.0\nTR0001 KDML105              . IB0001 502.3 123.3 386.5  12.7  45.7 .0270  1.00  83.0  29.5  15.0  15.0  !  0.95   1.0\nTR0002 NIEW SANPATONG       . IB0001 495.8 128.3 364.2  12.7  40.7 .0277  0.70  83.0  32.9  15.0  15.0  !  0.85   1.0\nTR0003 SUPANBURI 60         . IB0001 540.0 154.7 497.0  11.9  77.7 .0280  1.00  83.0  27.2  15.0  15.0  !  1.03   1.0\nTR0004 CHAINAT 1            . IB0001 570.0 122.8 334.8  11.9  63.1 .0278  1.00  83.0  28.0  15.0  15.0  !  1.00   1.0\nTR0005 DOA 1                . IB0001 388.5  20.0 381.8  12.0  73.8 .0275  1.10  83.0  24.3  15.0  15.0  !  1.15   1.0\n\n! The cultivar coefficient G5 was added to CSM-CERES-Rice Version 4.7.5\n! v4.7.7 - remove G4 and G5 and introduce THOT, TCLDP, and TCLDF\n!\n! COEFF    DEFINITIONS\n! ======== ===========\n! VAR#     Identification code or number for a specific cultivar.\n! VAR-NAME Name of cultivar.\n! EXPNO    Number of experiments used to estimate cultivar parameters\n! ECO#     Ecotype code for this cultivar points to the Ecotype in the ECO\n!          file (currently not used).\n\n! P1       Time period (expressed as growing degree days [GDD] in oC-d above a\n!          base temperature of 9oC) from seedling emergence during which the\n!          rice plant is not responsive to changes in photoperiod. This period\n!          is also referred to as the basic vegetative phase of the plant.\n!          Range: 150-800 oC-d. \n!          Calibration: flexible, compare with observed panicle initiation \n!          and flowering dates.\n\n! P2O      Critical photoperiod or the longest day length (in hours) at\n!          which the development occurs at a maximum rate. At values higher\n!          than P2O developmental rate is slowed, hence there is delay due\n!          to longer day lengths. \n!          Range 11-13 h. Default 12 h. \n!          Calibration: Do not go below 11 unless data are available. \n\n! P2R      Extent to which phasic development leading to panicle initiation\n!          is delayed (expressed as GDD in oC-d) for each hour increase in\n!          photoperiod above P2O. \n!          Range 5-300 oC-d. \n!          Calibration: Modern rice varieties will have values in \n!          the lower range.\n\n! P5       Time period in GDD oC-d) from beginning of grain filling (3 to\n!          4 days after flowering) to physiological maturity with a base\n!          temperature of 9oC. \n!          Range 150-850 oC-d. \n!          Calibration: Ensure P1, P2O and P2R are correctly calibrated for \n!          anthesis data. Then calibrate P5 for observed maturity date.\n\n! G1       Potential spikelet number coefficient as estimated from the\n!          number of spikelets per g of main culm dry weight (less leaf\n!          blades and sheaths plus spikes) at anthesis. \n!          Range 50-75 #/g. A typical value is 55 #/g.\n\n! G2       Single grain weight (g) under ideal growing conditions, i.e.\n!          nonlimiting light, water, nutrients, and absence of pests\n!          and diseases.\n!          Range 0.015-0.030 g. Default 0.025 g.\n!          Calibration: Very low flexibility. \n\n! G3       Tillering coefficient (scalar value) relative to IR64 cultivar\n!          under ideal conditions. \n!          Range 0.7-1.3.\n!          Calibration: A higher tillering cultivar would have a coefficient \n!          greater than 1.0.\n\n! PHINT    Phyllochron Interval (oC-d). Time interval in degree-days for each \n!          leaf-tip to appear under non-stressed conditions.  \n!          Range 55-90 oC-d. Default 83 oC-d.\n!          Calibration: Recommend to not change unless field data on leaf \n!          numbers are available.\n\n! THOT     Temperature (oC) above which spikelet sterility is affected by \n!          high temperature.  \n!          Range 25-34 oC. Default 28oC. \n!          Calibration: recommended to not change unless hot environment\n!          data are available. Convert old cultivars THOT = 28./G4.\n\n! TCLDP    Temperature (oC) below which panicle initiation is further delayed \n!          (other than P1, P2O and P2R) by low temperature.\n!          Range 12-18 oC. Default 15oC. \n!          Calibration: recommended to not change unless cold environment\n!          data are available. Convert old cultivars TCLDP = 15.*G5.\n\n! TCLDF    Temperature (oC) below which spikelet sterility is affected by \n!          low temperature.\n!          Range 10-20 oC. Default 15oC. \n!          Calibration: recommended to not change unless cold environment\n!          data are available. Convert old cultivars TCLDF = 15.*G5.\n\n","BaseX": "*EXP.DETAILS: Historical X file compliant w DSSAT, for two years, starting 2021\n\n*GENERAL\n@PEOPLE\nGeetha&Bhuvana\n@ADDRESS\nTNAU\n@SITE\nTanjore\n\n*TREATMENTS                        -------------FACTOR LEVELS------------\n@N R O C TNAME.................... CU FL SA IC MP MI MF MR MC MT ME MH SM\n 1 1 1 0 Tanjavur                   1  1  0  1  1  1  1  0  0  0  0  0  1\n 2 1 1 0 Tanjavur                   2  1  0  1  1  1  1  0  0  0  0  0  1\n 3 1 1 0 Tanjavur                   3  1  0  1  1  1  1  0  0  0  0  0  1\n 4 1 1 0 Tanjavur                   4  1  0  1  1  1  1  0  0  0  0  0  1\n 5 1 1 0 Tanjavur                   5  1  0  1  1  1  1  0  0  0  0  0  1\n\n*CULTIVARS\n@C CR INGENO CNAME\n 1 RI IB0036 BPT5204\n 2 RI IB0803 ADT45\n 3 RI IB0806 CO51\n 4 RI IB0802 ASD16\n 5 RI IB0805 ADT36\n\n*FIELDS\n@L ID_FIELD WSTA....  FLSA  FLOB  FLDT  FLDD  FLDS  FLST SLTX  SLDP  ID_SOIL    FLNAME\n 1 CDZT2201 TNJR8141   -99   -99 DR000   -99   -99   -99 CL     -99  IN04042298 test1\n@L ...........XCRD ...........YCRD .....ELEV .............AREA .SLEN .FLWR .SLAS FLHST FHDUR\n 1             -99             -99       -99               -99   -99   -99   -99   -99   -99\n\n*INITIAL CONDITIONS\n@C   PCR ICDAT  ICRT  ICND  ICRN  ICRE  ICWD ICRES ICREN ICREP ICRIP ICRID ICNAME\n 1    RI 21255   -99   -99     1     1   -99   -99   -99   -99   -99   -99 ini1\n@C  ICBL  SH2O  SNH4  SNO3\n 1    10  .301    .2   1.3\n 1    30  .354    .2   1.3\n 1    80  .375    .2   1.3\n 1   100  .418    .2   1.3\n 1   150   .43    .2   1.3\n 1   200  .453    .2   1.3\n\n*PLANTING DETAILS\n@P PDATE EDATE  PPOP  PPOE  PLME  PLDS  PLRS  PLRD  PLDP  PLWT  PAGE  PENV  PLPH  SPRL                        PLNAME\n 1 21263 21268    33    33     T     H    20    90     3   -99    21    24     3   -99                        Sep21\n\n*IRRIGATION AND WATER MANAGEMENT\n@I  EFIR  IDEP  ITHR  IEPT  IOFF  IAME  IAMT IRNAME\n 1     1    30    50   100 GS000 IR001    10 -99\n@I IDATE  IROP IRVAL\n 1     1 IR009   100\n 1     1 IR008     1\n 1     1 IR006    25\n 1     3 IR006    25\n 1     6 IR006    25\n 1     9 IR006    25\n 1    12 IR006    25\n 1    16 IR006    25\n 1    20 IR006    25\n 1    24 IR006    50\n 1    28 IR006    50\n 1    32 IR006    50\n 1    36 IR006    50\n 1    40 IR006    50\n 1    44 IR006    50\n 1    48 IR006    50\n 1    52 IR006    50\n 1    54 IR006    50\n 1    56 IR006    50\n 1    60 IR006    50\n 1    64 IR006    50\n 1    68 IR006    50\n 1    72 IR006    50\n 1    76 IR006    50\n 1    80 IR006    50\n 1    84 IR006    50\n 1    88 IR006    50\n\n*FERTILIZERS (INORGANIC)\n@F FDATE  FMCD  FACD  FDEP  FAMN  FAMP  FAMK  FAMC  FAMO  FOCD FERNAME\n 1     1 FE005 AP016     1    38     0   -99   -99   -99   -99 ferti\n 1    35 FE005 AP015     1    38     0   -99   -99   -99   -99 ferti\n 1    65 FE005 AP015     1    38     0   -99   -99   -99   -99 ferti\n 1    95 FE005 AP014     1    38     0   -99   -99   -99   -99 ferti\n\n*RESIDUES AND ORGANIC FERTILIZER\n@R RDATE  RCOD  RAMT  RESN  RESP  RESK  RINP  RDEP  RMET RENAME\n 1     0 RE003  6000    .5   .25    .5    70     4 AP012 ORGANIC1\n\n*TILLAGE AND ROTATIONS\n@T TDATE TIMPL  TDEP TNAME\n 1 21173   -99   -99 -99\n\n*ENVIRONMENT MODIFICATIONS\n@E ODATE EDAY  ERAD  EMAX  EMIN  ERAIN ECO2  EDEW  EWIND ENVNAME  \n 1 21141 A   0 M 3.6 A   0 A   0 A 0.0 A   0 A   0 A   0 \n\n*HARVEST DETAILS\n@H HDATE  HSTG  HCOM HSIZE   HPC  HBPC HNAME\n 1 21173 GS000   -99   -99   -99   -99 Rice\n\n*SIMULATION CONTROLS\n@N GENERAL     NYERS NREPS START SDATE RSEED SNAME.................... SMODEL\n 1 GE              2     1     S 21255  2150 DEFAULT SIMULATION CONTR  RICER\n@N OPTIONS     WATER NITRO SYMBI PHOSP POTAS DISES  CHEM  TILL   CO2\n 1 OP              Y     Y     Y     N     N     N     N     Y     M\n@N METHODS     WTHER INCON LIGHT EVAPO INFIL PHOTO HYDRO NSWIT MESOM MESEV MESOL\n 1 ME              M     M     E     R     S     L     R     1     G     S     2\n@N MANAGEMENT  PLANT IRRIG FERTI RESID HARVS\n 1 MA              R     D     D     D     M\n@N OUTPUTS     FNAME OVVEW SUMRY FROPT GROUT CAOUT WAOUT NIOUT MIOUT DIOUT VBOSE CHOUT OPOUT FMOPT\n 1 OU              N     Y     Y     1     Y     Y     Y     Y     Y     N     Y     N     Y     A\n\n@  AUTOMATIC MANAGEMENT\n@N PLANTING    PFRST PLAST PH2OL PH2OU PH2OD PSTMX PSTMN\n 1 PL          21244 21263    40   100    30    40    10\n@N IRRIGATION  IMDEP ITHRL ITHRU IROFF IMETH IRAMT IREFF\n 1 IR              5    50   100 GS000 IR006    10    .9\n@N NITROGEN    NMDEP NMTHR NAMNT NCODE NAOFF\n 1 NI             30    50    25 FE001 GS000\n@N RESIDUES    RIPCN RTIME RIDEP\n 1 RE            100     1    20\n@N HARVEST     HFRST HLAST HPCNP HPCNR\n 1 HA              0 20173   100     0\n\n\n\u001a\n"}}],"Version":4.1,"UserEmailID": "vasu@eprobito.com"}'

    headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PATCH, DELETE, PUT, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With',
}

    url = "https://05mmdxz7gd.execute-api.us-east-2.amazonaws.com/v1/uploadspatialspecs"
    
    response = requests.post(url, data=json_string, headers=headers)

    if response.status_code == 200:
        print(response.json())
        return JsonResponse({"statusCode": 200, "name": name, "product":selectedholosproduct})
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return JsonResponse({"statusCode": 701, "error": "AWS Call error"})

    return JsonResponse({"statusCode": 200, "name": name, "product":selectedholosproduct})

@csrf_exempt  
def pdf_to_image(req):
    images = []
    id = req.POST.get("caseId")
    print(id)
    try:
        snippet = Case_Detiles.objects.get(id=id)
    except Case_Detiles.DoesNotExist:
        return HTTPResponse(status=404)

    if req.method == "POST":
        Xfilename = req.POST.get("Xfilename")
        
        CULfilename = req.POST.get("CULfilename")
        
        caseid = req.POST.get("caseId")
        path = req.POST.get("path")
        orgid = req.POST.get("orgid")
        X_existing_new = req.POST.get("X_existing_new")
        CUL_existing_new = req.POST.get("CUL_existing_new")
        file_userid = req.POST.get("userid")
        
        if X_existing_new == "new":
            Xts = req.FILES["Xfile"]
            #print("Path Here", Xts)
            x = str(Xts).split(".")
            #print("file path here", x[1])
            handle_uploaded_file(Xts, path)
            Xts_as_string = str(Xts)
            #print("tables", FilePath + "/" + Xts_as_string)
            # Upload X file to S3
            object_key_txt = path+"/Xfiles/"+ Xfilename
            print("X S3 location",object_key_txt)
            s3.upload_file(FilePath +"/"+ Xfilename, bucket_name, object_key_txt)
            # check if record exists in file_details for X file for orgid and userid
            
            print("userid")
            print(orgid, file_userid,Xfilename)

            casedetailasupdate = {"XfileName": Xfilename}
            serializer = Case_Detiles_serializers(snippet, data=casedetailasupdate)
            if serializer.is_valid():
                serializer.save()

            record_exists = file_details.objects.filter(orgid=orgid, userid=file_userid,filetype="Xfile", filename=Xfilename).exists()
            print(record_exists)
            if record_exists == False:
               # if no, create record
               print("creating X file record")
               file_details_record = file_details.objects.create(
               orgid  = orgid,
               userid = file_userid,
               filetype = "Xfile",
               filename = Xfilename,
               )
               file_details_record.save()

        if CUL_existing_new == "new":
            CULts = req.FILES["CULfile"]
            handle_uploaded_file(CULts, path)
            # print("FilePath",FilePath)
            CULts_as_string = str(CULts)
            # Upload CUL file to S3
            object_key_txt = path+"/CULfiles/"+ CULfilename
            print("CUL S3 location",object_key_txt)
            s3.upload_file(FilePath +"/"+ CULfilename, bucket_name, object_key_txt)

            casedetailasupdate = {"CULfileName": CULfilename}
            serializer = Case_Detiles_serializers(snippet, data=casedetailasupdate)
            if serializer.is_valid():
                serializer.save()

            # check if record exists in file_details for CUL file for orgid and userid
            record_exists = file_details.objects.filter(orgid=orgid, userid=file_userid,filetype="CULfile", filename=CULfilename).exists()
            print(record_exists)
            if record_exists == False:
            # if no, create record
              print("creating CUL file record")
              file_details_record = file_details.objects.create(
              orgid  = orgid,
              userid = file_userid,
              filetype = "CULfile",
              filename = CULfilename,
              )
              file_details_record.save()    
        # if no, create record

        """ casedetailasupdate = {"Xfilename": Xfilename, "CULfilename": CULfilename}
        print(casedetailasupdate)

        serializer = Case_Detiles_serializers(snippet, data=casedetailasupdate)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse({"statusCode": 200}) """
    return JsonResponse({"StatusCode": 200}, status=200)

@csrf_exempt
def createFarm(req):
    """
    This function is to insert a farm record in our database.
    """
    print("I am in createFarm")
    if req.method == "POST":
        data = JSONParser().parse(req)
        orgid = data["companyID"]
        userid = data["UserID"]
        farmname = data["farmname"]
        coords_string = data["Coordinates"]
        out = ''
        for x in coords_string:
            for y in x:
                i = 0
                for z in y:
                    if i == 0:
                       out = out + " " + str(z)
                       i = 1
                    elif i == 1:
                       out = out +" "+ str(z) + ","
        out = out[:-1]
        print (out)
        #polygon_coordinates = GEOSGeometry('POLYGON ((-98.503358 29.335668, -98.503086 29.335668, -98.503086 29.335423, -98.503358 29.335423, -98.503358 29.335668))', srid=4326)
        #polygon_coordinates = GEOSGeometry('POLYGON (('+ out+ '))', srid=4326)
        farm_details_record = farm_details.objects.create(
            orgid  = orgid,
            userid = userid,
            farmname = farmname,
            polygon_coords = coords_string,
            )
        farm_details_record.save()  
        return JsonResponse(
                {"response": "Farm data", "statusCode": 200, "errorMsg": "success"},
                status=200,
            )
    
@csrf_exempt
def create_zip(request):

    myfilename = "results.zip"

    orgid = request.GET.get('orgid')
    username = request.GET.get('username')
    projectname = request.GET.get('projectname')
    dir = request.GET.get('dir')
    zipfilename = request.GET.get('zipfiles3loc')

    zipfiles3loc = orgid +'/'+ username +'/'+ projectname +'/'+dir +'/'+zipfilename 
    # Download the file from S3
    zipfile = s3.get_object(Bucket=bucket_name, Key=zipfiles3loc)

    # Get the file content
    zip_content = zipfile['Body'].read()

    response = HttpResponse(zip_content, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{myfilename}"'

    return response        


@csrf_exempt
def insertion(req):
    """
    This function is provide us a dispay and insertion in our database.
    """
    print("I am in insertion")
    if req.method == "GET":  # its dispay the data
        queryset = Case_Detiles.objects.all().order_by("-id")
        serializer = Case_Detiles_serializers(queryset, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )

    elif (
        req.method == "POST"
    ):  # its  save the data if data is json formate and  send it by valid user
        data = JSONParser().parse(req)
        serializer = Case_Detiles_serializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
                status=201,
            )
        return JsonResponse(
            {"response": serializer.errors, "errorCode": 200, "errorMsg": "success"},
            status=400,
        )


@csrf_exempt
def insertion_details(request, id):
    """
    This fuction will allow to our data
    Retrieve, update or delete a code snippet.
    """
    print("I am in insertion details")
    try:
        snippet = Case_Detiles.objects.filter(id=id)
    except Case_Detiles.DoesNotExist:
        return HTTPResponse(status=404)

    if (
        request.method == "GET"
    ):  # its show the data by using slug if the slug is exsist its show the data other wise its show 404 error
        serializer = Case_Detiles_serializers(snippet, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )

    elif (
        request.method == "PUT"
    ):  # its update the data if method type is put Then its check all details are correct or not if all details are correct its update the previous data
        data = JSONParser().parse(request)
        serializer = Case_Detiles_serializers(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
                safe=False,
            )
        return JsonResponse(
            {"response": serializer.errors, "errorCode": 200, "errorMsg": "success"},
            status=400,
        )

    elif (
        request.method == "DELETE"
    ):  # This method is delete the data by using slug value  if once you delete the data u never retrive that data.
        snippet.delete()
        #  return HTTPResponse(status=204)
        return JsonResponse(
            {
                "response": "successfully deleted",
                "errorCode": 200,
                "errorMsg": "success",
            },
            safe=False,
        )


@csrf_exempt
def rolebase_insertion_details(request, id):
    """
    This fuction will allow to our data
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Case_Detiles.objects.get(orgid=id)
    except Case_Detiles.DoesNotExist:
        return HTTPResponse(status=404)

    if (
        request.method == "GET"
    ):  # its show the data by using slug if the slug is exsist its show the data other wise its show 404 error
        serializer = Case_Detiles_serializers(snippet, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )

    elif (
        request.method == "PUT"
    ):  # its update the data if method type is put Then its check all details are correct or not if all details are correct its update the previous data
        data = JSONParser().parse(request)
        serializer = Case_Detiles_serializers(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
                safe=False,
            )
        return JsonResponse(
            {"response": serializer.errors, "errorCode": 200, "errorMsg": "success"},
            status=400,
        )

    elif (
        request.method == "DELETE"
    ):  # This method is delete the data by using slug value  if once you delete the data u never retrive that data.
        snippet.delete()
        return HTTPResponse(status=204)


@csrf_exempt
def insertion_details_1(request, id):
    """
    This fuction will allow to our data
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = whole_data.objects.filter(case_id=id)

    except whole_data.DoesNotExist:
        return HTTPResponse(status=404)

    if (
        request.method == "GET"
    ):  # its show the data by using slug if the slug is exsist its show the data other wise its show 404 error
        queryset = whole_data.objects.all()
        serializer = whole_data_serializers(snippet, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )


@csrf_exempt
def registrationform(req):
    """
    This function is provide us a dispay and insertion in our database.
    """
    if req.method == "GET":  # its dispay the data
        queryset = Registration.objects.all()
        serializer = Registration_serializers(queryset, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )

    elif (
        req.method == "POST"
    ):  # its  save the data if data is json formate and  send it by valid user
        data = JSONParser().parse(req)
        encryptedpassword = make_password(data["password"])
        #        print("data", encryptedpassword)
        data["password"] = encryptedpassword
        print("data", data)
        print("data", data["orgid"])
        serializer = Registration_serializers(data=data)
        if serializer.is_valid():
            # Directory
            directory = str(data["orgid"])

            s3.put_object(Bucket=bucket_name, Key=(directory + "/"))

            # Parent Directory path
            parent_dir = "./mediafiles/"
            path = os.path.join(parent_dir, directory)

            os.mkdir(path)
            print("Directory '% s' created" % directory)
            serializer.save()
            return JsonResponse(
                {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
                status=201,
            )
        return JsonResponse(
            {"response": serializer.errors, "errorCode": 200, "errorMsg": "success"},
            status=400,
        )


@csrf_exempt
def login(request, email, password):
    """
    This fuction will allow to our data
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Registration.objects.get(email=email, password=password)
    except Registration.DoesNotExist:
        return HTTPResponse(status=404)

    if (
        request.method == "GET"
    ):  # its show the data by using slug if the slug is exsist its show the data other wise its show 404 error
        serializer = Registration_serializers(snippet)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )


@csrf_exempt
def setProject(req):
    """
    This function is provide us a dispay and insertion in our database.
    """
    if req.method == "GET":  # its dispay the data
        print("In set Project 1 GET")
        queryset = Set_project_detils.objects.all()
        serializer = Set_project_detils_serializers(queryset, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )

    elif (
        req.method == "POST"
    ):  # its  save the data if data is json formate and  send it by valid user
        print("In set Project 1 POST")
        data = JSONParser().parse(req)
        print("data", data["orgid"])
        serializer = Set_project_detils_serializers(data=data)
        if serializer.is_valid():
            # Directory
            # directory = str(data['orgid'])

            # # Parent Directory path
            # parent_dir = "./mediafiles/"
            # path = os.path.join(parent_dir, directory)

            # os.mkdir(path)
            # print("Directory '% s' created" % directory)

            username = data["username"]
            username = username.replace(" ","")


            bucket_name1 = data["orgid"] + "/" +username +"/"+ data["setProjectName"] + "/"
            print("bucket_name", bucket_name1)
            s3.put_object(Bucket=bucket_name, Key=(bucket_name1))
            serializer.save()
            return JsonResponse(
                {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
                status=201,
            )
        return JsonResponse(
            {"response": serializer.errors, "errorCode": 200, "errorMsg": "success"},
            status=400,
        )

@csrf_exempt
def getfilelist(req):
    """
    This function is provide us a dispay and insertion in our database.
    """
    if req.method == "GET":  # its dispay the data
        orgid = req.GET.get('orgid')
        userid = req.GET.get('userid')
        filetype = req.GET.get('filetype')
        print(orgid)
        print(userid)
        print(filetype)
        print("In getfileList GET")
        queryset = file_details.objects.filter(orgid=orgid, userid=userid, filetype=filetype)
        serializer = file_details_serializers(queryset, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )
    
@csrf_exempt
def getfarmlist(req):
    """
    This function is provide us a dispay and insertion in our database.
    """
    if req.method == "GET":  # its dispay the data
        orgid = req.GET.get('orgid')
        userid = req.GET.get('userid')
        print("In getfarmlList GET")
        print(orgid)
        print(userid)
        queryset = farm_details.objects.filter(orgid=orgid, userid=userid)
        serializer = farm_details_serializers(queryset, many=True)
        print(serializer.data)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )

@csrf_exempt
def getfarmdetails(req):
    """
    This function is provide us a dispay and insertion in our database.
    """
    if req.method == "GET":  # its dispay the data
        farmid = req.GET.get('farmid')
        print("farmid", farmid)
        queryset = farm_details.objects.filter(id=farmid)
        serializer = farm_details_serializers(queryset, many=True)
        print(serializer.data[0]['polygon_coords'])
        #print(serializer.data)
        return JsonResponse(
            #{"response": serializer.data[0]['polygon_coords'], "errorCode": 200, "errorMsg": "success"},
            {"response": serializer.data[0], "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )

@csrf_exempt
def getexptresults(req):
    """
    This function is provide us a dispay and insertion in our database.
    """
    if req.method == "GET":  # its dispay the data
        caseid = req.GET.get('caseid')
        print("caseid", caseid)
        queryset = all_results.objects.filter(caseid=caseid)
        serializer = all_results_serializers(queryset, many=True)
        #print(serializer.data[0]['files3loc'])
        print(serializer.data)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )

@csrf_exempt
def setProject_orgid(req, id):
    """
    This function is provide us a dispay and insertion in our database.
    """
    if req.method == "GET":  # its dispay the data
        print("In set Project 2 GET")
        queryset = Set_project_detils.objects.filter(orgid=id)
        serializer = Set_project_detils_serializers(queryset, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )


@csrf_exempt
def setFolder(req, id):
    """
    This function is provide us a dispay and insertion in our database.
    """
    try:
        snippet = Set_folder_detils.objects.filter(project_name=id)
    except Set_folder_detils.DoesNotExist:
        return HTTPResponse(status=404)

    if req.method == "GET":  # its dispay the data
        print("In set Folder 1 GET")
        serializer = Set_folder_detils_serializers(snippet, many=True)
        # queryset = Set_folder_detils.objects.all()
        # serializer = Set_folder_detils_serializers(queryset, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )

    elif (
        req.method == "POST"
    ):  # its  save the data if data is json formate and  send it by valid user
        print("In set Folder 1 POST")
        data = JSONParser().parse(req)
        #print("data", data)

        serializer = Set_folder_detils_serializers(data=data)
        if serializer.is_valid():
            if data["project_type"] == "New":
                # Create the orgid folder
                directory_1 = data["project_name"]
                parent_dir_1 = "./mediafiles/" + str(data["orgid"]) + "/"
                path_1 = os.path.join(parent_dir_1, directory_1)
                os.mkdir(path_1)

            # Directory
            directory = data["setFolderName"]

            bucket_name1 = (
                data["orgid"]
                + "/"
                + data["project_name"]
                + "/"
                + data["setFolderName"]
                + "/"
            )
            print("bucket_name", bucket_name1)
            s3.put_object(Bucket=bucket_name, Key=(bucket_name1))
            # Parent Directory path
            parent_dir = (
                "./mediafiles/" + str(data["orgid"]) + "/" + data["project_name"] + "/"
            )
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            print("Directory '% s' created" % directory)
            serializer.save()
            return JsonResponse(
                {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
                status=201,
            )
        return JsonResponse(
            {"response": serializer.errors, "errorCode": 200, "errorMsg": "success"},
            status=400,
        )


@csrf_exempt
def setSearch(req, id):
    print("id in setsearch is: ", id)
    try:
        snippet = SearchWords.objects.filter(orgid=id)
    except SearchWords.DoesNotExist:
        return HTTPResponse(status=404)
    if req.method == "GET":  
        serializer = SearchWords_serializers(snippet,many=True)
        print("ser", serializer)
        print("ser data",serializer.data)
        return JsonResponse({
                        "response": serializer.data,
                        "errorCode": 200,
                        "errorMsg": "success"
                        }, safe=False)

@csrf_exempt
def setSearchRecord(req):
    if (
        req.method == "POST"
    ):  # its  save the data if data is json formate and  send it by valid user
        print("In set Search Record POST")
        data = JSONParser().parse(req)
        print("data", data)
        temp_words = (data["searchTitleWords"]).split(":")
        temp_words_len = len(temp_words)
        if temp_words_len > 1:
            title = temp_words[0]
            words = temp_words[1]
        else:
            title = "Title"
            words = data["searchTitleWords"]
        SearchWords_record = SearchWords.objects.create(
            userid=data["userid"],
            useremail=data["useremail"],
            project=data["project_name"],
            orgid=data["orgid"],
            empOrgid=data["orgid"],
            folder=data["folder_name"],
            searchtitle=title,
            searchwords=words,
            searchtitlewords=data["searchTitleWords"],
        )
        SearchWords_record.save()
    return JsonResponse(
        {"response": "success", "errorCode": 200, "errorMsg": "success"}, status=200
    )


@csrf_exempt
def createFolder(req):
    """
    This function is provide us a dispay and insertion in our database.
    """
    # try:
    #     snippet = Set_folder_detils.objects.filter(project_name=id)
    # except Set_folder_detils.DoesNotExist:
    #     return HTTPResponse(status=404)

    if req.method == "GET":  # its dispay the data
        print("In create Folder GET")
        # serializer = Set_folder_detils_serializers(snippet,many=True)
        queryset = Set_folder_detils.objects.all()
        serializer = Set_folder_detils_serializers(queryset, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )

    elif (
        req.method == "POST"
    ):  # its  save the data if data is json formate and  send it by valid user
        print("In create Folder POST")
        data = JSONParser().parse(req)
        print("data", data)

        serializer = Set_folder_detils_serializers(data=data)
        if serializer.is_valid():
            if data["project_type"] == "New":
                # Create the orgid folder
                directory_1 = data["project_name"]
                parent_dir_1 = "./mediafiles/" + str(data["orgid"]) + "/"
                path_1 = os.path.join(parent_dir_1, directory_1)
                os.mkdir(path_1)

            # Directory
            directory = data["setFolderName"]
            bucket_name1 = (
                data["orgid"]
                + "/"
                + data["project_name"]
                + "/"
                + data["setFolderName"]
                + "/"
            )
            print("bucket_name", bucket_name1)
            s3.put_object(Bucket=bucket_name, Key=(bucket_name1))
            # Parent Directory path
            parent_dir = (
                "./mediafiles/" + str(data["orgid"]) + "/" + data["project_name"] + "/"
            )
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            print("Directory '% s' created" % directory)
            serializer.save()
            return JsonResponse(
                {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
                status=201,
            )
        return JsonResponse(
            {"response": serializer.errors, "errorCode": 200, "errorMsg": "success"},
            status=400,
        )


@csrf_exempt
def setSummary(request, id):
    """
    This fuction will allow to our data
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = summary_details.objects.filter(case_id=id)

    except whole_data.DoesNotExist:
        return HTTPResponse(status=404)

    if (
        request.method == "GET"
    ):  # its show the data by using slug if the slug is exsist its show the data other wise its show 404 error
        queryset = summary_details.objects.all()
        serializer = summary_detils_serializers(snippet, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )


@csrf_exempt
def pdf_table_details(request, id):
    """
    This fuction will allow to our data
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = pdf_table_data.objects.filter(case_id=id)

    except pdf_table_data.DoesNotExist:
        return HTTPResponse(status=404)

    if (
        request.method == "GET"
    ):  # its show the data by using slug if the slug is exsist its show the data other wise its show 404 error
        queryset = pdf_table_data.objects.all()
        serializer = pdf_table_data_serializers(snippet, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )


@csrf_exempt
def basedon_status_casedetials(request, id):
    """
    This fuction will allow to our data
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Case_Detiles.objects.filter(status=id)

    except Case_Detiles.DoesNotExist:
        return HTTPResponse(status=404)

    if (
        request.method == "GET"
    ):  # its show the data by using slug if the slug is exsist its show the data other wise its show 404 error
        queryset = Case_Detiles.objects.all()
        serializer = Case_Detiles_serializers(snippet, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )


@csrf_exempt
def s3create(req):
    if req.method == "GET":  # its dispay the data
        queryset = Registration.objects.all()
        serializer = Registration_serializers(queryset, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )

    elif (
        req.method == "POST"
    ):  # its  save the data if data is json formate and  send it by valid user
        data = JSONParser().parse(req)
        print("data", data["orgid"])
        serializer = Registration_serializers(data=data)
        if serializer.is_valid():
            # Directory
            directory = str(data["orgid"])

            directory_name = "78542"  # it's name of your folders
            s3.put_object(Bucket=bucket_name, Key=(data["orgid"] + "/"))

            # Parent Directory path
            parent_dir = "./mediafiles/"
            path = os.path.join(parent_dir, directory)

            os.mkdir(path)
            print("Directory '% s' created" % directory)
            serializer.save()
            return JsonResponse(
                {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
                status=201,
            )
        return JsonResponse(
            {"response": serializer.errors, "errorCode": 200, "errorMsg": "success"},
            status=400,
        )


@csrf_exempt
def amazonExctract(req):
    if req.method == "POST":
        ts = req.FILES["file"]
        orgid = req.POST.get("orgid")
        #print(ts)
        object_name = os.path.basename(str(ts))
        print(object_name)
        print("-----------------------")
        path = req.POST.get("path")
        # S3 Bucket Data
        s3BucketName = "ocrnlp"
        print(s3BucketName)
        print("-----------------------------------------")
        print(FilePath + path + "/" + str(ts))
        # s3.Bucket(s3BucketName).put_object(Key=FilePath_1+ts, Body=ts)
        s3.upload_file(FilePath + path + "/" + str(ts), "ocrnlp", str(ts))
        # with open(FilePath + path +"/"+ f.name, 'wb+') as destination:
        #     s3.upload_file(data, 'ocrnlp', 'filenameintos3.txt')
        PlaindocumentName = str(ts)
        FormdocumentName = str(ts)
        TabledocumentName = str(ts)

        # Amazon Textract client
        textractmodule = boto3.client("textract")

        # 1. PLAINTEXT detection fr om documents:
        response = textractmodule.detect_document_text(
            Document={"S3Object": {"Bucket": s3BucketName, "Name": PlaindocumentName}}
        )
        print(
            "------------- Print Plaintext detected text ------------------------------"
        )
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                print("\033[92m" + item["Text"] + "\033[92m")

        # 2. FORM detection from documents:
        response = textractmodule.analyze_document(
            Document={"S3Object": {"Bucket": s3BucketName, "Name": FormdocumentName}},
            FeatureTypes=["FORMS"],
        )
        doc = Document(response)
        print("------------- Print Form detected text ------------------------------")
        for page in doc.pages:
            for field in page.form.fields:
                print("Key: {}, Value: {}".format(field.key, field.value))

        # 2. TABLE data detection from documents:
        response = textractmodule.analyze_document(
            Document={"S3Object": {"Bucket": s3BucketName, "Name": TabledocumentName}},
            FeatureTypes=["TABLES"],
        )
        doc = Document(response)
        print("------------- Print Table detected text ------------------------------")
        for page in doc.pages:
            for table in page.tables:
                for r, row in enumerate(table.rows):
                    itemName = ""
                    for c, cell in enumerate(row.cells):
                        print("Table[{}][{}] = {}".format(r, c, cell.text))


@csrf_exempt
def login(req, email, password):
    # if request.method == 'GET':

    if req.method == "GET":
        encryptedpassword = make_password(password)
        print(encryptedpassword)
        queryset = Registration.objects.filter(email=email).filter(
            password=encryptedpassword
        )

        serializer = Registration_serializers(queryset, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )


@csrf_exempt
def contactForm(req):
    """
    This function is provide us a dispay and insertion in our database.
    """
    if req.method == "GET":  # its dispay the data
        queryset = contact_form.objects.all()
        serializer = contact_form_serializers(queryset, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )

    elif (
        req.method == "POST"
    ):  # its  save the data if data is json formate and  send it by valid user
        data = JSONParser().parse(req)
        serializer = contact_form_serializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
                status=201,
            )
        return JsonResponse(
            {"response": serializer.errors, "errorCode": 200, "errorMsg": "success"},
            status=400,
        )


@csrf_exempt
def login(req):
    print("in login, right at the start")
    if req.method == 'GET':
      print(req)
    print("in login, before if POST")
    if req.method == "POST":
        print("in login, after POST")
        data = JSONParser().parse(req)
        print("in login, after POST",data)
        email = data["email"]
        password = data["password"]
        print("in login, after POST",email)
        print("in login, after POST",password)
        datavalue = Registration.objects.raw("SELECT * FROM app_registration WHERE email = %s", [email])
        print("in login, after POST",datavalue)
        for p in Registration.objects.raw("SELECT * FROM app_registration WHERE email = %s", [email]):
            print("data", p.password)
            print("input", password)
            if check_password(password, p.password):
                serializer = Registration_serializers(datavalue, many=True)
                return JsonResponse(
                    {
                        "response": serializer.data,
                        "errorCode": 200,
                        "errorMsg": "success",
                    },
                    safe=False,
                )
            else:
                return JsonResponse(
                    {
                        "response": "Data Did Not Match",
                        "errorCode": 400,
                        "errorMsg": "failed",
                    },
                    safe=False,
                )


@csrf_exempt
def pdfInfo_details(request, id):
    """
    This fuction will allow to our data
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = pdfcount_details.objects.filter(orgid=id)
    except pdfcount_details.DoesNotExist:
        return HTTPResponse(status=404)

    if (
        request.method == "GET"
    ):  # its show the data by using slug if the slug is exsist its show the data other wise its show 404 error
        serializer = Pdfinfo_details_serializers(snippet, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )

    elif (
        request.method == "PUT"
    ):  # its update the data if method type is put Then its check all details are correct or not if all details are correct its update the previous data
        data = JSONParser().parse(request)
        # print(data)
        mymodel = pdfcount_details.objects.get(orgid=id)
        serializer = Pdfinfo_details_serializers(mymodel, data=data)
        if serializer.is_valid():
            print(data)
            serializer.save()
            return JsonResponse(
                {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
                safe=False,
            )
        return JsonResponse(
            {"response": serializer.errors, "errorCode": 200, "errorMsg": "success"},
            status=400,
        )

    # This method is delete the data by using slug value  if once you delete the data u never retrive that data.
    elif request.method == "DELETE":
        snippet.delete()
        return JsonResponse({"errorCode": 200, "errorMsg": "success"}, safe=False)


@csrf_exempt
def pdfinfo_insert(req):
    # """
    # This function is provide us a dispay and insertion in our database.
    # """
    # if req.method == "GET":  # its dispay the data
    #     queryset = contact_form.objects.all()
    #     serializer = Pdfinfo_details_serializers(queryset, many=True)
    #     return JsonResponse({
    #         "response": serializer.data,
    #         "errorCode": 200,
    #         "errorMsg": "success"
    #     }, safe=False)

    if (
        req.method == "POST"
    ):  # its  save the data if data is json formate and  send it by valid user
        data = JSONParser().parse(req)
        serializer = Pdfinfo_details_serializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
                status=201,
            )
        return JsonResponse(
            {"response": serializer.errors, "errorCode": 200, "errorMsg": "success"},
            status=400,
        )


# @csrf_exempt
# def send(req):
#     if req.method == "POST":
#             data = JSONParser().parse(req)
#             Email_To = [data['email']]
#             msg = EmailMultiAlternatives(subject="Hello", body="RESET PASSWORD",from_email= settings.EMAIL_HOST_USER,to=Email_To)
#             msg.send()
#             return JsonResponse({
#             "response": "SUCCESS",
#             "errorCode": 200,
#             "errorMsg": "success"
#         }, status=400)


@csrf_exempt
def send(req):
    if req.method == "POST":
        data = JSONParser().parse(req)
        print(data["email"])
        Email_To = [data["email"]]
        # htmly     = get_template('email.html')
        # d = Context({ 'username': data['email'] })
        # template = get_template('my_custom_template.html').render(context)
        # html_content = htmly.render(d)
        # html_message = render_to_string('email.html', {'context': 'values'})
        # plain_message = """<h1>Testing Manikanta</h1>"""
        bodytest = """<!doctype html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Simple Transactional Email</title>
    <style>
      img {
        border: none;
        -ms-interpolation-mode: bicubic;
        max-width: 100%; 
      }

      body {
        background-color: #f6f6f6;
        font-family: sans-serif;
        -webkit-font-smoothing: antialiased;
        font-size: 14px;
        line-height: 1.4;
        margin: 0;
        padding: 0;
        -ms-text-size-adjust: 100%;
        -webkit-text-size-adjust: 100%; 
      }

      table {
        border-collapse: separate;
        mso-table-lspace: 0pt;
        mso-table-rspace: 0pt;
        width: 100%; }
        table td {
          font-family: sans-serif;
          font-size: 14px;
          vertical-align: top; 
      }

      /* -------------------------------------
          BODY & CONTAINER
      ------------------------------------- */

      .body {
        background-color: #f6f6f6;
        width: 100%; 
      }

      /* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */
      .container {
        display: block;
        margin: 0 auto !important;
        /* makes it centered */
        max-width: 580px;
        padding: 10px;
        width: 580px; 
      }

      /* This should also be a block element, so that it will fill 100% of the .container */
      .content {
        box-sizing: border-box;
        display: block;
        margin: 0 auto;
        max-width: 580px;
        padding: 10px; 
      }

      /* -------------------------------------
          HEADER, FOOTER, MAIN
      ------------------------------------- */
      .main {
        background: #ffffff;
        border-radius: 3px;
        width: 100%; 
      }

      .wrapper {
        box-sizing: border-box;
        padding: 20px; 
      }

      .content-block {
        padding-bottom: 10px;
        padding-top: 10px;
      }

      .footer {
        clear: both;
        margin-top: 10px;
        text-align: center;
        width: 100%; 
      }
        .footer td,
        .footer p,
        .footer span,
        .footer a {
          color: #999999;
          font-size: 12px;
          text-align: center; 
      }

      /* -------------------------------------
          TYPOGRAPHY
      ------------------------------------- */
      h1,
      h2,
      h3,
      h4 {
        color: #000000;
        font-family: sans-serif;
        font-weight: 400;
        line-height: 1.4;
        margin: 0;
        margin-bottom: 30px; 
      }

      h1 {
        font-size: 35px;
        font-weight: 300;
        text-align: center;
        text-transform: capitalize; 
      }

      p,
      ul,
      ol {
        font-family: sans-serif;
        font-size: 14px;
        font-weight: normal;
        margin: 0;
        margin-bottom: 15px; 
      }
        p li,
        ul li,
        ol li {
          list-style-position: inside;
          margin-left: 5px; 
      }

      a {
        color: #3498db;
        text-decoration: underline; 
      }

      /* -------------------------------------
          BUTTONS
      ------------------------------------- */
      .btn {
        box-sizing: border-box;
        width: 100%; }
        .btn > tbody > tr > td {
          padding-bottom: 15px; }
        .btn table {
          width: auto; 
      }
        .btn table td {
          background-color: #ffffff;
          border-radius: 5px;
          text-align: center; 
      }
        .btn a {
          background-color: #ffffff;
          border: solid 1px #3498db;
          border-radius: 5px;
          box-sizing: border-box;
          color: #3498db;
          cursor: pointer;
          display: inline-block;
          font-size: 14px;
          font-weight: bold;
          margin: 0;
          padding: 12px 25px;
          text-decoration: none;
          text-transform: capitalize; 
      }

      .btn-primary table td {
        background-color: #3498db; 
      }

      .btn-primary a {
        background-color: #3498db;
        border-color: #3498db;
        color: #ffffff; 
      }

      /* -------------------------------------
          OTHER STYLES THAT MIGHT BE USEFUL
      ------------------------------------- */
      .last {
        margin-bottom: 0; 
      }

      .first {
        margin-top: 0; 
      }

      .align-center {
        text-align: center; 
      }

      .align-right {
        text-align: right; 
      }

      .align-left {
        text-align: left; 
      }

      .clear {
        clear: both; 
      }

      .mt0 {
        margin-top: 0; 
      }

      .mb0 {
        margin-bottom: 0; 
      }

      .preheader {
        color: transparent;
        display: none;
        height: 0;
        max-height: 0;
        max-width: 0;
        opacity: 0;
        overflow: hidden;
        mso-hide: all;
        visibility: hidden;
        width: 0; 
      }

      .powered-by a {
        text-decoration: none; 
      }

      hr {
        border: 0;
        border-bottom: 1px solid #f6f6f6;
        margin: 20px 0; 
      }

      /* -------------------------------------
          RESPONSIVE AND MOBILE FRIENDLY STYLES
      ------------------------------------- */
      @media only screen and (max-width: 620px) {
        table.body h1 {
          font-size: 28px !important;
          margin-bottom: 10px !important; 
        }
        table.body p,
        table.body ul,
        table.body ol,
        table.body td,
        table.body span,
        table.body a {
          font-size: 16px !important; 
        }
        table.body .wrapper,
        table.body .article {
          padding: 10px !important; 
        }
        table.body .content {
          padding: 0 !important; 
        }
        table.body .container {
          padding: 0 !important;
          width: 100% !important; 
        }
        table.body .main {
          border-left-width: 0 !important;
          border-radius: 0 !important;
          border-right-width: 0 !important; 
        }
        table.body .btn table {
          width: 100% !important; 
        }
        table.body .btn a {
          width: 100% !important; 
        }
        table.body .img-responsive {
          height: auto !important;
          max-width: 100% !important;
          width: auto !important; 
        }
      }

      /* -------------------------------------
          PRESERVE THESE STYLES IN THE HEAD
      ------------------------------------- */
      @media all {
        .ExternalClass {
          width: 100%; 
        }
        .ExternalClass,
        .ExternalClass p,
        .ExternalClass span,
        .ExternalClass font,
        .ExternalClass td,
        .ExternalClass div {
          line-height: 100%; 
        }
        .apple-link a {
          color: inherit !important;
          font-family: inherit !important;
          font-size: inherit !important;
          font-weight: inherit !important;
          line-height: inherit !important;
          text-decoration: none !important; 
        }
        #MessageViewBody a {
          color: inherit;
          text-decoration: none;
          font-size: inherit;
          font-family: inherit;
          font-weight: inherit;
          line-height: inherit;
        }
        .btn-primary table td:hover {
          background-color: #34495e !important; 
        }
        .btn-primary a:hover {
          background-color: #34495e !important;
          border-color: #34495e !important; 
        } 
      }

    </style>
  </head>"""
    bodytest += f"""

  <body>
    <span class="preheader">This is preheader text. Some clients will show this text as a preview.</span>
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body">
      <tr>
        <td>&nbsp;</td>
        <td class="container">
          <div class="content">

            <!-- START CENTERED WHITE CONTAINER -->
            <table role="presentation" class="main">

              <!-- START MAIN CONTENT AREA -->
              <tr>
                <td class="wrapper">
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="background-color: #34495e;height: 100px;color: white;"> <img src="https://gaiadhi.net/assets/images/gaiadhi-logo.png" style="width: 45%;
                        align-items: center;
                        display: block;
                        margin-left: auto;
                        margin-right: auto;"></td>
                    </tr>
                  </table>
                  <br><br>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                    <tr>
                      <td>
                        <p>Hello {data['email']},</p>
                        <p>You have requested to reset your password. Please click the following link to reset your password:</p>
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="btn btn-primary">
                          <tbody>
                            <tr>
                              <td align="left">
                                <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                                  <tbody>
                                    <tr>
                                      <td> <a href="https://gaiadhi.net/#/resetPassword/{data['email']}" target="_blank">Reset Password Here</a> </td>
                                    </tr>
                                  </tbody>
                                </table>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <p>If you did not request a password reset, please ignore this email.</p>
                        <p>Good Luck and Happy Data Surfing.</p>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

            <!-- END MAIN CONTENT AREA -->
            </table>
            <!-- END CENTERED WHITE CONTAINER -->

            <!-- START FOOTER -->
            <div class="footer">
              <table role="presentation" border="0" cellpadding="0" cellspacing="0">
               
                <tr>
                  <td class="content-block powered-by">
                    Powered by <a href="http://htmlemail.io">Holos</a>.
                  </td>
                </tr>
              </table>
            </div>
            <!-- END FOOTER -->

          </div>
        </td>
        <td>&nbsp;</td>
      </tr>
    </table>
  </body>
</html>

"""
    # reset_url = f'{settings.RESET_PASSWORD_URL}/{uid}/{token}/'
    msg = EmailMultiAlternatives(
        subject="Reset Password",
        body=bodytest,
        from_email=settings.EMAIL_HOST_USER,
        to=Email_To,
    )
    msg.attach_alternative(bodytest, "text/html")
    msg.send()
    return JsonResponse(
        {"response": "SUCCESS", "errorCode": 200, "errorMsg": "success"}, status=400
    )


@csrf_exempt
def PasswordChange(request, id):
    """
    This fuction will allow to our data
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Registration.objects.get(id=id)
    except Registration.DoesNotExist:
        return HTTPResponse(status=404)

    # print(snippet)

    if (
        request.method == "GET"
    ):  # its show the data by using slug if the slug is exsist its show the data other wise its show 404 error
        serializer = Pdfinfo_details_serializers(snippet, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )

    elif (
        request.method == "PUT"
    ):  # its update the data if method type is put Then its check all details are correct or not if all details are correct its update the previous data
        data = JSONParser().parse(request)
        # print(data)
        encryptedpassword = make_password(data["password"])
        print("data", encryptedpassword)
        # key = Fernet.generate_key()
        # fernet = Fernet(key)
        # encryptedpassword = fernet.encrypt(data['password'].encode())
        data["password"] = str(encryptedpassword)
        print("datatest", str(encryptedpassword))
        # mymodel = Registration.objects.get(email=id)
        infodata = {"password": data["password"]}
        serializer = Registration_serializers(snippet, data=infodata)
        if serializer.is_valid():
            print(data)
            serializer.save()
            return JsonResponse(
                {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
                safe=False,
            )
        return JsonResponse(
            {"response": serializer.errors, "errorCode": 200, "errorMsg": "success"},
            status=400,
        )


@csrf_exempt
def packageUpdate(request, id):
    """
    This fuction will allow to our data
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Registration.objects.get(id=id)
    except Registration.DoesNotExist:
        return HTTPResponse(status=404)

    # print(snippet)

    if (
        request.method == "GET"
    ):  # its show the data by using slug if the slug is exsist its show the data other wise its show 404 error
        serializer = Pdfinfo_details_serializers(snippet, many=True)
        return JsonResponse(
            {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
            safe=False,
        )

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = Registration_serializers(snippet, data=data)
        if serializer.is_valid():
            print(data)
            serializer.save()
            return JsonResponse(
                {"response": serializer.data, "errorCode": 200, "errorMsg": "success"},
                safe=False,
            )
        return JsonResponse(
            {"response": serializer.errors, "errorCode": 200, "errorMsg": "success"},
            status=400,
        )
