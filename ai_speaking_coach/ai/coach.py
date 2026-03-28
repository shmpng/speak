import os
from speech.speech_to_text import Transcriber
from ai.evaluator import Evaluator
from config import TEMP_DIR


class SpeakingCoach:
    """Main controller for the speaking coach system"""
    
    def __init__(self):
        self.transcriber = Transcriber()
        self.evaluator = Evaluator()
    
    def process_session(self, audio_path: str, duration_seconds: int = 0) -> dict:
        """
        Process a complete speaking session:
        1. Transcribe audio to text
        2. Evaluate the speech
        3. Generate results
        
        Args:
            audio_path: Path to recorded audio file
            duration_seconds: Duration of the recording (optional for better pace analysis)
        
        Returns:
            Dictionary with transcript, analysis, and suggestions
        """
        
        try:
            # Step 1: Transcribe audio to text
            print(f"📝 Transcribing audio from {audio_path}...")
            transcription = self.transcriber.transcribe(audio_path)
            transcript_text = transcription["text"].strip()
            
            if not transcript_text:
                return self._get_error_result("No speech detected. Please try again.")
            
            print(f"✅ Transcription complete: {len(transcript_text)} characters")
            
            # Step 2: Evaluate the transcription
            print("🔍 Analyzing speech quality...")
            analysis = self.evaluator.analyze(transcript_text, duration_seconds)
            
            print(f"✅ Analysis complete. Score: {analysis['overall_score']}/10")
            
            # Step 3: Compile results
            result = {
                "status": "success",
                "transcript": transcript_text,
                "overall_score": analysis["overall_score"],
                "fluency_score": analysis["fluency_score"],
                "clarity_score": analysis["clarity_score"],
                "grammar_score": analysis["grammar_score"],
                "vocabulary_score": analysis["vocabulary_score"],
                "pace_score": analysis["pace_score"],
                "suggestions": analysis["suggestions"],
                "strengths": analysis["strengths"],
                "word_count": analysis["word_count"],
                "sentence_count": analysis["sentence_count"],
            }
            
            return result
            
        except FileNotFoundError as e:
            return self._get_error_result(f"Audio file not found: {e}")
        except Exception as e:
            return self._get_error_result(f"Error processing audio: {str(e)}")
        finally:
            # Cleanup
            self._cleanup_audio(audio_path)
    
    def _cleanup_audio(self, audio_path: str):
        """Delete temporary audio file"""
        try:
            if os.path.exists(audio_path):
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
