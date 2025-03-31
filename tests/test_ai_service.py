import unittest
from unittest.mock import patch, Mock
import json
from services.ai_service import AIService

class TestAIService(unittest.TestCase):
    @patch("services.ai_service.OCRService.extract_text")
    def test_extract_pitch_deck_info(self, mock_extract_text):
        # Set up the mock for OCRService.extract_text to return sample text.
        sample_text = "Sample pitch deck text."
        mock_extract_text.return_value = sample_text

        # New sample AI response with categorized_sections, filename, and message.
        sample_ai_response = (
            '{'
            '  "categorized_sections": {'
            '    "Business Model": "1-Click request from Geo-aware devices. SMS from any phone: \\u201cpickup @work in 5\\u201d. Book Trips, show Fleet status, trip history. Pre-specify locations with labels + coordinates to enable easy texting of pickup location. Google Maps integration: Lat/long for \\u201chome\\u2019, \\u201cbob-work\\u2019, \\u201calice-apt.",'
            '    "Market": "Professionals in American cities. Initial Service Area: Central SF to Start, Manhattan soon after. Focus on Urban service on-demand. Focus on SF/NYC to begin. Expand to LA, Chicago, Houston, PA, Dallas. This covers 50% of entire US market.",'
            '    "Problem": "Taxi-monopolies reduce quality of service. Medallions are expensive, Medallions cost ~$500k, and drivers underpaid. drivers make 31k for drivers/clients. No incentive/accountability for drivers/clients. Digital Hail can now make street hail unnecessary.",'
            '    "Solution": "UberCab Concept - A fast & efficient on-demand car service. Convenience of a cab in NYC + experience of a professional chauffeur. But in SF and NYC. Latest consumer web & device technology. Automate dispatch to reduce wait-time. Optimized fleets and incented drivers. The \\u201cNetJets of car service.",'
            '    "Team": "5 advisors & 15 clients now recruited."'
            '  },'
            '  "filename": "Uber-Pitch-Deck.pdf",'
            '  "message": "File uploaded successfully"'
            '}'
        )

        # Create a fake response object for the OpenAI client.
        fake_message = Mock()
        fake_message.content = sample_ai_response
        fake_choice = Mock(message=fake_message)
        fake_response = Mock()
        fake_response.choices = [fake_choice]
        
        # Set up AIService's _client to be a mock with the expected method.
        AIService._client = Mock()
        AIService._client.chat.completions.create.return_value = fake_response
        
        # Call the method under test.
        result = AIService.extract_pitch_deck_info("uploads/Uber-Pitch-Deck.pdf")
        
        # If the result is a string, convert it to a dictionary for assertion
        if isinstance(result, str):
            result = json.loads(result)
        
        # Convert the sample response to a dictionary for comparison.
        expected = json.loads(sample_ai_response)
        
        # Verify that the "Problem" section in categorized_sections matches expected.
        self.assertEqual(result.get("categorized_sections", {}).get("Problem"), 
                         expected.get("categorized_sections", {}).get("Problem"))

    def test_clean_extracted_data_success(self):
        sample_raw_json = (
            '{"Problem": "P", "Solution": "S", '
            '"Market": "M", "Business Model": "B", "Team": "T"}'
        )
        cleaned = AIService.clean_extracted_data(sample_raw_json)
        # Check that cleaned text contains expected section labels.
        self.assertIn("**Problem:**", cleaned)
        self.assertIn("P", cleaned)

    def test_clean_extracted_data_invalid_json(self):
        invalid_json = "invalid json"
        cleaned = AIService.clean_extracted_data(invalid_json)
        self.assertEqual(cleaned, "Error: Invalid JSON format.")

if __name__ == "__main__":
    unittest.main()
