import pytesseract
from pdf2image import convert_from_path

class OCRService:
    @staticmethod
    def extract_text(file_path):
        """Perform OCR on a scanned PDF."""
        try:
            images = convert_from_path(file_path)
            text = "\n".join([pytesseract.image_to_string(img) for img in images])
            return text if text.strip() else "No extractable text found"
        except Exception as e:
            return f"Error performing OCR: {str(e)}"

