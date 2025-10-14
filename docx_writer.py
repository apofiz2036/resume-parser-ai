import os
from docx import Document

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_drive_service():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
             creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
    
    with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('drive', 'v3', credentials=creds)

def save_docx_to_gdive(gpt_response, filename, local_folder="output_docs"):
    drive_folder_id = "1I4mXcSEGKU16397FXzb0QQnwGbVzDnxQ"

    os.makedirs(local_folder, exist_ok=True)
    local_path = os.path.join(local_folder, filename)
    doc = Document()
    doc.add_paragraph(gpt_response if gpt_response else "Нет ответа от модели")
    doc.save(local_path)

    service = get_drive_service()

    file_metadata = {'name': filename}
    if drive_folder_id:
        file_metadata['parents'] = [drive_folder_id]

    media = MediaFileUpload(local_path, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()

    print(f"✅ Файл '{filename}' успешно загружен в Google Drive!")
    print(f"🔗 Ссылка на просмотр: {uploaded_file.get('webViewLink')}")

    return uploaded_file.get('id'), uploaded_file.get('webViewLink')