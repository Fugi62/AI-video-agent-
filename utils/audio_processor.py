import os
import yt_dlp
from pydub import AudioSegment

# -----------------------------
# Configuration
# -----------------------------
DOWNLOAD_DIR = "downloads"  # Fixed spelling
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# -----------------------------
# Download YouTube Audio
# -----------------------------
def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        # Works for any original extension
        filename = os.path.splitext(ydl.prepare_filename(info))[0] + ".wav"

    return filename


# -----------------------------
# Convert Local File to WAV
# -----------------------------
def convert_to_wav(input_path: str) -> str:

    output_path = os.path.splitext(input_path)[0] + "_converted.wav"

    audio = AudioSegment.from_file(input_path)

    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)

    audio.export(output_path, format="wav")

    return output_path


# -----------------------------
# Split Audio into Chunks
# -----------------------------
def chunk_audio(wav_path: str, chunk_minutes: int = 10):

    audio = AudioSegment.from_wav(wav_path)

    chunk_ms = chunk_minutes * 60 * 1000

    chunks = []

    base_name = os.path.splitext(wav_path)[0]

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start:start + chunk_ms]

        chunk_path = f"{base_name}_chunk_{i+1}.wav"

        chunk.export(chunk_path, format="wav")

        chunks.append(chunk_path)

    return chunks


# -----------------------------
# Process Input
# -----------------------------
def process_input(source: str):

    if source.startswith(("http://", "https://")):

        print("Downloading YouTube Audio...")

        wav_path = download_youtube_audio(source)

    else:

        print("Processing Local File...")

        wav_path = convert_to_wav(source)

    print("Chunking Audio...")

    chunks = chunk_audio(wav_path)

    print(f"Created {len(chunks)} chunk(s).")

    return chunks


# -----------------------------
# Test
# -----------------------------
if __name__ == "__main__":

    youtube_url = "https://www.youtube.com/watch?v=zE9udJpNPIA"

    chunks = process_input(youtube_url)

    print("\nGenerated Chunks:")

    for chunk in chunks:
        print(chunk)