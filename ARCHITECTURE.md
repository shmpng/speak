# Architecture & Design - AI Speaking Coach

Comprehensive documentation of the application architecture, data flow, and design decisions.

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (Streamlit)               │
│  ┌──────────┬──────────────┬──────────┬─────────────────┐  │
│  │  Home    │  Call Screen │Processing│ Result Screen   │  │
│  │ Screen   │ (Recording)  │ Screen   │ (Display)       │  │
│  └──────────┴──────────────┴──────────┴─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Main App Controller                      │
│              (ui/app.py - Navigation Logic)                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                  Speaking Coach (ai/coach.py)              │
│        Orchestrates entire processing pipeline              │
└──────────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Audio     │      │  Speech      │      │     AI      │
│ Recording   │      │  Analysis    │      │ Evaluation  │
│  (audio/)   │      │  (speech/)   │      │  (ai/)      │
└─────────────┘      └──────────────┘      └─────────────┘
    ↓                     ↓                      ↓
 Microphone         Whisper Model         Advanced Analyzer
```

## Data Flow

### Complete Session Flow

```
1. USER INITIATES SESSION
   └─ Home Screen → Click "Start Speaking Practice"
   
2. NAVIGATION
   └─ Switch to Call Screen
   └─ Initialize recording variables
   
3. AUDIO RECORDING
   ├─ User clicks microphone
   ├─ AudioRecorder captures voice
   └─ Saved as WAV file in temp/ directory
   
4. USER ENDS CALL
   └─ Audio file path stored in session_state
   
5. PROCESSING TRIGGERED
   ├─ Show processing screen with progress
   ├─ SpeakingCoach.process_session() called
   │
   ├─ Step 1: TRANSCRIPTION
   │  ├─ Transcriber.transcribe(audio_path)
   │  ├─ Whisper model converts audio → text
   │  └─ Return transcript string
   │
   ├─ Step 2: ANALYSIS
   │  ├─ Evaluator.analyze(transcript_text)
   │  ├─ Calculate 5 scores:
   │  │  ├─ Fluency (speech smoothness)
   │  │  ├─ Clarity (enunciation)
   │  │  ├─ Grammar (syntax correctness)
   │  │  ├─ Vocabulary (word diversity)
   │  │  └─ Pace (speaking speed)
   │  ├─ Generate suggestions
   │  └─ Identify strengths
   │
   ├─ Step 3: CLEANUP
   │  └─ Delete temporary audio file
   │
   └─ Return complete results dictionary
   
6. DISPLAY RESULTS
   ├─ Store result in st.session_state
   ├─ Switch to Result Screen
   └─ Display:
      ├─ Overall score (0-10)
      ├─ Individual criterion scores
      ├─ Strengths and suggestions
      ├─ Statistics and transcript
      └─ Navigation options
      
7. RESET OR RETRY
   ├─ Option 1: Try Again → Back to Call Screen (new recording)
   ├─ Option 2: Go Home → Clear all state, back to home
   └─ All temp data deleted
```

## Module Architecture

### 1. UI Layer (`ui/`)

**Purpose**: Handle all user interface and navigation

#### `app.py` - Main Controller
```python
class AppController:
    def run_app()
        - Initialize session state
        - Route to correct screen based on state
        - Handle screen transitions
        - Manage processing flow
    
    def show_processing_screen()
        - Show progress indicator
        - Call coach.process_session()
        - Handle errors
        - Navigate to results
```

#### Screens (`ui/screens/`)

**home.py**
- Welcome screen
- Start button
- How-it-works guide
- Tips and scoring info

**call_screen.py**
- Streamlit audio input widget
- Recording UI
- Control buttons
- Tips for recording

**result_screen.py**
- Overall score display
- Detailed breakdown chart
- Strengths list
- Suggestions list
- Statistics table
- Full transcript
- Navigation buttons

### 2. Audio Layer (`audio/`)

**Purpose**: Record audio from microphone

#### `recorder.py - AudioRecorder Class`
```python
class AudioRecorder:
    def record_audio_streamlit()
        - Use Streamlit's audio input widget
        - Capture microphone input
        - Save as WAV file
        - Return file path
    
    def cleanup(audio_file)
        - Delete temporary audio file
```

### 3. Speech Layer (`speech/`)

**Purpose**: Convert audio to text

#### `speech_to_text.py - Transcriber Class`
```python
class Transcriber:
    def __init__()
        - Load Whisper model (lazy loading)
        - Configure for English
    
    def transcribe(audio_path)
        - Convert audio file to text
        - Extract transcription from Whisper output
        - Return {text, confidence, language}
```

### 4. AI Layer (`ai/`)

**Purpose**: Analyze speech and provide feedback

#### `coach.py - SpeakingCoach Class`
```python
class SpeakingCoach:
    def __init__()
        - Initialize Transcriber
        - Initialize Evaluator
    
    def process_session(audio_path, duration)
        - Orchestrate entire pipeline
        - Call transcriber
        - Call evaluator
        - Cleanup
        - Return complete result
    
    def _cleanup_audio(audio_path)
        - Delete temp file
        - Handle errors gracefully
```

#### `evaluator.py - AdvancedEvaluator Class`
```python
class AdvancedEvaluator:
    def analyze(text, duration)
        - Perform comprehensive analysis
        - Calculate 5 scores
        - Generate suggestions
        - Return analysis dict
    
    def _analyze_fluency(text, duration)
        - Measure speech smoothness
        - Check for filler words
        - Evaluate word count
        
    def _analyze_clarity(text)
        - Check repetition patterns
        - Evaluate sentence structure
        
    def _analyze_grammar(text)
        - Pattern matching for common errors
        - Subject-verb agreement check
        - Tense consistency
        
    def _analyze_vocabulary(text)
        - Calculate word diversity
        - Type-token ratio
        
    def _analyze_pace(text, duration)
        - Calculate words per minute
        - Compare to ideal range (120-150 WPM)
    
    def _generate_suggestions(analysis)
        - Identify 3 weakest areas
        - Return targeted improvement tips
    
    def _identify_strengths(analysis)
        - Find scores ≥ 8
        - Return strength messages
```

### 5. Configuration (`config.py`)

Central configuration file:
```python
# Paths
PROJECT_ROOT = Path(__file__).parent
TEMP_DIR = PROJECT_ROOT / "temp"

# Audio settings
AUDIO_SAMPLE_RATE = 16000
MAX_RECORDING_SECONDS = 120

# Model settings
WHISPER_MODEL = "base"

# Evaluation criteria
EVALUATION_CRITERIA = {...}
RATING_SCALE = 10

# API Keys (optional)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Session
CLEAR_ON_RESET = True
```

## Data Structures

### Session State

Stored in Streamlit's `st.session_state`:

```python
{
    "screen": str,              # Current screen: "home", "call", "processing", "result"
    "recording_started": bool,  # Recording status
    "audio_path": str,          # Path to recorded audio file
    "recording_time": int,      # Duration in seconds
    "last_result": dict         # Analysis results
}
```

### Analysis Result Dictionary

```python
{
    "status": "success" | "error",
    "transcript": str,
    "overall_score": float,     # 0-10
    "fluency_score": float,     # 0-10
    "clarity_score": float,     # 0-10
    "grammar_score": float,     # 0-10
    "vocabulary_score": float,  # 0-10
    "pace_score": float,        # 0-10
    "suggestions": [str, ...],  # 3 improvement tips
    "strengths": [str, ...],    # Highlighted strengths
    "word_count": int,
    "sentence_count": int,
    "error_message": str        # If status == "error"
}
```

## Scoring Algorithms

### Fluency Score
```
Base Score = min(10, word_count / 10)
Filler Penalty = filler_word_count * 0.2
Final Score = max(1, Base - Filler Penalty)

Filler Words: "um", "uh", "like", "you know", etc.
```

### Clarity Score
```
Base Score = 8.0
Repetition Penalty = repetitive_words * 0.5
Length Penalty = -1 if avg_sentence_length < 3
                 -0.5 if avg_sentence_length > 25
Final Score = max(1, min(10, Base - Penalties))
```

### Grammar Score
```
Base Score = 8.0
Penalty per error pattern found = -1.0
Tense inconsistency = -0.5
Final Score = max(1, min(10, Base - Penalties))
```

### Vocabulary Score
```
diversity_ratio = unique_words / total_words

if diversity_ratio > 0.7:
    score = 9.0
elif diversity_ratio > 0.5:
    score = 7.5
elif diversity_ratio > 0.3:
    score = 5.0
else:
    score = 3.0

Simple word ratio penalty: -1.5 if > 50% simple words
Final Score = max(1, min(10, score - penalty))
```

### Pace Score
```
WPM = (word_count / duration_seconds) * 60
Ideal: 120-150 WPM = 10/10

if 120 ≤ WPM ≤ 150: score = 10.0
elif 100 ≤ WPM < 120 or 150 < WPM ≤ 170: score = 8.0
elif 80 ≤ WPM < 100 or 170 < WPM ≤ 190: score = 6.0
elif WPM < 80: score = 4.0
else: score = 5.0
```

### Overall Score
```
Overall = (Fluency + Clarity + Grammar + Vocabulary + Pace) / 5
```

## File Organization

```
ai_speaking_coach/
├── main.py                  # Entry point
├── config.py               # Configuration
├── requirements.txt        # Dependencies
│
├── ui/
│   ├── __init__.py
│   ├── app.py             # Main controller
│   └── screens/
│       ├── __init__.py
│       ├── home.py        # Home screen
│       ├── call_screen.py # Call screen
│       └── result_screen.py
│
├── audio/
│   ├── __init__.py
│   └── recorder.py        # Audio recording
│
├── speech/
│   ├── __init__.py
│   └── speech_to_text.py  # Whisper transcription
│
├── ai/
│   ├── __init__.py
│   ├── coach.py          # Main orchestrator
│   └── evaluator.py      # Speech analysis
│
├── temp/                  # Temporary files (audio)
│
└── README.md, INSTALL.md, ARCHITECTURE.md
```

## Design Decisions

### 1. Lazy Loading of Whisper Model
- Model loads only on first use
- Reduces startup time
- Cached after first load

### 2. Temporary File Cleanup
- Audio files deleted after processing
- No persistent storage
- Privacy-focused design

### 3. Streamlit for UI
- Quick to build
- Great for data visualization
- Built-in session management
- Easy deployment

### 4. Modular Architecture
- Separation of concerns
- Easy to test individual components
- Simple to extend

### 5. No Database
- User requested - keep it simple
- No persistence between sessions
- All data cleared on reset

## Error Handling

### Audio Recording Errors
- Microphone not available → Show warning, suggest alternatives
- File saving fails → Retry or manual file upload

### Transcription Errors
- Audio quality too poor → Return empty transcript
- Model loading fails → Clear cache, retry

### Analysis Errors
- Empty text → Return minimal analysis
- Processing timeout → Show error message

### Recovery Strategy
- Each step has try-catch blocks
- Graceful degradation
- User-friendly error messages
- Options to retry or go back

## Performance Optimization

### Model Loading
- Lazy loading (load when needed)
- Single model instance (reused)
- GPU support when available

### Processing Pipeline
- Streaming transcription
- Parallel analysis calculations
- Progress indicators

### Memory Management
- Temp files immediately cleaned
- No large data structures in memory
- Session state cleared on reset

## Future Architecture Improvements

1. **Caching Layer**: Cache transcription results
2. **Queue System**: Process multiple requests
3. **Database**: Optional persistent storage
4. **API Layer**: REST API for external clients
5. **Worker Processes**: Background processing
6. **Analytics**: Track user progress

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| UI | Streamlit | Web interface |
| Audio Input | pyaudio | Microphone capture |
| Transcription | Whisper (OpenAI) | Speech-to-text |
| Audio Processing | scipy, librosa | Audio analysis |
| Analysis Engine | Custom Python | Speech evaluation |
| Language | Python 3.8+ | Implementation |

## Deployment Considerations

- **Local**: Requires Whisper model download (~140MB)
- **Docker**: Can containerize with model included
- **Cloud**: Streamlit Cloud, Heroku, AWS
- **Scaling**: Would need API refactoring

---

**This architecture provides a clean, maintainable, and user-friendly speaking practice application.**
