import os
import shutil
import sys
import tempfile
import whisper
from src.subtitle_cleaner import clean_segments
from src.srt_writer import write_srt



def _ensure_ffmpeg_on_path():
    try:
        import imageio_ffmpeg

        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        print("[DEBUG] Found ffmpeg at:", ffmpeg_exe)

        helper_dir = os.path.join(tempfile.gettempdir(), "vaak_ffmpeg")
        os.makedirs(helper_dir, exist_ok=True)

        helper_ffmpeg = os.path.join(helper_dir, "ffmpeg.exe")

        if not os.path.exists(helper_ffmpeg):
            shutil.copy2(ffmpeg_exe, helper_ffmpeg)
            print("[DEBUG] Copied ffmpeg to:", helper_ffmpeg)

        current_path = os.environ.get("PATH", "")

        if helper_dir not in current_path:
            os.environ["PATH"] = helper_dir + os.pathsep + current_path
            print("[DEBUG] Updated PATH")

        # 🔥 VERIFY IT WORKS
        import subprocess
        subprocess.run(["ffmpeg", "-version"], check=True)
        print("[DEBUG] ffmpeg is working")

    except Exception as e:
        print("[ERROR] ffmpeg setup failed:", e)
        raise  # DO NOT SILENCE

def transcribe_to_srt(input_path: str, output_folder: str = "output"):
    _ensure_ffmpeg_on_path()

    # 1️⃣ Check if input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    # 2️⃣ Create output folder if missing
    os.makedirs(output_folder, exist_ok=True)

    # 3️⃣ Create output file name
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_srt = os.path.join(output_folder, f"{base_name}.srt")

    print("[INFO] Loading Whisper model...")
    model = whisper.load_model("medium")

    print("[INFO] Transcribing audio...")
    result = model.transcribe(
        input_path,
        task="translate",
        language="ml"
    )


    # Whisper returns segments with timestamps + text
    segments = result["segments"]

    print("[INFO] Cleaning subtitles for cinematic format...")
    cleaned_segments = clean_segments(segments)

    print("[INFO] Writing subtitle file...")
    write_srt(cleaned_segments, output_srt)

    print("[DONE] Subtitle file created:", output_srt)


if __name__ == "__main__":
    # command line usage
    if len(sys.argv) < 2:
        print("Usage: python -m src.transcribe input/video_20260130_203537 copy.mp4")
        sys.exit(1)

    input_file = sys.argv[1]
    transcribe_to_srt(input_file)
