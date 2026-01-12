# VAAK
vaak is a lightweight AI-based subtitle generator that converts video or audio files into time-aligned .srt subtitles using automatic speech recognition.
# vaak 🎬  
> *vaak* (വാക്ക്) — Malayalam for “word”

**vaak** is a lightweight AI-based subtitle generator that converts **video or audio files into time-aligned `.srt` subtitles** using automatic speech recognition.

This repository currently contains the **core subtitle generation pipeline (Phase 1)**.

---

## 🎯 Current Scope (Phase 1)

- ✅ Convert video/audio → subtitles  
- ✅ English speech transcription  
- ✅ Accurate timestamped subtitles  
- ✅ Output in standard `.srt` format  

**Not included in this phase:**
- ❌ Translation  
- ❌ UI / Web interface  
- ❌ Speaker detection  

---

## 🧠 How It Works (Phase 1)

1. Audio is extracted from the input video  
2. An AI speech recognition model transcribes the audio  
3. The transcription is segmented with timestamps  
4. A `.srt` subtitle file is generated  

---

## 🛠️ Tech Stack

- Python  
- Whisper (speech-to-text)  
- FFmpeg (audio extraction)  
- PyTorch  

---

## 📂 Project Structure

vaak/
├── input/ # Input video or audio files
├── output/ # Generated subtitle files (.srt)
├── src/ # Core transcription logic
├── README.md
└── requirements.txt



---

## 🚧 Project Status

🟡 **Phase 1 – In Progress**

The focus of this phase is to build a **reliable and accurate subtitle generation pipeline** before introducing advanced features.

---

## 🧪 Example Output

1
00:00:01,200 --> 00:00:03,800
This is an example subtitle.

2
00:00:04,100 --> 00:00:06,500
Generated automatically by vaak.


---

## 🎯 Intended Use

- Learning and portfolio project  
- Understanding speech recognition pipelines  
- Exploring real-world AI system design  

---

## 📖 License

MIT License

---

## 👤 Induchoodan V S

Built as a **profile-oriented AI project** focusing on practical implementation and system design.

