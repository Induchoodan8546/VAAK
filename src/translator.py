# src/translator.py

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)

import langcodes

MODEL_NAME = (
    "facebook/nllb-200-distilled-600M"
)
LANG_MAP = {
    "en": "eng_Latn",
    "fr": "fra_Latn",
    "de": "deu_Latn",
    "es": "spa_Latn",
    "nl": "nld_Latn",
    "ru": "rus_Cyrl",
    "ko": "kor_Hang",
    "hi": "hin_Deva",
    "id": "ind_Latn",
    "ja": "jpn_Jpan",
    "zh": "zho_Hans",
    "ta": "tam_Taml",
    "ml": "mal_Mlym",
    "ar": "arb_Arab",
    "pt": "por_Latn",
    "it": "ita_Latn"
}
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

    code = LANG_MAP.get(
        whisper_lang
    )

    print(
        f"[DEBUG] {whisper_lang} -> {code}"
    )

    return code
    


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
if __name__ == "__main__":

    scene = """
시작하기 전에 휴대폰 수거부터 해야 할 것 같습니다

전화! 휴대폰 제출합니다!

귀찮아

그게 뭔데요?

아 유행어예요?

아 저 유행어 잘 모르는 거 아시잖아요

그래서 릴리스도 알...

한예리 학생 휴대폰 제출합니다

저 방송 중이라서요

선생님 새로 오셔서 못 들으셨나 보다

이거 교장쌤도 허락하신 건데?

마지막입니다

휴대폰 제출합니다

그럼 선생님이 제 팬들한테 직접 얘기하실래요?

미쳤어요? 지금 뭐 하는 거예요?

미친 건 이 반 학생들입니다

학교가 생각했던 것보다 더 개판입니다

선생보다 머리 위에 있으려는 것들

선생을 공기놀이 대상으로 다루는 것들

존경보다 구경거리로 만드는 것들

지금부터 이런 것들을

교권 침해로 간주합니다

도전은 언제나 응하겠지만

처벌은 각오해야 할 겁니다
"""

    result = translate_text(
        scene,
        "ko",
        "en"
    )

    print("\n===== TEST OUTPUT =====\n")
    print(result)
    print("\n=======================\n")