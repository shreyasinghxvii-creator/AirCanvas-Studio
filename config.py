import os

class Config:
    # Flask System Setup
    SECRET_KEY = os.environ.get('SECRET_KEY', 'air-coloring-book-secret-key-2026')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 't']
    
    # File Storage & Upload Directories
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
    TEMPLATES_DIR = os.path.join(ASSETS_DIR, 'templates')
    SAVED_ART_DIR = os.path.join(BASE_DIR, 'saved_art')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    
    # Upload Constraints
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    # Python OpenCV & Camera Hardware Defaults
    CAMERA_WIDTH = 1280
    CAMERA_HEIGHT = 720
    
    # AI Engine Thresholds (Preserving exact original setup)
    KNN_NEIGHBORS = 1
    KMEANS_CLUSTERS = 5
    MAX_NUM_HANDS = 1
    MIN_DETECTION_CONFIDENCE = 0.7
    MIN_TRACKING_CONFIDENCE = 0.5

# Guarantee required runtime directories exist on startup
os.makedirs(Config.SAVED_ART_DIR, exist_ok=True)
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.TEMPLATES_DIR, exist_ok=True)