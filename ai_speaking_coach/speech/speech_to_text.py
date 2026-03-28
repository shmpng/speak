import whisper
from config import WHISPER_MODEL
import os


class Transcriber:
    """Converts audio to text using OpenAI Whisper"""
    
    def __init__(self, model_name: str = WHISPER_MODEL):
        """
        Initialize transcriber with Whisper model
        Models: tiny, base, small, medium, large
        """
        self.model_name = model_name
        self.model = None
    
    def _load_model(self):
        """Lazy load model to avoid delays"""
        if self.model is None:
            print(f"Loading Whisper model: {self.model_name}...")
            self.model = whisper.load_model(self.model_name)
        return self.model
    
    def transcribe(self, audio_path: str, language: str = "en") -> dict:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file
            language: Language code (default: English)
        
        Returns:
            dict with 'text', 'confidence', and 'language'
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        try:
            model = self._load_model()
            result = model.transcribe(
                audio_path,
                language=language,
                verbose=False,
                fp16=False
            )
            
            return {
                "text": result["text"],
                "confidence": result.get("confidence", 0.0),
                "language": result.get("language", language),
                "segments": result.get("segments", [])
            }
        except Exception as e:
            print(f"Transcription error: {e}")
            raise
    
    def get_model_info(self) -> dict:
        """Get information about loaded model"""
        model = self._load_model()
        return {
            "model": self.model_name,
            "type": type(model).__name__,
        }
