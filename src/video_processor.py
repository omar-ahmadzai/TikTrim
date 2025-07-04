import os
from moviepy.editor import VideoFileClip


def load_video(path: str) -> VideoFileClip:
    """
    Load a video file from disk.
    
    Args:
        path: Path to the downloaded TikTok .mp4

    Returns: a MoviePy clip object.

    """
    # TODO: Validate file exists, check extension, etc.
    return VideoFileClip(path)


def detect_end_segment_length(clip: VideoFileClip) -> float:
    """
    Detect how many seconds should be trimmed from the end.
    This function can be as simple as returning a fixed offset (e.g., 3.0 seconds),
    or more advanced (e.g., analyze audio amplitude, look for “end-card” pattern).


    Args:
        clip: clip.duration gives total length in seconds.

    Returns: the length (in seconds) of the trailing segment to remove.

    """
    # TODO: collaborators implement logic here.
    # For a first pass, return a fixed number like 3.0 or read from config.
    return 3.0


def trim_video(clip: VideoFileClip, end_to_strip: float) -> VideoFileClip:
    """
    Trim the last `end_to_strip` seconds from the clip.

    Args:
        clip: clip.duration gives total length in seconds.
        end_to_strip: If clip.duration is e.g. 15.5, and end_to_strip is 3.0,
                      then new subclip should be clip.subclip(0, 12.5).

    Returns: a new VideoFileClip without the end segment.

    """
    # TODO: Add robust error handling for this function
    # - Validate that 'clip' is instance of VideoFileClip.
    # - Check 'end_to_strip' is a non-negative integer or float.
    # - Handle cases where 'clip.duration' is None or non-positive. (read the docs if <=0 or None is possible)
    # NOTE: Consider raising exceptions (TypeError, ValueError).
    total = clip.duration
    new_end = max(0, total - end_to_strip)
    return clip.subclip(0, new_end)


def save_video(clip: VideoFileClip, output_path: str) -> None:
    """
    Write the trimmed clip to disk.
    Ensures directory exists and writes with appropriate codec settings.

    Args:
        clip: The trimmed clip
        output_path: where to save (e.g., “trimmed_output.mp4”).

    Returns: Boolean indicating success

    """
    # TODO: Add any codec or ffmpeg parameters if needed.
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

def batch_trim(input_folder: str, output_folder: str, end_length: float = None):
    """
    Iterate over every .mp4 in input_folder, trim them, and save to output_folder.
    """
    # TODO: glob all .mp4, call load_video()/trim_video()/save_video()

