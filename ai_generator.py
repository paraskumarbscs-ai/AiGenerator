import os
import requests
import urllib.parse
import asyncio
import edge_tts
from deep_translator import GoogleTranslator

def translate_roman_to_english(roman_text):
    try:
        english_text = GoogleTranslator(source='auto', target='en').translate(roman_text)
        return english_text
    except Exception as e:
        print(f"Translation Error (EN): {e}")
        return roman_text

def translate_roman_to_urdu_script(roman_text):
    try:
        urdu_script = GoogleTranslator(source='auto', target='ur').translate(roman_text)
        return urdu_script
    except Exception as e:
        print(f"Translation Error (UR): {e}")
        return roman_text

# 🔥 NAYA: Asli Insaan Jaisi Aawaz Banane Wala Logic (Async)
async def _generate_realistic_audio(text, output_file):
    # 'ur-PK-AsadNeural' = Real Pakistani Male Voice
    # Agar female chahiye toh 'ur-PK-UzmaNeural' use kar sakte hain
    voice = "ur-PK-AsadNeural" 
    
    # Pitch aur speed set ki taaki aur deep aur story-telling wali feel aaye
    communicate = edge_tts.Communicate(text, voice, rate="-5%", pitch="-2Hz")
    await communicate.save(output_file)

def generate_audio(text, filename):
    try:
        urdu_text = translate_roman_to_urdu_script(text)
        print(f"Urdu Script for Voice: {urdu_text}")
        
        audio_path = f"{filename}.mp3"
        # Naye system ko command dena
        asyncio.run(_generate_realistic_audio(urdu_text, audio_path))
        return audio_path
    except Exception as e:
        print(f"Audio Error: {e}")
        return None

def generate_image(prompt, filename):
    try:
        english_prompt = translate_roman_to_english(prompt)
        print(f"English Prompt for AI Image: {english_prompt}")
        
        safe_prompt = urllib.parse.quote(english_prompt)
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1280&height=720&nologo=true"
        response = requests.get(url)
        
        image_path = f"{filename}.jpg"
        with open(image_path, 'wb') as f:
            f.write(response.content)
        return image_path
    except Exception as e:
        print(f"Image Error: {e}")
        return None

def process_script(script_text):
    scenes = [s.strip() for s in script_text.split('.') if len(s.strip()) > 5]
    assets = []
    
    for i, scene in enumerate(scenes):
        print(f"\n--- Processing Scene {i+1} ---")
        audio_file = generate_audio(scene, f"scene_{i}")
        image_file = generate_image(scene, f"scene_{i}")
        
        if audio_file and image_file:
            assets.append({
                "scene_num": i + 1,
                "text": scene,
                "audio": audio_file,
                "image": image_file
            })
            
    return assets