import json
from flask import Flask, request, jsonify, render_template
from models import db, UploadedFile
from config import Config
from services.file_handler import FileHandler
from services.text_extractor import TextExtractor
from utils.text_utils import clean_and_format_json
from flask_migrate import Migrate

app = Flask(__name__)
Config.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)  # Enable migrations


@app.before_request
def create_tables():
    """Ensure tables are created before the first request."""
    db.create_all()


@app.route("/")
def index():
    files = UploadedFile.query.all()
    return render_template("index.html", files=files)

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handles file uploads and content extraction."""
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if not file.filename or not FileHandler.allowed_file(file.filename):
        return jsonify({"error": "Invalid file format"}), 400

    file_path, filename = FileHandler.save_file(file)

    # Extract content
    if filename.endswith(".pdf"):
        extracted_text = TextExtractor.extract_from_pdf(file_path)
        extracted_text=clean_and_format_json(extracted_text)
    elif filename.endswith(".pptx"):
        extracted_text = TextExtractor.extract_from_pptx(file_path)
    else:
        return jsonify({"error": "Unsupported file format"}), 400

    new_file = UploadedFile(
        filename=filename,
        file_type=filename.rsplit(".", 1)[1].lower(),
        categorized_sections=extracted_text
    )
    
    db.session.add(new_file)
    db.session.commit()

    return jsonify({
        "message": "File uploaded successfully",
        "filename": filename,
        "categorized_sections": extracted_text
    }), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)




