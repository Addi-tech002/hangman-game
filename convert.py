from pydub import AudioSegment
import os

# Directory containing your MP3 files
source_folder = "sound"
target_folder = "sound"

# Convert all MP3s in the folder to WAVs
for filename in os.listdir(source_folder):
    if filename.endswith("D:\project\sound\buzzer-or-wrong-answer-20582.mp3"):
        mp3_path = os.path.join(source_folder, filename)
        wav_filename = filename.replace(".mp3", ".wav")
        wav_path = os.path.join(target_folder, wav_filename)

        print(f"Converting {mp3_path} to {wav_path}...")
        sound = AudioSegment.from_mp3(mp3_path)
        sound.export(wav_path, format="wav")

print("✅ All MP3 files converted to WAV.")
