# API Reference - AI Speaking Coach

Complete API documentation for all modules and classes.

## Table of Contents
1. [UI Layer](#ui-layer)
2. [Audio Layer](#audio-layer)
3. [Speech Layer](#speech-layer)
4. [AI Layer](#ai-layer)
5. [Configuration](#configuration)

---

## UI Layer

### `ui.app` - Application Controller

#### `run_app()`
Main entry point for the Streamlit application.

**Usage:**
```python
from ui.app import run_app
run_app()
```

**What it does:**
- Initializes Streamlit session state
- Routes to appropriate screen based on current state
- Handles screen transitions
- Manages the processing flow

**States:**
- `"home"` → Display home screen
- `"call"` → Display call recording screen
- `"processing"` → Show processing with progress
- `"result"` → Display results screen

#### `show_processing_screen()`
Displays progress indicator while analyzing speech.

**Workflow:**
```
Show "Analyzing..." message
  ↓
Load audio path from session
  ↓
Initialize SpeakingCoach
  ↓
Call coach.process_session(audio_path)
  ↓
Store results in session
  ↓
Navigate to result screen
```

---

### `ui.screens.home` - Home Screen

#### `show()`
Displays the welcome and information screen.

**Features:**
- Welcome message
- Feature cards (Real-time Analysis, Detailed Scoring, Smart Suggestions)
- Start button
- How-it-works guide
- Tips and scoring criteria explanation

**Usage:**
```python
from ui.screens import home
home.show()
```

---

### `ui.screens.call_screen` - Call Recording Screen

#### `show()`
Displays the recording interface with audio input.

**Features:**
- Streamlit audio input widget
- Recording status display
- Control buttons (Clear, Back, End Call & Analyze)
- Recording tips in expander

**Session State Updates:**
- `audio_path` → Path to recorded audio file
- `recording_started` → Recording status

**Usage:**
```python
from ui.screens import call_screen
call_screen.show()
```

---

### `ui.screens.result_screen` - Results Display

#### `show()`
Displays comprehensive analysis results.

**Displays:**
- Overall score (0-10) with color coding
- 5 detailed criterion scores
- Strengths (highlighted achievements)
- Suggestions (improvement tips)
- Statistics (word count, sentences, etc.)
- Full transcript (in expander)
- Navigation buttons

**Color Coding:**
- 🟢 Green: Score ≥ 8 (Excellent)
- 🟠 Orange: 6 ≤ Score < 8 (Good)
- 🔴 Red: Score < 6 (Needs work)

**Usage:**
```python
from ui.screens import result_screen
result_screen.show()
```

---

## Audio Layer

### `audio.recorder` - Audio Recording

#### `class AudioRecorder`
Handles microphone input and recording.

```python
from audio.recorder import AudioRecorder

recorder = AudioRecorder()
```

##### Methods

**`record_audio_streamlit(duration: int = 30) → str`**

Records audio using Streamlit's built-in audio input.

**Parameters:**
- `duration` (int): Max recording duration in seconds

**Returns:**
- `str`: Path to saved WAV file

**Example:**
```python
audio_path = recorder.record_audio_streamlit(duration=60)
# Returns: "temp/recording_1234567890.wav"
```

**Features:**
- Real-time Streamlit audio widget
- Automatic file saving
- Error handling

**`cleanup(audio_file: str) → None`**

Deletes temporary audio file.

**Parameters:**
- `audio_file` (str): Path to audio file to delete

**Example:**
```python
recorder.cleanup("temp/recording_1234567890.wav")
```

---

## Speech Layer

### `speech.speech_to_text` - Transcription

#### `class Transcriber`
Converts audio to text using Whisper.

```python
from speech.speech_to_text import Transcriber

transcriber = Transcriber(model_name="base")
```

##### Methods

**`transcribe(audio_path: str, language: str = "en") → dict`**

Transcribes audio file to text.

**Parameters:**
- `audio_path` (str): Path to audio file
- `language` (str): Language code (default: "en" for English)

**Returns:**
```python
{
    "text": str,              # Transcribed text
    "confidence": float,      # Confidence score
    "language": str,          # Detected language
    "segments": list          # Segment details
}
```

**Example:**
```python
result = transcriber.transcribe("temp/recording.wav")
print(result["text"])  # "Hello, I am practicing my English"
```

**`get_model_info() → dict`**

Returns information about loaded model.

**Returns:**
```python
{
    "model": str,    # Model name
    "type": str      # Model class type
}
```

---

## AI Layer

### `ai.coach` - Main Orchestrator

#### `class SpeakingCoach`
Main controller for processing speaking sessions.

```python
from ai.coach import SpeakingCoach

coach = SpeakingCoach()
```

##### Methods

**`process_session(audio_path: str, duration_seconds: int = 0) → dict`**

Complete pipeline: transcribe → analyze → return results.

**Parameters:**
- `audio_path` (str): Path to recorded audio file
- `duration_seconds` (int): Recording duration for pace analysis

**Returns:**
```python
{
    "status": "success" | "error",
    "transcript": str,
    "overall_score": float,      # 0-10
    "fluency_score": float,      # 0-10
    "clarity_score": float,      # 0-10
    "grammar_score": float,      # 0-10
    "vocabulary_score": float,   # 0-10
    "pace_score": float,         # 0-10
    "suggestions": [str, ...],   # 3 improvement tips
    "strengths": [str, ...],     # Highlighted strengths
    "word_count": int,           # Total words
    "sentence_count": int,       # Total sentences
    "error_message": str         # If status == "error"
}
```

**Example:**
```python
result = coach.process_session("temp/recording.wav", duration_seconds=45)
print(f"Score: {result['overall_score']}/10")
print(f"Suggestions: {result['suggestions']}")
```

**Workflow:**
```
1. Validate audio file exists
2. Transcribe audio → text (Whisper)
3. Analyze text → scores (Evaluator)
4. Generate suggestions & strengths
5. Cleanup temporary file
6. Return complete result
```

**Error Handling:**
- Returns error status if file not found
- Catches transcription errors
- Handles analysis exceptions
- Always cleans up temp files

---

### `ai.evaluator` - Speech Analysis

#### `class AdvancedEvaluator` / `class Evaluator`
Analyzes speech quality on 5 criteria.

```python
from ai.evaluator import Evaluator

evaluator = Evaluator()
```

##### Methods

**`analyze(text: str, duration_seconds: int = 0) → dict`**

Comprehensive speech analysis.

**Parameters:**
- `text` (str): Transcribed speech text
- `duration_seconds` (int): Duration for pace calculation

**Returns:**
```python
{
    "fluency_score": float,      # 0-10
    "clarity_score": float,      # 0-10
    "grammar_score": float,      # 0-10
    "vocabulary_score": float,   # 0-10
    "pace_score": float,         # 0-10
    "overall_score": float,      # 0-10 (average)
    "suggestions": [str, ...],   # Top 3 improvements
    "strengths": [str, ...],     # Highlighted achievements
    "transcript": str,           # Original text
    "word_count": int,           # Total words
    "sentence_count": int        # Total sentences
}
```

**Example:**
```python
transcript = "Hello, I am practicing my English speaking skills today."
result = evaluator.analyze(transcript, duration_seconds=10)

print(result["overall_score"])  # 7.8
print(result["suggestions"])    # ["Expand vocabulary...", ...]
```

##### Detailed Analysis Methods

**`_analyze_fluency(text: str, duration_seconds: int) → float`**

Evaluates speech smoothness and naturalness.

**Factors:**
- Word count (more = more fluent)
- Filler words ("um", "uh", "like", etc.) - penalized
- Response length
- Complexity

**Scoring:**
- Short responses (<5 words): 2/10
- Moderate (15-30 words): 4-6/10
- Good (30+ words): 7-10/10
- Filler words: -0.2 per word

**`_analyze_clarity(text: str) → float`**

Evaluates enunciation and speech structure.

**Factors:**
- Word repetition patterns
- Sentence length (too short or too long)
- Sentence structure quality
- Fragment detection

**`_analyze_grammar(text: str) → float`**

Evaluates syntax and grammar correctness.

**Factors:**
- Subject-verb agreement
- Tense consistency
- Common error patterns
- Clause structure

**`_analyze_vocabulary(text: str) → float`**

Evaluates word diversity and complexity.

**Factors:**
- Type-Token Ratio (unique / total words)
- Simple vs complex words ratio
- Vocabulary richness

**Scoring:**
- Diversity > 0.7: 9/10
- Diversity > 0.5: 7.5/10
- Diversity > 0.3: 5/10
- Diversity ≤ 0.3: 3/10

**`_analyze_pace(text: str, duration_seconds: int) → float`**

Evaluates speaking speed.

**Ideal:** 120-150 words per minute (WPM)

**Scoring:**
- 120-150 WPM: 10/10 (Perfect)
- 100-120 or 150-170 WPM: 8/10 (Good)
- 80-100 or 170-190 WPM: 6/10 (Fair)
- <80 WPM: 4/10 (Too slow)
- >190 WPM: 5/10 (Too fast)

**`_generate_suggestions(analysis: dict) → list`**

Creates improvement suggestions.

**Logic:**
1. Identifies 3 weakest scoring areas
2. Maps suggestions to each area
3. Returns personalized tips

**Example output:**
```python
[
    "Expand your vocabulary by reading more",
    "Try to minimize filler words like 'um' and 'like'",
    "Break up long sentences for better clarity"
]
```

**`_identify_strengths(analysis: dict) → list`**

Highlights areas of excellence.

**Criteria:**
- Score ≥ 8 for a criterion
- Generates emoji-prefixed messages

**Example output:**
```python
[
    "✨ Excellent grammar and syntax!",
    "✨ Clear and well-structured speech!"
]
```

---

## Configuration

### `config.py` - Settings File

Central configuration for the entire application.

#### Audio Settings
```python
AUDIO_SAMPLE_RATE = 16000       # Hz (samples per second)
AUDIO_CHUNK_SIZE = 1024         # Bytes per chunk
AUDIO_FORMAT = "wav"            # Audio format
MAX_RECORDING_SECONDS = 120     # Max duration
```

#### Model Settings
```python
WHISPER_MODEL = "base"          # Options: tiny, base, small, medium, large
USE_LOCAL_WHISPER = True        # Use local model (not API)
```

Options:
- `"tiny"`: 140MB, fastest (∼5 sec for 30 sec audio)
- `"base"`: 140MB, balanced (∼10 sec for 30 sec audio)
- `"small"`: 460MB, better accuracy (∼15 sec)
- `"medium"`: 1.5GB, very accurate (∼25 sec)
- `"large"`: 2.9GB, best accuracy (∼45 sec)

#### Evaluation Settings
```python
EVALUATION_CRITERIA = {
    "fluency": "How smoothly and naturally did the speaker speak?",
    "clarity": "How clear and understandable was the pronunciation?",
    "grammar": "How correct was the grammar used?",
    "vocabulary": "How diverse and appropriate was the vocabulary?",
    "pace": "Was the pace appropriate and consistent?"
}
RATING_SCALE = 10
```

#### Paths
```python
PROJECT_ROOT = Path(__file__).parent
TEMP_DIR = PROJECT_ROOT / "temp"  # For temporary audio files
```

#### Session Settings
```python
SESSION_TIMEOUT = 3600          # 1 hour
CLEAR_ON_RESET = True           # Clear all data on reset
```

#### API Keys (Optional)
```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
```

---

## Usage Examples

### Complete Session Example

```python
from ui.app import run_app
from ai.coach import SpeakingCoach
from audio.recorder import AudioRecorder

# Initialize components
coach = SpeakingCoach()
recorder = AudioRecorder()

# Record speech
audio_path = "temp/recording.wav"  # From Streamlit widget

# Process the session
result = coach.process_session(audio_path)

# Display results
print(f"Overall Score: {result['overall_score']}/10")
print(f"Fluency: {result['fluency_score']}/10")
print(f"Clarity: {result['clarity_score']}/10")
print(f"Grammar: {result['grammar_score']}/10")
print(f"Vocabulary: {result['vocabulary_score']}/10")
print(f"Pace: {result['pace_score']}/10")

print("\nSuggestions:")
for suggestion in result['suggestions']:
    print(f"  • {suggestion}")

print("\nStrengths:")
for strength in result['strengths']:
    print(f"  {strength}")

# Cleanup
recorder.cleanup(audio_path)
```

### Custom Analysis Example

```python
from ai.evaluator import Evaluator

evaluator = Evaluator()

text = "Hello, I am practicing my English speaking skills today. I want to improve my fluency and vocabulary."

result = evaluator.analyze(text, duration_seconds=15)

# Access individual scores
fluency = result['fluency_score']
clarity = result['clarity_score']
grammar = result['grammar_score']
vocabulary = result['vocabulary_score']
pace = result['pace_score']
overall = result['overall_score']

print(f"Overall: {overall}/10")
```

### Transcription Example

```python
from speech.speech_to_text import Transcriber

transcriber = Transcriber(model_name="base")

# Transcribe audio
result = transcriber.transcribe("audio.wav", language="en")

transcript = result['text']
confidence = result['confidence']
language = result['language']

print(f"Transcript: {transcript}")
print(f"Confidence: {confidence}")
```

---

## Error Handling

### Common Errors & Solutions

#### FileNotFoundError
```python
try:
    transcriber.transcribe("nonexistent.wav")
except FileNotFoundError:
    print("Audio file not found!")
```

#### Out of Memory
```python
# Use smaller model
config.WHISPER_MODEL = "tiny"
transcriber = Transcriber(model_name="tiny")
```

#### Microphone Not Available
- Check system audio settings
- Grant microphone permissions
- Try different audio input device

---

## Performance Notes

### Typical Processing Times

| Task | Time |
|------|------|
| Model Loading (first time) | 2-10 seconds |
| Audio Recording | Real-time |
| Transcription (30 sec audio) | 10-15 seconds |
| Analysis | <1 second |
| Total Session | 15-20 seconds |

### Optimization Tips

1. Use smaller models for faster processing
2. Pre-load model to avoid delays
3. Batch process multiple recordings
4. Use GPU for transcription if available

---

## Testing

### Unit Test Example

```python
from ai.evaluator import Evaluator

def test_fluency_scoring():
    evaluator = Evaluator()
    
    # Test short response
    result = evaluator.analyze("Hi", duration_seconds=2)
    assert result['fluency_score'] < 5
    
    # Test long response
    long_text = " ".join(["word"] * 50)
    result = evaluator.analyze(long_text, duration_seconds=30)
    assert result['fluency_score'] >= 5
```

---

**📖 For more detailed information, see README.md and ARCHITECTURE.md**
