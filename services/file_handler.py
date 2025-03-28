import os
from werkzeug.utils import secure_filename
from config import Config

class FileHandler:
    @staticmethod
    def allowed_file(filename):
        """Check if the file type is allowed."""
        return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    

    @staticmethod
    def save_file(file):
        """Save the uploaded file and return its path."""
        filename = secure_filename(file.filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(file_path)
        return file_path, filename
