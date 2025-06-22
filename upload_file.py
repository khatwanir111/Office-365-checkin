import os, requests

token = requests.post(
  f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}/oauth2/v2.0/token",
  data={
    "grant_type":"client_credentials",
    "client_id":os.getenv("CLIENT_ID"),
    "client_secret":os.getenv("CLIENT_SECRET"),
    "scope":"https://graph.microsoft.com/.default"
  }).json().get("access_token")

file_content = "This is a test file uploaded via Microsoft Graph."
headers = {"Authorization": f"Bearer {token}", "Content-Type": "text/plain"}
upload_url = f"https://graph.microsoft.com/v1.0/me/drive/root:/automated_upload.txt:/content"
resp = requests.put(upload_url, headers=headers, data=file_content)
print(resp.status_code, resp.text)
