# src/transcribe.py

import os
import sys
import whisper

from src.subtitle_cleaner import clean_segments
from src.srt_writer import write_srt
from src.translator import load_translator, translate_segments


def transcribe_to_srt(input_path: str, target_lang=None, source_lang="ml"):
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    os.makedirs("output", exist_ok=True)

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_srt = os.path.join("output", f"{base_name}.srt")

    print("[INFO] Loading Whisper model...")
    model = whisper.load_model("medium")

    print("[INFO] Transcribing audio...")
    result = model.transcribe(
        input_path,
        task="transcribe",
        language=source_lang
    )

    segments = result["segments"]

    print(f"[INFO] Segments detected: {len(segments)}")

    # 🌍 Translation Layer
    if target_lang:
        print(f"[INFO] Translating to {target_lang}...")
        translator = load_translator(source_lang, target_lang)
        segments = translate_segments(segments, translator)

    print("[INFO] Cleaning subtitles...")
    cleaned_segments = clean_segments(segments)

    print("[INFO] Writing SRT file...")
    write_srt(cleaned_segments, output_srt)

    print("[DONE] Subtitle file created:", output_srt)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m src.transcribe input.mp4 [target_lang]")
        sys.exit(1)

    input_file = sys.argv[1]
    target_lang = sys.argv[2] if len(sys.argv) >= 3 else None

    transcribe_to_srt(input_file, target_lang)