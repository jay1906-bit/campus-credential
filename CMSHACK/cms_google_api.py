# cms_google_api.py
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1️⃣ Path to your service account JSON
SERVICE_ACCOUNT_FILE = "service_account.json"

# 2️⃣ Define the scopes your app needs
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",  # for Google Sheets
    "https://www.googleapis.com/auth/drive"         # for Google Drive
]

# 3️⃣ Create credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# 4️⃣ Build the service object (Sheets API)
service = build('sheets', 'v4', credentials=credentials)

# 5️⃣ Example: read data from a spreadsheet
SPREADSHEET_ID = '1scuHemqjks2nomaRlLAl6UH1BZjM5RXHioexDUwkGpc'
RANGE_NAME = 'Certificates!A:D'


sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])

if not values:
    print("No data found.")
else:
    for row in values:
        print(row)
