from moviepy.editor import *
from moviepy.audio.fx import all as afx
import os

input_file = "today_riddles.txt"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

music_path = "music/calm_music.mp3"

# Load riddles
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
            fontsize=70,
            color='white',
            size=(1000, None),
            method='caption',
            align='center',
            font="Arial"
        ).set_duration(6)

        # 🪄 Answer text (fade-in + appear for 4 sec)
        answer_clip = TextClip(
            "Answer: " + answer_text,
            fontsize=65,
            color='yellow',
            size=(1000, None),
            method='caption',
            align='center',
            font="Arial"
        ).fadein(1).set_duration(4)

        # ⏳ Combine both text clips
        txt_sequence = concatenate_videoclips([riddle_clip, answer_clip]).resize(width=1000)

        # 🎞️ Background (black)
        background = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=10)

        # 💡 Combine text and background
        final = CompositeVideoClip([background, txt_sequence.set_position('center')])

        # 🎧 Add background music with fade-in/out
        if os.path.exists(music_path):
            try:
                audio = AudioFileClip(music_path).fx(afx.audio_loop, duration=final.duration)
                audio = audio.audio_fadein(1.5).audio_fadeout(1.5)
                final = final.set_audio(audio)
            except Exception as e:
                print(f"⚠️ audio error: {e}")

        # 🎬 Fade out video smoothly at the end
        final = final.crossfadeout(1.2)

        # 📤 Export final video
        output_path = os.path.join(output_dir, f"riddle_{i}.mp4")
        final.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            threads=2,
            verbose=False,
            logger=None
        )

        print(f"✅ Created: {output_path}")

    except Exception as e:
        print(f"❌ Error creating riddle_{i}: {e}")

print("🎉 All riddle videos created successfully with smooth fade effects!")
