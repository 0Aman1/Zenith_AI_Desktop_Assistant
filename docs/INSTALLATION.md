# Installation Guide

## Prerequisites

- Python 3.8 or higher
- Windows 10 or higher (some features are Windows-specific)
- Git (optional, for cloning the repository)
- Administrative privileges (for some system control features)

## Installation Steps

1. **Clone or Download the Repository**
   ```bash
   git clone https://github.com/yourusername/AI_Desktop_Assistant.git
   cd AI_Desktop_Assistant
   ```

2. **Create a Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install Required Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Additional Components**
   - Download and install spaCy English model:
     ```bash
     python -m spacy download en_core_web_sm
     ```
   - Download NLTK data:
     ```python
     import nltk
     nltk.download('punkt')
     nltk.download('stopwords')
     nltk.download('wordnet')
     ```

5. **Configure the Assistant**
   - Copy `config.example.json` to `config.json`
   - Adjust settings in `config.json` according to your preferences
   - Ensure proper paths are set for media and screenshot directories

6. **Test the Installation**
   ```bash
   python run.py --test
   ```

## Common Installation Issues

### Speech Recognition Issues
- Ensure your microphone is properly connected and set as default
- Install PyAudio if you encounter errors:
  ```bash
  pip install pyaudio
  ```

### System Control Issues
- Run the application with administrative privileges for full functionality
- Ensure Windows Media API is enabled for brightness control
- Check Windows permissions for system control features

### Python Dependencies
If you encounter issues with specific packages:
1. Try installing them individually:
   ```bash
   pip install <package_name>
   ```
2. Check for conflicts in your Python environment
3. Ensure you're using a compatible Python version

## Quick Start

1. **Using the Batch File (Windows)**
   - Double-click `start_assistant.bat`
   - Or run from command prompt:
     ```bash
     start_assistant.bat
     ```

2. **Manual Start**
   ```bash
   python run.py
   ```

3. **Testing Voice Commands**
   - Hold 'P' key while speaking
   - Release when done
   - Watch for confidence scores in the output

## Updating

To update the assistant:
1. Pull the latest changes (if using Git):
   ```bash
   git pull origin main
   ```
2. Update dependencies:
   ```bash
   pip install -r requirements.txt --upgrade
   ```
3. Check for any new configuration options in `config.example.json` 