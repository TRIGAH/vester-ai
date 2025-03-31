import os
import unittest
import json
from io import BytesIO
from unittest.mock import patch
from app import create_app, db, UploadedFile
from config import Config

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        # Create the Flask app in testing mode.
        self.app = create_app()
        self.app.config["TESTING"] = True
        
        # Override the upload folder with a temporary directory.
        self.temp_upload_dir = os.path.join(os.getcwd(), "temp_uploads")
        os.makedirs(self.temp_upload_dir, exist_ok=True)
        Config.UPLOAD_FOLDER = self.temp_upload_dir
        
        self.client = self.app.test_client()
        
        # Create tables in the test database.
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop all tables.
        with self.app.app_context():
            db.drop_all()
        # Clean up the temporary uploads directory.
        for f in os.listdir(self.temp_upload_dir):
            os.remove(os.path.join(self.temp_upload_dir, f))
        os.rmdir(self.temp_upload_dir)

    def test_index_route(self):
        # Test that the index route (GET "/") returns a 200 status code.
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    @patch("app.TextExtractor.extract_from_pdf")
    @patch("app.clean_and_format_json")
    def test_upload_valid_pdf(self, mock_clean, mock_extract_pdf):
        # Simulate a valid PDF file upload.
        dummy_pdf_content = b"%PDF-1.4 dummy pdf content"
        # Fake the extracted text from the PDF.
        sample_extracted_json = (
            '{"Problem": "Test Problem", '
            '"Solution": "Test Solution", '
            '"Market": "Test Market", '
            '"Business Model": "Test BM", '
            '"Team": "Test Team"}'
        )
        mock_extract_pdf.return_value = sample_extracted_json
        mock_clean.return_value = sample_extracted_json
        
        data = {
            "file": (BytesIO(dummy_pdf_content), "test.pdf")
        }
        response = self.client.post("/upload", data=data, content_type="multipart/form-data")
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data.get("message"), "File uploaded successfully")
        self.assertEqual(response_data.get("filename"), "test.pdf")
        # Check that the response includes the expected extracted problem text.
        self.assertIn("Test Problem", response_data.get("categorized_sections", ""))

    def test_upload_no_file(self):
        # Test the upload endpoint with no file provided.
        response = self.client.post("/upload", data={}, content_type="multipart/form-data")
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertEqual(response_data.get("error"), "No file part")

    def test_upload_invalid_file_format(self):
        # Test the upload endpoint with an invalid file extension.
        dummy_content = b"dummy content"
        data = {
            "file": (BytesIO(dummy_content), "test.exe")
        }
        response = self.client.post("/upload", data=data, content_type="multipart/form-data")
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertEqual(response_data.get("error"), "Invalid file format")

if __name__ == "__main__":
    unittest.main()
