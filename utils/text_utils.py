import re
import json

def clean_text(text):
    """Removes unwanted characters, multiple spaces, and newlines from text."""
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Remove special characters
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces and newlines
    return text.lower()

def categorize_section(title, text, section_keywords):
    """Categorizes sections based on keywords."""
    content = clean_text(f"{title} {text}")  # Clean text before matching
    for section, keywords in section_keywords.items():
        keyword_pattern = re.compile(r"\b(" + "|".join(re.escape(kw) for kw in keywords) + r")\b", re.IGNORECASE)
        if keyword_pattern.search(content):
            return section
    return "Other"



def clean_and_format_json(raw_data):
    """Extracts and formats JSON from a string-embedded dictionary."""
    json_string = raw_data.get("Problem", "")

    try:
        cleaned_data = json.loads(json_string)
    except json.JSONDecodeError:
        cleaned_data = {}

    return cleaned_data