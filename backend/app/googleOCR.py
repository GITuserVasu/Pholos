import subprocess
from google.cloud import vision
import io
import csv
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import boto3
from urllib3 import HTTPResponse
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path
from google.cloud import vision
from app.functions import handle_uploaded_file, handle_uploaded_file_1, handle_uploaded_file_2
from app.models import Case_Detiles, TextractJob, summary_details, pdfcount_details, UseCases
from app.serilizer import Case_Detiles_serializers, TextractJob_serializers, UseCases_serializers
from django.http import JsonResponse, FileResponse, Http404


s3_client = boto3.client('s3', region_name='us-east-1')
bucket_name = 'ocrnlp'
FilePath_2 = settings.MEDIA_ROOT+"/uplodedFiles/"
FilePath_1 = "/var/www/html/ocrApp/assets/temp/"

FilePath = settings.MEDIA_ROOT
ImgPath = "/var/www/html/ocrApp/assets/temp/images"


poppler_path_manual = '/usr/bin'

# poppler_path_manual = 'C:/Users/Manikanta/Downloads/poppler-0.68.0_x86 (1)/poppler-0.68.0_x86 (1)/poppler-0.68.0/bin'


@csrf_exempt
def googleOCR(request):

    file = request.FILES['file']
    caseid = request.POST.get('caseId')
    orgid = request.POST.get('orgid')
    path = request.POST.get('path')
   
    # FilePath_1 = settings.MEDIA_ROOT+"/uplodedFiles/apiImages/Output_0.jpg"
    FilePath_JSON = "/home/bitnami/AItools/AItoolkit/backend-python/myfirstapp.json"

    handle_uploaded_file_1(file)


    tempfilename = str(file).split(".")[0]
    tempfilename = tempfilename.replace(" ", "-")
    object_key = path+"/"+ tempfilename+"/"+str(file)
    print("object_key",object_key)
    print("object_key",file)
    print("file",tempfilename)
    # s3_client.upload_file(FilePath_1, bucket_name, "Output_0.jpg")
    s3_client.upload_file(FilePath_1 + str(file), bucket_name, object_key)

    print("FilePath_JSON",FilePath_JSON)



    # Load the service account JSON key
    client = vision.ImageAnnotatorClient.from_service_account_file(FilePath_JSON)
    # Load the image
    with io.open(FilePath_1, 'rb') as image_file:
        content = image_file.read()

    # Perform OCR
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    infoData = []
    # Print extracted text
    for text in texts:
        print(text.description)
        infoData.append(text.description)

    output_txt = FilePath_2  + "output_text.txt"
    with open(output_txt, 'w') as file_1:
            # Write the data to the file
                file_1.write(str(infoData))
    # object_key_txt = path+"/"+ tempfilename+"/"+tempfilename+"_text.txt"
    object_key_txt = "output_text.txt"
    s3_client.upload_file(output_txt, bucket_name, object_key_txt)

    # Update Case_Detiles table and textract_job table


    return JsonResponse({
        "data": infoData,
        "errorCode": 200,
        "errorMsg": "success"
    }, status=200)

@csrf_exempt
def mulltiPagesgoogleOCR(request):

    file = request.FILES['file']
    id = request.POST.get('caseId')
    orgid = request.POST.get('orgid')
    path = request.POST.get('path')
    try:
        snippet = Case_Detiles.objects.get(id=id)
    except Case_Detiles.DoesNotExist:
        return HTTPResponse(status=404)

    # FilePath_1 = settings.MEDIA_ROOT+"/uplodedFiles/apiImages/Output_0.jpg"
    FilePath_JSON = "/home/bitnami/AItools/AItoolkit/backend-python/myfirstapp.json"



    tempfilename = str(file).split(".")[0]
    tempfilename = tempfilename.replace(" ", "-")
    object_key = path+"/"+ tempfilename+"/"+str(file)
    # print("object_key",object_key)
    # print("object_key",file)
    # print("file",tempfilename)
    # s3_client.upload_file(FilePath_1, bucket_name, "Output_0.jpg")
    s3_client.upload_file(FilePath_1 + str(file), bucket_name, object_key)

    # print("FilePath_JSON",FilePath_JSON)

    # Create record in textract_job table
    output_file = tempfilename + ".csv"
    object_key_1 = path+"/"+ tempfilename+"/"+output_file
    textract_job = TextractJob.objects.create(
                file=file, job_id="Google AI", orgid=orgid, caseid=id, s3loc = object_key, csvpath = object_key_1)
    textract_job.save() 

    # Generating and saving the meta data in the database
    testinfo = subprocess.check_output(
                        [poppler_path_manual+'/pdfinfo', FilePath_1  + str(file)])
    print(testinfo)
    val_1 = summary_details(
        case_id=id, summary=testinfo, orgid=orgid)
    val_1.save()


    # Load the service account JSON key
    client = vision.ImageAnnotatorClient.from_service_account_file(FilePath_JSON)

    # START PDF TO JPEG CONVERT PROCESS HERE

    handle_uploaded_file_1(file)
    file = str(file)
    images = convert_from_path(
                FilePath_1 + file, 500, poppler_path=poppler_path_manual)
    pdfImagesList = []
    infoData_1 = []
    for i in range(len(images)):
                images[i].save(ImgPath+'Outputfinal_'+str(i) +
                               '.jpg', 'JPEG', quality=100)
                pdfImagesList.append(ImgPath+'Outputfinal_'+str(i) +
                               '.jpg')
                with io.open(ImgPath+'Outputfinal_'+str(i) +
                               '.jpg', 'rb') as image_file:
                    content = image_file.read()

                # Perform OCR
                image = vision.Image(content=content)
                response = client.text_detection(image=image)
                texts = response.text_annotations
                infoData = []
                # Print extracted text
                for text in texts:
                    # print(text.description)
                    infoData.append(text.description)
                
                infoData_1.append(infoData[0])

    # END PDF TO JPEG CONVERT PROCESS HERE
    #print("infoData_1", infoData_1)

    print("pdf to jpg convert done here", pdfImagesList)

    # Writing the text to a file and saving it in S3
    output_txt = FilePath_1  + "output_text.txt"
    with open(output_txt, 'w') as file_1:
            # Write the data to the file
                file_1.write(str(infoData_1))
    object_key_txt = path+"/"+ tempfilename+"/google_"+tempfilename+".txt"
    # object_key_txt = "output_text.txt"
    # object_key_txt = path+ tempfilename+"/output_text.txt"
    print(object_key_txt)
    print(output_txt)
    s3_client.upload_file(output_txt, bucket_name, object_key_txt)

    # Placeholder for saving a CSV file, right now it saves a dummy file
    output_file = tempfilename + ".csv"
    with open(FilePath_1 + output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['No Tables Found !'])
    object_key = path+"/"+ tempfilename+"/"+output_file
    s3_client.upload_file(output_file, bucket_name, object_key)

    # Place holder for saving Key/Values file
    kvlist = "No Field:Value list generated"
    textract_job.key_values = kvlist
    textract_job.save()

    casedetailasupdate = {
        "status": "Verified",
        "fileName": file
        }
    textract_job.text = infoData_1
    textract_job.save()
    print(casedetailasupdate)

    serializer = Case_Detiles_serializers(snippet, data=casedetailasupdate)
    if serializer.is_valid():
            serializer.save()

    return JsonResponse({
        "data": infoData_1,
        "errorCode": 200,
        "errorMsg": "success"
    }, status=200)



@csrf_exempt
def googleOCR_image(request):

    ts = request.FILES['file']
    caseid = request.POST.get('caseId')
    orgid = request.POST.get('orgid')
    path = request.POST.get('path')
    handle_uploaded_file(ts, path)
    ts = str(ts)
    images = convert_from_path(
                FilePath+ path + ts, 500, poppler_path=poppler_path_manual)
    pdfImagesList = []
    for i in range(len(images)):
                images[i].save(ImgPath+'Outputfinal_'+str(i) +
                               '.jpg', 'JPEG', quality=100)
                pdfImagesList.append('Outputfinal_'+str(i) +'.jpg')

    return JsonResponse({
        "data": pdfImagesList,
        "errorCode": 200,
        "errorMsg": "success"
    }, status=200)