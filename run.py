import os
import sys
import logging
from datetime import datetime
from assistant.modules.speech_utils import recognize_speech, speak
from assistant.modules.system_controls import control_system
from assistant.modules.web_search import search_web
from assistant.modules.advanced_features import AdvancedFeatures
from assistant.modules.nlp_learning import CommandLearner

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('assistant.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_command_category(command):
    """Determine the category of a command based on keywords"""
    command = command.lower()
    
    # News commands (highest priority)
    if any(word in command for word in ["news", "headlines", "latest", "what's happening", "tell me the latest"]):
        return "news"
    
    # Web search commands (high priority)
    if "youtube" in command or "google" in command or "search" in command or "look up" in command:
        return "web_search"
    
    # Screenshot commands
    if any(word in command for word in ["screenshot", "capture", "screen"]):
        return "screenshot"
    
    # Media control commands (only for local media)
    if any(word in command for word in ["play", "pause", "stop", "next", "previous", "volume", "music"]) and "youtube" not in command:
        return "media_control"
    
    # System control commands
    if any(word in command for word in ["open", "start", "launch", "run", "close", "shutdown", "restart"]):
        return "system_control"
    
    # Weather commands
    if any(word in command for word in ["weather", "temperature", "forecast"]):
        return "weather"
    
    # System information commands (lowest priority)
    if any(word in command for word in ["cpu", "memory", "disk", "system", "status", "info"]):
        return "system_info"
    
    # Default to web search for unknown commands
    return "web_search"

def process_command(command, advanced_features, command_learner):
    """Process user command with improved error handling and feedback"""
    try:
        # Get command category using both rule-based and ML approaches
        rule_category = get_command_category(command)
        ml_category = command_learner.predict_category(command)
        
        # Use rule-based category for clear cases (YouTube, system control, etc.)
        if rule_category in ["web_search", "system_control", "media_control"]:
            category = rule_category
        else:
            # Use ML category if available and confident, otherwise use rule-based
            category = ml_category if ml_category else rule_category
        
        if not category:
            speak("I'm not sure how to help with that. Could you please rephrase your request?")
            return False
        
        # Log command processing
        logger.info(f"Processing command: {command}")
        logger.info(f"Category: {category}")
        
        success = False
        
        # Handle command based on category
        if category == "web_search":
            success = search_web(command)
        elif category == "system_control":
            success = control_system(command)
        elif category == "media_control":
            success = advanced_features.handle_media(command)
        elif category == "screenshot":
            success = advanced_features.take_screenshot()
        elif category == "weather":
            city = command.lower().replace("weather", "").replace("in", "").strip()
            if not city:
                speak("Which city would you like to know the weather for?")
                city = recognize_speech()
            if city:
                success = advanced_features.get_weather(city)
            else:
                speak("I couldn't understand the city name. Please try again.")
                return False
        elif category == "news":
            success = advanced_features.get_news()
        elif category == "system_info":
            # Only show system info when explicitly requested
            if any(word in command.lower() for word in ["cpu", "memory", "disk", "system", "status", "info"]):
                if "cpu" in command.lower():
                    success = advanced_features.get_cpu_info()
                elif "memory" in command.lower():
                    success = advanced_features.get_memory_info()
                elif "disk" in command.lower():
                    success = advanced_features.get_disk_info()
                else:
                    success = advanced_features.get_system_info()
            else:
                speak("I'm not sure what system information you're looking for. Please specify CPU, memory, or disk usage.")
                return False
        
        # Add command to history if successful
        if success:
            command_learner.add_command(command, category)
            speak("Command executed successfully!")
        else:
            speak("Sorry, I couldn't execute that command. Please try again.")
        
        return success
    except Exception as e:
        logger.error(f"Error processing command: {e}")
        speak("Sorry, I encountered an error while processing your command. Please try again.")
        return False

def main():
    """Main function with improved initialization and error handling"""
    try:
        # Initialize components
        logger.info("Initializing AI Assistant...")
        advanced_features = AdvancedFeatures()
        command_learner = CommandLearner()
        
        # Welcome message
        speak("Hello! I'm your AI Assistant. How can I help you today?")
        logger.info("AI Assistant started successfully")
        
        while True:
            try:
                # Get user input
                command = recognize_speech()
                if not command:
                    continue
                
                # Log user command
                logger.info(f"User command: {command}")
                
                # Check for exit command
                if any(word in command.lower() for word in ["exit", "quit", "goodbye", "bye"]):
                    speak("Goodbye! Have a great day!")
                    break
                
                # Process command
                process_command(command, advanced_features, command_learner)
                
            except KeyboardInterrupt:
                logger.info("User interrupted the program")
                speak("Goodbye! Have a great day!")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                speak("Sorry, I encountered an error. Please try again.")
                continue
                
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        speak("Sorry, I encountered a fatal error. Please restart the program.")
        sys.exit(1)

if __name__ == "__main__":
    main()
