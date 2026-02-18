import os
import sys
import whisper
from src.srt_writer import write_srt


def transcribe_to_srt(input_path: str, output_folder: str = "output"):
    # 1️⃣ Check if input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    # 2️⃣ Create output folder if missing
    os.makedirs(output_folder, exist_ok=True)

    # 3️⃣ Create output file name
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_srt = os.path.join(output_folder, f"{base_name}.srt")

    print("[INFO] Loading Whisper model...")
    model = whisper.load_model("base")

    print("[INFO] Transcribing audio...")
    result = model.transcribe(
    input_path,
    language="en",     
    task="transcribe"
)


    # Whisper returns segments with timestamps + text
    segments = result["segments"]

    print("[INFO] Writing subtitle file...")
    write_srt(segments, output_srt)

    print("[DONE] Subtitle file created:", output_srt)


if __name__ == "__main__":
    # command line usage
    if len(sys.argv) < 2:
        print("Usage: python -m src.transcribe input/sample.mp4")
        sys.exit(1)

    input_file = sys.argv[1]
    transcribe_to_srt(input_file)
