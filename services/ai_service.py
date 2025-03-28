import os
import json
import logging
from openai import OpenAI
from services.ocr_service import OCRService
from dotenv import load_dotenv

class AIService:
    _client = None  # Class attribute to store OpenAI client

    @classmethod
    def initialize(cls):
        """Initialize the OpenAI client (only once)"""
        if cls._client is None:
            load_dotenv()  # Load environment variables
            api_key = os.getenv("API_KEY")
            if not api_key:
                raise ValueError("API_KEY is missing! Set it in environment variables or .env file.")
            cls._client = OpenAI(api_key=api_key)

    # @classmethod
    # def extract_pitch_deck_info(cls, pdf_path):
    #     """Extract structured information from a pitch deck using OpenAI API."""
    #     cls.initialize()  # Ensure client is initialized

    #     try:
    #         # Extract text from PDF
    #         text = OCRService.extract_text(pdf_path)
    #         if not text.strip():
    #             raise ValueError("OCR extraction failed: No text extracted from the PDF.")

    #         # Construct the prompt
    #         prompt = f"""
    #         Extract and return only the exact text from the following sections in the pitch deck: 
    #         "Problem", "Solution", "Market", "Business Model", "Team".

    #         **Input Document:**
    #         {text}

    #         **Return JSON Format:**
    #         {{
    #             "Problem": "Extracted text...",
    #             "Solution": "Extracted text...",
    #             "Market": "Extracted text...",
    #             "Business Model": "Extracted text...",
    #             "Team": "Extracted text..."
    #         }}
    #         """

    #         # Call OpenAI API
    #         response = cls._client.chat.completions.create(
    #             model="gpt-4",
    #             messages=[{"role": "user", "content": prompt}],
    #             temperature=0.1,
    #             max_tokens=2000
    #         )

    #         # Extract response content
    #         content = response.choices[0].message.content.strip()

    #         if not content:
    #             raise ValueError("OpenAI API returned an empty response.")

    #         # Parse JSON response
    #         return json.loads(content)

    #     except json.JSONDecodeError:
    #         logging.error("Error parsing JSON response from OpenAI.", exc_info=True)
    #         return {"error": "Invalid JSON format received from OpenAI."}

    #     except Exception as e:
    #         logging.error(f"Error extracting pitch deck info: {str(e)}", exc_info=True)
    #         return {"error": str(e)}
        
    @classmethod    
    def extract_pitch_deck_info(cls, pdf_path):
        """
        Extracts exact information from a pitch deck without reformulating.

        Args:
            pdf_path (str): Path to the pitch deck PDF file.

        Returns:
            LiteralString: Extracted structured information as a JSON string.
        """
        """Extract structured information from a pitch deck using OpenAI API."""
        cls.initialize()  # Ensure client is initialized
        
        try:
            # Extract text from PDF
            text = OCRService.extract_text(pdf_path)
            if isinstance(text, dict) and "error" in text:
                return json.dumps(text, indent=4)  # Return error as JSON string

            prompt = f"""
            Extract and return only the exact text from the following sections in the pitch deck. 
            Do not rephrase or summarize—only return the exact words.

            **Extract these sections as they appear:**
            - "Problem": The challenge or issue being addressed.
            - "Solution": The exact description of the solution.
            - "Market": Information about the target market.
            - "Business Model": How revenue is generated.
            - "Team": Names and roles of founders, advisors, and key members.

            **Input Document:**
            {text}

            **Return JSON in this format (with exact extracted text):**
            {{
                "Problem": "Extracted text...",
                "Solution": "Extracted text...",
                "Market": "Extracted text...",
                "Business Model": "Extracted text...",
                "Team": "Extracted text..."
            }}
            """

            response = cls._client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Extract only the exact text from the pitch deck sections and return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )

            extracted_text = response.choices[0].message.content
            return json.dumps(json.loads(extracted_text), indent=4)  # Ensure valid JSON string

        except json.JSONDecodeError:
            return json.dumps({"error": "Failed to parse AI response as JSON"}, indent=4)
        except Exception as e:
            return json.dumps({"error": f"Error extracting pitch deck information: {str(e)}"}, indent=4)

    # @staticmethod
    # def clean_extracted_data(raw_text):
    #     """Format extracted pitch deck data."""
    #     try:
    #         data = json.loads(raw_text)
    #         return json.dumps(data, indent=4)
    #     except json.JSONDecodeError:
    #         return "Invalid JSON format"
    @staticmethod
    def clean_extracted_data(raw_text: str) -> str:
        """
        Cleans and formats extracted pitch deck data for readability.
        
        Args:
            raw_text (str): The raw JSON string containing extracted information.
        
        Returns:
            str: A cleaned and formatted string representation of the extracted data.
        """
        try:
            # Parse the raw JSON string
            data = json.loads(raw_text)
            
            # Format the extracted data
            formatted_text = f"""
    **Problem:**
    {data.get("Problem", "N/A")}

    **Solution:**
    {data.get("Solution", "N/A")}

    **Market:**
    {data.get("Market", "N/A")}

    **Business Model:**
    {data.get("Business Model", "N/A")}

    **Team:**
    {data.get("Team", "N/A")}
    """.strip()
            
            return formatted_text
        except json.JSONDecodeError:
            return "Error: Invalid JSON format."