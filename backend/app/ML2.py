import csv
from http.client import HTTPResponse
import os
import requests
import json
from django.http import HttpResponse

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser

from django.http import JsonResponse
import subprocess
import boto3

# Create your views here.

#########
""" @csrf_exempt
def prednow(predjson):
    print("In prednow")
    #reportfile = open_reporting_session("","")
    return JsonResponse({"statusCode": 200, "name": "test"}) """
#####


