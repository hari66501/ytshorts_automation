from moviepy.editor import TextClip, ColorClip, CompositeVideoClip

# Black background
bg = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=3)

# Text overlay
txt = TextClip("✅ MoviePy is working!", fontsize=80, color='white', size=(900, None), method='caption')
txt = txt.set_position('center').set_duration(3)

# Combine and export
final = CompositeVideoClip([bg, txt])
final.write_videofile("test_output.mp4", fps=24, codec="libx264", audio_codec="aac")

print("🎬 Done! Check test_output.mp4")
