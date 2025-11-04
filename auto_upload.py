import os
import random
import glob
import subprocess
from datetime import date, datetime

# Folder for today's output
today_folder = f"output/{date.today()}"
video_files = sorted(glob.glob(f"{today_folder}/*.mp4"))

if not video_files:
    print("⚠️ No videos found to upload. Please run daily_riddle_generator.py first.")
    exit()

# Pick one random video
video_to_upload = random.choice(video_files)

# YouTube upload details
title = f"Riddle of the Day 🤔 #Shorts"
description = "Can you solve this? 🔥 #riddle #shorts #fun #quiz"
tags = "riddle,shorts,fun,quiz,brain,teaser"

print(f"🚀 Uploading video: {video_to_upload}")
cmd = [
    "youtube-upload",
    "--title", title,
    "--description", description,
    "--tags", tags,
    "--category", "Entertainment",
    "--privacy", "public",
    "--client-secrets", "client_secret.json",
    video_to_upload
]

subprocess.run(cmd)
print(f"✅ Uploaded at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
