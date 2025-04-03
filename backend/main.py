from fastapi import FastAPI
from routes import leads, emails, outlook_auth

app = FastAPI()

app.include_router(leads.router)
app.include_router(emails.router)
app.include_router(outlook_auth.router)

@app.get("/")
def read_root():
    return {"message": "Sales Assistant API is running!"}

