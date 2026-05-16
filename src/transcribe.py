# src/transcribe.py

import os
import sys
import whisper

from src.subtitle_cleaner import clean_segments
from src.srt_writer import write_srt
from src.translator import translate_segments


def transcribe_to_srt(
    input_path: str,
    source_lang=None,
    target_lang=None
):

    # ✅ Check input exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    # ✅ Create output folder
    os.makedirs("output", exist_ok=True)

    # ✅ Output filename
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_srt = os.path.join("output", f"{base_name}.srt")

    # ✅ Load Whisper
    # Allow overriding model via env var for performance testing on CPU
    model_name = os.getenv("WHISPER_MODEL", "small")
    print(f"[INFO] Loading Whisper model '{model_name}'...")
    model = whisper.load_model(model_name)

    # ✅ Transcription
    print("[INFO] Transcribing audio...")

    result = model.transcribe(
        input_path,
        task="transcribe",
        language=source_lang   # None = auto detect
    )

    # ✅ Detected language
    detected_lang = result.get("language", "unknown")

    print(f"[INFO] Detected language: {detected_lang}")

    # If the user didn't force a source language, re-run transcription
    # with the detected language to ensure the model decodes in that language
    # (helps avoid cases where detection and decoding mismatch).
    if source_lang is None and detected_lang != "unknown":
        try:
            print(f"[INFO] Re-transcribing with detected language '{detected_lang}' for accuracy...")
            result = model.transcribe(
                input_path,
                task="transcribe",
                language=detected_lang
            )

            # Update segments after re-transcription
            detected_lang = result.get("language", detected_lang)

        except Exception as e:
            print(f"[WARN] Re-transcription failed: {e}. Using original transcription.")

    # ✅ Segments
    segments = result["segments"]

    print(f"[INFO] Segments detected: {len(segments)}")

    # 🌍 Translation Layer
    if target_lang:

        # if source not manually given,
        # use Whisper detected language
        if source_lang is None:
            source_lang = detected_lang

        print(
            f"[INFO] Translating from "
            f"{source_lang} → {target_lang}..."
        )

        segments = translate_segments(
            segments,
            src_lang=source_lang,
            tgt_lang=target_lang
        )

    # ✅ Subtitle cleanup
    print("[INFO] Cleaning subtitles...")

    cleaned_segments = clean_segments(segments)

    # ✅ Write SRT
    print("[INFO] Writing SRT file...")

    write_srt(cleaned_segments, output_srt)

    print("[DONE] Subtitle file created:", output_srt)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "python -m src.transcribe input.mp4\n"
            "python -m src.transcribe input.mp4 -t en  # translate to en"
        )
        sys.exit(1)

    input_file = sys.argv[1]

    # By default: do not translate. To enable translation pass -t/--translate LANG
    target_lang = None

    if len(sys.argv) >= 3:
        # Expect: python -m src.transcribe file -t en
        if sys.argv[2] in ("-t", "--translate") and len(sys.argv) >= 4:
            target_lang = sys.argv[3]
        else:
            print("[WARN] Translation disabled. Use -t/--translate LANG to enable translation.")

    transcribe_to_srt(
        input_file,
        source_lang=None,
        target_lang=target_lang
    )

    