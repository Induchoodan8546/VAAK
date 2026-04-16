# src/translator.py

from transformers import pipeline


def load_translator(src_lang: str, tgt_lang: str):
    model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
    return pipeline("translation", model=model_name)


def translate_segments(segments, translator):
    translated = []

    for seg in segments:
        text = seg["text"]

        try:
            translated_text = translator(text, max_length=512)[0]["translation_text"]
        except Exception:
            translated_text = text  # fallback

        translated.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": translated_text
        })

    return translated