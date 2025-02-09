import time
import math
import boto3
from botocore.exceptions import ClientError
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from urllib3 import HTTPResponse
#from app.functions import handle_uploaded_file, handle_uploaded_file_1, get_document_summary_nltk, get_document_summary_googleT5, get_search_results
from app.functions import handle_uploaded_file, handle_uploaded_file_1
import subprocess
import csv
import os
import os.path
from app.models import Case_Detiles, TextractJob, summary_details, pdfcount_details, UseCases
from app.serilizer import Case_Detiles_serializers, TextractJob_serializers, UseCases_serializers
#import pandas as pd
import sys
import re
from collections import defaultdict
import pathlib
from PyPDF2 import PdfFileReader

# Mani's local paths - uncomment for local testing
#FilePath_1 = settings.MEDIA_ROOT+"/uplodedFiles/"
#poppler_path_manual = 'C:/Users/Manikanta/Downloads/poppler-0.68.0_x86 (1)/poppler-0.68.0_x86 (1)/poppler-0.68.0/bin'

# Server paths
poppler_path_manual = '/usr/bin'
FilePath_1 = "/var/www/html/ocrApp/assets/temp/"

textract_client = boto3.client('textract', region_name='us-east-1')
s3_client = boto3.client('s3', region_name='us-east-1')
bucket_name = 'ocrnlp'

pdf_numpages = 0
objectkey_list =[]
job_id_list = []
job_id = ''

multicolumn_pdf = 0

class parBlock:
    def __init__(self, left):
        self.lines = []
        self.left = left

@csrf_exempt
def start_textract_job(request):
    
    pdf_numpages = 0
    objectkey_list =[]
    job_id_list = []
    job_id = ''
    job_id_string = ''

    pdf_numpages = 0
    objectkey_list =[]
    job_id_list = []
    job_id = ''

    file = request.FILES['file']
    caseid = request.POST.get('caseId')
    orgid = request.POST.get('orgid')
    path = request.POST.get('path')

    handle_uploaded_file_1(file)

    try:
        snippet = Case_Detiles.objects.get(id=caseid)
    except Case_Detiles.DoesNotExist:
        return HTTPResponse(status=404)

    # Uploading to S3 the user's file (PDF or JPG or PNG or TXT)
    tempfilename = str(file).split(".")[0]
    tempfilename = tempfilename.replace(" ", "-")
    object_key = path+"/"+ tempfilename+"/"+str(file)
    print("object_key",object_key)
    print("object_key",file)
    print("file",tempfilename)
    s3_client.upload_file(FilePath_1 + str(file), bucket_name, object_key)


    # Generate input file metadata and saving the same in the database
    if(str(file).split(".")[1] == "pdf" or str(file).split(".")[1] == "PDF"):
            testinfo = subprocess.check_output(
                        [poppler_path_manual+'/pdfinfo', FilePath_1 +"/" + str(file)])
            print(testinfo)
            val_1 = summary_details(
                case_id=caseid, summary=testinfo, orgid=orgid)
            val_1.save()
    else: 
            testinfo = subprocess.check_output(
                        ['file','-i', FilePath_1 +"/" + str(file)])
            print("testinfo", testinfo)
            testinfo2 = testinfo.decode('utf8').split(":")[1]
            print ("testinfo2", testinfo2)
            val_1 = summary_details(
                             case_id=caseid, summary=testinfo2, orgid=orgid)
            val_1.save()

    # if it is a PDF file, split into page wise pdfs
    # save each of these page pdfs on S3
    # start the textract jobs for each of the pages

    # find out number of pages in the pdf file
    if str(file).split(".")[1] == "pdf" or str(file).split(".")[1] == "PDF":
        pdf = PdfFileReader(FilePath_1 +"/" + str(file))
        pdf_numpages = pdf.getNumPages()
        # split pdf into a pdf per page
        testinfo = subprocess.check_output([poppler_path_manual+'/pdfseparate', FilePath_1 +"/" + str(file), FilePath_1 +"/" + tempfilename +"-%d.pdf"])
        for pagenum in range(pdf_numpages):
            pagenum = pagenum + 1
            objectkey_list.append(path +'/' + tempfilename +'/' + tempfilename +'-'+str(pagenum) + '.pdf')
        pagenum = 1
        for obj_key in objectkey_list:
            if pagenum <= pdf_numpages:
                s3_client.upload_file(FilePath_1 + tempfilename +'-'+ str(pagenum) +'.pdf', bucket_name, obj_key)
                pagenum = pagenum + 1
    else:
        objectkey_list.append(path+"/"+ tempfilename+"/"+str(file))

    try:
      if str(file).split(".")[1] == "pdf" or str(file).split(".")[1] == "PDF":
        pagenum = 1
        for obj_key in objectkey_list:
            response = textract_client.start_document_analysis(
            DocumentLocation={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': obj_key
                }
            },
            FeatureTypes=['TABLES', 'FORMS', 'SIGNATURES'],
            )
            print("jobs started", response['JobId'])
            job_id_list.append(response['JobId'])
            if pagenum == 1:
              job_id = response['JobId']
              print(f'Started Textract pdf job with ID: {job_id}')
            # saving case, job info and s3 file locations in database
              output_file = tempfilename +"-"+str(pagenum)+ ".csv"
              object_key_1 = path+"/"+ tempfilename+"/"+output_file
              textract_job = TextractJob.objects.create(
                file=file, job_id=job_id_list[0], orgid=orgid, caseid=caseid, s3loc = object_key, csvpath = object_key_1)
              textract_job.save()
            pagenum = pagenum + 1           
          
      else:
        if str(file).split(".")[1] != "txt":
           response = textract_client.start_document_analysis(
            DocumentLocation={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': object_key
                }
            },
            FeatureTypes=['TABLES', 'FORMS', 'SIGNATURES'],
            )
           
           job_id_list.append(response['JobId'])
           print("job id list in start textract job", job_id_list)
           job_id = response['JobId']
           print(f'Started Textract non pdf job with ID: {job_id}')
        # saving case, job info and s3 file locations in database
           output_file = tempfilename + ".csv"
           object_key_1 = path+"/"+ tempfilename+"/"+output_file
           textract_job = TextractJob.objects.create(
            file=file, job_id=job_id_list[0], orgid=orgid, caseid=caseid, s3loc = object_key, csvpath = object_key_1)
           textract_job.save()
        else:
            if str(file).split(".")[1] == "txt":
                output_file = tempfilename + ".csv"
                object_key_1 = path+"/"+ tempfilename+"/"+output_file
                textract_job = TextractJob.objects.create(
                   file=file, job_id="text-job", orgid=orgid, caseid=caseid, s3loc = object_key, csvpath = object_key_1)
            textract_job.save()


      if str(file).split(".")[1] == "txt":
         job_id_string = "txt"
      else:
         job_id_string = ' '.join([str(item) for item in job_id_list])
      textract_case = TextractJob.objects.get(caseid=caseid)
      textract_case.job_id_string = job_id_string
      textract_case.job_status = "Submitted"
      textract_case.save()
      casedetailasupdate = {
            "status": "Submitted"
            }
      #job_id_keys = list(range(len(job_id_list)))
      #job_id_values = job_id_list
      #job_id_dict = {job_id_keys[i]: job_id_values[i] for i in range(len(job_id_keys))}
        
    except ClientError as e:
        print(f'Error starting Textract job: {e}')
        casedetailasupdate = {
            "status": "Error-101"
            }
        textract_case = TextractJob.objects.get(caseid=caseid)
        textract_case.job_status = "Error-101"
        textract_case.save()
        serializer = Case_Detiles_serializers(snippet, data=casedetailasupdate)
        if serializer.is_valid():
                serializer.save()
        return JsonResponse(job_id_string, safe=False)
    return JsonResponse(job_id_string, safe=False)
    #    return JsonResponse({"statusCode":999, 'job_id': job_id})
    #return JsonResponse({"statusCode": 200, 'job_id': job_id})


@csrf_exempt
def get_textract_results(request):
    print("Am in get textract results")
    file_name = ''
    #job_id = request.POST.get('job_id')
    job_id_string = request.POST.get('job_id_string')
    print("job id string in get textract results", job_id_string)
    id = request.POST.get('caseId')
    file = request.POST.get('file')
    path = request.POST.get('path')
    tempfilename = str(file).split(".")[0]
    tempfilename = tempfilename.replace(" ", "-")
    searchtextwords = request.POST.get('searchtextwords')

    s3_client = boto3.client('s3', region_name='us-east-1')
    bucket_name = 'ocrnlp'

    try:
        snippet = Case_Detiles.objects.get(id=id)
    except Case_Detiles.DoesNotExist:
        return HTTPResponse(status=404)
    text = []
    text4summ = []
    key_map = {}
    value_map = {}
    blocks_map = {}
    table_blocks = []
    numPage = 0
    output_file = FilePath_1 + tempfilename + ".csv"
    with open(output_file, 'w', newline='') as csvfile:
              writer = csv.writer(csvfile)
              writer.writerow("Tables")

    try:
     if str(file).split(".")[1] != "txt" :
      print("Am in file is not a text file")
      print("job id string", job_id_string)
      job_id_items_list = job_id_string.split(' ')
      lines = []
      for job_id_item in job_id_items_list:
        print("job_id_item", job_id_item)
        response = textract_client.get_document_analysis(JobId=job_id_item)
        status = response['JobStatus']
    #    print("status",status)
    #    retries = 5
    #    backoff = 6
        while status == 'IN_PROGRESS':
    #      if retries > 0 :  
            response = textract_client.get_document_analysis(JobId=job_id_item)
            status = response['JobStatus']
    #   #     print("status1",status)
    #        backoff = backoff * 10
    #        retries = retries - 1
    #        time.sleep(60)
        if status == 'SUCCEEDED':
            # Process the text results here
        #    print("status2",status)
            newResponse = response
            if multicolumn_pdf == 1:
               numPage = numPage + 1    
            lineElements = []
            summlineElements = []
            pageNums = []
            endflag = 0
            runflag = 1
            
            class Line:
                  def __init__(self, text, top, left, width, height, centerX, centerY):
                      self.text = text
                      self.top = top
                      self.left = left
                      self.width = width
                      self.height = height
                      self.centerX = centerX
                      self.centerY = centerY

            while runflag == 1:  
              if multicolumn_pdf == 1:
               for block in newResponse["Blocks"]:
                   if block['BlockType'] == 'LINE':
                       box = block['Geometry']['BoundingBox']
                       center_result = calculate_center(box['Top'], box['Left'], box['Width'], box['Height'])
                       centerX = center_result[0]
                       centerY = center_result[1]
                       lines.append(Line(block['Text'], box['Top'], box['Left'], box['Width'], box['Height'],centerX, centerY))
                      
            #   new_blocks = partition_into_blocks(lines)
            #   sorted_blocks = sort_blocks(new_blocks)
            #   for blox in sorted_blocks:
            #       for line in blox.lines:
            #         print(line.text)

            # Start of text extraction setup
              if numPage == 1:
                documentMetadata = response['DocumentMetadata']
            #    print("documentMetadata:", documentMetadata)
              if multicolumn_pdf == 0:
               numLine = 0
               for block in newResponse['Blocks']:
                #print(block)
                 if block['BlockType'] == 'PAGE':
                    if(numPage > 0):
                      pageNums.append("Page Num  ")
                      pageNums.append(str(numPage))
                      pageNums.append("\n")
                      text.append(pageNums)
                      text.append(lineElements)
                      text4summ.append(summlineElements)
                      pageNums = []
                      lineElements = []
                      summlineElements = []
                    numPage = numPage + 1
                   #numLine = 0
                 elif block['BlockType'] == 'LINE':
                    #   box = block['Geometry']['BoundingBox']
                    #   center_result = calculate_center(box['Top'], box['Left'], box['Width'], box['Height'])
                    #   centerX = center_result[0]
                    #   centerY = center_result[1]
                    #   lines.append(Line(block['Text'], box['Top'], box['Left'], box['Width'], box['Height'],centerX, centerY))

                    numLine = numLine +1
                    lineElements.append("P")
                    lineElements.append(numPage)
                    lineElements.append(":L")
                    lineElements.append(numLine)
                    lineElements.append("  ")
                    lineElements.append(block['Text'])
                    lineElements.append("\n")
                    summlineElements.append(block['Text'])
                    summlineElements.append("\n")
               pageNums.append("Page Num  ")
               pageNums.append(str(numPage))
               pageNums.append("\n")
               text.append(pageNums)
               text.append(lineElements)
               text4summ.append(summlineElements)
               pageNums = []
               lineElements = []      
               summlineElements = []
            #  print("text per response", text)
            # End of text extraction setup
            
            # Start of table & forms extraction setup
            
              blocks = newResponse['Blocks']
               #print(blocks)
              for block in blocks:
                  block_id = block['Id']
                  blocks_map[block_id] = block
                  if block['BlockType'] == "TABLE":
                       table_blocks.append(block) 
                  if block['BlockType'] == "KEY_VALUE_SET":
                      if 'KEY' in block['EntityTypes']:
                         key_map[block_id] = block
                      else:
                         value_map[block_id] = block 

            # End of table & forms extraction setup

              if endflag == 1:
                 break
              if 'NextToken' in newResponse:
                 newResponse = textract_client.get_document_analysis(JobId=job_id_item, NextToken=newResponse["NextToken"] )
                 if 'NextToken' not in newResponse:
                    endflag = 1
              else:
                  break
              # End of while loop

      # Text Extraction per page
            if multicolumn_pdf == 1:
              new_blocks = partition_into_blocks(lines)
              sorted_blocks = sort_blocks(new_blocks)
              for blox in sorted_blocks:
                for line in blox.lines:
                    # numLine = numLine +1
                    # lineElements.append("P")
                    # lineElements.append(numPage)
                    # lineElements.append(":L")
                    # lineElements.append(numLine)
                    # lineElements.append("  ")
                    lineElements.append(line.text)
                    lineElements.append("\n")
                    print(line.text)
        #pageNums.append("Page Num  ")
        #pageNums.append(str(numPage))
        #pageNums.append("\n")
        #text.append(pageNums)
        if multicolumn_pdf == 1:
          text.append(lineElements)
          pageNums = []
          lineElements = []      
          print(text)
      # End of Text Extraction

      # Key Value Extraction      
      kvs = get_kv_relationship(key_map, value_map, blocks_map)
      #print("\n\n== FOUND KEY : VALUE pairs ===\n")
      #print_kvs(kvs)
      # Key Value Extraction ends

      # Table Extraction 
      table_csv = get_table_csv_results(table_blocks,blocks_map)
      #print("table_csv",table_csv)
      #print("table_csv_len",len(table_csv))
            #if len(table_csv) > 0:          
      with open(output_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if (table_csv != "<b> NO Table FOUND </b>"):
                  for row in table_csv:
                      for item in row:
                         writer.writerow(item.values())
                  writer.writerow([])
                else:
                  writer.writerow("  ")    

            # Table Extraction Ends

            # Save Key Value extract in a file and S3
      kvlist = []      
      kvoutput_txt = FilePath_1 + tempfilename + "_kv.txt"
      with open(kvoutput_txt, 'w') as file_2:
                # Write the data to the file
                    file_2.write("== FOUND KEY : VALUE pairs ===\n")
                    for key, value in kvs.items():
                        #print(key, ":", value)
                        kvlist.append(str(key) +" : "+ str(value))
                        kvlist.append("\n")
                        file_2.write(str(key))
                        file_2.write(":")
                        file_2.write(str(value))
                        file_2.write("\n")
      object_key_txt = path+"/"+ tempfilename+"/"+tempfilename+"_kv.txt"
      s3_client.upload_file(kvoutput_txt, bucket_name, object_key_txt)

            # Save Key Value extract in a file and S3 ends

            # flattened_data = {}
            # for dictionary in table_csv:
            #     for key, value in dictionary.items():
            #         flattened_data.update(value)
            
            # print("flattened_data",flattened_data)
            # rows = [v for k, v in table_csv.items()]
            #     # Convert the dictionary to a DataFrame
            # df = pd.DataFrame(rows)

            # # Specify the output Excel file path
            # # output_file = "outputMani.xlsx"

            # # Write the DataFrame to Excel
            # df.to_csv(output_file, index=False)

            # print(f"Excel file '{output_file}' created successfully.")
            # with open(output_file, "at") as fout:
            #     fout.write(table_csv)

            #S3 BUCKET STORAGE HERE

            #EXCEL FILE STORE
      object_key = path+"/"+ tempfilename+"/"+tempfilename+".csv"
      s3_client.upload_file(output_file, bucket_name, object_key)

           
            # for block in response['Blocks']:
            #     if block['BlockType'] == 'LINE':
            #         text.append(block['Text'])



             # TXT FILE STORE
      output_txt = FilePath_1 + tempfilename + "_text.txt"
      with open(output_txt, 'w') as file_1:
                # Write the data to the file
                    file_1.write(str(text))
      object_key_txt = path+"/"+ tempfilename+"/"+tempfilename+"_text.txt"
      s3_client.upload_file(output_txt, bucket_name, object_key_txt)

# Run the preset search
      print("in async", searchtextwords)
      search_results = get_search_results(str(text), searchtextwords)
      print("in async", search_results)

# Get the summary of the document
      nltk_summ = get_document_summary_nltk(str(text4summ))   
      nltk_summ = nltk_summ.replace("','", "")   
      googleT5_summ = get_document_summary_googleT5(str(text4summ))
      print("google", googleT5_summ)
      googleT5_summ = googleT5_summ.replace("<pad>","")
      googleT5_summ = googleT5_summ.replace("<unk>n","")
      googleT5_summ = googleT5_summ.replace("<unk>","")
      googleT5_summ = googleT5_summ.replace("</s>","")
      googleT5_summ = googleT5_summ.replace("[","")
      googleT5_summ = googleT5_summ.replace("]","")
      googleT5_summ = googleT5_summ.replace("''","")
      lengsumm = len(googleT5_summ)
      print ("lengsumm", lengsumm)
      add_string = "\n"
      n = 1
      for i in range(int(lengsumm)):
         if n*i >= 80:
             googleT5_summ = googleT5_summ[:i] + add_string + googleT5_summ[i:]
             n = n/2
      print("google with line breaks", googleT5_summ)
      # Save in S3
      nltksumm_txt = FilePath_1 + tempfilename + "_nltksumm.txt"
      with open(nltksumm_txt, 'w') as file_1:
                # Write the data to the file
                    file_1.write(str(nltk_summ))
      object_key_txt = path+"/"+ tempfilename+"/"+tempfilename+"_nltksumm.txt"
      s3_client.upload_file(nltksumm_txt, bucket_name, object_key_txt)
      
      googleT5summ_txt = FilePath_1 + tempfilename + "_googleT5summ.txt"
      with open(googleT5summ_txt, 'w') as file_1:
                # Write the data to the file
                    file_1.write(str(googleT5_summ))
      object_key_txt = path+"/"+ tempfilename+"/"+tempfilename+"_googleT5summ.txt"
      s3_client.upload_file(googleT5summ_txt, bucket_name, object_key_txt)

      summary_record = summary_details.objects.get(case_id=id)
      summary_record.nltksumm = str(nltk_summ)
      summary_record.googleT5summ = str(googleT5_summ)
      summary_record.save()
            
            # Retrieve the page count and document count from the database
      org_id = path.split("/")[0]
      print("ORGID", org_id)
      pdfcount = pdfcount_details.objects.get(orgid=org_id)
      doc = pdfcount.document
      doc = doc + 1
      pdfcount.document = doc
      pages = pdfcount.pages
      pages = pages + pdf_numpages
      pdfcount.pages = pages
      pdfcount.save()
      print(job_id_items_list[0])
            # Retrieve the Textract job object from the database
      textract_job = TextractJob.objects.get(job_id=job_id_items_list[0])
      #print("textract_job", textract_job)
            
# Save the results to the database
      print("Saving results to the database\n")
      print(text)
      print("this was the text to be saved in the database")
      textract_job.text = text
      textract_job.key_values = kvlist
      textract_job.job_status = "Verified"
      textract_job.search_results = search_results
      #print("Textract Job Text", textract_job.text)
      #print("Textract Key Value", textract_job.key_values)    
      textract_job.save()
      casedetailasupdate = {
            "status": "Verified",
            "fileName": file
            }
      print(casedetailasupdate)

      serializer = Case_Detiles_serializers(snippet, data=casedetailasupdate)
      if serializer.is_valid():
                serializer.save()
      return JsonResponse({"statusCode": 200, 'data': text, 'nltk_summ':nltk_summ, 'googleT5_summ':googleT5_summ , 'search_results': search_results })
     else:
            if str(file).split(".")[1] == "txt":
               input_file = FilePath_1 + str(file)
               with open(input_file, 'r') as infile:
                  textfiledata = infile.read()
                  textfiledata = textfiledata.replace(",","\n")
               #textfiledata.append("Text file same as original file")
               #print("textfiledata",textfiledata)
               textract_job = TextractJob.objects.get(job_id="text-job", caseid = id)

               output_file = FilePath_1 + tempfilename + ".csv"
               with open(output_file, 'w', newline='') as csvfile:
                  writer = csv.writer(csvfile)
                  writer.writerow(['No Tables Found !'])

            #S3 BUCKET STORAGE HERE
               s3_client = boto3.client('s3', region_name='us-east-1')
               bucket_name = 'ocrnlp'

            #EXCEL FILE STORE IN S3
               object_key = path+"/"+ tempfilename+"/"+output_file
               s3_client.upload_file(output_file, bucket_name, object_key)

            # TXT FILE STORE IN S3
               output_txt = FilePath_1 + tempfilename + "_text.txt"
               with open(output_txt, 'w') as file_1:
                # Write the data to the file
                    file_1.write(str(textfiledata))
               object_key_txt = path+"/"+ tempfilename+"/"+output_txt
               s3_client.upload_file(output_txt, bucket_name, object_key_txt)

            # Save the results to the database
               textract_job.text = textfiledata   
               textract_job.job_status = "Verified"
               textract_job.save()
               casedetailasupdate = {
                  "status": "Verified",
                  "fileName": file
                }
               serializer = Case_Detiles_serializers(snippet, data=casedetailasupdate)
               if serializer.is_valid():
                   serializer.save()
               return JsonResponse({"statusCode": 200, 'data': textfiledata})
            else:
               casedetailasupdate = {
               "status": "Error"
               }
               serializer = Case_Detiles_serializers(snippet, data=casedetailasupdate)
               if serializer.is_valid():
                   serializer.save()
               return JsonResponse({'error': 'Analysis job failed'})
    except ClientError as e:
        casedetailasupdate = {
            "status": "Error"
            }
        serializer = Case_Detiles_serializers(snippet, data=casedetailasupdate)
        if serializer.is_valid():
                serializer.save()
        return JsonResponse({'error': e})

@csrf_exempt
def get_textract_results_by_caseid(request,id):
    s3_client = boto3.client('s3', region_name='us-east-1')
    bucket_name = 'ocrnlp'
    try:
        snippet = TextractJob.objects.filter(caseid=id)
        snippet2 = TextractJob.objects.get(caseid=id)
    except TextractJob.DoesNotExist:
        return HTTPResponse(status=404)
    filename = snippet2.file
    

    csvfilename = filename.replace(".pdf", ".csv")
    csvfilename = filename.replace(".PDF", ".csv")
    csvfilename = csvfilename.replace(".txt", ".csv")
    
    csvs3loc = snippet2.s3loc
    csvs3loc = csvs3loc.replace(".pdf", ".csv")
    csvs3loc = csvs3loc.replace(".PDF", ".csv")
    csvs3loc = csvs3loc.replace(".txt", ".csv")
    print("Hahahahaha")
    print(csvs3loc)
    csvfilename = csvfilename.split(".")[0]
    csvfilename = csvfilename.replace(" ", "-") + ".csv"
    print(csvfilename)
    if os.path.isfile(FilePath_1 + filename) == False:
        s3_client.download_file(bucket_name, snippet2.s3loc, "/var/www/html/ocrApp/assets/temp/"+ filename)
    if os.path.isfile(FilePath_1 + csvfilename) == False:
        s3_client.download_file(bucket_name, snippet2.csvpath, "/var/www/html/ocrApp/assets/temp/"+ csvfilename)

    queryset = TextractJob.objects.all()
    serializer = TextractJob_serializers(snippet, many=True)
    return JsonResponse({
        "response": serializer.data,
        "errorCode": 200,
        "errorMsg": "success"
    }, safe=False)

@csrf_exempt
def pdf_view(request):
    print("Hi")
    try:
        return FileResponse(open(r'mediafiles\uplodedFiles\sample.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()
    

def extract_table_data(blocks):
    table_data = []
    for block in blocks:
        if block['BlockType'] == 'CELL':
            cell_text = block['Text']
            confidence = block['Confidence']
            child_ids = block['Relationships'][0]['Ids'] if 'Relationships' in block and 'Ids' in block['Relationships'][0] else []
            table_data.append({'Cell Text': cell_text, 'Confidence': confidence, 'Child IDs': child_ids})
            # table_data.append({'Cell Text': cell_text, 'Confidence': confidence})
    return table_data


def get_table_csv_results(table_blocks, blocks_map):

    # print(blocks)
    if len(table_blocks) <= 0:
        return "<b> NO Table FOUND </b>"
    csvvalue = []
    for index, table in enumerate(table_blocks):
        csv = generate_table_csv(table, blocks_map, index + 1)
        # csv += '\n\n'
        # for valueHere in csv:
        #     print("valueHere",valueHere)
        csvvalue.append(csv)
        #print("csvcsv",csv)
        # In order to generate separate CSV file for every table, uncomment code below
        #inner_csv = ''
        #inner_csv += generate_table_csv(table, blocks_map, index + 1)
        #inner_csv += '\n\n'
        #output_file = file_name + "___" + str(index) + ".csv"
        # replace content
        #with open(output_file, "at") as fout:
        #    fout.write(inner_csv)

    return csvvalue

def generate_table_csv(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)
    #print("rowsrowsrows",rows)
    table_id = str(table_index)
    converted_data = []
    for key, values in rows.items():
        converted_row = {}
        for sub_key, sub_value in values.items():
            if sub_value.strip() != '':
                converted_row[sub_key] = sub_value.strip()
        if converted_row:
            converted_data.append(converted_row)
    # get cells.
    #print("dataAppand",converted_data)
    csv = '{0}\n\n'.format(table_id)
    # print("csvcsvcsvcsv",csv)
    for row_index, cols in rows.items():
        for col_index, text in cols.items():
            csv += format(text)
        csv += '\n'
    #print("csvcsvcsvcsv",csv)
    # csv += '\n\n\n'
    return converted_data

def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                try:
                    cell = blocks_map[child_id]
                    if cell['BlockType'] == 'CELL':
                        row_index = cell['RowIndex']
                        col_index = cell['ColumnIndex']
                        if row_index not in rows:
                            # create new row
                            rows[row_index] = {}

                        # get the text value
                        rows[row_index][col_index] = get_text(cell, blocks_map)
                except KeyError:
                    print("Error extracting Table data - {}:".format(KeyError))
                    pass
    # print("rows",rows)
    return rows

def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    try:
                        word = blocks_map[child_id]
                        if word['BlockType'] == 'WORD':
                            text += word['Text'] + ' '
                        if word['BlockType'] == 'SELECTION_ELEMENT':
                            if word['SelectionStatus'] == 'SELECTED':
                                text += 'X '
                    except KeyError:
                        print("Error extracting Table data - {}:".format(KeyError))
    # print("text here",text)

    return text



def get_children_ids(block):
    for rels in block.get('Relationships', []):
        if rels['Type'] == 'CHILD':
            yield from rels['Ids']


def map_blocks(blocks, block_type):
    return {
        block['Id']: block
        for block in blocks
        if block['BlockType'] == block_type
    }



def get_text_content(block_id, blocks_map):
    block = blocks_map[block_id]
    if 'Relationships' in block:
        for relationship in block['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    return get_text_content(child_id, blocks_map)
    elif block['BlockType'] == 'WORD':
        return block['Text']


def get_table_data(table_block, blocks):
    table_data = []
    blocks_map = {block['Id']: block for block in blocks}
    for relationship in table_block['Relationships']:
        if relationship['Type'] == 'CHILD':
            for cell_id in relationship['Ids']:
                if cell_id in blocks_map:
                    cell_block = blocks_map[cell_id]
                    if cell_block['BlockType'] == 'CELL':
                        cell_text = get_text_content(cell_id, blocks_map)
                        if cell_text:
                            table_data.append(cell_text)
                else:
                    print(f"Cell Block with ID {cell_id} not found in the blocks list.")
    return table_data


def csv_file_to_store():
    with open('test.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            # Extract values from the CSV row
            column1 = row[0]
            column2 = row[1]
            column3 = int(row[2])

# following 4 routines are for Key: value extraction 

def get_kv_relationship(key_map, value_map, blocks_map):
    kvs = defaultdict(list)
    for block_id, key_block in key_map.items():
        value_block = find_value_block(key_block, value_map)
        key = get_text_kv(key_block, blocks_map)
        val = get_text_kv(value_block, blocks_map)
        kvs[key].append(val)
    return kvs


def find_value_block(key_block, value_map):
    for relationship in key_block['Relationships']:
        if relationship['Type'] == 'VALUE':
            for value_id in relationship['Ids']:
                value_block = value_map[value_id]
    return value_block


def get_text_kv(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] == 'SELECTED':
                            text += 'X '

    return text


def print_kvs(kvs):
    for key, value in kvs.items():
        print(key, ":", value)

@csrf_exempt
def get_usecasedata(request,useCaseparam):
    #fullPath = pathlib.Path(FilePath_1)
    #UCpath = fullPath.parent
    #fileName = str(UCpath) + "/USECASES/" +useCaseparam +".txt"
    #with open(fileName, 'r') as f:
    #    UCdata = f.readlines()

    industry = useCaseparam.split("-")[0]
    print(industry)
    title = useCaseparam.split("-")[1]
    print(title)

    try:
        UCdata = UseCases.objects.get(industry=industry)
    except UseCases.DoesNotExist:
        return HTTPResponse(status=404)
    
    serializer = UseCases_serializers(UCdata)
    
    return JsonResponse({
          "response": serializer.data,
          "errorCode": 200,
          "errorMsg": "success"
        }, safe=False)

def pretty_similar(x, x1, tolerance):
    return abs(x - x1) < tolerance

def calculate_center(top, left, width, height):
    x = left
    y = top
    x1 = left + width
    y1 = top - height
    xCenter = (x + x1) / 2
    yCenter = (y + y1) / 2
    return [xCenter, yCenter]

def distance(x, y, x1, y1):
    dx = max(x1 - x, x - x1, 0)
    dy = max(y1 - y, y - y1, 0)
    return math.sqrt(dx * dx + dy * dy)

def sort_blocks(blocks):
    sorted_blocks = [blocks[0]]  # Title as the first
    while len(sorted_blocks) != len(blocks):
        target_block = block_most_left([b for b in blocks if b not in sorted_blocks])
        sorted_blocks.append(target_block)
    return sorted_blocks

def block_most_left(blocks):
    most_left = blocks[0].left
    result = blocks[0]
    for block in blocks:
        if block.left < most_left:
            most_left = block.left
            result = block
    return result

# class parBlock:
#     def __init__(self, left):
#         self.lines = []
#         self.left = left

def partition_into_blocks(all_lines):
    lines = all_lines
    parblocks = []
    
    left_tolerance = 0.06
    distance_tolerance = 0.06
    
    while lines:
        parblock = parBlock(0)
        target_line = lines[0]
        same_left = target_line.left
        parblock.left = same_left
        lines_to_remove = []
        
        for line in lines:
            width_tolerance = max(0.4, abs(target_line.width - line.width) / 2)
            if (
                pretty_similar(same_left, line.left, left_tolerance) and
                (
                    pretty_similar(target_line.width, line.width, width_tolerance) or
                    distance(
                        parblock.lines[-1].centerX, parblock.lines[-1].centerY,
                        line.centerX, line.centerY
                    ) < distance_tolerance
                )
            ):
                parblock.lines.append(line)
                lines_to_remove.append(line)
        
        for line in lines_to_remove:
            lines.remove(line)
        
        parblocks.append(parblock)
    
    return parblocks

