import unittest
from unittest.mock import patch, MagicMock
from services.ocr_service import OCRService

class TestOCRService(unittest.TestCase):
    @patch("services.ocr_service.convert_from_path")
    @patch("services.ocr_service.pytesseract.image_to_string")
    def test_extract_text_success(self, mock_image_to_string, mock_convert_from_path):
        # Setup: simulate convert_from_path returning a list of dummy images.
        dummy_images = [MagicMock(), MagicMock()]
        mock_convert_from_path.return_value = dummy_images
        
        # Setup: simulate pytesseract returning different text for each image.
        mock_image_to_string.side_effect = ["Text from image 1", "Text from image 2"]

        # Call the OCR extraction function.
        result = OCRService.extract_text("dummy/path.pdf")

        # Expected result is the concatenation of the two strings separated by newline.
        expected = "Text from image 1\nText from image 2"
        self.assertEqual(result, expected)

    @patch("services.ocr_service.convert_from_path")
    def test_extract_text_failure(self, mock_convert_from_path):
        # Simulate an exception during conversion (e.g., file not found or other error).
        mock_convert_from_path.side_effect = Exception("Test error")

        result = OCRService.extract_text("dummy/path.pdf")
        self.assertIn("Error performing OCR: Test error", result)

if __name__ == "__main__":
    unittest.main()
