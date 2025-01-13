import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Define the Google Drive API scopes and service account file path
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "client_secret_799854351159-gplth67h5fm0aqk4lu83522v0phaajlt.apps.googleusercontent.com.json"



def authenticate():
    creds = None
    if (os.path.exists('token.pickle')):
        with open('token.pickle','rb') as token:
            creds = pickle.load(token)
    if (not creds or not creds.valid):
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(SERVICE_ACCOUNT_FILE,SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle','wb') as token:
            pickle.dump(creds,token)
    service = build('drive','v3',credentials=creds)
    return service


def list_folders(service):
    query = "mimeType = 'application/vnd.google-apps.folder'"
    try:
        results = service.files().list(q=query,fields="nextPageToken,files(id,name)").execute()
        items = results.get('files',[])

        if (not items):
            print("no items")
        else :
            print("folders")
            for item in items:
                print(f"item {item.name} id: {item.id}")
    except Exception as e:
        print(e)



# Create credentials using the service account file
# credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# # Build the Google Drive service
# drive_service = build('drive', 'v3', credentials=credentials)

# def create_folder(folder_name, parent_folder_id=None):
#     """Create a folder in Google Drive and return its ID."""
#     folder_metadata = {
#         'name': folder_name,
#         "mimeType": "application/vnd.google-apps.folder",
#         'parents': [parent_folder_id] if parent_folder_id else []
#     }

#     created_folder = drive_service.files().create(
#         body=folder_metadata,
#         fields='id'
#     ).execute()

#     print(f'Created Folder ID: {created_folder["id"]}')
#     return created_folder["id"]

# def list_folder(parent_folder_id=None, delete=False):
#     """List folders and files in Google Drive."""
#     results = drive_service.files().list(
#         q=f"'{parent_folder_id}' in parents and trashed=false" if parent_folder_id else None,
#         pageSize=1000,
#         fields="nextPageToken, files(id, name, mimeType)"
#     ).execute()
#     items = results.get('files', [])

#     if not items:
#         print("No folders or files found in Google Drive.")
#     else:
#         print("Folders and files in Google Drive:")
#         for item in items:
#             print(f"Name: {item['name']}, ID: {item['id']}, Type: {item['mimeType']}")
#             if delete:
#                 delete_files(item['id'])

# def delete_files(file_or_folder_id):
#     """Delete a file or folder in Google Drive by ID."""
#     try:
#         drive_service.files().delete(fileId=file_or_folder_id).execute()
#         print(f"Successfully deleted file/folder with ID: {file_or_folder_id}")
#     except Exception as e:
#         print(f"Error deleting file/folder with ID: {file_or_folder_id}")
#         print(f"Error details: {str(e)}")

# # def download_file(file_id, destination_path):
# #     """Download a file from Google Drive by its ID."""
# #     request = drive_service.files().get_media(fileId=file_id)
# #     fh = io.FileIO(destination_path, mode='wb')
    
# #     downloader = MediaIoBaseDownload(fh, request)
    
# #     done = False
# #     while not done:
# #         status, done = downloader.next_chunk()
# #         print(f"Download {int(status.progress() * 100)}%.")

if __name__ == '__main__':
    service = authenticate()
    list_folders(service)
#     # Example usage:

#     # Create a new folder
#     create_folder("MyNewFolder")
    
#     # List folders and files
#     # list_folder()
    
#     # Delete a file or folder by ID
#     # delete_files("your_file_or_folder_id")

#     # Download a file by its ID
#     # download_file("your_file_id", "destination_path/file_name.extension")
