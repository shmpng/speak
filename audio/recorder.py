import streamlit as st
from config import TEMP_DIR
from pathlib import Path
import time


class AudioRecorder:
    """Records audio using Streamlit's audio input"""
    
    def __init__(self):
        pass
    
    def record_audio_streamlit(self, duration: int = 30) -> str:
        """
        Record audio using Streamlit's built-in audio input.
        No PyAudio needed!
        
        Returns: path to saved audio file or None
        """
        # Streamlit's audio input widget
        audio_data = st.audio_input("🎤 Click the microphone to record your speech")
        
        if audio_data is not None:
            # Save the recorded audio
            timestamp = int(time.time())
            audio_file = TEMP_DIR / f"recording_{timestamp}.wav"
            
            with open(audio_file, 'wb') as f:
                f.write(audio_data.getbuffer())
            
            return str(audio_file)
        
        return None
    
    def cleanup(self, audio_file: str):
        """Delete temporary audio file"""
        try:
            path = Path(audio_file)
            if path.exists():
                path.unlink()
                print(f"🧹 Cleaned up: {audio_file}")
        except Exception as e:
            print(f"Warning: Could not delete {audio_file}: {e}")
