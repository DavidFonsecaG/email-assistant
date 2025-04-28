from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import emails, outlook_auth
from background import email_sync

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(emails.router)
app.include_router(outlook_auth.router)

@app.get("/")
def read_root():
    return {"message": "Email Assistant"}