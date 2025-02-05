from app.models import EmpRegistration, Registration
from app.serilizer import EmpRegistration_serializers, Registration_serializers
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from http.client import HTTPResponse
import os
from rest_framework.parsers import JSONParser
from django.contrib.auth.hashers import make_password, check_password
from cryptography.fernet import Fernet
from django.core.mail import EmailMultiAlternatives

@csrf_exempt
def empregistrationform(req):
    """
    This function is provide us a dispay and insertion in our database.
    """
    if req.method == "GET":  # its dispay the data
        queryset = EmpRegistration.objects.all()
        serializer = EmpRegistration_serializers(queryset, many=True)
        return JsonResponse({
            "response": serializer.data,
            "errorCode": 200,
            "errorMsg": "success"
        }, safe=False)

    elif req.method == "POST":  # its  save the data if data is json formate and  send it by valid user
        data = JSONParser().parse(req)

        encryptedpassword = make_password(data['password'])
        print("data", encryptedpassword)
        # key = Fernet.generate_key()
        # fernet = Fernet(key)
        # encryptedpassword = fernet.encrypt(data['password'].encode())
        data['password'] = str(encryptedpassword)
        print("datatest", str(encryptedpassword))

        serializer = EmpRegistration_serializers(data=data)
        if serializer.is_valid():
            # Directory
            # directory = str(data['orgid'])

            # s3.put_object(Bucket=bucket_name, Key=(directory+'/'))

            # # Parent Directory path
            # parent_dir = "./mediafiles/"
            # path = os.path.join(parent_dir, directory)

            # os.mkdir(path)
            # print("Directory '% s' created" % directory)
            serializer.save()
            return JsonResponse({
                "response": serializer.data,
                "errorCode": 200,
                "errorMsg": "success"
            }, status=201)
        return JsonResponse({
            "response": serializer.errors,
            "errorCode": 200,
            "errorMsg": "success"
        }, status=400)
    
@csrf_exempt
def getregistrationform(req,orgid):
    """
    This function is provide us a dispay and insertion in our database.
    """
    try:
        snippet = Registration.objects.filter(orgid=orgid)
    except Registration.DoesNotExist:
        return HTTPResponse(status=404)
    
    if req.method == "GET":  # its dispay the data
        # queryset = Registration.objects.all()
        serializer = Registration_serializers(snippet, many=True)
        return JsonResponse({
            "response": serializer.data,
            "errorCode": 200,
            "errorMsg": "success"
        }, safe=False)
    

@csrf_exempt
def emplogin(req):
    # if request.method == 'GET':

    if req.method == "POST":
        data = JSONParser().parse(req)
        mystring = "mani1"
        key = Fernet.generate_key()
        fernet = Fernet(key)

        email = data['email']
        print("email",email)
        password = data['password']
        datavalue = EmpRegistration.objects.raw(
            "SELECT * FROM app_empregistration WHERE email = %s", [email])
        for p in EmpRegistration.objects.raw("SELECT * FROM app_empregistration WHERE email = %s", [email]):
            print("data", p.password)
            print("status", p.status)
            if(p.status == 'Active'):
                if check_password(password, p.password):
                    serializer = EmpRegistration_serializers(datavalue, many=True)
                    return JsonResponse({
                        "response": serializer.data,
                        "errorCode": 200,
                        "errorMsg": "success"
                    }, safe=False)
                else:
                    return JsonResponse({
                        "response": 'Data Does Not Match',
                        "errorCode": 400,
                        "errorMsg": "failed"
                    }, safe=False)
            else:
                return JsonResponse({
                    "response": 'Account Not Activated',
                    "errorCode": 400,
                    "errorMsg": "faild"
                }, safe=False)
            
        # try:
        #     user = Registration.objects.filter(email=email)
        # except Registration.DoesNotExist:
        #     return None

        # print("user",user)

        # queryset = Registration.objects.get(email=data['email'])
        # print("queryset",queryset)
        # serializer = Registration_serializers(queryset, many=True)
        # decode = fernet.decrypt(serializer.data)



@csrf_exempt
def activateEmailsend(req):
    if req.method == "POST":
        data = JSONParser().parse(req)
        print(data['email'])
        Email_To = [data['email']]
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
        /* background-color: #3498db;  */
        padding: 10px;
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
                      <td style="background-color: #34495e;height: 100px;color: white;"> <img src="https://ezaitool.com/assets/images/ezaitool-logo-final.png" style="width: 45%;
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
                        <p>Dear {data['email']},</p>
                        <p>You have an account with ezaitool. Your organization id is {data['orgId']}.
                        </p>
                        <p>
                            Your employee/teammate/colleague ({data['empName']} and {data['empEmail']}) has requested access to tool.
Please click on Approve or Reject below to allow or disallow access for this teammate to the tool.
                        </p>
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="btn btn-primary">
                          <tbody>
                            <tr>
                              <td align="left">
                                <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                                  <tbody>
                                    <tr>
                                      <td> <a href="https://localhost:4200/#/statuschange/{data['email']}/{data['id']}/Approve" target="_blank">Approve</a> </td>&nbsp;&nbsp;
                                      <td> <a href="https://localhost:4200/#/statuschange/{data['email']}/{data['id']}/Reject" target="_blank" style="background: #ff3434;
                                        border: #ff2626;">Reject</a> </td>
                                    </tr>
                                  </tbody>
                                </table>
                              </td>
                            </tr>
                          </tbody>
                        </table>

                        <p>ezaitool converts unstructured data in documents to structured data and presents the data in Excel (csv) files and text files.</p>
                        <p>The tool leverages AI in terms of NLP (Natural Language Processing) in addition to OCR (Optical Character Recognition) in a simplified no code Business User Interface (BUI) enabling business users to utilize the most modern, technologically state of the art AI models and algorithms directly to business operations easily.
                        </p>
                        <p>(If you have any questions or comments or suggestions, please email them to info@ezaitool.com)</p>
                        <p>Sincerely,</p><br>
                        <p>
                            The EZAITOOL team<br>
Date: 7/12/2023<br>
https://www.ezaitool.com<br>
https://www.eprobito.com  <br>
                        </p>

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
                  <td class="content-block">
                    <span class="apple-link">Eprobit LLC, 3 Abbey Road, San Francisco CA 94102</span>
                    <br> Don't like these emails? <a href="">Unsubscribe</a>.
                  </td>
                </tr>
                <tr>
                  <td class="content-block powered-by">
                    Powered by <a href="https://www.ezaitool.com">Eprobito</a>.
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
        subject="Activate Your Employee Account ", body=bodytest, from_email=settings.EMAIL_HOST_USER, to=Email_To)
    msg.attach_alternative(bodytest, "text/html")
    msg.send()
    return JsonResponse({
        "response": "SUCCESS",
        "errorCode": 200,
        "errorMsg": "success"
    }, status=400)

@csrf_exempt
def empstatus_update(request, id):
    """
    This fuction will allow to our data
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = EmpRegistration.objects.get(id=id)
    except EmpRegistration.DoesNotExist:
        return HTTPResponse(status=404)

    if request.method == 'GET':  # its show the data by using slug if the slug is exsist its show the data other wise its show 404 error
        serializer = EmpRegistration_serializers(snippet, many=True)
        return JsonResponse({
            "response": serializer.data,
            "errorCode": 200,
            "errorMsg": "success"
        }, safe=False)

    elif request.method == 'PUT':  # its update the data if method type is put Then its check all details are correct or not if all details are correct its update the previous data
        data = JSONParser().parse(request)
        serializer = EmpRegistration_serializers(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "response": serializer.data,
                "errorCode": 200,
                "errorMsg": "success"
            }, safe=False)
        return JsonResponse({
            "response": serializer.errors,
            "errorCode": 200,
            "errorMsg": "success"
        }, status=400)
