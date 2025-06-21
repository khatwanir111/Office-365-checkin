import requests
import os

# Azure AD App credentials
TENANT_ID = 'your-tenant-id'
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
USER_ID = 'user@yourdomain.com'

# File to upload
LOCAL_FILE_PATH = 'example_upload.txt'  # Make sure this file exists locally
UPLOAD_FILENAME = os.path.basename(LOCAL_FILE_PATH)

# Microsoft Identity Platform endpoint
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0"

def get_access_token():
    payload = {
        'client_id': CLIENT_ID,
        'scope': 'https://graph.microsoft.com/.default',
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(AUTHORITY, data=payload)
    response.raise_for_status()
    return response.json()['access_token']

def upload_file_to_onedrive(access_token, user_id, file_path):
    upload_url = f"{GRAPH_ENDPOINT}/users/{user_id}/drive/root:/{UPLOAD_FILENAME}:/content"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/octet-stream'
    }
    with open(file_path, 'rb') as file_data:
        response = requests.put(upload_url, headers=headers, data=file_data)
    response.raise_for_status()
    return response.json()

def main():
    if not os.path.exists(LOCAL_FILE_PATH):
        print(f"❌ File not found: {LOCAL_FILE_PATH}")
        return

    access_token = get_access_token()
    result = upload_file_to_onedrive(access_token, USER_ID, LOCAL_FILE_PATH)

    print(f"✅ File uploaded successfully to OneDrive:")
    print(f"   Name: {result.get('name')}")
    print(f"   Size: {result.get('size')} bytes")
    print(f"   Web URL: {result.get('webUrl')}")

if __name__ == "__main__":
    main()
