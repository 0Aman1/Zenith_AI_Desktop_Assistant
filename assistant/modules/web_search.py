import webbrowser
import re
import requests
import json
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
            # Modern approach to extract video IDs
            video_ids = re.findall(r"watch\?v=(\S{11})", response.text)
            
            # Remove duplicates while preserving order
            unique_video_ids = []
            for video_id in video_ids:
                if video_id not in unique_video_ids:
                    unique_video_ids.append(video_id)
            
            if unique_video_ids and len(unique_video_ids) > video_index:
                # Get the video URL at the specified index
                video_url = f"https://www.youtube.com/watch?v={unique_video_ids[video_index]}"
                return video_url
            
            # Fallback to old method if no videos found
            soup = BeautifulSoup(response.text, 'html.parser')
            video_elements = soup.find_all('a', href=re.compile(r'/watch\?v='))
            
            if video_elements and len(video_elements) > video_index:
                # Get the video URL at the specified index
                href = video_elements[video_index]['href']
                if href.startswith('/watch'):
                    video_url = f"https://www.youtube.com{href}"
                    return video_url
    except Exception as e:
        print(f"Error getting video URL: {e}")
    return None

def get_video_info(video_url):
    """Get information about a YouTube video"""
    try:
        if not video_url:
            return None
            
        # Extract video ID
        video_id = re.search(r'watch\?v=(\S{11})', video_url).group(1)
        
        # Get video info
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(video_url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to get title
            title = None
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.text.replace(' - YouTube', '')
            
            return {
                'id': video_id,
                'url': video_url,
                'title': title
            }
    except Exception as e:
        print(f"Error getting video info: {e}")
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

def extract_youtube_query(command):
    """Extract the search query from a YouTube command"""
    command = command.lower()
    
    # Remove common YouTube command phrases
    phrases_to_remove = [
        "play", "watch", "search", "youtube", "for", "look up", 
        "find", "video", "videos", "on youtube", "of", "the"
    ]
    
    query = command
    for phrase in phrases_to_remove:
        query = query.replace(phrase, " ")
    
    # Clean up the query
    query = re.sub(r'\s+', ' ', query).strip()
    
    return query

def play_youtube_video(command):
    """Play a YouTube video based on the command"""
    # Extract search query
    search_query = extract_youtube_query(command)
    
    if not search_query:
        speak("What would you like to play on YouTube?")
        return False
    
    speak(f"Searching for {search_query} on YouTube...")
    
    # Extract video index if specified
    video_index = extract_video_index(command)
    video_url = get_youtube_video_url(search_query, video_index)
    
    if video_url:
        # Get video info
        video_info = get_video_info(video_url)
        
        if video_info and video_info['title']:
            speak(f"Playing '{video_info['title']}' on YouTube")
        else:
            speak("Playing the video on YouTube")
            
        # Open the video in the browser
        webbrowser.open(video_url)
        return True
    else:
        speak("Sorry, I couldn't find the video. Opening search results instead...")
        # Fallback to search results
        url = f"https://www.youtube.com/results?search_query={search_query}"
        webbrowser.open(url)
        return True

def clean_text(text):
    """Clean and format text for speech"""
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove special characters that might interfere with speech
    text = text.replace('&', 'and')
    text = text.replace('|', '')
    text = text.replace('/', ' or ')
    return text

def extract_search_result(url):
    """Extract readable content from a webpage"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text and clean it
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Get first 200 characters for a summary
        summary = text[:200] + "..."
        return clean_text(summary)
    except Exception as e:
        print(f"Error extracting content: {e}")
        return None

def search_web(query, speak_result=False):
    """
    Search the web and optionally speak the results
    
    Args:
        query (str): Search query
        speak_result (bool): Whether to speak the search results
    """
    try:
        # For demonstration, we'll use a simple Google search
        search_url = f"https://www.google.com/search?q={query}"
        
        if speak_result:
            # Try to get readable content
            content = extract_search_result(search_url)
            if content:
                speak(content)
            else:
                speak(f"Here's what I found for {query}")
        
        # Open in browser
        webbrowser.open(search_url)
        return True
        
    except Exception as e:
        print(f"Error in web search: {e}")
        speak("I encountered an error while searching. Please try again.")
        return False
