import streamlit as st
import os
from ai_generator import process_script
from timeline_builder import create_timeline_and_video

st.set_page_config(page_title="AI Video Engine", layout="centered")

st.title("🎬 AI Script-to-Video Engine")
st.markdown("Enter a moral story or educational script, and watch the AI build a complete video!")

script_input = st.text_area("Your Script:", height=150, placeholder="Once upon a time in a beautiful village. There lived a wise old man...")

if st.button("Generate Video ✨"):
    if len(script_input) > 20:
        st.info("Step 1: AI is analyzing script and generating images & voiceovers... This may take a minute.")
        
        with st.spinner("Generating Assets..."):
            assets = process_script(script_input)
            
        if assets:
            st.success(f"Generated {len(assets)} scenes successfully!")
            st.info("Step 2: Compiling timeline and rendering final MP4 video...")
            
            with st.spinner("Rendering Video..."):
                json_file, video_file = create_timeline_and_video(assets)
                
            if video_file and os.path.exists(video_file):
                st.balloons()
                st.success("🎉 Project Completed Successfully!")
                
                # Video Screen par dikhayen
                st.video(video_file)
                
                # Download Buttons
                col1, col2 = st.columns(2)
                with col1:
                    with open(video_file, "rb") as file:
                        st.download_button("⬇️ Download Final Video", data=file, file_name="AI_Movie.mp4", mime="video/mp4")
                with col2:
                    with open(json_file, "rb") as file:
                        st.download_button("⬇️ Download Project Timeline (JSON)", data=file, file_name="timeline.json", mime="application/json")
        else:
            st.error("Failed to generate assets. Check your internet connection.")
    else:
        st.warning("Please enter a longer script (at least two sentences ending with full stops).")