import os
from dotenv import load_dotenv
load_dotenv()
# class Config:
#     UPLOAD_FOLDER = "uploads"
#     ALLOWED_EXTENSIONS = {"pdf", "pptx"}
#     MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
#     SQLALCHEMY_DATABASE_URI = "sqlite:///files.db"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
    


#     @staticmethod
#     def init_app(app):
#         """Initialize application with necessary configurations."""
#         app.config.from_object(Config)
#         os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)




class Config:
    UPLOAD_FOLDER = "uploads"
    ALLOWED_EXTENSIONS = {"pdf", "pptx"}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    SECTION_KEYWORDS = {
    "Problem": ["problem", "pain point", "challenge"],
    "Solution": ["solution", "how it works"],
    "Market": ["market size", "opportunity", "industry"],
    "Business Model": ["revenue", "monetization", "business model"],
    "Team": ["team", "founders", "advisors"]
    }

    # PostgreSQL Configuration (update with your credentials)
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")  # Change if using a cloud database
    DB_PORT = os.getenv("DB_PORT")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        """Initialize application with necessary configurations."""
        app.config.from_object(Config)
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
