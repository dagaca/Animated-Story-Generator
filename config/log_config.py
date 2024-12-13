"""
This module sets up logging configurations for a Flask application, 
including request and response logging.
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import request
from dotenv import load_dotenv

# Load the .env file to get environment variables
load_dotenv()

def configure_logging(app):
    """
    Configure logging for the Flask application.
    
    This function sets up a RotatingFileHandler for the application logger, ensuring that log files
    are rotated when they reach a certain size. The log directory and file name are specified in the
    environment variables.

    Parameters:
    - app: Flask application instance
    """
    log_dir = os.getenv('LOG_DIR')  # Default to 'logs' if not specified
    log_file = os.getenv('LOG_FILE')  # Default to 'app.log' if not specified
    log_path = os.path.join(log_dir, log_file)

    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Set log level to INFO
    app.logger.setLevel(logging.INFO)

    # Create a RotatingFileHandler
    handler = RotatingFileHandler(log_path, maxBytes=2*1024*1024, backupCount=5)  # 2MB per file, keep 5 backups
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # Add the handler to the app's logger
    app.logger.addHandler(handler)

def log_request_info(app):
    """
    Log the incoming request information.
    
    This function sets up a before_request handler that logs the request URL, method,
    and data for each incoming request.
    
    Parameters:
        app: Flask application instance.
    """
    @app.before_request
    def log_request():
        app.logger.info('Request URL: %s', request.url)
        app.logger.info('Request Method: %s', request.method)
        app.logger.info('Request Data: %s', request.data)

def log_response_info(app):
    """
    Log the response information.
    
    This function sets up an after_request handler that logs the response status for
    each response sent by the server.
    
    Parameters:
        app: Flask application instance.
    
    Returns:
        The response object.
    """
    @app.after_request
    def log_response(response):
        app.logger.info('Response Status: %s', response.status)
        return response
