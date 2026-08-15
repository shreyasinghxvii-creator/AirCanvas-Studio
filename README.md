# 🎨 AirCanvas Studio – AI Air Colouring Book

**AirCanvas Studio** is a web-based AI and Computer Vision project that allows users to draw and colour digital artwork using **finger movements captured through a webcam**.

The project combines **real-time hand tracking, image processing, and Machine Learning techniques** to create an interactive air-drawing and colouring experience.

---

## ✨ Project Overview

Traditional digital drawing applications usually require a mouse, stylus, or touchscreen.

AirCanvas Studio explores a different approach: the user can place their hand in front of a webcam and use their **index finger as a virtual drawing tool**.

The system detects the user's hand, tracks the finger position, and uses that movement to create strokes on a digital canvas.

The project also includes AI-based colour processing to help generate and recommend suitable colours for colouring templates.

---

## 🚀 Main Features

* ✋ **Real-Time Finger Tracking**

  * Detects the user's hand through a webcam.
  * Tracks finger movement for air drawing.

* 🖌️ **Air Drawing**

  * Allows users to draw on a digital canvas using finger movements.
  * No physical mouse or stylus is required for gesture-based drawing.

* 🎨 **AI Colour Palette**

  * Uses K-Means Clustering to identify dominant colours from images.
  * Generates a colour palette based on the extracted colours.

* 🤖 **Colour Recommendation**

  * Uses K-Nearest Neighbour (KNN) to recommend colours based on colour similarity.

* 🖼️ **Colouring Templates**

  * Provides predefined images that users can use for digital colouring.

* 🌐 **Web-Based Interface**

  * Built using Flask with a browser-based user interface.

---

## 🧠 AI & Machine Learning Techniques

### 1. MediaPipe Hand Tracking

MediaPipe is used for real-time hand detection and landmark tracking.

The project uses the detected hand landmarks, particularly the **index finger position**, to determine where the user is drawing on the canvas.

### 2. K-Means Clustering

K-Means is an unsupervised Machine Learning algorithm.

In AirCanvas Studio, it is used to analyse image colours and identify dominant colour groups that can be used to create a palette.

### 3. K-Nearest Neighbour (KNN)

KNN is a supervised Machine Learning algorithm based on similarity between data points.

In this project, it is used for colour recommendation by comparing colour information and finding similar colours.

---

## 🛠️ Technologies Used

| Technology       | Purpose                                       |
| ---------------- | --------------------------------------------- |
| **Python**       | Backend development and AI/ML processing      |
| **Flask**        | Web application framework                     |
| **OpenCV**       | Computer Vision and image processing          |
| **MediaPipe**    | Real-time hand tracking                       |
| **NumPy**        | Numerical and image-data processing           |
| **Scikit-learn** | Machine Learning algorithms                   |
| **HTML**         | Web page structure                            |
| **CSS**          | User interface styling                        |
| **JavaScript**   | Canvas interaction and frontend functionality |
| **Jinja2**       | Flask HTML templating                         |

---

## 🏗️ Project Structure

```text
AirCanvas-Studio/
│
├── ai/
│   ├── hand_tracker.py
│   ├── kmeans_palette.py
│   ├── knn_recommender.py
│   └── smart_fill.py
│
├── routes/
│   ├── __init__.py
│   ├── api.py
│   ├── home.py
│   └── workspace.py
│
├── static/
│   ├── css/
│   │   ├── landing.css
│   │   └── style.css
│   │
│   ├── js/
│   │   ├── theme.js
│   │   └── workspace.js
│   │
│   └── templates/
│       └── coloring template images
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── workspace.html
│
├── utils/
│   └── logger.py
│
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

### Folder Description

**`ai/`**
Contains the Computer Vision and Machine Learning modules used by the project.

**`routes/`**
Contains Flask Blueprint route handlers and API endpoints.

**`static/`**
Contains CSS, JavaScript, and image assets used by the frontend.

**`templates/`**
Contains the Jinja2 HTML templates for the application.

**`utils/`**
Contains supporting utility functions such as logging.

**`app.py`**
Main entry point of the Flask application.

**`config.py`**
Contains application configuration.

**`requirements.txt`**
Contains the Python dependencies required to run the project.

---

## ⚙️ How It Works

The basic working flow of AirCanvas Studio is:

```text
        User
          │
          ▼
       Webcam
          │
          ▼
 MediaPipe Hand Tracking
          │
          ▼
   Index Finger Position
          │
          ▼
     Digital Canvas
          │
          ▼
   Drawing / Colouring
          │
          ▼
 K-Means Colour Extraction
          │
          ▼
     Colour Palette
          │
          ▼
 KNN Colour Recommendation
```

The webcam captures the user's hand, MediaPipe processes the hand landmarks, and the finger movement is used for drawing.

The Machine Learning components are used separately for colour analysis and recommendation.

---

## 💻 Installation

### 1. Clone the repository

```bash
git clone https://github.com/shreyasinghxvii-creator/AirCanvas-Studio.git
```

### 2. Open the project directory

```bash
cd AirCanvas-Studio
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

Then open the local Flask address shown in the terminal, usually:

```text
http://127.0.0.1:5000
```

---

## 📷 Requirements

To use the gesture-based drawing functionality, you need:

* A computer with a webcam
* Python installed
* Required Python packages
* A modern web browser

Good lighting and a clearly visible hand can help improve hand tracking.

---

## 🎯 Project Objectives

The main objectives of AirCanvas Studio are:

1. To create a touch-free drawing and colouring experience.
2. To track finger movements using Computer Vision.
3. To demonstrate real-time hand tracking using MediaPipe.
4. To apply K-Means Clustering for colour palette generation.
5. To apply KNN for colour recommendation.
6. To combine AI techniques with a practical web application.
7. To provide a simple and interactive digital colouring environment.

---

## 📚 Academic Purpose

AirCanvas Studio was developed as an academic project to demonstrate the practical implementation of **Artificial Intelligence, Machine Learning, Computer Vision, and Web Development**.

The project focuses on applying these technologies together in a simple and interactive application rather than building a complex commercial drawing platform.

---

## 🔮 Future Scope

The project can be further improved by adding:

* More hand gestures for different drawing operations
* Additional brush styles and drawing tools
* Improved hand tracking under different lighting conditions
* Automatic AI-based colouring
* Mobile and tablet support
* Additional colouring templates
* Improved colour recommendation techniques

---

## 👩‍💻 Author

**Shreya Singh**
---

## 📄 License

This project was created for educational and academic purposes.
