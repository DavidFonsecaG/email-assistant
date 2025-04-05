from fastapi import FastAPI
from routes import emails, outlook_auth

app = FastAPI()

app.include_router(emails.router)
app.include_router(outlook_auth.router)

@app.get("/")
def read_root():
    return {"message": "Email Assistant"}

