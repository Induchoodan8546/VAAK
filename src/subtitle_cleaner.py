# src/subtitle_cleaner.py

MAX_CHARS_PER_LINE = 42
MIN_DURATION = 1.0  # seconds


def clean_text(text: str) -> str:
    """Basic text cleanup for cinematic subtitles."""
    text = text.strip()
    if text:
        text = text[0].upper() + text[1:]
    return text


MAX_CHARS_PER_LINE = 42

def split_text_balanced(text: str):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        # If adding this word exceeds limit → new line
        if len(current_line) + len(word) + 1 > MAX_CHARS_PER_LINE:
            lines.append(current_line.strip())
            current_line = word
        else:
            current_line += (" " + word if current_line else word)

    if current_line:
        lines.append(current_line.strip())

    # 🎬 Enforce max 2 lines (cinematic rule)
    if len(lines) > 2:
        return [
            lines[0],
            " ".join(lines[1:])
        ]

    return lines

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
