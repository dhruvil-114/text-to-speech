import streamlit as st
import edge_tts
import asyncio
import base64
import sys

# Page Configuration
st.set_page_config(
    page_title="PixelPaji AI Studio", 
    page_icon="🎙️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# External CSS file ko load karna
try:
    with open("style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠️ style.css file nahi mili! Kripya check karein ki wo is file ke sath wale folder mein hai.")

# Organized Dictionary for Languages and Genders
VOICE_MAP = {
    "Hindi": {
        "Male": "hi-IN-MadhurNeural",
        "Female": "hi-IN-SwaraNeural"
    },
    "English": {
        "Male": "en-IN-PrabhatNeural", 
        "Female": "en-IN-NeerjaNeural"
    },
    "Gujarati": {
        "Male": "gu-IN-NiranjanNeural",
        "Female": "gu-IN-DhwaniNeural"
    }
}

# Core TTS Function
async def generate_voice_file(text, voice_id, output_path):
    communicate = edge_tts.Communicate(text, voice_id)
    await communicate.save(output_path)

# UI Header
st.markdown('<div class="app-header"><p class="brand-title">PixelPaji</p><p class="brand-tagline">PROFESSIONAL AI VOICE STUDIO</p></div>', unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)

input_col, settings_col = st.columns([2, 1])

with input_col:
    script_content = st.text_area(
        "📄 Enter Script Here", 
        height=250, 
        placeholder="Type or paste your text in Hindi, English, or Gujarati..."
    )

with settings_col:
    st.write("🔧 Voice Configuration")
    
    selected_language = st.selectbox("1. Select Language:", ["Hindi", "English", "Gujarati"])
    selected_gender = st.radio("2. Select Gender:", ["Male", "Female"], horizontal=True)
    
    st.write("") 
    generate_action = st.button("Generate Audio ▶️")

st.markdown('</div>', unsafe_allow_html=True)

output_section = st.container()

with output_section:
    if generate_action:
        if script_content.strip():
            selected_voice_id = VOICE_MAP[selected_language][selected_gender]
            result_filename = "ai_voice_studio.mp3"
            
            with st.spinner(f"⏳ Generating {selected_language} ({selected_gender}) voice..."):
                try:
                    asyncio.run(generate_voice_file(script_content, selected_voice_id, result_filename))
                    st.success("✅ Conversion successful!")
                    st.audio(result_filename, format="audio/mp3")
                    
                    with open(result_filename, "rb") as audio_file:
                        audio_bytes = audio_file.read()
                        
                    st.download_button(
                        label="Download MP3 📥",
                        data=audio_bytes,
                        file_name=f"PixelPaji_{selected_language}_{selected_gender}.mp3",
                        mime="audio/mp3"
                    )
                except Exception as e:
                    st.error(f"❌ Error during generation: {e}")
        else:
            st.warning("⚠️ Script content cannot be empty.")

# --- NAYA AUR SAFE MAGIC CODE ---
if __name__ == "__main__":
    from streamlit.runtime import exists
    # Ye check karega ki Streamlit already start toh nahi ho gaya
    if not exists():
        import subprocess
        print("Starting PixelPaji AI Studio... Please wait!") 
        # Alag process mein safe tarike se streamlit run karega
        subprocess.run([sys.executable, "-m", "streamlit", "run", sys.argv[0]])