# src/translate_srt.py

import os
import sys

from langdetect import detect

from src.translator import translate_segments
from src.srt_writer import write_srt


def parse_timestamp(timestamp):

    h, m, s = timestamp.split(":")

    sec, ms = s.split(",")

    return (
        int(h) * 3600
        + int(m) * 60
        + int(sec)
        + int(ms) / 1000
    )


def read_srt(file_path):

    segments = []

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        content = f.read()

    blocks = content.strip().split("\n\n")

    for block in blocks:

        lines = block.splitlines()

        if len(lines) < 3:
            continue

        timing = lines[1]

        start, end = timing.split(
            " --> "
        )

        text = "\n".join(
            lines[2:]
        )

        segments.append({

            "start": parse_timestamp(start),

            "end": parse_timestamp(end),

            "text": text

        })

    return segments


def detect_source_language(
    segments
):

    sample = ""

    for seg in segments[:10]:

        sample += (
            seg["text"] + " "
        )

    try:

        return detect(sample)

    except Exception:

        return "en"


def translate_srt(
    input_srt,
    target_lang
):

    if not os.path.exists(
        input_srt
    ):

        raise FileNotFoundError(
            f"File not found: "
            f"{input_srt}"
        )

    print(
        "[INFO] Reading SRT..."
    )

    segments = read_srt(
        input_srt
    )

    print(
        f"[DEBUG] Loaded "
        f"{len(segments)} segments"
    )

    source_lang = (
        detect_source_language(
            segments
        )
    )

    print(
        f"[INFO] Source language: "
        f"{source_lang}"
    )

    print(
        f"[INFO] Translating "
        f"{source_lang} -> "
        f"{target_lang}"
    )

    translated_segments = (
        translate_segments(
            segments,
            source_lang,
            target_lang
        )
    )

    base_name = (
        os.path.splitext(
            input_srt
        )[0]
    )

    output_srt = (
        f"{base_name}_"
        f"{target_lang}.srt"
    )

    print(
        "[INFO] Writing SRT..."
    )

    write_srt(
        translated_segments,
        output_srt
    )

    print(
        "[DONE] Created:",
        output_srt
    )


if __name__ == "__main__":

    if len(sys.argv) < 3:

        print(
            "Usage:\n"
            "python -m src.translate_srt "
            "input.srt en"
        )

        sys.exit(1)

    input_srt = sys.argv[1]

    target_lang = sys.argv[2]

    translate_srt(
        input_srt,
        target_lang
    )