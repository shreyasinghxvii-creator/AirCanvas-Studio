"""
routes/workspace.py

This file opens the drawing workspace.
When the user clicks "Start Drawing",
this page loads workspace.html.
"""

from flask import Blueprint, render_template

# Create a blueprint for the workspace page
workspace_bp = Blueprint("workspace", __name__)


# Open the workspace page
@workspace_bp.route("/")
def index():

    # Show the workspace page
    return render_template("workspace.html")