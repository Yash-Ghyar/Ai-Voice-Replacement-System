import moviepy.editor as mp
import os

def extract_audio(video_path):
    audio_path = os.path.join("uploads", "extracted_audio.wav")
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, codec='pcm_s16le')
    return audio_path
