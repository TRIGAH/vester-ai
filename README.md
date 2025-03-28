# Flask File Upload & Parsing Service

This project is a Flask-based web application that allows users to upload PDF and PPTX files, parse their contents, store extracted data in PostgreSQL, and display results in a web dashboard. The application is containerized with Docker and uses Redis for caching.

## Features
- Upload PDF & PPTX files
- Extract text from files
- Store parsed content in PostgreSQL
- Display uploaded files in a web dashboard
- Dockerized setup with PostgreSQL and Redis

## Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone <repo-url>
cd <project-folder>
```

### 2️⃣ Setup Using Docker
```bash
docker-compose up --build
```
This will start:
- The Flask API (`http://localhost:5000`)
- PostgreSQL database
- Redis caching service

### 3️⃣ Manual Setup (Without Docker)
#### Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```
#### Setup Database
Create a PostgreSQL database and update `SQLALCHEMY_DATABASE_URI` in `flask_file_upload.py`.

#### Run Flask Application
```bash
python flask_file_upload.py
```

## API Endpoints

### 1️⃣ Upload File
**Endpoint:** `POST /upload`
- **Request:**
  - `file` (form-data): PDF or PPTX file
- **Response:**
  ```json
  {
      "message": "File uploaded successfully",
      "filename": "example.pdf",
      "extracted_text": "Extracted content here..."
  }
  ```

### 2️⃣ View Uploaded Files
**Endpoint:** `GET /`
- Displays a dashboard with uploaded files and extracted content.

## Environment Variables
- `SQLALCHEMY_DATABASE_URI`: PostgreSQL connection string
- `FLASK_ENV`: Set to `development` for debug mode

## Troubleshooting
- Ensure PostgreSQL is running and credentials are correct.
- Use `docker logs <container_id>` to check for errors.

## License
MIT License


# flask db init
# flask db migrate -m "Initial migration"
# flask db upgrade