from db.database import Base, engine
from models.tables import EmailDraftTable, EmailTable, AttachmentTable

print("Creating database...")
Base.metadata.create_all(bind=engine)
print("Database created successfully!")
