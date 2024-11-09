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


def delete_video(filename):
    """
    Deletes a video file from the media folder.

    Args:
        filename (str): Name of the video file without extension
    """
    video_path = os.path.join("media", f"{filename}.mp4")

    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return {"status": False, "message": f"Video file '{video_path}' not found"}

    try:
        os.remove(video_path)
        return {"status": True, "message": "Video deleted successfully"}
    except Exception as e:
        return {"status": False, "message": f"Error deleting video: {str(e)}"}
