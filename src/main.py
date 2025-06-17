"""
Logic for starter to change later.
"""

import argparse
from video_processor import load_video, detect_end_segment_length, trim_video, save_video

def parse_args():
    p = argparse.ArgumentParser(description="TikTrim: Strip off the final TikTok end-card.")
    p.add_argument("input_path", help="Path to the downloaded TikTok video (.mp4)")
    p.add_argument("output_path", help="Path to save the trimmed video")
    p.add_argument("--end-length", type=float, default=None,
                   help="(Optional) Seconds to strip from end. Overrides auto-detection.")
    return p.parse_args()

def main():
    args = parse_args()
    clip = load_video(args.input_path)

    if args.end_length is not None:
        end_seconds = args.end_length
    else:
        end_seconds = detect_end_segment_length(clip)

    trimmed = trim_video(clip, end_seconds)
    save_video(trimmed, args.output_path)
    print(f"Trimmed last {end_seconds:.2f}s. Saved to {args.output_path}.")

if __name__ == "__main__":
    main()
