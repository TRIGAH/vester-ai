from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON  # Import JSON type

db = SQLAlchemy()

class UploadedFile(db.Model):
    __tablename__ = "uploaded_files"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)
    more_data = db.Column(db.Text, nullable=True)
    categorized_sections = db.Column(JSON)  # Use JSON for structured storage