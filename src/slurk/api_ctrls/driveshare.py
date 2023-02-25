from Google import Create_Service
from googleapiclient.http import MediaFileUpload

CLIENT_SERVICE_FILE = 'DRIVE.json' #file that will contain api auth
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = 'https://googleapis.com/auth/drive'

service = Create_Service(CLIENT_SERVICE_FILE, API_NAME, API_VERSION, SCOPES)

folder_id = "1DDqOWhkMa1TM43VOhbKFG4GLaqlz3joU" #folder id on google drive to store images

file_names = ['Apple1.png', 'Apple1Slice.png', 'Apple2.png', 'Apple2Slice.png']  #image list to upload
file_type = ['image/png']  #file type

for file_name, file_type in zip(file_names, file_type):
    file_metadata = {
        'name': file_names,
        'parents': [folder_id]
    }
    #uploading file from local directory to google drive
    media = MediaFileUpload(
        'images/thumbnails/{0}'.format(file_name), filetype=file_type)

    service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()


results = service.files().list(
    pageSize=10, fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])
if not items:
    print('No files found.')
else:
    print('Files:')

#getting file shareable link in form of list
file_data = []
for file_id in items:
    request_body = {
        'role': 'reader',
        'type': 'anyone'
    }
    response_permission = service.permissions().create(
        fileId=file_id,
        body=request_body).execute()

    response_share_link = service.file().get(
        fileId=file_id,
        fields='weViewLink'
    ).execute()

    if response_share_link:
        file_data.append(response_share_link)

print(file_data)
