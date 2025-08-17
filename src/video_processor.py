import os
from os import PathLike
from moviepy import VideoFileClip
from librosa import feature as feature
import librosa
import logging

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

    """For this I will use a library called librosa to take the clip, load it and turn it into numbers
    -> samples -> floating point numbers
    
    we use RMS then to show loudness in the raw data we receive.
    
    for more info you can read documentation.txt file below the detect.... func. 
    
    """

    logging.basicConfig(filename="logs.txt", level=logging.INFO)

    # we will take the clip and make it a wav file for it to work with librosa
    # this will check if there is audio in the clip
    if not clip.audio:
        logging.error("Clip is corrupted or video has no audio track")
        raise RuntimeError("Clip is corrupted or video has no audio track!!!")

    # this will change the audio. to audio.wav
    clip.audio.write_audiofile("audio.wav")
    try:
        # loading with librosa to change the audio into samples
        # y is raw audio samples
        # sr is the sampling rate -> number of samples per second
        y, sr = librosa.load("audio.wav", sr=None, mono=False)
        # rms is to calculate the signal's loudness or energy over time
        rms = feature.rms(y=y, hop_length=600)
    except Exception as e:
        logging.error(e)
        raise e

    # here we just calculate frames till the wave becomes bigger than 0.001
    # which means it is not quit anymore.
    frames = 0
    for num in rms[0][::-1]:
        if num > 0.001:
            break
        frames += 1

    # checking to be sure that we don't cut a part that we don't cut the entire video
    # even if we checked with if clip.audio that the audio should exist in the video.
    if frames >= clip.duration:
        return 0.0
    # we change the frames back to seconds adding one more for a better result(maybe).
    else:
        return (frames * 600 / sr) + 1
    # sorry that if there is any mistake.

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
        return clip.subclipped(0, new_end)
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

    # Error handling
    if not isinstance(clip, VideoFileClip):
        raise TypeError("Clip must be of type VideoFileClip")
    if not isinstance(output_path, str):
        raise TypeError("output_path must be of type str")
    if not output_path.endswith(".mp4"):
        file_name = os.path.basename(clip.filename)
        output_path = os.path.join(output_path, file_name)

    # Creating the files in the path if they don't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Saving the VideoFileClip to the output path
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac")


def batch_trim(input_folder: str, output_folder: str, end_length: float = None):
    """
    Iterate over every .mp4 in input_folder, trim them, and save to output_folder.
    """
    # TODO: glob all .mp4, call load_video()/trim_video()/save_video()

    # Error handling the inputs
    if not isinstance(input_folder, str) or not isinstance(output_folder, str):
        raise TypeError("Folder path should be of type str!")
    
    if not isinstance(end_length, float):
        raise TypeError("End length must be of type float")
    
    if not os.path.isdir(input_folder) or not os.path.isdir(output_folder):
        raise FileNotFoundError("The path provided is not invalid")

    # getting a list of all files in the input folder
    folder = os.listdir(input_folder)

    # Trimming every video in the folder and saving t in the output directory
    for i in folder:
        if i.endswith(".mp4"):
            video_path = os.path.join(input_folder, i)
            video_clip = load_video(video_path)
            output_path = os.path.join(output_folder, i)
            save_video(trim_video(video_clip, detect_end_segment_length(video_clip)), output_path)
