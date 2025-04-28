from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import os
from msal import ConfidentialClientApplication
from utils.env import get_env_var
from db.database import SessionLocal
from datetime import datetime, timedelta
from models.tables import OAuthTokenTable


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
        db = SessionLocal()

        user_email = result["id_token_claims"]["preferred_username"]
        access_token = result["access_token"]
        refresh_token = result["refresh_token"]
        expires_in = result["expires_in"]

        expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

        existing = db.query(OAuthTokenTable).filter(OAuthTokenTable.user_email == user_email).first()
        if existing:
            existing.access_token = access_token
            existing.refresh_token = refresh_token
            existing.expires_at = expires_at
        else:
            new_token = OAuthTokenTable(
                user_email=user_email,
                access_token=access_token,
                refresh_token=refresh_token,
                expires_at=expires_at
            )
            db.add(new_token)

        db.commit()
        db.close()

        frontend_url = f"http://localhost:5173/mail?user_email={user_email}"
        return RedirectResponse(frontend_url)
    else:
        return {"error": result.get("error_description")}