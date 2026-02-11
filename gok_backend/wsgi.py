# WSGI configuration for PythonAnywhere deployment
# This file configures the FastAPI application to run on PythonAnywhere

import sys
import os

# Add your project directory to the sys.path
# Replace 'Chiqoke254' with your PythonAnywhere username if different
path = '/home/Chiqoke254/Nasa/gok_backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables if needed
os.environ['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'sqlite:///./federal_blockchain.db')

# Import the FastAPI application
from main import app

# For ASGI applications like FastAPI, we need to use an ASGI-to-WSGI adapter
# PythonAnywhere doesn't natively support ASGI, so we use asgiref
from asgiref.wsgi import WsgiToAsgi

# Wrap the FastAPI app for WSGI compatibility
application = WsgiToAsgi(app)
