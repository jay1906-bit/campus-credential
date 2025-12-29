import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def upload_to_drive(file_path, file_name):
    """
    Uploads a file to Google Drive using OAuth token
    """

    if not os.path.exists("token.json"):
        raise Exception("token.json not found. Run OAuth authentication first.")

    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    service = build("drive", "v3", credentials=creds)

    file_metadata = {
        "name": file_name
    }

    media = MediaFileUpload(file_path, resumable=True)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, webViewLink"
    ).execute()

    return file["id"], file["webViewLink"]
