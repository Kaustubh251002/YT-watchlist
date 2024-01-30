# app/__init__.py

from flask import Flask

app = Flask(__name__)

# Import routes after creating the Flask app
from app import app
