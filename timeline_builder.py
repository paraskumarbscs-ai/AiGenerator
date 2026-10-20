import json
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

def create_timeline_and_video(assets_list, output_json="timeline.json", output_video="final_video.mp4"):
    timeline_data = {"project": "AI_Auto_Video_Pro", "clips": []}
    video_clips = []
    
    for item in assets_list:
        audio = AudioFileClip(item["audio"])
        duration = audio.duration
        
        # Base Image Clip
        img_clip = ImageClip(item["image"]).set_duration(duration)
        
        # 🔥 MAGIC MOVEMENT: Slow Zoom-In Effect (Ken Burns Effect)
        # Har second image 3% badi hogi, jisse professional camera movement dikhegi
        img_clip = img_clip.resize(lambda t: 1.0 + 0.03 * t)
        
        # Audio connect karein
        img_clip = img_clip.set_audio(audio)
        video_clips.append(img_clip)
        
        timeline_data["clips"].append({
            "image_file": item["image"],
            "audio_file": item["audio"],
            "duration_seconds": duration,
            "scene_text": item["text"]
        })
        
    with open(output_json, 'w') as f:
        json.dump(timeline_data, f, indent=4)
        
    if video_clips:
        # Clips ko jodh kar final render
        final_video = concatenate_videoclips(video_clips, method="compose")
        final_video.write_videofile(output_video, fps=24, codec="libx264", audio_codec="aac")
        return output_json, output_video
    
    return None, None