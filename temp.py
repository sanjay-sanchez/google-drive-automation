from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import re

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

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
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'creds.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=100, fields="nextPageToken, files(id,name,mimeType,parents)").execute()
    items = results.get('files', [])
    file_metadata = {
    'name': 'Invoices',
    'mimeType': 'application/vnd.google-apps.folder'
             }
    file = service.files().create(body=file_metadata,
                                    fields='id').execute()
    folid=file.get('id')
    count=0
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            #print(items)
            if (item['parents'][0]=='0AFNJvLv0WWqWUk9PVA' and item['name'].startswith("Copy") and item['name'].endswith(".mp4")):
                count+=1
                filemove(item['id'],creds,folid)
                print(item['name'],item['id'],item['mimeType'],item['parents'][0])
                
    print("total count",count)
def filemove(file_id,creds,folder_id):
    service = build('drive', 'v3', credentials=creds)
    file = service.files().get(fileId=file_id,
                                fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
# Move the file to the new folder
    file =service.files().update(fileId=file_id,
                                    addParents=folder_id,
                                    removeParents=previous_parents,
                                    fields='id, parents').execute()
    print("sucess")
        
if __name__ == '__main__':
    main()