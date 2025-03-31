import unittest
from unittest.mock import patch, MagicMock, mock_open
import json
from services.text_extractor import TextExtractor

# Dummy replacement for the NLP parsing utility:
def dummy_parse_text_with_nlp(text, section_keywords):
    # For testing, simply return a dict with one key "Other" and the entire text as its value.
    return {"Other": text}

class TestTextExtractor(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data=b"dummy pdf content")
    @patch("services.text_extractor.PyPDF2.PdfReader")
    @patch("services.text_extractor.parse_text_with_nlp", side_effect=dummy_parse_text_with_nlp)
    @patch("services.text_extractor.AIService.extract_pitch_deck_info")
    def test_extract_from_pdf_fallback_to_ocr(self, mock_ai_service, mock_parse_nlp, mock_pdf_reader, mock_file_open):
        # Simulate PdfReader returning pages with no extractable text.
        dummy_page = MagicMock()
        dummy_page.extract_text.return_value = ""  # No text extracted from this page.
        fake_reader = MagicMock()
        fake_reader.pages = [dummy_page]
        fake_reader.metadata = {}  # No metadata.
        mock_pdf_reader.return_value = fake_reader

        # Simulate AIService.extract_pitch_deck_info returning a JSON string.
        ocr_response_dict = {
            "Problem": "OCR Problem text",
            "Solution": "OCR Solution text",
            "Market": "OCR Market text",
            "Business Model": "OCR Business Model text",
            "Team": "OCR Team text"
        }
        sample_ai_response = json.dumps(ocr_response_dict)
        mock_ai_service.return_value = sample_ai_response

        file_path = "dummy.pdf"  # The file path to use in the test.
        result = TextExtractor.extract_from_pdf(file_path)
        
        # Our dummy parse_text_with_nlp returns {"Other": <text>}, where <text> is the sample_ai_response.
        expected = {"Other": sample_ai_response}
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
