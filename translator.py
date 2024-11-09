import openai
import speech_recognition as sr
import pyttsx3
import streamlit as st
from googletrans import Translator
import toml

# Set OpenAI API key
openai.api_key = st.secrets["openai"]["api_key"]

# Initialize pyttsx3 engine for text-to-speech
engine = pyttsx3.init()

# Function to recognize speech and convert it to text
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening for speech...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.write(f"Transcribed text: {text}")
            return text
        except Exception as e:
            st.error(f"Error recognizing speech: {str(e)}")
            return None

# Function to translate text using OpenAI API
def translate_text(text, target_language='en'):
    try:
        # Using OpenAI for translation (Can also use Google Translate API or other models)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Translate this text into {target_language}: {text}",
            max_tokens=200
        )
        translated_text = response['choices'][0]['text'].strip()
        return translated_text
    except Exception as e:
        st.error(f"Error translating text: {str(e)}")
        return None

# Function for text-to-speech (audio playback)
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Streamlit UI setup
st.title("Speech to Text with Real-Time Translation")
st.sidebar.header("Settings")

# Language selection (input and output languages)
input_language = st.sidebar.selectbox("Select input language", ["en", "es", "fr", "de", "hi"])
output_language = st.sidebar.selectbox("Select output language", ["en", "es", "fr", "de", "hi"])

# Button to start speech recognition
if st.button("Start Speaking"):
    original_text = recognize_speech()
    if original_text:
        # Translate the text to the selected output language
        translated_text = translate_text(original_text, output_language)
        if translated_text:
            # Display both original and translated transcripts
            st.subheader("Original Transcript")
            st.write(original_text)
            st.subheader("Translated Transcript")
            st.write(translated_text)

            # Button to speak the translated text
            if st.button("Speak Translated Text"):
                speak_text(translated_text)
