# src/subtitle_cleaner.py

MAX_CHARS_PER_LINE = 42
MIN_DURATION = 1.0  # seconds


def clean_text(text: str) -> str:
    """Basic text cleanup for cinematic subtitles."""
    text = text.strip()
    if text:
        text = text[0].upper() + text[1:]
    return text


def split_text_balanced(text: str):
    """
    Split long subtitle text into balanced two-line format.
    """
    if len(text) <= MAX_CHARS_PER_LINE:
        return [text]

    words = text.split()
    mid = len(words) // 2

    # try to split near middle without breaking words
    line1 = " ".join(words[:mid])
    line2 = " ".join(words[mid:])

    return [line1, line2]


def enforce_min_duration(segments):
    """
    Ensure subtitles stay on screen long enough to read.
    """
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
    """
    Main Phase 1.5 function:
    Takes Whisper segments and returns cinematic subtitles.
    """
    cleaned = []

    for seg in segments:
        text = clean_text(seg["text"])
        lines = split_text_balanced(text)

        combined_text = "\n".join(lines)

        cleaned.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": combined_text
        })

    cleaned = enforce_min_duration(cleaned)

    return cleaned
