import os
import yt_dlp


def youtube_downloader(url: str, filename: str) -> dict:
    """
    Downloads a YouTube video with best quality to the 'media' folder.

    Args:
        url (str): YouTube video URL
        filename (str): Desired filename for the video (without extension)

    Returns:
        dict: Contains status (bool) and message (str) indicating success or failure
    """
    try:
        # Create media directory if it doesn't exist
        if not os.path.exists("media"):
            os.makedirs("media")

        # Sanitize filename
        filename = "".join(
            c for c in filename if c.isalnum() or c in (" ", "-", "_")
        ).strip()
        output_template = os.path.join("media", filename + ".%(ext)s")

        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": output_template,
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
        }

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return {
                "status": True,
                "message": "Video downloaded successfully",
                "filename": filename,
            }

    except Exception as e:
        return {
            "status": False,
            "message": f"Error downloading video: {str(e)}",
            "filename": None,
        }
