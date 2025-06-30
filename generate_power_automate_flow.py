import os
import json
import requests
from msal import PublicClientApplication

# Setup environment variables
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
tenant_id = os.environ['TENANT_ID']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']

authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["https://graph.microsoft.com/.default"]

# Authenticate with MSAL
app = PublicClientApplication(client_id, authority=authority)
result = app.acquire_token_by_username_password(username, password, scopes=scopes)

if "access_token" not in result:
    raise Exception(f"Failed to acquire token: {result.get('error_description')}")

access_token = result["access_token"]
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Define a simple Power Automate flow definition
flow_definition = {
    "name": "GitHubAutoFlow",
    "properties": {
        "definition": {
            "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
            "actions": {
                "Send_an_email": {
                    "type": "OpenApiConnection",
                    "inputs": {
                        "host": {
                            "connectionName": "shared_office365",
                            "operationId": "SendEmail",
                            "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365"
                        },
                        "parameters": {
                            "To": username,
                            "Subject": "Automated Flow Email",
                            "Body": "This email was sent by a programmatically created flow."
                        }
                    }
                }
            },
            "triggers": {
                "manual": {
                    "type": "Request",
                    "kind": "Http",
                    "inputs": {
                        "schema": {}
                    }
                }
            },
            "contentVersion": "1.0.0.0"
        },
        "displayName": "GitHub Auto Flow",
        "state": "Enabled"
    }
}

# Create the flow via Graph API
endpoint = "https://graph.microsoft.com/v1.0/users/{}/flows".format(username)
response = requests.post(endpoint, headers=headers, data=json.dumps(flow_definition))

if response.status_code == 201:
    print("✅ Flow created successfully.")
else:
    print(f"❌ Failed to create flow: {response.status_code} - {response.text}")
