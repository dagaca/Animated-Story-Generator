"""
This module initializes the Flask application and sets up logging and configurations.
"""
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Swagger
app.config['SWAGGER'] = {
    'title': 'Animated Story Generator API',
    'description': 'API for generating animated story videos with AI-generated visuals and audio.',
}

# Initialize Swagger
swagger = Swagger(app)

# Ensure required directories exist
os.makedirs(os.getenv("OUTPUT_DIR", "output"), exist_ok=True)
os.makedirs(os.getenv("TEMP_DIR", "temp"), exist_ok=True)

# Import log configuration and apply to the app
from config.log_config import configure_logging, log_request_info, log_response_info
configure_logging(app)
log_request_info(app)
log_response_info(app)

# Import routes
from app import routes
