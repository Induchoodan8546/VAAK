# src/transcribe.py

import os
import sys


from faster_whisper import WhisperModel

from src.subtitle_cleaner import clean_segments
from src.srt_writer import write_srt
from src.translator import translate_segments

def transcribe_to_srt(input_path: str,target_lang = None):

    # Check input
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    # Output folder
    os.makedirs("output", exist_ok=True)

    base_name = os.path.splitext(
        os.path.basename(input_path)
    )[0]

    output_srt = os.path.join(
        "output",
        f"{base_name}.srt"
    )

    print(
        "[INFO] Loading Faster-Whisper large-v3..."
    )

    model = WhisperModel(
        "large-v3",
        device="cpu",
        compute_type="float32"
    )

    print("[INFO] Transcribing audio...")

    segments_generator, info = model.transcribe(
        input_path,
        beam_size=5
    )
    print("Detected language:", info.language)
    print("Probability:", info.language_probability)
    print(
        f"[INFO] Detected language: {info.language}"
    )
    source_lang = info.language
    

    segments = []

    for seg in segments_generator:

        segments.append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text.strip()
        })
    if target_lang:

     print(
        f"[INFO] Translating "
        f"{source_lang} -> {target_lang}"
    )

     segments = translate_segments(
        segments,
        source_lang,
        target_lang
    )

   
    

    print(
        f"[INFO] Segments detected: {len(segments)}"
    )



    print("[INFO] Cleaning subtitles...")

    cleaned_segments = clean_segments(
        segments
    )

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

target_lang = None

if len(sys.argv) >= 3:
    target_lang = sys.argv[2]

transcribe_to_srt(
    input_file,
    target_lang
)