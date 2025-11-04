import os
from datetime import datetime
import subprocess

# Step 1: Generate new riddles
print("🧩 Generating new riddles...")
subprocess.run(["python", "fetch_riddles.py"])

# Step 2: Create videos
print("🎬 Creating videos...")
subprocess.run(["python", "create_riddle_videos.py"])

print(f"✅ Daily generation complete at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
