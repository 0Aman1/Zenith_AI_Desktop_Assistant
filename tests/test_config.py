"""
Test Configuration and Common Utilities
"""
import os
import sys
import logging
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test data paths
TEST_DIR = Path(__file__).parent
PROJECT_ROOT = TEST_DIR.parent
TEST_MEDIA_DIR = PROJECT_ROOT / "data" / "media"
TEST_MUSIC_DIR = PROJECT_ROOT / "data" / "music"

# Test configuration
TEST_CONFIG = {
    "media_files": [
        "test_audio.mp3",
        "test_video.mp4"
    ],
    "commands": [
        "play music",
        "pause",
        "next song",
        "take screenshot",
        "search web"
    ]
}

# Setup logging for tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(PROJECT_ROOT / "logs" / "test.log"),
        logging.StreamHandler()
    ]
)

def setup_test_environment():
    """Setup required directories and files for testing"""
    # Create test directories if they don't exist
    TEST_MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    TEST_MUSIC_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create empty test files if needed
    for media_file in TEST_CONFIG["media_files"]:
        file_path = TEST_MEDIA_DIR / media_file
        if not file_path.exists():
            file_path.touch()

def cleanup_test_environment():
    """Clean up test files and directories"""
    # Add cleanup code if needed
    pass 