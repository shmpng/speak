import os
import tempfile
from pathlib import Path

# ============== PATHS ==============
PROJECT_ROOT = Path(__file__).parent

# Use Windows TEMP directory (avoids OneDrive file locking issues)
# OneDrive locks files during sync, causing "file not found" errors
TEMP_DIR = os.path.join(tempfile.gettempdir(), "ai_speaking_coach")

# Ensure temp directory exists
try:
    os.makedirs(TEMP_DIR, exist_ok=True)
    print(f"✅ Temp directory: {TEMP_DIR}")
except Exception as e:
    print(f"Warning: Could not create temp directory: {e}")

# ============== AUDIO SETTINGS ==============
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHUNK_SIZE = 1024
AUDIO_FORMAT = "wav"
MAX_RECORDING_SECONDS = 120

# ============== MODEL SETTINGS ==============
WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large
USE_LOCAL_WHISPER = True  # Set to False if using API

# ============== EVALUATION SETTINGS ==============
EVALUATION_CRITERIA = {
    "fluency": "How smoothly and naturally did the speaker speak?",
    "clarity": "How clear and understandable was the pronunciation?",
    "grammar": "How correct was the grammar used?",
    "vocabulary": "How diverse and appropriate was the vocabulary?",
    "pace": "Was the pace appropriate and consistent?",
}

RATING_SCALE = 10

# ============== API KEYS (Optional) ==============
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# ============== SESSION SETTINGS ==============
SESSION_TIMEOUT = 3600  # 1 hour in seconds
CLEAR_ON_RESET = True  # Clear all data when going back to home
