air_coloring_book/
│
├── ai/                      # AI & Computer Vision Modules
│   ├── hand_tracker.py      # MediaPipe gesture tracking
│   ├── kmeans_palette.py    # K-Means clustering for palette generation
│   ├── knn_recommender.py   # KNN color recommendation model
│   └── smart_fill.py        # OpenCV flood-fill / auto-coloring logic
│
├── routes/                  # Flask Blueprint Route Handlers
│   ├── __init__.py          # Blueprint initialization
│   ├── api.py               # REST API endpoints (gestures, colors, fill)
│   ├── home.py              # Landing page routes
│   └── workspace.py         # Main drawing workspace route
│
├── static/                  # Frontend Static Assets
│   ├── css/
│   │   ├── landing.css      # Landing page styling
│   │   └── style.css        # Base/workspace styles
│   ├── js/
│   │   ├── landing.js        # Landing page interactivity
│   │   ├── theme.js          # Dark/light mode switcher
│   │   └── workspace.js      # Canvas rendering & real-time interaction
│   └── templates/           # Starter coloring canvas templates/images
│
├── templates/               # Jinja2 HTML Templates
│   ├── base.html            # Base template layout
│   ├── index.html           # Home/Landing page
│   └── workspace.html       # Primary drawing workspace
│
├── utils/                   # General Utilities
│   └── logger.py            # System logging configuration
│
├── app.py                   # Main Flask application entry point
├── config.py                # Environment & app configuration
└── requirements.txt         # Project Python dependencies