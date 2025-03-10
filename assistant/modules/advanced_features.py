import os
import pyautogui
import psutil
import requests
from datetime import datetime
from ..modules.speech_utils import speak

class AdvancedFeatures:
    def __init__(self):
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def handle_media(self, command):
        """Handle media control commands"""
        try:
            if "youtube" in command.lower():
                # YouTube commands are handled by web_search.py
                return False
                
            # Local media controls
            if "play" in command or "pause" in command:
                pyautogui.press('playpause')
                speak("Toggled play/pause")
            elif "next" in command:
                pyautogui.press('nexttrack')
                speak("Playing next track")
            elif "previous" in command:
                pyautogui.press('prevtrack')
                speak("Playing previous track")
            elif "volume up" in command or "increase volume" in command:
                for _ in range(5):  # Press multiple times for noticeable change
                    pyautogui.press('volumeup')
                speak("Volume increased")
            elif "volume down" in command or "decrease volume" in command:
                for _ in range(5):  # Press multiple times for noticeable change
                    pyautogui.press('volumedown')
                speak("Volume decreased")
            elif "mute" in command:
                pyautogui.press('volumemute')
                speak("Volume muted")
            else:
                speak("Please specify what you want to do with the media (play, pause, next, previous, or volume)")
                return False
                
            return True
        except Exception as e:
            print(f"Error in media control: {e}")
            speak("Sorry, I couldn't control the media. Make sure a media player is running.")
            return False
    
    def take_screenshot(self):
        """Take a screenshot and save it"""
        try:
            # Create screenshots directory if it doesn't exist
            screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'screenshots')
            os.makedirs(screenshots_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(screenshots_dir, filename)
            
            # Take screenshot with error handling
            try:
                screenshot = pyautogui.screenshot()
                screenshot.save(filepath)
                speak(f"Screenshot saved as {filename}")
                return True
            except Exception as e:
                print(f"Screenshot capture error: {e}")
                speak("Sorry, I couldn't capture the screenshot. Please try again.")
                return False
                
        except Exception as e:
            print(f"Error in screenshot process: {e}")
            speak("Sorry, I couldn't take a screenshot. Please check if I have permission to save files.")
            return False
    
    def get_system_info(self):
        """Get system information"""
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        try:
            # Get all disk partitions and use the first one
            partitions = psutil.disk_partitions()
            if partitions:
                disk = psutil.disk_usage(partitions[0].mountpoint)
            else:
                disk = psutil.disk_usage("C:/")
        except Exception as e:
            print(f"Error getting disk info: {e}")
            disk = None
        
        info = (
            f"CPU usage is {cpu_percent}%\n"
            f"Memory usage is {memory.percent}%"
        )
        if disk:
            info += f"\nDisk usage is {disk.percent}%"
        speak(info)
        return info
    
    def get_cpu_info(self):
        """Get CPU information"""
        cpu_percent = psutil.cpu_percent()
        cpu_freq = psutil.cpu_freq()
        cpu_count = psutil.cpu_count()
        info = (
            f"CPU usage is {cpu_percent}%\n"
            f"CPU frequency is {cpu_freq.current:.1f} MHz\n"
            f"Number of CPU cores: {cpu_count}"
        )
        speak(info)
        return info
    
    def get_memory_info(self):
        """Get memory information"""
        memory = psutil.virtual_memory()
        info = (
            f"Memory usage is {memory.percent}%\n"
            f"Total memory: {memory.total / (1024**3):.1f} GB\n"
            f"Available memory: {memory.available / (1024**3):.1f} GB"
        )
        speak(info)
        return info
    
    def get_disk_info(self):
        """Get disk information"""
        try:
            # Get all disk partitions and use the first one
            partitions = psutil.disk_partitions()
            if partitions:
                disk = psutil.disk_usage(partitions[0].mountpoint)
            else:
                disk = psutil.disk_usage("C:/")
        except Exception as e:
            print(f"Error getting disk info: {e}")
            speak("Sorry, I couldn't get disk information.")
            return None
            
        info = (
            f"Disk usage is {disk.percent}%\n"
            f"Total disk space: {disk.total / (1024**3):.1f} GB\n"
            f"Free disk space: {disk.free / (1024**3):.1f} GB"
        )
        speak(info)
        return info
    
    def get_weather(self, city):
        """Get weather information"""
        # You'll need to sign up for an API key at OpenWeatherMap
        API_KEY = os.getenv('WEATHER_API_KEY')
        if not API_KEY:
            speak("Weather API key not found. Please set it in your environment variables.")
            return
            
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                result = f"The temperature in {city} is {temp}°C with {desc}"
                speak(result)
                return result
        except Exception as e:
            speak("Sorry, I couldn't fetch the weather information.")
            return str(e)
    
    def get_news(self):
        """Get latest news headlines"""
        # Sign up for API key at NewsAPI
        API_KEY = os.getenv('NEWS_API_KEY')
        if not API_KEY:
            speak("News API key not found. Please set it in your environment variables.")
            return
            
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                news = response.json()
                headlines = [article['title'] for article in news['articles'][:5]]
                result = "Here are the top headlines:\n" + "\n".join(headlines)
                speak(result)
                return result
        except Exception as e:
            speak("Sorry, I couldn't fetch the news.")
            return str(e) 