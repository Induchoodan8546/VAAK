from faster_whisper import WhisperModel

model = WhisperModel(
    "large-v3",
    device="cpu",
    compute_type="float32"
)

segments, info = model.transcribe(
    "input\\d3.mp4",
    language="ml"
)

print("Detected language:", info.language)

for segment in segments:
    print(segment.text)