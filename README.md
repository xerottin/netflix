# **Streamify** - A Netflix-Like Streaming Platform

## Overview
Streamify is a backend project designed to provide a seamless video streaming experience, similar to Netflix. It supports real-time interactions, scalable data management, and high-performance API handling.

## Technologies Used
- **FastAPI** - High-performance web framework for APIs.
- **SQLAlchemy** - ORM for efficient database management.
- **WebSockets** - Real-time communication support.
- **Pydantic** - Data validation and settings management.
- **PostgreSQL** - Relational database for structured data.
- **MongoDB** - NoSQL database for flexible data storage.

## Running the Project Locally

### 1. Clone the Repository
```bash
    git clone https://github.com/xerottin/streamify.git
```

### 2. Install Dependencies
Ensure you have all necessary dependencies installed:
```bash
    pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file and add the required database connection settings for PostgreSQL and MongoDB.

### 4. Start the Application
```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Conclusion
Your project is now ready for development and testing! Make sure to configure your databases properly and optimize for production when deploying.

