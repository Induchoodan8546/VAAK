# src/transcribe.py

import os
import sys


from faster_whisper import WhisperModel

from src.subtitle_cleaner import clean_segments
from src.srt_writer import write_srt
from src.translator import translate_segments

def transcribe_to_srt(input_path: str,target_lang = None, translate = False):

    # Check input
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    # Output folder
    os.makedirs("output", exist_ok=True)

    base_name = os.path.splitext(
        os.path.basename(input_path)
    )[0]

    if translate:

        output_srt = os.path.join(
        "output",
        f"{base_name}_english.srt"
    )

    else:

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
    task = (
    "translate"
    if translate
    else "transcribe")

    segments_generator, info = model.transcribe(
        input_path,
        beam_size=5,
        task = task
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
            "python -m src.transcribe video.mp4\n"
            "python -m src.transcribe video.mp4 translate"
        )

        sys.exit(1)

    input_file = sys.argv[1]

    translate_mode = False

    if (
        len(sys.argv) >= 3
        and
        sys.argv[2].lower()
        == "translate"
    ):

        translate_mode = True

    transcribe_to_srt(
        input_file,
        translate=translate_mode
    )