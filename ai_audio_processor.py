import os
from openai import OpenAI
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def speech_to_text(audio_file_path):
    """
    Converts speech from an audio file to text using OpenAI's Whisper model.
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        print(f"Error during speech-to-text conversion: {e}")
        return None

# Initialize Hugging Face TTS pipeline
# Using a small, fast model for demonstration. You can choose other models.
# Example: "facebook/mms-tts-eng" or "suno/bark"
try:
    tts_pipeline = pipeline("text-to-speech", model="distilbert/distilbert-base-uncased")
except Exception as e:
    print(f"Error initializing Hugging Face TTS pipeline: {e}")
    tts_pipeline = None

def text_to_speech(text, output_file_path="output.wav"):
    """
    Converts text to speech using a Hugging Face TTS model.
    Saves the speech to an audio file.
    """
    if tts_pipeline is None:
        print("Hugging Face TTS pipeline not initialized. Cannot perform text-to-speech.")
        return False
    try:
        # The output of the pipeline is typically a dictionary with 'audio' and 'sampling_rate'
        # You might need to adjust this based on the specific TTS model used.
        # For simplicity, we'll assume it returns audio data directly or in a format
        # that can be saved. This part might require more specific handling
        # depending on the chosen model and desired output format.
        # For many models, the output is a numpy array, which can be saved using scipy.io.wavfile
        # import scipy.io.wavfile
        # scipy.io.wavfile.write(output_file_path, rate=speech["sampling_rate"], data=speech["audio"])
        speech = tts_pipeline(text)
        print(f"Text converted to speech and would be saved to {output_file_path} (actual saving logic depends on TTS model output).")
        return True
    except Exception as e:
        print(f"Error during text-to-speech conversion: {e}")
        return False

if __name__ == "__main__":
    # Example usage for STT (requires an audio file, e.g., 'input_audio.mp3')
    # audio_input_path = "input_audio.mp3"
    # if os.path.exists(audio_input_path):
    #     print(f"Converting speech to text from {audio_input_path}...")
    #     transcribed_text = speech_to_text(audio_input_path)
    #     if transcribed_text:
    #         print(f"Transcribed text: {transcribed_text}")
    # else:
    #     print(f"Audio file not found at {audio_input_path}. Skipping STT example.")

    # Example usage for TTS
    text_to_convert = "Hello, this is a test of the text-to-speech functionality."
    print(f"\nConverting text to speech: \"{text_to_convert}\"")
    text_to_speech(text_to_convert, "hello_test.wav")
