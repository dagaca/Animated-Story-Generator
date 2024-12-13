"""
This module runs the Flask application.
"""
from app import app  # Import the 'app' variable from the app module

if __name__ == '__main__':
    # Run the Flask application in debug mode and make it accessible externally
    app.run(debug=True, use_reloader=False, host="0.0.0.0")
