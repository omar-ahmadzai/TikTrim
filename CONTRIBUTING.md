Planned Improvements:
  - Smart end detection: Analyze audio waveform to find that “TikTok end-card” music pattern.
  - Batch processing: Loop through a whole folder of downloads.
  - GUI wrapper: Simple desktop app for non-tech users.
  - Docker container: For consistent environment and CI testing.

CLI Improvements:
  - Add flags like --dry-run (to just print what would happen without writing a file).
  - Verbosity levels (-v or --verbose) to log how many seconds are detected and trimmed.
