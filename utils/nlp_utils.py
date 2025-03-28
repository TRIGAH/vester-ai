from utils.text_utils import categorize_section
def parse_text_with_nlp(text, section_keywords):
    """Categorizes extracted text using regex-based keyword matching."""
    sections = {}
    paragraphs = text.split("\n\n")  # Splitting by double newline to get paragraphs
    for para in paragraphs:
        title = para.split("\n")[0] if "\n" in para else "Untitled Section"
        category = categorize_section(title, para, section_keywords)
        sections[category] = para
    return sections