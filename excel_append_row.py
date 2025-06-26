# Appends row to Excel table

import os, requests
from msal import PublicClientApplication

# Define workbook and table details
ITEM_ID = "your_excel_file_id"  # Get from OneDrive file metadata
TABLE_NAME = "Table1"

app = PublicClientApplication(
    os.environ["CLIENT_ID"],
    authority=f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}"
)
result = app.acquire_token_by_username_password(
    os.environ["USERNAME"], os.environ["PASSWORD"],
    scopes=["https://graph.microsoft.com/.default"]
)
token = result["access_token"]

# Append a row
url = f"https://graph.microsoft.com/v1.0/me/drive/items/{ITEM_ID}/workbook/tables/{TABLE_NAME}/rows/add"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

payload = {
    "values": [["Automated", "Row", "Insert", "GitHub", "✅"]]
}
requests.post(url, headers=headers, json=payload)
