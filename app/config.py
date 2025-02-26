import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # General Flask config
    SECRET_KEY = os.environ.get("SECRET_KEY", "YOUR_SECRET_KEY")

    # Database config for PostgreSQL
    # Replace the placeholders with your real credentials and DB name
    SQLALCHEMY_DATABASE_URI = "postgresql://<username>:<password>@localhost:5432/<dbname>"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "YOUR_JWT_SECRET_KEY")
