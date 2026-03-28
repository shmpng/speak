import streamlit as st
import time
from audio.recorder import AudioRecorder

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
    
    recorder = AudioRecorder()
    
    # Two-column layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎙️ Record Your Speech")
        
        # Use Streamlit's built-in audio input
        audio_data = st.audio_input("Click the microphone to record", key="audio_input")
        
        if audio_data is not None:
            # Save the recorded audio
            import os
            from config import TEMP_DIR
            
            timestamp = int(time.time())
            audio_file = os.path.join(TEMP_DIR, f"recording_{timestamp}.wav")
            
            with open(audio_file, 'wb') as f:
                f.write(audio_data.getbuffer())
            
            st.session_state.audio_path = audio_file
            st.success("✅ Audio recorded successfully!")
    
    with col2:
        st.subheader("💾 Recording Status")
        
        if st.session_state.audio_path:
            st.success(f"✅ Audio ready for analysis")
            st.caption(f"File: {os.path.basename(st.session_state.audio_path)}")
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
        if st.session_state.audio_path:
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
