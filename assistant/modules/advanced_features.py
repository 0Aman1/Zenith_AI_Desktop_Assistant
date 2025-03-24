import os
import pyautogui
import psutil
import requests
import random
import subprocess
import glob
import time
import threading
from datetime import datetime
from ..modules.speech_utils import speak
from ..modules.web_search import search_web

class AdvancedFeatures:
    def __init__(self):
        # Create base directories
        self.screenshot_dir = "screenshots"
        self.media_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'media')
        self.audio_dir = os.path.join(self.media_dir, 'audio')
        self.video_dir = os.path.join(self.media_dir, 'video')
        
        # Create directories if they don't exist
        os.makedirs(self.screenshot_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.video_dir, exist_ok=True)
        
        # Supported media file extensions
        self.audio_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac']
        self.video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv']
        
        # Default media players based on OS
        if os.name == 'nt':  # Windows
            self.default_audio_player = 'wmplayer.exe'
            self.default_video_player = 'wmplayer.exe'
            self.media_players = ['wmplayer.exe', 'vlc.exe', 'spotify.exe', 'musicapp.exe', 'groove.exe', 'movies.exe', 'video.exe']
        else:  # Linux/Mac
            self.default_audio_player = 'vlc'
            self.default_video_player = 'vlc'
            self.media_players = ['vlc', 'rhythmbox', 'audacious', 'totem', 'mplayer', 'mpv']
        
        # Track current playlist and media process
        self.current_playlist_path = None
        self.media_process = None
        self.media_thread = None
        self.is_playing = False
    
    def _is_media_player_running(self):
        """Check if any known media player is running"""
        for proc in psutil.process_iter(['name']):
            try:
                process_name = proc.info['name'].lower()
                if any(player.lower() in process_name for player in self.media_players):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    
    def _ensure_media_player_running(self):
        """Ensure a media player is running, launch one if needed"""
        if not self._is_media_player_running():
            speak("No media player detected. Launching default media player.")
            try:
                if os.name == 'nt':  # Windows
                    os.system(f"start {self.default_audio_player}")
                else:  # Linux/Mac
                    subprocess.Popen([self.default_audio_player], 
                                    stdout=subprocess.DEVNULL, 
                                    stderr=subprocess.DEVNULL)
                return True
            except Exception as e:
                print(f"Error launching media player: {e}")
                return False
        return True
    
    def _is_windows_media_player_running(self):
        """Check if Windows Media Player is running"""
        if os.name != 'nt':  # Only for Windows
            return False
            
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'].lower() == 'wmplayer.exe':
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    
    def _focus_media_player(self):
        """Focus the media player window to ensure commands are received"""
        try:
            if os.name == 'nt':  # Windows
                # Try to focus Windows Media Player
                if self._is_windows_media_player_running():
                    # Use Windows API to find and focus the window
                    try:
                        import win32gui
                        import win32con
                        
                        def callback(hwnd, windows):
                            if win32gui.IsWindowVisible(hwnd) and "Windows Media Player" in win32gui.GetWindowText(hwnd):
                                windows.append(hwnd)
                            return True
                        
                        windows = []
                        win32gui.EnumWindows(callback, windows)
                        
                        if windows:
                            # Focus the first found window
                            win32gui.ShowWindow(windows[0], win32con.SW_RESTORE)
                            win32gui.SetForegroundWindow(windows[0])
                            return True
                    except ImportError:
                        # If win32gui is not available, try alternative method
                        os.system("taskkill /f /im wmplayer.exe")
                        time.sleep(0.5)
                        os.system("start wmplayer")
                        time.sleep(2)  # Wait for it to start
                        return True
            
            # For other OS or if Windows-specific method failed
            return False
        except Exception as e:
            print(f"Error focusing media player: {e}")
            return False
    
    def _is_vlc_player_running(self):
        """Check if VLC Player is running"""
        for proc in psutil.process_iter(['name']):
            try:
                process_name = proc.info['name'].lower()
                if 'vlc' in process_name:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def _create_vlc_playlist(self, directory, file_extensions, random_selection=False, max_items=10):
        """Create a VLC playlist with all media files in the directory or a random selection
        
        Args:
            directory: Directory containing media files
            file_extensions: List of file extensions to include
            random_selection: If True, select random files instead of all files
            max_items: Maximum number of items to include if random_selection is True
            
        Returns:
            Path to the created playlist or None if failed
        """
        try:
            # Get all media files with absolute paths
            media_files = []
            for ext in file_extensions:
                found_files = glob.glob(os.path.join(directory, f"*{ext}"))
                # Convert to absolute paths
                found_files = [os.path.abspath(f) for f in found_files]
                media_files.extend(found_files)
            
            if not media_files:
                print("No media files found in directory:", directory)
                return None
            
            # Print found files for debugging
            print(f"Found {len(media_files)} media files in {directory}:")
            for file in media_files[:5]:  # Print first 5 files
                print(f"  - {os.path.basename(file)}")
            if len(media_files) > 5:
                print(f"  ... and {len(media_files) - 5} more")
            
            # If random selection is requested and we have enough files
            if random_selection and len(media_files) > max_items:
                print(f"Selecting {max_items} random media files for playlist")
                media_files = random.sample(media_files, max_items)
            else:
                print(f"Adding all {len(media_files)} media files to playlist")
                
            # If there's only one file, duplicate it to ensure playlist navigation works
            if len(media_files) == 1:
                print(f"Only one media file found in {directory}. Next/previous track commands may not work as expected.")
                # Duplicate the file in the playlist to make next/previous work
                media_files = [media_files[0]] * 3  # Add the same file multiple times
                
            # Create a temporary playlist file with absolute path
            playlist_path = os.path.join(directory, "playlist.m3u")
            playlist_path = os.path.abspath(playlist_path)
            
            print(f"Creating playlist at: {playlist_path}")
            
            with open(playlist_path, 'w', encoding='utf-8') as f:
                f.write("#EXTM3U\n")
                for file_path in media_files:
                    # Use absolute paths for better compatibility
                    f.write(f"{file_path}\n")
            
            # Verify playlist was created
            if os.path.exists(playlist_path):
                print(f"Playlist created successfully with {len(media_files)} entries")
                # Store the playlist path for cleanup later
                self.current_playlist_path = playlist_path
                return playlist_path
            else:
                print("Failed to create playlist file")
                return None
                
        except Exception as e:
            print(f"Error creating VLC playlist: {e}")
            return None
    
    def _cleanup_playlist(self):
        """Remove the temporary playlist file when exiting"""
        try:
            if hasattr(self, 'current_playlist_path') and self.current_playlist_path:
                if os.path.exists(self.current_playlist_path):
                    os.remove(self.current_playlist_path)
                    print(f"Removed temporary playlist: {self.current_playlist_path}")
                    self.current_playlist_path = None
        except Exception as e:
            print(f"Error cleaning up playlist: {e}")
    
    def _play_media_in_thread(self, file_path, player):
        """Play media in a separate thread"""
        try:
            if os.name == 'nt':  # Windows
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                self.media_process = subprocess.Popen(
                    [player, file_path],
                    startupinfo=startupinfo,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            else:  # Linux/Mac
                self.media_process = subprocess.Popen(
                    [player, file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            self.is_playing = True
            self.media_process.wait()
            self.is_playing = False
        except Exception as e:
            print(f"Error playing media: {e}")
            self.is_playing = False

    def _open_media_file(self, file_path, default_player):
        """Open media file in a non-blocking way"""
        try:
            # Stop any currently playing media
            self.stop_media()
            
            # Start new media playback in a thread
            self.media_thread = threading.Thread(
                target=self._play_media_in_thread,
                args=(file_path, default_player)
            )
            self.media_thread.daemon = True  # Thread will be terminated when main program exits
            self.media_thread.start()
            return True
        except Exception as e:
            print(f"Error opening media file: {e}")
            return False

    def stop_media(self):
        """Stop currently playing media"""
        try:
            if self.media_process and self.is_playing:
                self.media_process.terminate()
                self.is_playing = False
                time.sleep(0.5)  # Give some time for the process to terminate
            return True
        except Exception as e:
            print(f"Error stopping media: {e}")
            return False

    def handle_media(self, command):
        """Handle media control commands"""
        try:
            if "youtube" in command.lower():
                # YouTube commands are handled by web_search.py
                return False
            
            # Clean up any existing playlist if we're starting a new media session
            if any(keyword in command.lower() for keyword in ["play", "watch", "open"]):
                self._cleanup_playlist()
            
            # Ensure a media player is running
            self._ensure_media_player_running()
            
            # Try to focus the media player window
            self._focus_media_player()
            
            # Media control commands
            command = command.lower()
            
            # Check which media player is running
            is_wmp = self._is_windows_media_player_running()
            is_vlc = self._is_vlc_player_running()
            
            # Handle volume controls
            if "volume up" in command or "increase volume" in command or "louder" in command:
                speak("Increasing volume")
                # Try multiple methods for volume control
                try:
                    # Method 1: Standard volume keys
                    for _ in range(5):
                        pyautogui.press('volumeup')
                        time.sleep(0.1)  # Small delay between presses
                except:
                    # Method 2: Try keyboard shortcuts
                    if is_vlc:
                        pyautogui.hotkey('ctrl', 'up')  # VLC volume up
                    else:
                        pyautogui.hotkey('ctrl', 'up')
                return True
                
            elif "volume down" in command or "decrease volume" in command or "quieter" in command:
                speak("Decreasing volume")
                # Try multiple methods for volume control
                try:
                    # Method 1: Standard volume keys
                    for _ in range(5):
                        pyautogui.press('volumedown')
                        time.sleep(0.1)  # Small delay between presses
                except:
                    # Method 2: Try keyboard shortcuts
                    if is_vlc:
                        pyautogui.hotkey('ctrl', 'down')  # VLC volume down
                    else:
                        pyautogui.hotkey('ctrl', 'down')
                return True
                
            elif "mute" in command:
                speak("Muting audio")
                # Try multiple methods for mute
                try:
                    # Method 1: Standard mute key
                    pyautogui.press('volumemute')
                except:
                    # Method 2: Try keyboard shortcuts
                    if is_wmp:
                        pyautogui.press('f8')  # Windows Media Player mute shortcut
                    elif is_vlc:
                        pyautogui.press('m')  # VLC mute shortcut
                    else:
                        pyautogui.hotkey('ctrl', 'm')
                return True
                
            # Handle playback controls
            elif "pause" in command or "stop" in command:
                speak("Pausing playback")
                
                # Player-specific shortcuts
                if is_wmp:
                    pyautogui.press('space')  # WMP uses space for play/pause
                    return True
                elif is_vlc:
                    pyautogui.press('space')  # VLC uses space for play/pause
                    return True
                
                # Try one method at a time with fallbacks
                success = False
                
                # Method 1: Standard media key
                try:
                    pyautogui.press('playpause')
                    success = True
                except:
                    pass
                
                # If Method 1 failed, try Method 2
                if not success:
                    try:
                        # Space bar (works in most players)
                        pyautogui.press('space')
                        success = True
                    except:
                        pass
                
                # If Method 2 failed, try Method 3
                if not success:
                    try:
                        # K key (works in YouTube)
                        pyautogui.press('k')
                    except:
                        pass
                
                return True
                
            elif "play" in command and not any(word in command for word in ["music", "song", "video", "movie", "audio"]):
                speak("Resuming playback")
                
                # Player-specific shortcuts
                if is_wmp:
                    # For Windows Media Player, try multiple methods
                    # Method 1: Space for play/pause toggle
                    pyautogui.press('space')
                    time.sleep(0.5)  # Wait a bit to see if it worked
                    
                    # Method 2: Try the play button (p key)
                    pyautogui.press('p')
                    
                    # Method 3: Try Alt+P shortcut
                    time.sleep(0.5)
                    pyautogui.hotkey('alt', 'p')
                    return True
                elif is_vlc:
                    # VLC uses space for play/pause
                    pyautogui.press('space')
                    return True
                
                # For other players, try different methods
                # Method 1: Standard media key
                pyautogui.press('playpause')
                time.sleep(0.5)  # Wait a bit between methods
                
                # Method 2: Space bar (works in most players)
                pyautogui.press('space')
                time.sleep(0.5)  # Wait a bit between methods
                
                # Method 3: K key (works in YouTube)
                pyautogui.press('k')
                time.sleep(0.5)  # Wait a bit between methods
                
                # Method 4: P key (works in some players)
                pyautogui.press('p')
                
                return True
                
            elif "next" in command or "skip" in command:
                speak("Playing next track")
                
                # Player-specific shortcuts
                if is_wmp:
                    pyautogui.hotkey('ctrl', 'f')  # WMP uses Ctrl+F for next track
                    return True
                elif is_vlc:
                    pyautogui.press('n')  # VLC uses 'n' for next
                    return True
                
                # Try one method at a time with fallbacks
                success = False
                
                # Method 1: Standard media key
                try:
                    pyautogui.press('nexttrack')
                    success = True
                except:
                    pass
                
                # If Method 1 failed, try Method 2
                if not success:
                    try:
                        # Right arrow (works in many players)
                        pyautogui.press('right')
                        success = True
                    except:
                        pass
                
                # If Method 2 failed, try Method 3
                if not success:
                    try:
                        # N key (works in some players)
                        pyautogui.press('n')
                        success = True
                    except:
                        pass
                
                # If Method 3 failed, try Method 4
                if not success:
                    try:
                        # L key (works in YouTube)
                        pyautogui.press('l')
                    except:
                        pass
                
                return True
                
            elif "previous" in command or "back" in command:
                speak("Playing previous track")
                
                # Player-specific shortcuts
                if is_wmp:
                    pyautogui.hotkey('ctrl', 'b')  # WMP uses Ctrl+B for previous track
                    return True
                elif is_vlc:
                    pyautogui.press('p')  # VLC uses 'p' for previous
                    return True
                
                # Try one method at a time with fallbacks
                success = False
                
                # Method 1: Standard media key
                try:
                    pyautogui.press('prevtrack')
                    success = True
                except:
                    pass
                
                # If Method 1 failed, try Method 2
                if not success:
                    try:
                        # Left arrow (works in many players)
                        pyautogui.press('left')
                        success = True
                    except:
                        pass
                
                # If Method 2 failed, try Method 3
                if not success:
                    try:
                        # P key (works in some players)
                        pyautogui.press('p')
                        success = True
                    except:
                        pass
                
                # If Method 3 failed, try Method 4
                if not success:
                    try:
                        # J key (works in YouTube)
                        pyautogui.press('j')
                    except:
                        pass
                
                return True
                
            # If no specific media control command was recognized
            else:
                speak("Please specify what you want to do with the media (play, pause, next, previous, or volume)")
                return False
                
            return True
        except Exception as e:
            print(f"Error in media control: {e}")
            speak("Sorry, I couldn't control the media. Make sure a media player is running.")
            return False
    
    def play_audio(self, audio_name=None):
        """Play audio from the audio directory"""
        try:
            # Clean up any existing playlist before creating a new one
            self._cleanup_playlist()
            
            # Get all audio files
            audio_files = []
            for ext in self.audio_extensions:
                audio_files.extend(glob.glob(os.path.join(self.audio_dir, f"*{ext}")))
            
            if not audio_files:
                speak("No audio files found in the audio directory. Please add some audio files to the media/audio folder.")
                return False
            
            # If audio name is specified, try to find a matching audio
            if audio_name:
                matching_files = []
                for file in audio_files:
                    if audio_name.lower() in os.path.basename(file).lower():
                        matching_files.append(file)
                
                if matching_files:
                    # Play the first matching audio
                    file_path = matching_files[0]
                    file_name = os.path.basename(file_path)
                    speak(f"Playing audio: {file_name}")
                else:
                    speak(f"Couldn't find audio matching '{audio_name}'. Playing a random audio file instead.")
                    file_path = random.choice(audio_files)
                    file_name = os.path.basename(file_path)
                    speak(f"Playing audio: {file_name}")
            else:
                # Play a random audio
                file_path = random.choice(audio_files)
                file_name = os.path.basename(file_path)
                speak(f"Playing random audio: {file_name}")
            
            # Open the audio with the default media player
            return self._open_media_file(file_path, self.default_audio_player)
                
        except Exception as e:
            print(f"Error playing audio: {e}")
            speak("Sorry, I couldn't play the audio.")
            return False
    
    def play_video(self, video_name=None):
        """Play video from the video directory"""
        try:
            # Clean up any existing playlist before creating a new one
            self._cleanup_playlist()
            
            # Get all video files
            video_files = []
            for ext in self.video_extensions:
                video_files.extend(glob.glob(os.path.join(self.video_dir, f"*{ext}")))
            
            if not video_files:
                speak("No video files found in the video directory. Please add some video files to the media/video folder.")
                return False
            
            # Check if user wants random videos
            is_random = video_name and "random" in video_name.lower()
            
            # If video name is specified, try to find a matching video
            if video_name and not is_random:
                matching_files = []
                for file in video_files:
                    if video_name.lower() in os.path.basename(file).lower():
                        matching_files.append(file)
                
                if matching_files:
                    # Play the first matching video
                    file_path = matching_files[0]
                    file_name = os.path.basename(file_path)
                    speak(f"Playing video: {file_name}")
                else:
                    speak(f"Couldn't find video matching '{video_name}'. Playing a random video file instead.")
                    file_path = random.choice(video_files)
                    file_name = os.path.basename(file_path)
                    speak(f"Playing video: {file_name}")
            elif is_random:
                # Play random videos (the playlist creation will handle selecting random videos)
                file_path = random.choice(video_files)
                speak("Playing random videos in playlist mode")
            else:
                # Play a random video
                file_path = random.choice(video_files)
                file_name = os.path.basename(file_path)
                speak(f"Playing random video: {file_name}")
            
            # Open the video with the default media player
            return self._open_media_file(file_path, self.default_video_player)
                
        except Exception as e:
            print(f"Error playing video: {e}")
            speak("Sorry, I couldn't play the video.")
            return False
    
    def play_music(self, song_name=None):
        """Legacy method for backward compatibility"""
        return self.play_audio(song_name)
    
    def take_screenshot(self):
        """Take a screenshot"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(self.screenshot_dir, f"screenshot_{timestamp}.png")
            pyautogui.screenshot(screenshot_path)
            speak("Screenshot taken successfully")
            return True
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            speak("Sorry, I couldn't take the screenshot.")
            return False
    
    def get_system_info(self):
        """Get basic system information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info_text = (
                f"CPU usage is {cpu_percent}%. "
                f"Memory usage is {memory.percent}%. "
                f"Disk usage is {disk.percent}%."
            )
            speak(info_text)
            return True
        except Exception as e:
            print(f"Error getting system info: {e}")
            speak("Sorry, I couldn't get the system information.")
            return False
    
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
    
    def get_weather_info(self, city):
        """Get weather information using web search"""
        try:
            search_query = f"weather in {city} today"
            speak(f"Searching for weather information in {city}")
            return search_web(search_query, speak_result=True)
        except Exception as e:
            print(f"Error getting weather info: {e}")
            speak("Sorry, I couldn't get the weather information.")
            return False
    
    def get_news(self):
        """Get news using web search"""
        try:
            search_query = "latest news headlines today"
            speak("Searching for the latest news")
            return search_web(search_query, speak_result=True)
        except Exception as e:
            print(f"Error getting news: {e}")
            speak("Sorry, I couldn't get the latest news.")
            return False
    
    def cleanup(self):
        """Clean up resources when the application exits"""
        try:
            self.stop_media()
            self._cleanup_playlist()
            print("Advanced features cleanup completed")
        except Exception as e:
            print(f"Error during cleanup: {e}")
            
    def __del__(self):
        """Destructor to ensure cleanup when object is destroyed"""
        self.cleanup() 