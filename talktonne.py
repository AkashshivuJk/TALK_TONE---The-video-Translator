#IMP!!

import os
import moviepy.editor as mp
import speech_recognition as sr
from google.cloud import translate_v2 as translate
from spleeter.separator import Separator
from gtts import gTTS
import langid
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip
import numpy as np


def separate_vocals_and_music(audio_path):
    try:
        separator = Separator('spleeter:2stems')
        separator.separate_to_file(audio_path, 'downloads/audio_stem')
        vocals_path = os.path.join('downloads', 'audio_stem','original_audio','vocals.wav')
        music_path = os.path.join('downloads', 'audio_stem','original_audio','accompaniment.wav')

        return vocals_path, music_path
    except AttributeError:
        print("Audio separation failed. Please check the input audio file.")
        return None, None
def convert_audio_to_text(audio_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
    return text
def translate_text(input_text, target_language, credentials_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    client = translate.Client()
    translation = client.translate(input_text, target_language=target_language)
    return translation['translatedText']
def convert_text_to_speech(file_path):

    with open(file_path, 'r') as file:
        text = file.read()
    language = langid.classify(text)[0]
    tts = gTTS(text, lang=language)
    audio_path = os.path.splitext(file_path)[0] + '.mp3'
    tts.save(audio_path)
    print("Audio file generated successfully.")
def get_pitch_factor(audio):
    
    samples = np.array(audio.get_array_of_samples())
    frequencies = np.fft.fftfreq(samples.size, 1.0/audio.frame_rate)
    positive_frequencies = frequencies[np.where(frequencies >= 0)]
    magnitude = np.abs(np.fft.fft(samples))
    peak_frequency = positive_frequencies[np.argmax(magnitude[np.where(frequencies >= 0)])]
    return peak_frequency / 440.0  
def change_voice(input_voice_sample, second_audio_file, output_file):
   
    try:
        voice_sample = AudioSegment.from_file(input_voice_sample)
        second_audio = AudioSegment.from_file(second_audio_file)
        voice_sample_pitch_factor = get_pitch_factor(voice_sample)
        second_audio_pitch_factor = get_pitch_factor(second_audio)
        pitch_shift_needed = voice_sample_pitch_factor / second_audio_pitch_factor
        new_audio = second_audio._spawn(second_audio.raw_data, overrides={
            "frame_rate": int(second_audio.frame_rate * pitch_shift_needed)
        }).set_frame_rate(second_audio.frame_rate)
        new_audio.export(output_file, format="wav")
        print("Voice change successful.")
    except Exception as e:
        print("Error:", e)
def change_audio_speed(input_file, output_file, required_duration):
    try:
        audio = AudioSegment.from_file(input_file)
        actual_duration = len(audio) / 1000.0  # Convert from milliseconds to seconds
        speed_factor =  actual_duration/required_duration
        new_audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * speed_factor)
        }).set_frame_rate(audio.frame_rate)
        new_audio.export(output_file, format="wav")
        print("Audio speed change successful.")
    except Exception as e:
        print("Error:", e)
def get_audio_length(audio_file):
   
    try:
        audio = AudioSegment.from_file(audio_file)
        audio_length = len(audio)/1000
        return audio_length
    except Exception as e:
        print("Error:", e)
        return None
def change_voicee(input_file, output_file, pitch_factor):
    
    try:
        audio = AudioSegment.from_file(input_file)
        new_audio = audio.set_frame_rate(int(audio.frame_rate * pitch_factor))
        new_audio.export(output_file, format="wav")
        print("Voice change successful.")
    except Exception as e:
        print("Error:", e)
def add_audio_overlay(background_file, overlay_file, output_file):

    background_audio = AudioSegment.from_file(background_file)
    overlay_audio = AudioSegment.from_file(overlay_file)
    combined_audio = background_audio.overlay(overlay_audio)
    combined_audio.export(output_file, format="wav")
    print("Audio overlay completed successfully.")
def combine_audio_video(audio_file, video_file, output_file):

    audio = AudioFileClip(audio_file)
    video = VideoFileClip(video_file)
    video_with_audio = video.set_audio(audio)
    video_with_audio.write_videofile(output_file, codec="libx264", audio_codec="aac")
    print("Audio and video combined successfully.")



video_path = input("video path : ")
target_language =input("Target language: ")
credentials_path = input("credentials :")


video = mp.VideoFileClip(video_path)
video_clip = video.without_audio()
audio_clip = video.audio
output_folder = 'downloads'
os.makedirs(output_folder, exist_ok=True)
no_voice_video_path = os.path.join(output_folder, 'no_voice_video.mp4')
video_clip.write_videofile(no_voice_video_path)
audio_path = os.path.join(output_folder, 'original_audio.wav')
audio_clip.write_audiofile(audio_path)
vocals, music = separate_vocals_and_music(audio_path)
print("Vocals saved as:", vocals)
print("Music saved as:", music)


if vocals:
    vocal_text = convert_audio_to_text(vocals)
    print("Vocal Text:", vocal_text)
    text_path = os.path.join(output_folder, 'vocal_text.txt')
    with open(text_path, 'w') as file:
        file.write(vocal_text)
    print("Audio to text conversion complete. Vocal text saved as:", text_path)
    translated_text = translate_text(vocal_text, target_language, credentials_path)
    print("Translated Text:", translated_text)
    translated_text_path = os.path.join(output_folder, 'Translated_text.txt')
    with open(translated_text_path, 'w') as file:
        file.write(translated_text)
    print("Translation complete. Translated text saved as:", translated_text_path)
    input_text_file = text_path
    translate_text(input_text_file, target_language, credentials_path)


input_file = translated_text_path
convert_text_to_speech(input_file)



input_voice_sample = "/content/downloads/audio_stem/original_audio/vocals.wav"
second_audio_file = "/content/downloads/Translated_text.mp3"
output_file = "/content/downloads/raw_audio.wav"
change_voice(input_voice_sample, second_audio_file, output_file)



input_file = "/content/downloads/raw_audio.wav"
output_file = "/content/downloads/raw_audio2.wav"
try:
    required_duration = get_audio_length(vocals)
    change_audio_speed(input_file, output_file, required_duration)
except ValueError:
    print("Invalid input. Please enter a valid duration in seconds.")



input_file = "/content/downloads/raw_audio2.wav" 
output_file = "/content/downloads/raw_audio3.wav"  
try:
    audio = AudioSegment.from_file(input_file)
    pitch_factor = get_pitch_factor(audio)
    change_voicee(input_file, output_file, pitch_factor)
except ValueError:
    print("Invalid input. Please enter a valid pitch factor.")



background_file = "/content/downloads/audio_stem/original_audio/accompaniment.wav"
overlay_file = "/content/downloads/raw_audio3.wav"
output_file = "/content/downloads/final_audio.wav"
add_audio_overlay(background_file, overlay_file, output_file)



audio_file = "/content/downloads/final_audio.wav"
video_file = "/content/downloads/no_voice_video.mp4"
output_file = "/content/downloads/final_video.mp4"
combine_audio_video(audio_file, video_file, output_file)


