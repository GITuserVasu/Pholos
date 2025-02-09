import io
import os
import zipfile
# import StringIO
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse


# @csrf_exempt
# def getfiles(request):
#     # Files (local path) to put in the .zip
#     # FIXME: Change this (get paths from DB etc)
#     filenames = ["/tmp/file1.txt", "/tmp/file2.txt"]

#     # Folder name in ZIP archive which contains the above files
#     # E.g [thearchive.zip]/somefiles/file2.txt
#     # FIXME: Set this to something better
#     zip_subdir = "somefiles"
#     zip_filename = "%s.zip" % zip_subdir

#     # Open StringIO to grab in-memory ZIP contents
#     s = StringIO.StringIO()

#     # The zip compressor
#     zf = zipfile.ZipFile(s, "w")

#     for fpath in filenames:
#         # Calculate path for file in zip
#         fdir, fname = os.path.split(fpath)
#         zip_path = os.path.join(zip_subdir, fname)

#         # Add file, at correct path
#         zf.write(fpath, zip_path)

#     # Must close zip for all contents to be written
#     zf.close()

#     # Grab ZIP file from in-memory, make response with correct MIME-type
#     resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
#     # ..and correct content-disposition
#     resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

#     return resp
FilePath = "/var/www/html/ocrApp/assets/temp"


@csrf_exempt
def create_zip(request,file):
   
    fileName = file.split(".")
    
    fullFilename =fileName[0].replace(" ", "-")
    print(fileName[0]);
    # return;
    # file_paths = [
    #     './mediafiles/Baum-Phillip&Joan-0 premium ill to maturity-050120-r.pdf',
    # ]
    file_paths = [
        f'{FilePath}/{fullFilename}.csv',
        f'{FilePath}/{fullFilename}_text.txt',
        f'{FilePath}/{fullFilename}_kv.txt',
    ]
    buffer = io.BytesIO()

    # Create the zip file
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for file_path in file_paths:
            if os.path.exists(file_path):
                zip_file.write(file_path, os.path.basename(file_path))
            else:
                return HttpResponse(f"File not found: {file_path}", status=404)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{fullFilename}.zip"'

    return response