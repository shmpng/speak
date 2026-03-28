import streamlit as st
import time
import os
from pathlib import Path
from config import TEMP_DIR

def show():
    """Display call screen with recording functionality"""
    
    st.title("📞 Speaking Practice")
    st.markdown("---")
    
    # Instructions
    st.info("🎤 **Click the microphone button below to start recording your speech**  \nYou can speak for up to 2 minutes. Click 'End Call & Analyze' when finished.")
    
    # Initialize session state
    if "recording_started" not in st.session_state:
        st.session_state.recording_started = False
    if "audio_path" not in st.session_state:
        st.session_state.audio_path = None
    if "recording_time" not in st.session_state:
        st.session_state.recording_time = 0
    
    # Ensure temp directory exists
    try:
        Path(TEMP_DIR).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        st.error(f"Error creating temp directory: {e}")
        return
    
    # Two-column layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎙️ Record Your Speech")
        
        # Use Streamlit's built-in audio input
        audio_data = st.audio_input("Click the microphone to record", key="audio_input")
        
        if audio_data is not None:
            try:
                # Ensure temp directory exists and convert to string
                temp_dir_str = str(TEMP_DIR)
                Path(temp_dir_str).mkdir(parents=True, exist_ok=True)
                
                # Save the recorded audio with proper string path
                timestamp = int(time.time())
                audio_file = os.path.join(temp_dir_str, f"recording_{timestamp}.wav")
                
                # Write audio file with explicit flush
                with open(audio_file, 'wb') as f:
                    f.write(audio_data.getbuffer())
                    f.flush()  # Ensure data is written to disk
                    os.fsync(f.fileno())  # Force sync to disk
                
                # Small delay to ensure file is fully written
                time.sleep(0.5)
                
                # Verify file was saved
                if os.path.exists(audio_file) and os.path.getsize(audio_file) > 0:
                    # Store as string, not Path object
                    st.session_state.audio_path = audio_file
                    file_size = os.path.getsize(audio_file)
                    abs_path = os.path.abspath(audio_file)
                    st.success("✅ Audio recorded successfully!")
                    st.caption(f"📁 Path: {abs_path}")
                    st.caption(f"📊 Size: {file_size} bytes")
                else:
                    st.error("❌ Failed to save audio file. Please try again.")
                    st.session_state.audio_path = None
            except Exception as e:
                st.error(f"❌ Error saving audio: {e}")
                st.session_state.audio_path = None
    
    with col2:
        st.subheader("💾 Recording Status")
        
        if st.session_state.audio_path:
            if os.path.exists(st.session_state.audio_path):
                file_size = os.path.getsize(st.session_state.audio_path)
                st.success(f"✅ Audio ready for analysis")
                st.caption(f"File: {os.path.basename(st.session_state.audio_path)}")
                st.caption(f"Size: {file_size} bytes")
            else:
                st.warning("⚠️ Audio file not found. Please record again.")
                st.session_state.audio_path = None
        else:
            st.warning("⏳ Waiting for audio input...")
    
    st.markdown("---")
    
    # Control buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔄 Clear Recording", use_container_width=True):
            if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
                try:
                    os.remove(st.session_state.audio_path)
                except:
                    pass
            st.session_state.audio_path = None
            st.rerun()
    
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.screen = "home"
            st.rerun()
    
    with col3:
        if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
            if st.button("✅ End Call & Analyze", use_container_width=True, type="primary"):
                st.session_state.screen = "processing"
                st.rerun()
        else:
            st.button("✅ End Call & Analyze", use_container_width=True, disabled=True)
    
    st.markdown("---")
    
    # Tips
    with st.expander("📋 Recording Tips"):
        st.markdown("""
        - **Clear your throat** before starting
        - **Speak naturally** - Don't read or memorize
        - **Use varied vocabulary** - Show your range
        - **Complete your thoughts** - Full sentences are better
        - **Maintain steady pace** - Not too fast, not too slow
        - **Pause when needed** - It's okay to take a breath
        """)
