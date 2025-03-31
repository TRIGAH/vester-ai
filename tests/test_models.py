import os
import unittest
import json
from flask import Flask
from models import db, UploadedFile
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class UploadedFileModelTest(unittest.TestCase):
    def setUp(self):
        # Create a Flask app configured for testing with PostgreSQL.
        self.app = Flask(__name__)
        
        # Build the PostgreSQL connection string from environment variables.
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_name = os.getenv("DB_NAME")
        db_port = os.getenv("DB_PORT")
        self.app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Initialize the database with the app.
        db.init_app(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_uploaded_file_creation(self):
        # Prepare test data.
        categorized_sections_data = {
            "Problem": "Test problem",
            "Solution": "Test solution",
            "Market": "Test market",
            "Business Model": "Test business model",
            "Team": "Test team"
        }
        more_data = {"extra": "value"}

        # Create a new UploadedFile instance.
        file_instance = UploadedFile(
            filename="test.pdf",
            file_type="pdf",
            more_data=json.dumps(more_data),  # storing extra data as a JSON string
            categorized_sections=categorized_sections_data  # SQLAlchemy will store this as JSON
        )

        # Add and commit the new file to the database.
        db.session.add(file_instance)
        db.session.commit()

        # Retrieve the instance by filename.
        retrieved_file = UploadedFile.query.filter_by(filename="test.pdf").first()
        self.assertIsNotNone(retrieved_file)
        self.assertEqual(retrieved_file.filename, "test.pdf")
        self.assertEqual(retrieved_file.file_type, "pdf")
        self.assertEqual(retrieved_file.categorized_sections, categorized_sections_data)
        
        # Also verify that the more_data field was stored as a JSON string.
        self.assertEqual(json.loads(retrieved_file.more_data), more_data)

if __name__ == "__main__":
    unittest.main()
