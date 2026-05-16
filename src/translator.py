# src/translator.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "facebook/nllb-200-distilled-600M"

# Language code mapping
LANG_CODES = {
    "en": "eng_Latn",
    "ml": "mal_Mlym",
    "hi": "hin_Deva",
    "ja": "jpn_Jpan",
    "ko": "kor_Hang",
    "ta": "tam_Taml",
    "ar": "arb_Arab",
    "fr": "fra_Latn",
    "de": "deu_Latn",
    "es": "spa_Latn",
}


tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def translate_text(text, src_lang="ml", tgt_lang="en"):

    src_code = LANG_CODES[src_lang]
    tgt_code = LANG_CODES[tgt_lang]

    tokenizer.src_lang = src_code

    inputs = tokenizer(text, return_tensors="pt")

    generated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_code),
        max_length=512
    )

    translated = tokenizer.batch_decode(
        generated_tokens,
        skip_special_tokens=True
    )[0]

    return translated


def translate_segments(segments, src_lang="ml", tgt_lang="en"):

    translated_segments = []

    for seg in segments:

        text = seg["text"]

        try:
            translated_text = translate_text(
                text,
                src_lang,
                tgt_lang
            )

        except Exception:
            translated_text = text

        translated_segments.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": translated_text
        })

    return translated_segments