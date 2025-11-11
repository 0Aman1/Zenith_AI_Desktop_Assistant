# Zenith Desktop Assistant

An intelligent desktop assistant that uses speech recognition, natural language processing, and AI to help with various tasks.

## Features

- Voice Commands & Speech Recognition
- Media Control (music, videos)
- System Controls (screenshots, applications)
- Web Integration (searches, news, weather)
- Advanced AI Features (using Hugging Face)
- File Management

## Project Structure

```
AI_Desktop_Assistant/
├── assistant/           # Core assistant modules
│   └── modules/        # Individual feature modules
├── data/               # Data directories
│   ├── media/         # Media files
│   ├── music/         # Music files
│   └── screenshots/   # Saved screenshots
├── docs/              # Documentation
├── logs/              # Log files
├── models/            # AI models
├── tests/             # Test files
├── training_data/     # Training data for AI
├── config.py          # Configuration settings
├── load_env.py        # Environment setup
├── requirements.txt   # Dependencies
├── run.py            # Main execution file
└── setup_api_keys.py  # API configuration
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure API keys:
```bash
python setup_api_keys.py
```

3. Run the assistant:
```bash
python run.py
```

## Available Commands

- Media Control: "play music", "pause", "next song", etc.
- System: "take screenshot", "open chrome", etc.
- Web: "search for...", "weather in...", "show news"
- File Operations: "open folder", "create file", etc.

## AI Features

- Speech Recognition with Indian English support
- Natural Language Understanding
- Sentiment Analysis
- Intent Classification
- Question Answering
- Text Generation

## Dependencies

- SpeechRecognition
- pyttsx3
- PyAudio
- transformers
- torch
- Other requirements in requirements.txt

## Contributing

Feel free to submit issues and enhancement requests.

## License


