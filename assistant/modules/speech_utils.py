import speech_recognition as sr
import pyttsx3
import logging
import os
from google.cloud import texttospeech
from pathlib import Path

# Set up logging to show only important information
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',  # Simplified format
    handlers=[
        logging.FileHandler('assistant.log'),  # Full logs in file
        logging.StreamHandler()  # Simplified logs in console
    ]
)
logger = logging.getLogger(__name__)

# Disable debug logs from other libraries
logging.getLogger('comtypes').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

# Voice settings
VOICE_TYPE = "local"  # Can be "local" or "google"
GOOGLE_VOICE_NAME = "en-IN-Standard-A"  # Indian English female voice
GOOGLE_VOICE_GENDER = texttospeech.SsmlVoiceGender.FEMALE

def recognize_speech():
    """Captures voice command and converts it to text"""
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("\nListening...")
            
            # Make it more sensitive to speech
            recognizer.energy_threshold = 250  # Lower threshold for softer speech
            recognizer.dynamic_energy_threshold = True
            recognizer.pause_threshold = 0.6  # Slightly longer pause for Indian English rhythm
            recognizer.operation_timeout = None
            
            # Shorter duration for ambient noise adjustment
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Ready to listen.")
            
            try:
                audio = recognizer.listen(source)
                print("Processing speech...")

                try:
                    # Using en-IN for Indian English
                    text = recognizer.recognize_google(
                        audio,
                        language="en-IN",  # Indian English
                        show_all=False  # Only return most confident result
                    )
                    print(f"You said: {text}")
                    return text.lower()
                except sr.UnknownValueError:
                    print("Sorry, I couldn't understand what you said.")
                    return None
                except sr.RequestError as e:
                    print("Could not request results from speech service.")
                    return None
            except Exception as e:
                print("Error during listening. Please try again.")
                return None
                
    except Exception as e:
        print("Error accessing microphone. Please check your microphone settings.")
        return None

def speak_google(text):
    """Converts text to speech using Google Cloud TTS"""
    try:
        # Initialize the client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-IN",
            name=GOOGLE_VOICE_NAME,
            ssml_gender=GOOGLE_VOICE_GENDER
        )

        # Select the type of audio file
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,
            pitch=0
        )

        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # Create output directory if it doesn't exist
        output_dir = Path("temp_audio")
        output_dir.mkdir(exist_ok=True)
        
        # Save the audio file
        output_file = output_dir / "output.mp3"
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
            
        # Play the audio file using system default player
        os.system(f'start {output_file}')
        
    except Exception as e:
        print(f"Error with Google TTS: {e}")
        # Fallback to local TTS
        speak_local(text)

def speak_local(text):
    """Converts text to speech using local Windows TTS"""
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # Adjust speed
    
    # Get available voices
    voices = engine.getProperty('voices')
    
    # Try to find an Indian English voice
    indian_voice_found = False
    for voice in voices:
        if "indian" in voice.name.lower() or "en-in" in voice.id.lower():
            engine.setProperty('voice', voice.id)
            indian_voice_found = True
            break
    
    if not indian_voice_found:
        print("No Indian English voice found, using default voice")
    
    engine.say(text)
    engine.runAndWait()

def speak(text):
    """Main speak function that chooses between Google Cloud TTS and local TTS"""
    if VOICE_TYPE == "google":
        speak_google(text)
    else:
        speak_local(text)

def list_available_voices():
    """Lists all available voices (both local and Google Cloud)"""
    print("\nLocal Windows Voices:")
    print("===================")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for idx, voice in enumerate(voices):
        print(f"{idx + 1}. {voice.name}")
        print(f"   ID: {voice.id}")
        print("-------------------")
    
    print("\nGoogle Cloud Voices (Indian English):")
    print("=================================")
    try:
        client = texttospeech.TextToSpeechClient()
        voices = client.list_voices(language_code="en-IN")
        for idx, voice in enumerate(voices.voices):
            print(f"{idx + 1}. {voice.name}")
            print(f"   Gender: {voice.ssml_gender}")
            print("-------------------")
    except Exception as e:
        print("Error accessing Google Cloud voices. Make sure you have set up Google Cloud credentials.")
