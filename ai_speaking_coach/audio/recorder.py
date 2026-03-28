import streamlit as st
import pyaudio
import wave
import numpy as np
from config import AUDIO_SAMPLE_RATE, AUDIO_CHUNK_SIZE, TEMP_DIR
from pathlib import Path
import time


class AudioRecorder:
    """Records audio from microphone and saves as WAV file"""
    
    def __init__(self):
        self.sample_rate = AUDIO_SAMPLE_RATE
        self.chunk = AUDIO_CHUNK_SIZE
        self.audio_format = pyaudio.paFloat32
        
    def record_audio(self, duration: int = 30) -> str:
        """
        Record audio from microphone
        Returns: path to saved audio file
        """
        p = pyaudio.PyAudio()
        
        # Open stream
        stream = p.open(
            format=self.audio_format,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        frames = []
        print(f"Recording for {duration} seconds...")
        
        for i in range(0, int(self.sample_rate / self.chunk * duration)):
            try:
                data = stream.read(self.chunk, exception_on_overflow=False)
                frames.append(data)
            except Exception as e:
                print(f"Error reading audio: {e}")
                break
        
        # Stop stream
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Save audio file
        timestamp = int(time.time())
        audio_file = TEMP_DIR / f"recording_{timestamp}.wav"
        
        with wave.open(str(audio_file), 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(self.audio_format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))
        
        print(f"Audio saved to {audio_file}")
        return str(audio_file)
    
    def record_audio_streamlit(self, duration: int = 30) -> str:
        """
        Record audio using Streamlit's audio input (if available)
        Falls back to file upload method
        """
        st.info("📱 Please use your system's microphone or upload an audio file")
        
        # Try using Streamlit's audio input
        audio_data = st.audio_input("Record your speech (Click the microphone icon)")
        
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
        except Exception as e:
            print(f"Error deleting audio file: {e}")
