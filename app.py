import speech_recognition as sr
from translate import Translator
from gtts import gTTS
import os
import streamlit as st
from playsound import playsound

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Calibrate microphone to ambient noise
        
        print("Listening for speech...")
        
        try:
            # Increase the timeout and phrase time limit to allow more time for speech input
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)  
            print("Speech detected, processing...")
            
            # Using Google's speech recognition API to convert speech to text
            recognized_text = recognizer.recognize_google(audio)
            print(f"Recognized text: {recognized_text}")
            return recognized_text
        
        except sr.WaitTimeoutError:
            print("No speech detected within the given time. Please try again.")
            return None
        
        except sr.RequestError as e:
            print(f"API request error: {e}. Please check your internet connection.")
            return None
        
        except sr.UnknownValueError:
            print("Could not understand the audio. Please speak clearly.")
            return None
        
def translate_text(text, target_language="es"):
    """Translate text to the target language."""
    translator = Translator(to_lang=target_language)
    try:
        translated_text = translator.translate(text)
        st.write(f"Translated Text: {translated_text}")
        return translated_text
    except Exception as e:
        st.write(f"Translation Error: {e}")
        return None

def speak_text(text, language="es"):
    """Convert text to speech and play the audio."""
    try:
        tts = gTTS(text=text, lang=language)
        audio_file = "output.mp3"
        tts.save(audio_file)
        playsound(audio_file)  # Play the audio
        os.remove(audio_file)  # Delete the audio file after playing
    except Exception as e:
        st.write(f"Text-to-Speech Error: {e}")

def real_time_translator(target_language="es"):
  """Continuously listen, translate, and speak the translation."""
  st.title("Real-Time Speech Translator")
  st.write(f"Starting Real-Time Translator (Target Language: {target_language})...")

  # Button to start recognition and translation
  if st.button("Start Listening"):
    recognized_text = recognize_speech()
    if recognized_text:
      translated_text = translate_text(recognized_text, target_language)
      if translated_text:
        speak_text(translated_text, language=target_language)  # Speak the translated text

# Frontend code with Streamlit
if __name__ == "__main__":
    # Choose target language
    target_language = st.selectbox("Select Target Language", ["es", "fr", "de", "it", "ja"])

    # Call the real-time translator function
    real_time_translator(target_language)
