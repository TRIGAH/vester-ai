import os
import unittest
import tempfile
from unittest.mock import MagicMock
from services.file_handler import FileHandler
from config import Config

# A dummy file-like object for testing
class DummyFile:
    def __init__(self, filename, content=b"dummy content"):
        self.filename = filename
        self.content = content

    def save(self, file_path):
        with open(file_path, "wb") as f:
            f.write(self.content)

class TestFileHandler(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for uploads and override Config.UPLOAD_FOLDER.
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_upload_folder = Config.UPLOAD_FOLDER
        Config.UPLOAD_FOLDER = self.temp_dir.name

    def tearDown(self):
        # Restore the original upload folder and clean up the temporary directory.
        Config.UPLOAD_FOLDER = self.original_upload_folder
        self.temp_dir.cleanup()

    def test_allowed_file_valid(self):
        # Test allowed_file for valid file types.
        self.assertTrue(FileHandler.allowed_file("document.pdf"))
        self.assertTrue(FileHandler.allowed_file("presentation.pptx"))
        # Test for an invalid file type.
        self.assertFalse(FileHandler.allowed_file("malicious.exe"))

    def test_save_file(self):
        # Create a dummy file object with known content.
        dummy_file = DummyFile("test.pdf", b"Sample content")
        file_path, filename = FileHandler.save_file(dummy_file)
        # Verify that the file was saved.
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, "rb") as f:
            self.assertEqual(f.read(), b"Sample content")
        # Verify that the filename is as expected.
        self.assertEqual(filename, "test.pdf")

if __name__ == "__main__":
    unittest.main()
