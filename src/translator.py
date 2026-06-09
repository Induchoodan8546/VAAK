# src/translator.py

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)

import langcodes

MODEL_NAME = (
    "facebook/nllb-200-distilled-600M"
)

tokenizer = None
model = None

# Build dynamically from NLLB
NLLB_CODES = None


def load_translator():

    global tokenizer
    global model
    global NLLB_CODES

    if tokenizer is None:

        print(
            "[INFO] Loading NLLB..."
        )

        tokenizer = (
            AutoTokenizer
            .from_pretrained(
                MODEL_NAME
            )
        )

        model = (
            AutoModelForSeq2SeqLM
            .from_pretrained(
                MODEL_NAME
            )
        )

        NLLB_CODES = list(
            tokenizer.lang_code_to_id.keys()
        )

    return tokenizer, model


def resolve_nllb_code(
    whisper_lang
):

    tokenizer, model = load_translator()

    try:

        language = (
            langcodes.Language
            .get(whisper_lang)
        )

        language_name = (
            language.language
        )

        for code in NLLB_CODES:

            if code.startswith(
                language_name
            ):
                return code

    except Exception:

        pass

    return None


def translate_text(
    text,
    source_lang,
    target_lang
):

    tokenizer, model = load_translator()

    src_code = resolve_nllb_code(
        source_lang
    )

    tgt_code = resolve_nllb_code(
        target_lang
    )

    if not src_code:

        raise ValueError(
            f"Unsupported source language: "
            f"{source_lang}"
        )

    if not tgt_code:

        raise ValueError(
            f"Unsupported target language: "
            f"{target_lang}"
        )

    tokenizer.src_lang = src_code

    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

    generated_tokens = (
        model.generate(
            **inputs,
            forced_bos_token_id=
            tokenizer.convert_tokens_to_ids(
                tgt_code
            ),
            max_length=512
        )
    )

    translated = (
        tokenizer.batch_decode(
            generated_tokens,
            skip_special_tokens=True
        )[0]
    )

    return translated


def translate_segments(
    segments,
    source_lang,
    target_lang
):

    translated_segments = []

    total = len(segments)

    for i, seg in enumerate(
        segments
    ):

        print(
            f"[INFO] Translating "
            f"{i+1}/{total}"
        )

        try:

            translated_text = (
                translate_text(
                    seg["text"],
                    source_lang,
                    target_lang
                )
            )

        except Exception as e:

            print(
                "[WARNING]",
                e
            )

            translated_text = (
                seg["text"]
            )

        translated_segments.append({

            "start":
                seg["start"],

            "end":
                seg["end"],

            "text":
                translated_text

        })

    return translated_segments