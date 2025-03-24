import os
import sys
import glob
from assistant.modules.advanced_features import AdvancedFeatures
from assistant.modules.speech_utils import speak

def test_media_functionality():
    """Test the media playback functionality"""
    print("=== Testing Media Functionality ===")
    
    # Initialize the AdvancedFeatures class
    advanced_features = AdvancedFeatures()
    
    # Check if media directories exist
    print(f"Audio directory: {advanced_features.audio_dir}")
    print(f"Video directory: {advanced_features.video_dir}")
    
    # Check if directories exist
    print(f"Audio directory exists: {os.path.exists(advanced_features.audio_dir)}")
    print(f"Video directory exists: {os.path.exists(advanced_features.video_dir)}")
    
    # Check for media files
    audio_files = []
    for ext in advanced_features.audio_extensions:
        audio_files.extend([os.path.basename(f) for f in glob.glob(os.path.join(advanced_features.audio_dir, f"*{ext}"))])
    
    video_files = []
    for ext in advanced_features.video_extensions:
        video_files.extend([os.path.basename(f) for f in glob.glob(os.path.join(advanced_features.video_dir, f"*{ext}"))])
    
    print(f"\nAudio files found: {len(audio_files)}")
    for file in audio_files:
        print(f"  - {file}")
    
    print(f"\nVideo files found: {len(video_files)}")
    for file in video_files:
        print(f"  - {file}")
    
    # Test functionality based on available files
    print("\n=== Testing Media Commands ===")
    
    # Test audio playback if files exist
    if audio_files:
        print("\nTesting audio playback...")
        # Disable actual playback for testing
        print(f"Would play audio: {audio_files[0]}")
    else:
        print("\nNo audio files found for testing.")
        print("Please add some audio files to the media/audio directory.")
    
    # Test video playback if files exist
    if video_files:
        print("\nTesting video playback...")
        # Disable actual playback for testing
        print(f"Would play video: {video_files[0]}")
    else:
        print("\nNo video files found for testing.")
        print("Please add some video files to the media/video directory.")
    
    # Test media controls
    print("\nTesting media controls...")
    print("These commands would control the currently playing media:")
    print("  - Pause/Play")
    print("  - Next track")
    print("  - Previous track")
    print("  - Volume up/down")
    print("  - Mute")

if __name__ == "__main__":
    test_media_functionality() 