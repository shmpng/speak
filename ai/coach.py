import os
from pathlib import Path
from ai.audio_analyzer import AudioAnalyzer
from config import TEMP_DIR


class SpeakingCoach:
    """Main controller for the speaking coach system"""
    
    def __init__(self):
        self.audio_analyzer = AudioAnalyzer()
    
    def process_session(self, audio_path: str, duration_seconds: int = 0) -> dict:
        """
        Process a complete speaking session:
        Analyze user's audio and compare with American English
        
        Args:
            audio_path: Path to recorded audio file
            duration_seconds: Duration of the recording
        
        Returns:
            Dictionary with analysis results
        """
        
        try:
            # Convert to string if Path object
            if isinstance(audio_path, Path):
                audio_path = str(audio_path)
            
            # Validate audio file exists
            if not audio_path:
                return self._get_error_result("No audio file provided.")
            
            # Get absolute path
            audio_path_abs = os.path.abspath(audio_path)
            
            print(f"\n{'='*60}")
            print(f"🎤 AUDIO ANALYSIS")
            print(f"{'='*60}")
            print(f"File: {audio_path_abs}")
            print(f"Exists: {os.path.exists(audio_path_abs)}")
            
            if not os.path.exists(audio_path_abs):
                if os.path.exists(audio_path):
                    audio_path_to_use = audio_path
                else:
                    return self._get_error_result(f"Audio file not found")
            else:
                audio_path_to_use = audio_path_abs
            
            file_size = os.path.getsize(audio_path_to_use)
            if file_size == 0:
                return self._get_error_result("Audio file is empty. Please record again.")
            
            print(f"Size: {file_size} bytes")
            print(f"{'='*60}\n")
            
            # Analyze the audio
            print(f"🔍 Analyzing your voice...")
            analysis = self.audio_analyzer.analyze_audio(audio_path_to_use)
            
            if analysis.get("status") == "error":
                return analysis
            
            print(f"✅ Analysis complete. Score: {analysis['overall_score']}/10")
            
            return analysis
            
        except Exception as e:
            import traceback
            print(f"Unexpected error: {traceback.format_exc()}")
            return self._get_error_result(f"Unexpected error: {str(e)}")
        finally:
            # Cleanup
            try:
                if 'audio_path_to_use' in locals():
                    self._cleanup_audio(audio_path_to_use)
            except:
                pass
    
    def _cleanup_audio(self, audio_path):
        """Delete temporary audio file"""
        try:
            if isinstance(audio_path, Path):
                audio_path = str(audio_path)
            
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
                print(f"🧹 Cleaned up: {audio_path}")
        except Exception as e:
            print(f"Warning: Could not delete {audio_path}: {e}")
    
    def _get_error_result(self, error_message: str) -> dict:
        """Return error result"""
        return {
            "status": "error",
            "error_message": error_message,
            "transcript": "",
            "overall_score": 0,
            "fluency_score": 0,
            "clarity_score": 0,
            "grammar_score": 0,
            "vocabulary_score": 0,
            "pace_score": 0,
            "suggestions": [error_message],
            "strengths": [],
            "word_count": 0,
            "sentence_count": 0,
        }
