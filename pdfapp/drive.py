import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class DriveUploader:
    def __init__(self):
        self.service_account_path = 'pdfapp/drive_creds.json'
        self.scope = 'https://www.googleapis.com/auth/drive'
        self.parent_folder_id = '1Ozz0SY1J9G5NkTUrVvTFotHnqdrFd0jN'
        self.service = self._authenticate()

    def _authenticate(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.service_account_path, scopes=[self.scope])
        return build('drive', 'v3', credentials=credentials)

    def _create_drive_folder(self, folder_name):
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [self.parent_folder_id]
        }
        folder = self.service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')

    def upload_files(self, local_folder_path):
        today = datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
        drive_folder_id = self._create_drive_folder(today)

        for filename in os.listdir(local_folder_path):
            if not filename.startswith('.'):
                file_path = os.path.join(local_folder_path, filename)
                file_metadata = {
                    'name': filename,
                    'parents': [drive_folder_id]
                }
                media = MediaFileUpload(file_path, mimetype='application/pdf')
                self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                os.remove(file_path)  # Delete file after upload

        print(f"All files from {local_folder_path} have been uploaded and deleted.")

# Usage
if __name__ == "__main__":
    LOCAL_FOLDER_PATH = 'files'
    uploader = DriveUploader()
    uploader.upload_files(LOCAL_FOLDER_PATH)
