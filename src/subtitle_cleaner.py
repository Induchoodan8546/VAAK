import re

MAX_WORDS = 12
MIN_DURATION = 1.0


def clean_text(text):
    text = text.strip()
    text = " ".join(text.split())

    if text:
        text = text[0].upper() + text[1:]

    return text


def split_long_subtitle(text):

    words = text.split()

    if len(words) <= MAX_WORDS:
        return [text]

    chunks = []

    for i in range(0, len(words), MAX_WORDS):
        chunk = " ".join(words[i:i + MAX_WORDS])
        chunks.append(chunk)

    return chunks


def enforce_min_duration(segments):

    result = []

    for seg in segments:

        start = seg["start"]
        end = seg["end"]

        if end - start < MIN_DURATION:
            end = start + MIN_DURATION

        result.append({
            "start": start,
            "end": end,
            "text": seg["text"]
        })

    return result


def clean_segments(segments):

    cleaned = []

    for seg in segments:

        text = clean_text(seg["text"])

        parts = split_long_subtitle(text)

        duration = seg["end"] - seg["start"]

        part_duration = duration / len(parts)

        for idx, part in enumerate(parts):

            cleaned.append({
                "start": seg["start"] + idx * part_duration,
                "end": seg["start"] + (idx + 1) * part_duration,
                "text": part
            })

    return enforce_min_duration(cleaned)