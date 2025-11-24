import moviepy.editor as mp
import os

def replace_audio_in_video(video_path, new_audio_path):
    print("🎥 Combining video with AI audio...")

    output_path = os.path.join("assets/outputs", "final_output.mp4")

    video_clip = mp.VideoFileClip(video_path)
    new_audio = mp.AudioFileClip(new_audio_path)
    final = video_clip.set_audio(new_audio)
    final.write_videofile(output_path, codec='libx264', audio_codec='aac')

    print("✅ Final video saved:", output_path)
    return output_path
