import gradio as gr
from transformers import pipeline
import gtts
from io import BytesIO
import tempfile

# Language dictionary for more readable dropdown
language_dict = {
    "English": "en",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Italian": "it"
}

# Load speech-to-text and translation pipelines
asr_pipeline = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-large-960h")  # English ASR
translation_pipelines = {}  # Cache translation pipelines for different languages

def load_translation_pipeline(target_language):
    """Load and cache translation pipeline."""
    if target_language not in translation_pipelines:
        translation_pipelines[target_language] = pipeline("translation", model=f"Helsinki-NLP/opus-mt-en-{target_language}")
    return translation_pipelines[target_language]

# Translation and audio generation function with error handling
def translate_speech_to_text(audio, input_lang_name, output_lang_name, modified_text=None):
    try:
        # Map selected language names to codes
        input_lang = language_dict[input_lang_name]
        output_lang = language_dict[output_lang_name]

        # Speech-to-text conversion if no manual modification has been made
        if modified_text is None or modified_text == "":
            asr_result = asr_pipeline(audio)["text"]
            original_text = asr_result if asr_result else "No transcription available."
        else:
            original_text = modified_text

        # Translation
        try:
            translation_pipeline = load_translation_pipeline(output_lang)
            translation = translation_pipeline(original_text)
            translated_text = translation[0]['translation_text']
        except Exception as e:
            translated_text = f"Translation error: {str(e)}"

        # Generate audio for translated text
        try:
            tts = gtts.gTTS(translated_text, lang=output_lang)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_file.name)
            audio_path = temp_file.name
        except Exception as e:
            audio_path = None
            translated_text += f" (Audio generation error: {str(e)})"

    except Exception as e:
        # Handle transcription error
        original_text = f"Transcription error: {str(e)}"
        translated_text = ""
        audio_path = None

    return original_text, translated_text, audio_path

# Gradio interface with editable "Original Transcript" field
interface = gr.Interface(
    fn=translate_speech_to_text,
    inputs=[
        gr.Audio(type="filepath", label="Speak Now"),
        gr.Dropdown(choices=list(language_dict.keys()), value="English", label="Input Language"),
        gr.Dropdown(choices=list(language_dict.keys()), value="German", label="Output Language"),
        gr.Textbox(label="Original Transcript", placeholder="Edit transcript here if needed"),  # Editable input-output field
    ],
    outputs=[
        gr.Textbox(label="Original Transcript"),
        gr.Textbox(label="Translated Transcript"),
        gr.Audio(label="Play Translated Speech"),
    ],
    live=True
)

interface.launch(share=True)