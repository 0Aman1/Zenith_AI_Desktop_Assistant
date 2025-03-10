import webbrowser
import re
import requests
from bs4 import BeautifulSoup
from ..modules.speech_utils import speak

def get_youtube_video_url(search_query, video_index=0):
    """Get the video URL from YouTube search results based on index"""
    try:
        # Clean up the search query
        search_query = re.sub(r'[^\w\s]', '', search_query)
        search_query = re.sub(r'\s+', '+', search_query)
        
        # Create search URL
        search_url = f"https://www.youtube.com/results?search_query={search_query}"
        
        # Send request to get search results
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(search_url, headers=headers)
        
        if response.status_code == 200:
            # Parse the response to find video URLs
            soup = BeautifulSoup(response.text, 'html.parser')
            video_elements = soup.find_all('a', {'class': 'yt-uix-tile-link'})
            
            if video_elements and len(video_elements) > video_index:
                # Get the video URL at the specified index
                video_url = f"https://www.youtube.com{video_elements[video_index]['href']}"
                return video_url
    except Exception as e:
        print(f"Error getting video URL: {e}")
    return None

def extract_video_index(command):
    """Extract video index from command (e.g., 'first', 'second', '1st', '2nd', etc.)"""
    command = command.lower()
    
    # Dictionary mapping words to numbers
    number_words = {
        'first': 0, '1st': 0,
        'second': 1, '2nd': 1,
        'third': 2, '3rd': 2,
        'fourth': 3, '4th': 3,
        'fifth': 4, '5th': 4,
        'one': 0, 'two': 1, 'three': 2, 'four': 3, 'five': 4
    }
    
    # Look for number words in the command
    for word, index in number_words.items():
        if word in command:
            return index
            
    # Look for numeric values
    numbers = re.findall(r'\d+', command)
    if numbers:
        return int(numbers[0]) - 1  # Convert to 0-based index
        
    return 0  # Default to first video

def search_web(command):
    """Handle web search related commands"""
    
    # YouTube search
    if "youtube" in command.lower():
        speak("Searching YouTube...")
        # Extract search query
        search_query = command.lower()
        search_query = search_query.replace("search", "").replace("youtube", "").replace("for", "").replace("look up", "").strip()
        
        if not search_query:
            speak("What would you like to search on YouTube?")
            return False
            
        # If the command includes "play" or "watch", try to play the video directly
        if any(word in command.lower() for word in ["play", "watch"]):
            speak(f"Searching for {search_query} on YouTube...")
            
            # Extract video index if specified
            video_index = extract_video_index(command)
            video_url = get_youtube_video_url(search_query, video_index)
            
            if video_url:
                speak("Opening the video...")
                webbrowser.open(video_url)
                return True
            else:
                speak("Sorry, I couldn't find the video. Opening search results instead...")
                # Fallback to search results
                url = f"https://www.youtube.com/results?search_query={search_query}"
                webbrowser.open(url)
                return True
        else:
            # Just show search results
            url = f"https://www.youtube.com/results?search_query={search_query}"
            webbrowser.open(url)
            speak(f"I've opened YouTube results for {search_query}")
            return True
        
    # Google search
    elif "google" in command.lower():
        speak("Searching Google...")
        search_query = re.sub(r'.*google\s*', '', command).strip()
        if not search_query:
            speak("What would you like to search on Google?")
            return False
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)
        speak(f"I've opened Google results for {search_query}")
        return True
        
    # Default to Google search if no specific platform mentioned
    else:
        speak("Performing a web search...")
        search_query = re.sub(r'search\s+|look\s+up\s+|find\s+', '', command).strip()
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)
        speak(f"Here are the search results for {search_query}")
        return True
