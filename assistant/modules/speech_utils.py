import speech_recognition as sr
import pyttsx3

def recognize_speech():
    """Captures voice command and converts it to text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
        return None
    except sr.RequestError:
        print("Speech service unavailable.")
        return None

def speak(text):
    """Converts text to speech"""
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # Adjust speed
    engine.say(text)
    engine.runAndWait()
