import datetime
from ..modules.speech_utils import speak

def process_command(command):
    """Process and respond to general commands and queries"""
    command = command.lower()
    
    # Time related queries
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"
        
    # Date related queries
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        return f"Today's date is {current_date}"
        
    # Greeting responses
    elif any(word in command for word in ["hello", "hi", "hey"]):
        return "Hello! How can I help you today?"
        
    elif any(word in command for word in ["how are you", "how're you"]):
        return "I'm doing well, thank you for asking! How can I assist you?"
        
    # Basic questions
    elif "what can you do" in command:
        return ("I can help you with various tasks like: \n"
                "1. Web searches on Google and YouTube\n"
                "2. Opening applications like Notepad, Calculator, Chrome\n"
                "3. System controls like shutdown and restart\n"
                "4. Answering basic questions about time and date\n"
                "Just tell me what you'd like me to do!")
                
    elif "who are you" in command:
        return "I am your AI desktop assistant, designed to help you with various tasks on your computer."
        
    # Default response
    else:
        return None  # This will trigger the default "I'm not sure" response in main.py
