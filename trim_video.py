from moviepy.editor import VideoFileClip
import os
from datetime import datetime


def time_to_seconds(time_str):
    """Convert time string (HH:MM:SS) to seconds."""
    try:
        # First try HH:MM:SS format
        time_obj = datetime.strptime(time_str, "%H:%M:%S")
        return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
    except ValueError:
        try:
            # If that fails, try MM:SS format
            time_obj = datetime.strptime(time_str, "%M:%S")
            return time_obj.minute * 60 + time_obj.second
        except ValueError:
            # If both fail, assume it's just seconds
            return float(time_str)


def trim_video(video_name: str, start_time: str, end_time: str) -> dict:
    """
    Trims a video file from the media folder.

    Args:
        video_name (str): Name of the video file in the media folder
        start_time (str): Start time in format HH:MM:SS, MM:SS, or seconds
        end_time (str): End time in format HH:MM:SS, MM:SS, or seconds

    Returns:
        dict: Contains status (bool) and message (str) indicating success or failure
    """
    try:
        input_path = os.path.join("media", f"{video_name}.mp4")
        video = VideoFileClip(input_path)

        start_seconds = time_to_seconds(start_time)
        end_seconds = time_to_seconds(end_time)

        if start_seconds >= end_seconds or end_seconds > video.duration:
            raise ValueError("Invalid time range")

        output_path = os.path.join("media", f"{video_name}_trimmed.mp4")

        cropped_video = video.subclip(start_seconds, end_seconds)
        cropped_video.write_videofile(output_path, logger=None)

        video.close()
        cropped_video.close()

        return {
            "status": True,
            "message": "Video trimmed successfully",
            "output_file": output_path,
        }

    except Exception as e:
        return {
            "status": False,
            "message": f"Error trimming video: {str(e)}",
            "output_file": None,
        }
