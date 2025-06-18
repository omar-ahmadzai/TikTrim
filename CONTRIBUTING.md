# Necessary Tools & Dependencies and Planned Improvements

## Python 3.8+

FFmpeg: MoviePy depends on having the ffmpeg binary in PATH.  
(Documentation: https://kkroening.github.io/ffmpeg-python/)
  - On macOS: brew install ffmpeg
  - On Ubuntu: sudo apt update && sudo apt install ffmpeg
  - On Windows: download from ffmpeg.org and add to PATH.

MoviePy: We’re using MoviePy for simplicity. Under the hood it calls ffmpeg to do the trim. Version ≥1.0 is recommended.
(Documentation: https://zulko.github.io/moviepy/)

pytest: For running the unit tests.
(Documentation: https://docs.pytest.org/en/stable/contents.html)


## Planned Improvements:
  - Smart end detection: Analyze audio waveform to find that “TikTok end-card” music pattern.
  - Batch processing: Loop through a whole folder of downloads.
  - GUI wrapper: Simple desktop app for non-tech users.
  - Docker container: For consistent environment and CI testing.

## CLI Improvements:
  - Add flags like --dry-run (to just print what would happen without writing a file).
  - Verbosity levels (-v or --verbose) to log how many seconds are detected and trimmed.
