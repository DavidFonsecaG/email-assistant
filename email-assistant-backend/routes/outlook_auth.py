from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import os
from msal import ConfidentialClientApplication
from utils.env import get_env_var 

router = APIRouter()

client_id = get_env_var("AZURE_CLIENT_ID")
client_secret = get_env_var("AZURE_CLIENT_SECRET")
tenant_id = get_env_var("AZURE_TENANT_ID")
redirect_uri = get_env_var("AZURE_REDIRECT_URI")

authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["User.Read", "Mail.Send"]

msal_app = ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret
)

@router.get("/auth/login")
def login():
    auth_url = msal_app.get_authorization_request_url(
        scopes=["User.Read", "Mail.Read", "Mail.Send"],
        redirect_uri=redirect_uri,
    )
    return RedirectResponse(auth_url)

@router.get("/auth/callback")
def auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Missing auth code"}
    
    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=scopes,
        redirect_uri=redirect_uri
    )

    if "access_token" in result:
        return {
            "access_token": result["access_token"], 
            "user_info": {
                "name": result["id_token_claims"]["name"], 
                "email": result["id_token_claims"]["preferred_username"]
            }
        }
    else:
        return {"error": result.get("error_description")}