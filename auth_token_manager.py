import os, json
from msal import PublicClientApplication, SerializableTokenCache

cache = SerializableTokenCache()
if os.path.exists("token_cache.json"):
    cache.deserialize(open("token_cache.json", "r").read())

app = PublicClientApplication(
    os.environ["CLIENT_ID"],
    authority=f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}",
    token_cache=cache
)

accounts = app.get_accounts()
if accounts:
    result = app.acquire_token_silent(["https://graph.microsoft.com/.default"], account=accounts[0])
else:
    result = app.acquire_token_by_username_password(
        os.environ["USERNAME"], os.environ["PASSWORD"],
        scopes=["https://graph.microsoft.com/.default"]
    )

print("✅ Access token:", result.get("access_token")[:30], "...")

# Save cache
with open("token_cache.json", "w") as f:
    f.write(cache.serialize())
