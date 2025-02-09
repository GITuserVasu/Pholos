import boto3
from botocore.exceptions import ClientError
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from urllib3 import HTTPResponse
from app.functions import handle_uploaded_file, handle_uploaded_file_1
from django.http import HttpResponse
import csv
import json
from django.http import JsonResponse

@csrf_exempt
def download_file(request):
    path = request.GET.get('path')
    # Replace 'YOUR_ACCESS_KEY' and 'YOUR_SECRET_KEY' with your AWS credentials
    s3 = boto3.client('s3')
    #print("path: ", path)
    # Replace 'YOUR_BUCKET_NAME' and 'YOUR_FILE_KEY' with the appropriate values
    bucket_name = 'ocrnlp'
    file_key = path

    try:
        # Download the file from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_key)

        # Get the file content
        file_content = response['Body'].read()

        # Set the appropriate content-type header based on the file's MIME type
        content_type = response['ContentType']

        # Set the appropriate response headers
        response = HttpResponse(file_content, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename=' + file_key.split('/')[-1]

        return response
    except Exception as e:
        # Handle any exceptions that may occur during the download
        return HttpResponse(str(e), status=500)
    

def download_csv(request):
    path = request.GET.get('path')
    # Replace 'YOUR_ACCESS_KEY' and 'YOUR_SECRET_KEY' with your AWS credentials
    s3 = boto3.client('s3')

    # Replace 'YOUR_BUCKET_NAME' and 'YOUR_FILE_KEY' with the appropriate values
    bucket_name = 'ocrnlp'
    file_key = path

    try:
        # Download the file from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_key)

        # Read the CSV file content
        file_content = response['Body'].read().decode('utf-8')

        # Parse the CSV content into a list of dictionaries
        csv_data = csv.DictReader(file_content.splitlines())

        # Convert the CSV data to JSON
        json_data = json.dumps(list(csv_data))

        # Return the JSON response
        return JsonResponse(json_data, safe=False)
    except Exception as e:
        # Handle any exceptions that may occur during the download or conversion
        return JsonResponse({'error': str(e)}, status=500)