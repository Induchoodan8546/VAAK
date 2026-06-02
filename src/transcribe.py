# src/transcribe.py

import os
import sys
import whisper

from src.subtitle_cleaner import clean_segments
from src.srt_writer import write_srt


def transcribe_to_srt(input_path: str):

    # Check input
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    # Output folder
    os.makedirs("output", exist_ok=True)

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_srt = os.path.join(
        "output",
        f"{base_name}.srt"
    )

    # Load model
    model_name = os.getenv(
        "WHISPER_MODEL",
        "medium"
    )

    print(
        f"[INFO] Loading Whisper model '{model_name}'..."
    )

    model = whisper.load_model(model_name)

    # Transcribe
    print("[INFO] Transcribing audio...")

    result = model.transcribe(
        input_path,
        task="transcribe"
        # Let Whisper auto-detect language
    )

    detected_lang = result.get(
        "language",
        "unknown"
    )

    print(
        f"[INFO] Detected language: {detected_lang}"
    )

    segments = result["segments"]

    print(
        f"[INFO] Segments detected: {len(segments)}"
    )

    # Clean subtitles
    print("[INFO] Cleaning subtitles...")

    cleaned_segments = clean_segments(
        segments
    )

    # Write SRT
    print("[INFO] Writing SRT file...")

    write_srt(
        cleaned_segments,
        output_srt
    )

    print(
        "[DONE] Subtitle file created:",
        output_srt
    )


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "python -m src.transcribe input.mp4"
        )
        sys.exit(1)

    input_file = sys.argv[1]

    transcribe_to_srt(input_file)