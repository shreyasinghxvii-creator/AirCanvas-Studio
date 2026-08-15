"""
routes/__init__.py

This file registers all the routes (blueprints)
used in the Air Coloring Book application.
"""

# Import all route blueprints
from .home import home_bp
from .workspace import workspace_bp
from .api import api_bp


def register_blueprints(app):
    """
    Register all application routes with Flask.
    """

    # Home page
    app.register_blueprint(home_bp)

    # Workspace page
    app.register_blueprint(workspace_bp, url_prefix="/workspace")

    # AI API routes
    app.register_blueprint(api_bp, url_prefix="/api")