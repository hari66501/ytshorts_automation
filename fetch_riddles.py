# daily_riddles_runner.py
import os
import time
import requests
from datetime import date
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip
from moviepy.audio.fx import all as afx
from moviepy.video.fx import fadein
import random

# CONFIG
OUT_DIR = "output"
MUSIC_PATH = "music/calm_music.mp3"   # optional (create music/ and place an mp3)
USED_FILE = "used_riddles.txt"
TODAY_PREFIX = "today_riddles"
COUNT = 5           # number of videos per day
WIDTH, HEIGHT = 1080, 1920
TOTAL_DURATION = 10  # seconds per video (6s riddle + 4s answer)

# --- Fetch free riddles ---
def fetch_free_riddles(count=5, try_multiplier=3, delay=0.6):
    fetched = []
    tries = 0
    need = count
    # fetch more than needed to improve chances of uniqueness
    while len(fetched) < need and tries < count * try_multiplier:
        tries += 1
        try:
            resp = requests.get("https://riddles-api.vercel.app/random", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                r = data.get("riddle", "").strip()
                a = data.get("answer", "").strip()
                if r and a:
                    fetched.append(f"Riddle: {r} | Answer: {a}")
        except Exception as e:
            # transient network issue — continue
            print("⚠️ fetch error:", e)
        time.sleep(delay)
    return fetched

# --- Save only unique riddles (no repeats across days) ---
def save_unique_riddles(fetched, count=5):
    os.makedirs(OUT_DIR, exist_ok=True)
    used = set()
    if os.path.exists(USED_FILE):
        with open(USED_FILE, "r", encoding="utf-8") as f:
            used = set(line.strip() for line in f if line.strip())

    new = []
    for r in fetched:
        if r not in used:
            new.append(r)
        if len(new) >= count:
            break

    # If not enough unique from this batch, try fetching again once
    if len(new) < count:
        more = fetch_free_riddles(count=count - len(new), try_multiplier=4)
        for r in more:
            if r not in used and r not in new:
                new.append(r)
            if len(new) >= count:
                break

    today_file = f"{TODAY_PREFIX}_{date.today()}.txt"
    with open(today_file, "w", encoding="utf-8") as f_today, open(USED_FILE, "a", encoding="utf-8") as f_used:
        for r in new:
            f_today.write(r + "\n")
            f_used.write(r + "\n")

    print(f"✅ Saved {len(new)} unique riddles for {date.today()} -> {today_file}")
    return new

# --- Create a single riddle video ---
def make_riddle_video(full_riddle, index, out_dir=OUT_DIR):
    # parse
    try:
        parts = full_riddle.split("|")
        riddle_text = parts[0].replace("Riddle:", "").strip()
        answer_text = parts[1].replace("Answer:", "").strip()
    except Exception as e:
        print("❌ parse error for:", full_riddle, e)
        return None

    # create black background
    bg = ColorClip(size=(WIDTH, HEIGHT), color=(0, 0, 0), duration=TOTAL_DURATION)

    # riddle text clip (first 6 seconds)
    riddle_clip = TextClip(riddle_text, fontsize=64, color="white",
                           size=(WIDTH - 160, None), method="caption", align="center", font="Arial").set_duration(6)

    # answer clip (appears at t=6, duration 4s) with fade-in + slight zoom
    answer_txt = TextClip("Answer: " + answer_text, fontsize=60, color="yellow",
                          size=(WIDTH - 160, None), method="caption", align="center", font="Arial").set_duration(4)
    # fadein fx applied when setting start
    # resize to slightly zoom over its duration (1.0 -> 1.08)
    answer_txt = answer_txt.set_start(6).fx(fadein.fadein, 0.8).resize(lambda t: 1 + 0.02 * t)

    # position both centered vertically: we'll center riddle in upper half and answer in center
    riddle_clip = riddle_clip.set_position(("center", HEIGHT * 0.38))
    answer_txt = answer_txt.set_position(("center", HEIGHT * 0.55))

    # combine
    final = CompositeVideoClip([bg, riddle_clip.set_start(0), answer_txt])

    # audio: loop background music if present
    if os.path.exists(MUSIC_PATH):
        try:
            audio = AudioFileClip(MUSIC_PATH).fx(afx.audio_loop, duration=final.duration)
            final = final.set_audio(audio)
        except Exception as e:
            print("⚠️ audio error:", e)

    # export
    out_path = os.path.join(out_dir, f"riddle_{date.today()}_{index}.mp4")
    # use reasonable preset
    final.write_videofile(out_path, fps=24, codec="libx264", audio_codec="aac", threads=2, verbose=False, logger=None)
    print(f"✅ Created: {out_path}")
    return out_path

# --- Main runner ---
def main_daily_run():
    print("🔎 Fetching riddles...")
    fetched = fetch_free_riddles(count=COUNT)
    if not fetched:
        print("❌ Could not fetch riddles from free API.")
        return

    unique = save_unique_riddles(fetched, count=COUNT)
    if not unique:
        print("⚠️ No unique riddles available (maybe exhausted).")
        return

    # create output folder for today's batch
    day_out = os.path.join(OUT_DIR, str(date.today()))
    os.makedirs(day_out, exist_ok=True)

    # create videos
    for idx, r in enumerate(unique, start=1):
        try:
            make_riddle_video(r, idx, out_dir=day_out)
        except Exception as e:
            print("❌ Error creating video for riddle:", r, e)

if __name__ == "__main__":
    main_daily_run()
