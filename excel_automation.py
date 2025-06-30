import os, requests
from msal import PublicClientApplication

app = PublicClientApplication(os.environ["CLIENT_ID"], authority=f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}")
token = app.acquire_token_by_username_password(
    os.environ["USERNAME"], os.environ["PASSWORD"],
    scopes=["https://graph.microsoft.com/.default"]
)["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Create file
resp = requests.put(
    "https://graph.microsoft.com/v1.0/me/drive/root:/AutoSheet.xlsx:/content",
    headers=headers,
    data=""
)
file_id = resp.json()["id"]

# Add table
table = {
    "address": "A1:C1",
    "hasHeaders": True
}
requests.post(f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/workbook/worksheets('Sheet1')/tables/add",
              headers=headers, json=table)

# Add header + data rows
headers_row = { "values": [["Name", "Score", "Bonus"]] }
requests.post(f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/workbook/worksheets('Sheet1')/range(address='A1:C1')",
              headers=headers, json=headers_row)

rows = { "values": [["Alice", 85, "=B2*0.1"], ["Bob", 92, "=B3*0.1"]] }
requests.post(f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/workbook/tables('Table1')/rows/add",
              headers=headers, json=rows)
