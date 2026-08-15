"""
routes/home.py

This file handles the Home page of the application.
When the user opens the website, this route loads index.html.
"""

from flask import Blueprint, render_template

# Create a blueprint for all home page routes
home_bp = Blueprint("home", __name__)


# Home page
@home_bp.route("/")
def index():
    # Open the landing page
    return render_template("index.html")