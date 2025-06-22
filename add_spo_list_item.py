import os, requests

token = requests.post(
  f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}/oauth2/v2.0/token",
  data={
    "grant_type":"client_credentials",
    "client_id":os.getenv("CLIENT_ID"),
    "client_secret":os.getenv("CLIENT_SECRET"),
    "scope":"https://graph.microsoft.com/.default"
  }).json().get("access_token")

headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
site_id = os.environ["SITE_ID"]
list_id = os.environ["LIST_ID"]

item = {
    "fields": {
        "Title": "Graph-generated list item"
    }
}
resp = requests.post(f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items", headers=headers, json=item)
print(resp.status_code, resp.text)
