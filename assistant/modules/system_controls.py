import os
import subprocess
import webbrowser
from ..modules.speech_utils import speak

def control_system(command):
    """Handle system control commands"""
    command = command.lower()
    
    # Common applications
    if "notepad" in command:
        speak("Opening Notepad...")
        subprocess.Popen("notepad.exe")
        
    elif "calculator" in command:
        speak("Opening Calculator...")
        subprocess.Popen("calc.exe")
        
    elif "chrome" in command:
        speak("Opening Google Chrome...")
        try:
            subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"])
        except FileNotFoundError:
            speak("Chrome is not installed in the default location.")
            webbrowser.open("https://www.google.com")
            
    elif "firefox" in command:
        speak("Opening Firefox...")
        try:
            subprocess.Popen(["C:\\Program Files\\Mozilla Firefox\\firefox.exe"])
        except FileNotFoundError:
            speak("Firefox is not installed in the default location.")
            webbrowser.open("https://www.google.com")
    
    # System commands
    elif any(word in command for word in ["shutdown", "turn off"]):
        speak("Do you want to shutdown your computer? Say 'yes' to confirm.")
        confirmation = input("Confirm shutdown (yes/no): ")  # Using input for safety
        if confirmation.lower() == 'yes':
            speak("Shutting down the computer...")
            os.system("shutdown /s /t 60")
            speak("Shutdown scheduled in 60 seconds. Say 'cancel shutdown' to cancel.")
        else:
            speak("Shutdown cancelled.")
            
    elif "cancel shutdown" in command:
        speak("Cancelling shutdown...")
        os.system("shutdown /a")
        speak("Shutdown cancelled.")
        
    elif "restart" in command:
        speak("Do you want to restart your computer? Say 'yes' to confirm.")
        confirmation = input("Confirm restart (yes/no): ")  # Using input for safety
        if confirmation.lower() == 'yes':
            speak("Restarting the computer...")
            os.system("shutdown /r /t 60")
            speak("Restart scheduled in 60 seconds. Say 'cancel shutdown' to cancel.")
        else:
            speak("Restart cancelled.")
    
    else:
        speak("Sorry, I don't know how to handle that system command.")
