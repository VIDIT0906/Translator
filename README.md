# Speech-to-Text Translation App
This project is a speech-to-text translation application that allows users to:
* Convert spoken input into text.
* Translate the text to a target language.
* Play the translated text as audio.

Built with Gradio, Hugging Face Transformers, and Google Text-to-Speech (gTTS), this app supports multiple languages for translation, enabling seamless multilingual communication.

# Features
* Automatic Speech Recognition (ASR): Converts spoken English input to text using a speech recognition model.
* Real-Time Translation: Translates text from English to a target language of choice.
* Audio Playback: Generates audio of the translated text, allowing users to hear the translated phrase.
* User-Friendly Interface: Dual transcript display (original and translated), language selection dropdowns, and a “Speak” button for audio playback.


# Technologies Used
*  Gradio: User interface framework for easy integration of the app with a web-based UI.
* Hugging Face Transformers: Provides models for automatic speech recognition (ASR) and translation.
* gTTS: Text-to-speech library for generating audio of translated text.


## Getting Started
# Requirements
* Python 3.7 or later
* gradio, transformers, gtts, and tempfile libraries
* ffmpeg installed and added to your system path for audio processing


# Installation
1. Clone the Repository  
git clone https://github.com/your-username/speech-to-text-translation-app.git
cd speech-to-text-translation-app

2. Install Dependencies  
pip install -r requirements.txt

3. Install ffmpeg  
* Follow these instructions to install ffmpeg for your operating system.
* Add the ffmpeg installation path to your system path.


# Running the App  
Once dependencies are installed, run the app with:  
python main.py  

The app will launch in your default browser, displaying the Gradio interface for audio input, transcription, translation, and playback.

***

# Usage Guide
1. Select Input Language: Choose the language you’ll be speaking in.
2. Select Output Language: Choose the language for the translation.
3. Speak into the Microphone: Click on the "Speak Now" button and say your phrase or sentence. The app will automatically transcribe your speech.
4. View and Listen to Translations:
* Original Transcript: Shows the text converted from your speech.
* Translated Transcript: Displays the translated text.
* Play Translated Speech: Listen to the translated text spoken in the target language.

***

# Supported Languages  
Input Language
* English (additional input languages may be supported in future versions)

Output Languages  
* German, French, Spanish, Italian

***

# Code Structure
* main.py: Main file containing the application code.
* requirements.txt: List of Python dependencies.
* README.md: Documentation file.

# Security Considerations  
* Ensure you handle temporary audio files securely, deleting them after processing.
* Regularly update dependencies to minimize security vulnerabilities.

***

# Contributing
Feel free to open issues or submit pull requests for new features, bug fixes, or other improvements!
1. Fork the repository
2. Create a new branch (git checkout -b feature/YourFeature)
3. Commit your changes (git commit -m 'Add new feature')
4. Push to the branch (git push origin feature/YourFeature)
5. Open a pull request
   
## License
This project is licensed under the MIT License. See LICENSE for details.

***

# Acknowledgments
Special thanks to the developers of the Gradio and Hugging Face Transformers libraries, which made building this app possible.

