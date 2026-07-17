"""
Global Configuration for the Application

All configuration is loaded from environment variables with sensible
defaults for local development.
"""
import os

# Database connection: defaults to a local SQLite database for development
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///test.db")

SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Secret for session management
SECRET_KEY = os.getenv("SECRET_KEY", "s3cr3t-key-shhhh")
