import os
import re
import nltk
import pronouncing
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from pydub import AudioSegment
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, vfx
import boto3

# Load environment variables from the .env file
load_dotenv(dotenv_path='key.env')

# Setting up the Flask app
app = Flask(__name__)

# Download some necessary NLTK resources before we start
nltk.download('punkt')
nltk.download('cmudict')

# Create a Polly client to handle the text-to-speech conversion
def get_polly_client():
    return boto3.client(
        'polly',
        region_name='us-east-1',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )

# Set up paths for the ffmpeg library. This will help with audio and video processing.
ffmpeg_path = r'C:/Path_ff/ffmpeg.exe'
AudioSegment.converter = ffmpeg_path
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path

# This function will handle the basic cleaning up of text, such as lowercasing, 
# replacing certain symbols, and removing unnecessary characters.
def nlp_preprocessing(text):
    text = text.lower()
    text = text.replace('₹', 'rupees')
    text = re.sub(r'(\d+),(\d+)', r'\1\2', text)  # Remove commas from numbers
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    tokens = nltk.word_tokenize(text)  # Tokenize text into words
    return ' '.join(tokens)

# This function slows down the audio a bit by altering the playback speed.
def slow_down_audio(sound, playback_speed=1.00):
    # Adjust the frame rate to change the speed
    slowed_sound = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * playback_speed)
    }).set_frame_rate(sound.frame_rate)
    return slowed_sound

# Polly has a text limit per request, so this function splits text into chunks
def split_text(text, max_length=3000):
    words = text.split()
    chunks = []
    current_chunk = ''

    # Collect words into chunks that don’t exceed the maximum character limit
    for word in words:
        if len(current_chunk) + len(word) + 1 <= max_length:
            current_chunk += (' ' + word) if current_chunk else word
        else:
            chunks.append(current_chunk)
            current_chunk = word

    if current_chunk:
        chunks.append(current_chunk)
    return chunks

# Convert text into speech with Polly, then combine the audio chunks into a single file
def text_to_speech(text, voice_id='Matthew'):
    polly = get_polly_client()
    chunks = split_text(text)
    audio_segments = []

    # For each text chunk, request Polly to convert it into speech
    for i, chunk in enumerate(chunks):
        response = polly.synthesize_speech(Text=chunk, OutputFormat='mp3', VoiceId=voice_id)
        if 'AudioStream' in response:
            temp_audio_path = f'static/speech_{i}.mp3'
            with open(temp_audio_path, 'wb') as file:
                file.write(response['AudioStream'].read())
            audio_segment = AudioSegment.from_mp3(temp_audio_path)
            audio_segments.append(audio_segment)
            os.remove(temp_audio_path)

    if audio_segments:
        combined_audio = sum(audio_segments)
        slowed_sound = slow_down_audio(combined_audio)
        slowed_sound.export("static/slowed_speech.mp3", format="mp3")

# Turn the text into a series of phonemes using NLTK and Pronouncing libraries
def text_to_phonemes(text):
    words = nltk.word_tokenize(text.lower())
    phonemes = []
    for word in words:
        pronunciations = pronouncing.phones_for_word(word)
        phonemes.extend(pronunciations[0].split() if pronunciations else ['SIL'])  # Default to silence if unknown word
    return phonemes

# Mapping of phonemes to the mouth shapes (visemes) we'll use for the avatar
phoneme_viseme_map = {
    'AA': 'open', 'AE': 'wide', 'AH': 'open', 'AO': 'open', 'EH': 'wide',
    'ER': 'open', 'IH': 'happy', 'IY': 'happy', 'UH': 'sad', 'UW': 'sad',
    'SIL': 'neutral', 'CH': 'surprised', 'JH': 'surprised', 'SH': 'surprised',
    'TH': 'surprised', 'DH': 'surprised', 'F': 'sad', 'V': 'sad'
}

# This will adjust the video speed by a given factor, slowing it down or speeding it up
def adjust_video_speed(video_clip, speed_factor):
    return video_clip.fx(vfx.speedx, speed_factor)

# This function takes the phonemes, audio, and mouth shapes to generate the avatar video
def generate_avatar_video(phonemes, audio_path, output_video_path, speed_factor=0.80):
    # We have different images for different mouth shapes
    mouth_shapes = {
        'neutral': 'static/avatar/neutral.png', 'open': 'static/avatar/open.png',
        'wide': 'static/avatar/wide.png', 'happy': 'static/avatar/happy.png',
        'sad': 'static/avatar/sad.png', 'surprised': 'static/avatar/surprised.png',
    }

    audio_clip = AudioFileClip(audio_path)
    total_duration = audio_clip.duration
    duration_per_phoneme = total_duration / len(phonemes)

    clips = [
        ImageClip(mouth_shapes.get(phoneme_viseme_map.get(phoneme, 'neutral')))
        .set_duration(duration_per_phoneme)
        for phoneme in phonemes
    ]

    video = concatenate_videoclips(clips, method="compose").set_audio(audio_clip)

    # Slow down or speed up the video
    video = adjust_video_speed(video, speed_factor)
    video.write_videofile(output_video_path, fps=24, codec='libx264')

# Routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate-avatar', methods=['POST'])
def generate_avatar():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    preprocessed_text = nlp_preprocessing(text)
    text_to_speech(preprocessed_text, voice_id='Joanna')
    phonemes = text_to_phonemes(preprocessed_text)

    audio_path = 'static/slowed_speech.mp3'
    output_video_path = 'static/avatar_video.mp4'
    generate_avatar_video(phonemes, audio_path, output_video_path, speed_factor=0.80)

    return jsonify({"message": "Avatar video generated successfully", "file": "/static/avatar_video.mp4"}), 200

# Entry point to start the app
if __name__ == "__main__":
    app.run(debug=True)
