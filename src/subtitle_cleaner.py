# src/subtitle_cleaner.py

import re

MAX_CHARS_PER_LINE = 42
MIN_DURATION = 1.0


def clean_text(text: str) -> str:
    text = text.strip()
    if text:
        text = text[0].upper() + text[1:]
    return " ".join(text.split())


def merge_segments(segments):
    merged = []
    buffer = None

    for seg in segments:
        text = seg["text"].strip()

        if not buffer:
            buffer = seg.copy()
            continue

        if (
            len(buffer["text"]) < 40 or
            not buffer["text"].endswith((".", "!", "?"))
        ):
            buffer["end"] = seg["end"]
            buffer["text"] += " " + text
        else:
            merged.append(buffer)
            buffer = seg.copy()

    if buffer:
        merged.append(buffer)

    return merged


def split_text_balanced(text: str):
    # Try punctuation-based split
    parts = re.split(r'([,.;!?])', text)

    if len(parts) >= 3:
        first = parts[0] + parts[1]
        second = "".join(parts[2:])
        return [first.strip(), second.strip()]

    # fallback split
    words = text.split()
    mid = len(words) // 2

    return [
        " ".join(words[:mid]),
        " ".join(words[mid:])
    ]


def enforce_min_duration(segments):
    new_segments = []

    for seg in segments:
        start = seg["start"]
        end = seg["end"]

        if end - start < MIN_DURATION:
            end = start + MIN_DURATION

        new_segments.append({
            "start": start,
            "end": end,
            "text": seg["text"]
        })

    return new_segments


def clean_segments(segments):
    segments = merge_segments(segments)

    cleaned = []

    for seg in segments:
        text = clean_text(seg["text"])
        lines = split_text_balanced(text)

        cleaned.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": "\n".join(lines)
        })

    cleaned = enforce_min_duration(cleaned)

    return cleaned