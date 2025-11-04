# ✅ Force Pillow compatibility for all MoviePy calls (fixes ANTIALIAS)
import PIL
from PIL import Image

# Pillow 10+ removed ANTIALIAS; this ensures backward compatibility
if not hasattr(Image, "Resampling"):
    Image.Resampling = Image
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# 🧩 Now import moviepy AFTER patch
from moviepy.editor import *
from moviepy.audio.fx import all as afx
from datetime import datetime
import os

# 🗓 Automatically match today's riddle file name
today_date = datetime.now().strftime("%Y-%m-%d")
input_file = f"today_riddles_{today_date}.txt"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

music_path = "music/calm_music.mp3"

# 🧩 Load riddles file safely
if not os.path.exists(input_file):
    print(f"❌ Riddle file not found: {input_file}")
    exit(1)

with open(input_file, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

for i, line in enumerate(lines, 1):
    try:
        parts = line.split("|")
        riddle_text = parts[0].replace("Riddle:", "").strip()
        answer_text = parts[1].replace("Answer:", "").strip()

        # 🧩 Riddle text (first 6 seconds)
        riddle_clip = TextClip(
            riddle_text,
            fontsize=60,
            color='white',
            size=(700, None),
            method='caption',
            align='center',
            font="Arial"
        ).set_duration(6)

        # 🪄 Answer text (fade-in + appear for 4 sec)
        answer_clip = TextClip(
            "Answer: " + answer_text,
            fontsize=55,
            color='yellow',
            size=(700, None),
            method='caption',
            align='center',
            font="Arial"
        ).fadein(1).set_duration(4)

        # ⏳ Combine both text clips
        txt_sequence = concatenate_videoclips([riddle_clip, answer_clip])

        # 🎞️ Background (720x1280 for YouTube Shorts)
        background = ColorClip(size=(720, 1280), color=(0, 0, 0), duration=txt_sequence.duration)

        # 💡 Combine text and background
        final = CompositeVideoClip([background, txt_sequence.set_position('center')])

        # 🎧 Add background music with fade
        if os.path.exists(music_path):
            try:
                audio = AudioFileClip(music_path).fx(afx.audio_loop, duration=final.duration)
                audio = audio.audio_fadein(1.5).audio_fadeout(1.5)
                final = final.set_audio(audio)
            except Exception as e:
                print(f"⚠️ Audio error: {e}")

        # 🎬 Smooth fade out
        final = final.crossfadeout(1.0)

        # 📤 Export optimized for low-memory systems (Google VM)
        output_path = os.path.join(output_dir, f"riddle_{i}.mp4")
        final.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            threads=1,
            ffmpeg_params=["-preset", "ultrafast", "-bufsize", "512k"]
        )

        print(f"✅ Created: {output_path}")

    except Exception as e:
        print(f"❌ Error creating riddle_{i}: {e}")

print("🎉 All riddle videos created successfully with smooth fade effects!")
