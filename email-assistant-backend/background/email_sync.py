from fastapi_utils.tasks import repeat_every
from db.database import SessionLocal
from models.tables import OAuthTokenTable
from routes.emails import sync_received_emails, sync_sent_emails
from msal import ConfidentialClientApplication
from utils.env import get_env_var
from datetime import datetime, timedelta

client_id = get_env_var("AZURE_CLIENT_ID")
client_secret = get_env_var("AZURE_CLIENT_SECRET")
tenant_id = get_env_var("AZURE_TENANT_ID")
authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["User.Read", "Mail.Read", "Mail.Send"]

msal_app = ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret
)

def register_background_tasks(app):
    @app.on_event("startup")
    @repeat_every(seconds=300)  # every 5 minutes
    def background_email_sync():
        db = SessionLocal()
        try:
            tokens = db.query(OAuthTokenTable).all()

            for token_row in tokens:
                user_email = token_row.user_email
                access_token = token_row.access_token
                refresh_token = token_row.refresh_token
                expires_at = token_row.expires_at

                if datetime.utcnow() >= expires_at:
                    print(f"Refreshing token for {user_email}")
                    result = msal_app.acquire_token_by_refresh_token(
                        refresh_token,
                        scopes=scopes
                    )
                    if "access_token" in result:
                        access_token = result["access_token"]
                        token_row.access_token = access_token
                        token_row.refresh_token = result["refresh_token"]
                        token_row.expires_at = datetime.utcnow() + timedelta(seconds=result["expires_in"])
                        db.commit()
                    else:
                        print(f"Failed to refresh token for {user_email}: {result.get('error_description')}")
                        continue

                try:
                    print(f"Syncing emails for {user_email}...")
                    sync_received_emails(token=access_token, user_email=user_email, db=db)
                    sync_sent_emails(token=access_token, user_email=user_email, db=db)
                except Exception as e:
                    print(f"Error syncing emails for {user_email}: {e}")

        finally:
            db.close()
