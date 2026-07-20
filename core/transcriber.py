import os
import sys
from faster_whisper import WhisperModel

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.audio_processor import process_input

# ==========================================
# Configuration
# ==========================================

WHISPER_MODEL = "small"
DEVICE = "cpu"          # Change to "cuda" if you have NVIDIA GPU
COMPUTE_TYPE = "int8"

TRANSCRIPT_DIR = "transcripts"
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

_model = None

# ==========================================
# Load Whisper Model
# ==========================================

def load_model():
    global _model

    if _model is None:
        print(f"\nLoading Faster Whisper ({WHISPER_MODEL})...")

        _model = WhisperModel(
            WHISPER_MODEL,
            device=DEVICE,
            compute_type=COMPUTE_TYPE,
        )

        print("✅ Model Loaded Successfully.\n")

    return _model


# ==========================================
# Transcribe One Audio Chunk
# ==========================================

def transcribe_chunk(audio_path: str, language=None):

    model = load_model()

    # Convert user input to Whisper language codes
    if isinstance(language, str):
        language = language.strip().lower()

        if language == "english":
            language = "en"

        elif language == "hindi":
            language = "hi"

        elif language in ["auto", "none", ""]:
            language = None

    segments, info = model.transcribe(
        audio_path,
        language=language,
        beam_size=5,
    )

    transcript = ""

    for segment in segments:
        print(f"[{segment.start:.2f}s --> {segment.end:.2f}s]")
        transcript += segment.text + " "

    return transcript.strip()


# ==========================================
# Transcribe All Chunks
# ==========================================

def transcribe_all(chunks: list, language=None):

    print(f"\nTotal Chunks: {len(chunks)}\n")

    full_transcript = ""

    for i, chunk in enumerate(chunks, start=1):

        print(f"Transcribing Chunk {i}/{len(chunks)}")

        text = transcribe_chunk(chunk, language)

        full_transcript += text + "\n"

    print("\n✅ Transcription Completed.\n")

    return full_transcript.strip()


# ==========================================
# Save Transcript
# ==========================================

def save_transcript(text: str):

    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

    file_path = os.path.join(
        TRANSCRIPT_DIR,
        "transcript.txt"
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"✅ Transcript saved to:\n{file_path}")

    return file_path


# ==========================================
# Standalone Test
# ==========================================

if __name__ == "__main__":

    source = input("Enter YouTube URL or local file path:\n").strip()

    language = input(
        "Language (english/hindi/auto): "
    ).strip().lower()

    if language == "auto":
        language = None
    elif language == "english":
        language = "en"
    elif language == "hindi":
        language = "hi"
    else:
        language = None

    print("\nDownloading and processing audio...\n")

    chunks = process_input(source)

    transcript = transcribe_all(chunks, language)

    save_transcript(transcript)

    print("\n==============================")
    print("FINAL TRANSCRIPT")
    print("==============================\n")

    print(transcript)