from __future__ import print_function
import pickle
import os
import sys
import imghdr
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from mimetypes import MimeTypes

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no(valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_250453635125-eo2n8qctlotaivg6btnvgh5gr8bmae7p.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    # file_metadata = {
    #     'name': 'Invoices',
    #     'mimeType': 'application/vnd.google-apps.folder'
    # }
    # file = service.files().create(body=file_metadata,
    #                               fields='id').execute()
    # 1LZGb06usjNOvaVRDdLhblAYCw0N85xYj id folder where we'll upload our pictures
    folder_id = '1LZGb06usjNOvaVRDdLhblAYCw0N85xYj'
    for currentFile in os.listdir(sys.argv[1]):
        mime = MimeTypes()
        absFilePath = os.path.abspath(os.path.join(sys.argv[1], currentFile))
        if (os.path.isfile(absFilePath)):
            if imghdr.what(absFilePath) is not None:
                meme_file = {'name': currentFile, 'parents': [folder_id]}
                media = MediaFileUpload(
                    absFilePath, mimetype=mime.guess_type(absFilePath)[0])
                response = service.files().list(q="name='" + currentFile + "'").execute()
                if not response.get('files', []):
                    service.files().create(body=meme_file, media_body=media, fields='id').execute()
    print('all files uploaded')
# results = service.files().list(
#     pageSize=10, fields="nextPageToken, files(id, name)").execute()
# items = results.get('files', [])

# if not items:
#     print('No files found.')
# else:
#     print('Files:')
#     for item in items:
#         print(u'{0} ({1})'.format(item['name'], item['id']))


if __name__ == '__main__':
    main()
