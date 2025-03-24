import os
import sys
import logging
from datetime import datetime
from assistant.modules.speech_utils import recognize_speech, speak
from assistant.modules.system_controls import control_system
from assistant.modules.web_search import search_web
from assistant.modules.advanced_features import AdvancedFeatures
from assistant.modules.ai_orchestrator import AIOrchestrator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler('assistant.log'),  # Full logs in file
        logging.StreamHandler()  # Simplified logs in console
    ]
)
logger = logging.getLogger(__name__)

# Disable debug logs from other libraries
logging.getLogger('comtypes').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('nltk').setLevel(logging.WARNING)
logging.getLogger('transformers').setLevel(logging.WARNING)

def get_command_category(command):
    """Determine the category of a command based on keywords"""
    command = command.lower()
    
    # News commands (high priority)
    if any(word in command for word in ["news", "headlines", "latest news"]):
        return "info_request"
    
    # Weather commands (high priority)
    if "weather" in command:
        return "info_request"
    
    # Screenshot commands
    if any(word in command for word in ["screenshot", "capture", "take a picture", "screen capture"]):
        return "screenshot"
    
    # Media control commands
    if any(word in command for word in ["pause", "stop", "next", "previous", "volume", "mute"]):
        return "media_control"
    
    # Video commands
    if any(word in command for word in ["play video", "watch video", "movie"]):
        return "video_control"
    
    # Audio commands
    if any(word in command for word in ["play music", "play song", "audio"]):
        return "audio_control"
    
    # System commands
    if any(word in command for word in ["open", "start", "launch", "close"]):
        return "system_control"
    
    # Information commands
    if any(word in command for word in ["cpu", "memory", "system"]):
        return "info_request"
    
    # Web search (default fallback)
    return "web_search"

def process_command(command, advanced_features, ai_orchestrator):
    """Process user command with AI enhancement"""
    try:
        # Get command category directly without AI preprocessing for these common commands
        if "news" in command.lower() or "headlines" in command.lower():
            category = "info_request"
        else:
            # Preprocess command with AI
            analysis = ai_orchestrator.preprocess_command(command)
            category = analysis["category"]
        
        # Enhanced command processing
        enhanced = ai_orchestrator.enhance_command(command, category)
        sentiment = enhanced["sentiment"]
        
        # Adjust response based on sentiment
        if sentiment["sentiment"] == "NEGATIVE":
            speak("I'll try my best to help you with that.")
        
        # Process command based on category
        success = False
        
        if category == "info_request":
            if "news" in command.lower() or "headlines" in command.lower():
                speak("Getting the latest news...")
                success = advanced_features.get_news()
            elif "weather" in command.lower():
                city = command.lower().replace("weather", "").replace("in", "").strip()
                if not city:
                    speak("Which city would you like to know the weather for?")
                    city = recognize_speech()
                if city:
                    success = advanced_features.get_weather_info(city)
            elif any(word in command for word in ["cpu", "memory", "system"]):
                success = advanced_features.get_system_info()
        elif category == "web_search":
            success = search_web(command)
        elif category == "system_control":
            success = control_system(command)
        elif category in ["media_control", "audio_control", "video_control"]:
            success = advanced_features.handle_media(command)
        elif category == "screenshot":
            success = advanced_features.take_screenshot()
        
        # Generate natural response
        if success:
            response = enhanced["response"]
            if not category in ["web_search", "info_request"]:  # Skip for web searches as they have their own speech
                speak(response if response else "Command executed successfully!")
        else:
            speak("I apologize, but I couldn't complete that task. Would you like to try something else?")
        
        return success
        
    except Exception as e:
        logger.error(f"Error processing command: {e}")
        speak("I encountered an error. Please try again.")
        return False

def main():
    """Main function with improved AI integration"""
    try:
        # Initialize components
        logger.info("Initializing AI Assistant...")
        advanced_features = AdvancedFeatures()
        ai_orchestrator = AIOrchestrator()
        
        # Welcome with context-aware greeting
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            greeting = "Good morning!"
        elif 12 <= current_hour < 17:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"
            
        speak(f"{greeting} I'm your AI Assistant. How can I help you today?")
        logger.info("AI Assistant started successfully")
        
        try:
            while True:
                try:
                    # Get user input
                    command = recognize_speech()
                    if not command:
                        continue
                    
                    # Log command
                    logger.info(f"User command: {command}")
                    
                    # Check for exit
                    if any(word in command.lower() for word in ["exit", "quit", "goodbye", "bye"]):
                        # Generate farewell based on interaction context
                        context = ai_orchestrator.get_context()
                        farewell = ai_orchestrator.generate_response("goodbye", context)
                        speak(farewell if farewell else "Goodbye! Have a great day!")
                        break
                    
                    # Process command
                    process_command(command, advanced_features, ai_orchestrator)
                    
                except KeyboardInterrupt:
                    logger.info("User interrupted the program")
                    speak("Goodbye! Have a great day!")
                    break
                except Exception as e:
                    logger.error(f"Error in main loop: {e}")
                    speak("I encountered an error. Please try again.")
                    continue
                    
        finally:
            # Cleanup
            logger.info("Cleaning up resources...")
            advanced_features.cleanup()
            ai_orchestrator.cleanup()
            logger.info("Cleanup completed")
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        speak("I encountered a fatal error. Please restart the program.")
        sys.exit(1)

if __name__ == "__main__":
    main()
