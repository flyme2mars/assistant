import os
import subprocess


def open_video(filename):
    """
    Opens a video file from the media folder in Elmedia Player.

    Args:
        filename (str): Name of the video file without extension
    """
    video_path = os.path.join("media", f"{filename}.mp4")

    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return

    try:
        subprocess.run(["open", "-a", "Elmedia Video Player", video_path])
    except Exception as e:
        print(f"Error opening video: {str(e)}")
