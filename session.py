import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

# Load environment variables from .env file
load_dotenv()

# Define roles and permissions
roles_permissions = {
    "admin": ["Cashflow Tracking", "GPS Reporting", "Analysis", "Management", "Reset"],
    "manager": ["Cashflow Tracking", "GPS Reporting", "Analysis"],
    "user": ["Cashflow Tracking", "GPS Reporting"]
}

# Function to check permissions
def has_permission(role, section):
    return section in roles_permissions.get(role, [])

# Function to authenticate user with Authentik
def authenticate_user():
    auth_url = os.getenv("AUTHENTIK_URL")
    client_id = os.getenv("AUTHENTIK_CLIENT_ID")
    client_secret = os.getenv("AUTHENTIK_CLIENT_SECRET")
    redirect_uri = f"{os.getenv('APP_FQDN')}/callback"
    scope = "openid profile email"

    auth_response = requests.get(
        auth_url,
        params={
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": scope
        },
        auth=HTTPBasicAuth(client_id, client_secret)
    )
    return True, "admin"
    # if auth_response.status_code == 200:
    #     return True, "admin"  # Placeholder for role assignment
    # else:
    #     return False, None
