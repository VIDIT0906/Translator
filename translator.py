import speech_recognition as sr
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from gtts import gTTS
import tempfile
import torch

# Function to dynamically load the Hugging Face translation model based on language pair
def load_translation_model(src_lang, tgt_lang):
    model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

# Function to recognize speech and convert it to text
def recognize_speech():
    # Check if a microphone is available
    if not sr.Microphone.list_microphone_names():
        st.error("No microphone detected. Please check your audio settings.")
        return None

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

# Function to translate text using Hugging Face model
def translate_text(text, src_lang, tgt_lang):
    try:
        # Load tokenizer and model for the specified language pair
        tokenizer, model = load_translation_model(src_lang, tgt_lang)
        
        # Tokenize input text and translate
        inputs = tokenizer(text, return_tensors="pt", padding=True)
        outputs = model.generate(**inputs)
        
        # Decode translated text
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return translated_text
    except Exception as e:
        st.error(f"Error translating text: {str(e)}")
        return None

# Function for text-to-speech (audio playback) using gTTS
def speak_text(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts.save(fp.name + ".mp3")
            st.audio(fp.name + ".mp3", format="audio/mp3")
    except Exception as e:
        st.error(f"Error with text-to-speech playback: {str(e)}")

# Streamlit UI setup
st.title("Speech to Text with Real-Time Translation using Hugging Face")
st.sidebar.header("Settings")

# Language options with full names
language_options = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi"
}

# Language selection for source and target languages with readable names
input_language_name = st.sidebar.selectbox("Select input language", list(language_options.keys()))
output_language_name = st.sidebar.selectbox("Select output language", list(language_options.keys()))

# Get the language codes from the selected names
input_language = language_options[input_language_name]
output_language = language_options[output_language_name]

# Button to start speech recognition
if st.button("Start Speaking"):
    original_text = recognize_speech()
    if original_text:
        # Translate the text to the selected output language using Hugging Face
        translated_text = translate_text(original_text, input_language, output_language)

        if translated_text:
            # Display both original and translated transcripts
            st.subheader("Original Transcript")
            st.write(original_text)
            st.subheader("Translated Transcript")
            st.write(translated_text)

            # Button to speak the translated text
            if st.button("Speak Translated Text"):
                speak_text(translated_text, lang=output_language)

