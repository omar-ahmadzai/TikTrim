import os
from os import PathLike
from moviepy.editor import VideoFileClip


def load_video(path: str | bytes | PathLike) -> VideoFileClip:
    """
    Load a video .mp4 file from disk.

    Args:
        path: Path (string, bytes, or PathLike) to an .mp4 file.

    Returns:
        A MoviePy VideoFileClip instance.

    Raises:
        TypeError: if `path` isn’t path‑like or has the wrong extension.
        FileNotFoundError: if the file does not exist.
        RuntimeError: if MoviePy/ffmpeg fails to load the clip.

    """
    # Path-like check
    if not isinstance(path, (str, bytes, PathLike)):
        raise TypeError(f"Invalid path-like object: {path!r}")

    # Convert to string so both path and bytes word
    filename = os.fspath(path)

    # Existence check
    if not os.path.exists(filename):
        raise FileNotFoundError(f"No such file as: {path!r}!")

    # Extension check
    extension = os.path.splitext(filename)[1].lower()
    if extension != ".mp4":
        raise TypeError(f"Unsupported extension {extension!r}; only .mp4 is allowed")

    # Try loading and capture any FFmpeg errors
    try:
        clip = VideoFileClip(path)
    except Exception as error:
        raise RuntimeError(f"Failed to load video {filename!r}") from error

    return clip


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
    # -------------------- Input Validation --------------------
    if not isinstance(clip, VideoFileClip):
        raise TypeError("The loaded clip must be of type VideoFileClip.")

    if not isinstance(end_to_strip, (int, float)):
        raise TypeError("end_to_strip must be an integer/float")

    if end_to_strip < 0:
        raise ValueError("end_to_strip cannot be Negative")

    total = clip.duration

    if total is None or total <= 0:
        raise AttributeError(f"Duration of the clip file is invalid: {clip.duration}")

    if end_to_strip >= clip.duration:
        raise ValueError("end_to_strip cannot be >= (greater than or equal to) clip.duration")

    # -------------------- Main Logic --------------------
    new_end = max(0, total - end_to_strip)
    try:
        return clip.subclip(0, new_end)
    except Exception as error:
        raise RuntimeError(f"Failed to trim the clip: {error}") from error


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

