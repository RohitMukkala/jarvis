# Jarvis AI Assistant

A sophisticated AI-powered personal assistant that combines voice recognition, face authentication, machine learning, and system automation to create an intelligent desktop companion.

## Introduction

Jarvis AI Assistant is a comprehensive desktop application that transforms your computer into an intelligent, voice-controlled environment. Built with Python and modern web technologies, it provides hands-free access to system functions, health monitoring, information retrieval, and entertainment through natural voice commands and biometric security.

The project demonstrates advanced integration of multiple AI technologies including computer vision for face recognition, machine learning for health predictions, and natural language processing for intuitive user interaction.

## Features

### 🎤 Voice Control & Communication

- **Wake Word Detection**: Responds to "Jarvis" or "Alexa" for hands-free activation
- **Speech Recognition**: Converts voice commands to text for processing
- **Text-to-Speech**: Provides natural-sounding voice responses
- **Conversational AI**: Custom chatbot with probabilistic response matching

### 🔐 Security & Access Control

- **Face Recognition**: Biometric authentication using OpenCV and LBPH
- **User Verification**: Trained facial models for authorized access
- **Secure Login**: Local processing ensures privacy and security

### 🏥 Health & Medical Assistance

- **Heart Disease Prediction**: Machine learning model using TensorFlow
- **Health Metrics Analysis**: Processes blood pressure, cholesterol, heart rate data
- **Personalized Recommendations**: AI-powered health improvement suggestions

### ⚙️ System Control & Automation

- **Application Launching**: Voice-controlled desktop app management
- **Web Navigation**: Opens browsers and navigates to specified sites
- **System Functions**: Controls settings and utilities through voice commands

### 🌐 Information & Entertainment

- **Weather Updates**: Real-time weather information via OpenWeatherMap API
- **News Headlines**: Current events via NewsAPI
- **YouTube Integration**: Video playback through voice search queries
- **Knowledge Base**: Time, date, and general information responses

### 📱 Contact & Communication

- **Contact Database**: SQLite-based contact management system
- **Voice Search**: Find contacts by name for phone/email access
- **Data Organization**: Structured contact storage with multiple fields

### 🎨 Modern User Experience

- **Animated Interface**: Particle effects and smooth transitions
- **Responsive Design**: Web-based UI accessible through desktop
- **Real-time Feedback**: System status and command confirmation display

## Tech Stack

### Core Technologies

- **Backend**: Python 3.9+ with multiprocessing architecture
- **Frontend**: HTML5, CSS3, JavaScript
- **Desktop Integration**: Eel framework for Python-Web bridge
- **Database**: SQLite3 with custom schema management

### AI & Machine Learning

- **Computer Vision**: OpenCV 4.11 (LBPH face recognition)
- **Deep Learning**: TensorFlow 2.18 with Keras
- **Machine Learning**: Scikit-learn 1.5.2
- **NLP**: Custom chatbot with probabilistic response matching

### Audio & Speech Processing

- **Speech Recognition**: SpeechRecognition library with PyAudio
- **Text-to-Speech**: pyttsx3 (SAPI5 engine)
- **Voice Activation**: Porcupine wake word detection
- **Audio Playback**: playsound library

### System Integration & Automation

- **Desktop Automation**: PyAutoGUI
- **Process Management**: Python multiprocessing
- **Device Management**: ADB integration for Android connectivity

### Web Technologies & APIs

- **Frontend Framework**: Bootstrap 5.0
- **JavaScript Libraries**: Modernizr, custom particle animations
- **External APIs**: OpenWeatherMap, NewsAPI, YouTube integration
- **Web Scraping**: BeautifulSoup4

### Data Processing & Analytics

- **Data Manipulation**: NumPy, Pandas
- **Model Persistence**: Joblib
- **Data Visualization**: Matplotlib
- **CSV Processing**: Built-in CSV handling

### Security & Authentication

- **Face Recognition**: Haar Cascade classifiers with LBPH models
- **Database Security**: SQLite with parameterized queries

### Development & Deployment

- **Version Control**: Git
- **Dependencies**: Comprehensive requirements.txt (100+ packages)
- **Platform**: Windows-focused with PowerShell integration
- **Architecture**: Modular design (engine, web interface, auth modules)

## Installation & Setup

### Prerequisites

- Python 3.9 or higher
- Windows 10/11 (primary platform)
- Microphone and webcam for voice/face features
- Internet connection for API services

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

### Step 2: Install Dependencies

```bash
pip install -r engine/requirements.txt
```

### Step 3: Set Up API Keys

Create API keys for external services:

1. **OpenWeatherMap API**:

   - Visit [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up and get your free API key
   - Update `engine/long__responses.py` with your key

2. **NewsAPI**:
   - Visit [NewsAPI](https://newsapi.org/)
   - Sign up and obtain your API key
   - Update `engine/long__responses.py` with your key

### Step 4: Database Setup

Ensure the following files exist in your project root:

- `jarvis.db` (SQLite database)
- `contacts.csv` (contact data)
- `heart_disease_model.h5` (trained ML model)
- `scaler.save` (model preprocessing scaler)

### Step 5: Run the Application

```bash
python run.py
```

## Usage

### Wake Word Activation

- Say "Jarvis" or "Alexa" to activate the assistant
- Wait for the confirmation sound

### Voice Commands Examples

- **System Control**: "Open Chrome", "Launch Notepad"
- **Information**: "What's the weather in London?", "Tell me the news"
- **Entertainment**: "Play Despacito on YouTube"
- **Health**: "Analyze my heart health"
- **Time**: "What time is it?", "What's today's date?"

### Face Authentication

- Look at your webcam when prompted
- The system will recognize your face and grant access
- Ensure good lighting for optimal recognition

## Project Structure

```
jarvis-ai-assistant/
├── engine/                          # Core AI engine
│   ├── auth/                       # Face recognition module
│   │   ├── haarcascade_frontalface_default.xml
│   │   ├── recoganize.py          # Face authentication
│   │   └── trainer/               # Trained face models
│   ├── chatbot.py                 # NLP and conversation logic
│   ├── command.py                 # System command handling
│   ├── config.py                  # Configuration settings
│   ├── db.py                      # Database operations
│   ├── features.py                # Core functionality
│   ├── helper.py                  # Utility functions
│   ├── long_responses.py          # Extended response handling
│   └── requirements.txt           # Python dependencies
├── www/                           # Web interface
│   ├── assets/                    # Static resources
│   │   ├── audio/                # Sound files
│   │   ├── img/                  # Images and icons
│   │   └── vendorse/             # Third-party libraries
│   ├── index.html                # Main interface
│   ├── style.css                 # Styling
│   ├── script.js                 # Particle animations
│   ├── main.js                   # Core JavaScript
│   └── controller.js             # UI control logic
├── main.py                       # Main application entry point
├── run.py                        # Multiprocessing launcher
├── jarvis.db                     # SQLite database
├── contacts.csv                  # Contact data
├── heart_disease_model.h5        # Trained ML model
├── scaler.save                   # Model preprocessing
└── device.bat                    # ADB device setup script
```

## Screenshots / Demo

_[Screenshots and demo GIFs will be added here]_

## Future Improvements

- **Multi-language Support**: Expand beyond English
- **Enhanced NLP**: Integration with advanced language models
- **Mobile Integration**: Companion mobile app development
- **Cloud Sync**: Multi-device synchronization
- **Advanced Security**: Multi-factor authentication options
- **API Expansion**: More third-party service integrations
- **Performance Optimization**: Faster response times and reduced resource usage
- **Accessibility**: Voice commands for users with disabilities

## License

_[License information will be added here]_

## Acknowledgments

### APIs & External Services

- [OpenWeatherMap](https://openweathermap.org/) - Weather data
- [NewsAPI](https://newsapi.org/) - News headlines
- [YouTube](https://www.youtube.com/) - Video content

### Python Libraries & Frameworks

- **Speech Recognition**: [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- **Computer Vision**: [OpenCV](https://opencv.org/)
- **Machine Learning**: [TensorFlow](https://tensorflow.org/), [Scikit-learn](https://scikit-learn.org/)
- **Desktop Integration**: [Eel](https://github.com/ChrisKnott/Eel), [PyAutoGUI](https://pyautogui.readthedocs.io/)
- **Audio Processing**: [PyAudio](https://pypi.org/project/PyAudio/), [pyttsx3](https://pypi.org/project/pyttsx3/)
- **Web Framework**: [Flask](https://flask.palletsprojects.com/)

### Development Resources

- **Frontend**: [Bootstrap](https://getbootstrap.com/), [Modernizr](https://modernizr.com/)
- **Database**: [SQLite](https://www.sqlite.org/)
- **Version Control**: [Git](https://git-scm.com/)

---

**Note**: This project is for educational and personal use. Ensure compliance with API terms of service and respect user privacy when implementing face recognition features.
