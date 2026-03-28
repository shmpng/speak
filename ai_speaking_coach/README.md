# 🗣️ AI Speaking Coach

An intelligent speaking practice application that provides real-time feedback on your English speech. Get detailed analysis on fluency, clarity, grammar, vocabulary, and pace with personalized improvement suggestions.

## ✨ Features

- 🎤 **Real-time Speech Recording** - Record your speech directly in the app
- 📝 **Instant Transcription** - Convert speech to text using Whisper AI
- 🔍 **Comprehensive Analysis** - Get scored on 5 criteria:
  - Fluency (smoothness & naturalness)
  - Clarity (enunciation & understanding)
  - Grammar (syntax & correctness)
  - Vocabulary (diversity & appropriateness)
  - Pace (speed consistency, 120-150 WPM ideal)
- 💡 **Smart Suggestions** - Personalized tips based on your weak areas
- ✨ **Strength Recognition** - Learn what you're doing well
- 📊 **Detailed Statistics** - Word count, sentence analysis, and more
- 🏠 **Clean Interface** - Simple, intuitive workflow
- 💾 **No Data Storage** - All data is cleared after each session

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Microphone for recording

### Step 1: Clone or Download the Project
```bash
cd ai_speaking_coach
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- **streamlit** - Web UI framework
- **openai-whisper** - Speech-to-text conversion
- **pyaudio** - Microphone input
- **numpy, scipy, librosa** - Audio processing
- And other supporting libraries

### Step 4: Download Whisper Model (First Run)
When you first run the app, Whisper will automatically download its model (~140MB for 'base' model).

## 🚀 Usage

### Running the Application
```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

### Workflow

1. **Home Screen**
   - Click "Start Speaking Practice"
   - Read tips and scoring criteria

2. **Call Screen**
   - Click the microphone button to start recording
   - Speak naturally for up to 2 minutes
   - Click "End Call & Analyze" when done

3. **Processing**
   - The app transcribes and analyzes your speech
   - Shows a progress indicator

4. **Results Screen**
   - Overall score (0-10)
   - Individual scores for each criterion
   - Your strengths highlighted
   - Personalized improvement suggestions
   - Full transcript and statistics
   - Option to try again or go home

5. **Reset**
   - Click "Back to Home" to reset and try again
   - All data is automatically cleared

## 📊 Scoring System

### Overall Score
Average of all 5 criteria (0-10)

### Individual Criteria
- **8-10**: Excellent
- **6-8**: Good
- **4-6**: Fair, needs improvement
- **0-4**: Needs significant work

### Ideal Speaking Pace
- **120-150 words per minute** = 10/10
- **100-120 WPM** = 8/10
- **80-100 WPM** = 6/10
- **Below 80 WPM** = 4/10
- **Above 190 WPM** = 5/10

## 📁 Project Structure

```
ai_speaking_coach/
│
├── main.py                          # Entry point
├── config.py                        # Configuration settings
├── requirements.txt                 # Dependencies
│
├── ui/                              # User Interface
│   ├── __init__.py
│   ├── app.py                       # Main app controller & navigation
│   └── screens/
│       ├── __init__.py
│       ├── home.py                  # Home screen
│       ├── call_screen.py           # Recording screen
│       └── result_screen.py         # Results display
│
├── audio/                           # Audio Processing
│   ├── __init__.py
│   └── recorder.py                  # Microphone recording
│
├── speech/                          # Speech Processing
│   ├── __init__.py
│   └── speech_to_text.py           # Whisper transcription
│
├── ai/                              # AI Analysis
│   ├── __init__.py
│   ├── coach.py                     # Main coach controller
│   └── evaluator.py                 # Speech evaluation & scoring
│
└── README.md                        # This file
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Audio Settings
AUDIO_SAMPLE_RATE = 16000
MAX_RECORDING_SECONDS = 120

# Whisper Model (options: tiny, base, small, medium, large)
WHISPER_MODEL = "base"

# Evaluation
RATING_SCALE = 10

# Session
CLEAR_ON_RESET = True
```

## 💡 Tips for Best Results

### Recording Tips
1. **Choose a quiet environment** - Minimize background noise
2. **Speak clearly** - Enunciate each word properly
3. **Speak naturally** - Don't read or memorize
4. **Complete sentences** - Better than fragments
5. **Varied vocabulary** - Show your range of words
6. **Steady pace** - Avoid speaking too fast or slow

### Practice Tips
1. Practice daily for consistent improvement
2. Focus on the weak areas mentioned in suggestions
3. Record yourself and compare over time
4. Listen to native speakers as models
5. Read aloud to improve fluency
6. Join speaking groups for real practice
7. Watch educational videos and mimic patterns

## 🔄 Data & Privacy

- **No Storage**: All data is cleared after each session
- **No Database**: No information is saved or logged
- **Local Processing**: Audio is only stored temporarily during analysis
- **Automatic Cleanup**: Temp files are deleted after processing

## ⚙️ Advanced Setup

### Using GPU for Faster Transcription
For faster transcription on CUDA-compatible GPUs:

```python
# In config.py, set:
WHISPER_GPU = True
```

### Using Better Whisper Models
For more accurate transcription:

```python
# In config.py, change:
WHISPER_MODEL = "small"  # or "medium" for better accuracy
```

Note: Larger models require more memory and take longer to download (~1.5GB for 'medium').

## 🐛 Troubleshooting

### Issue: "No module named 'pyaudio'"
**Solution**: Install PyAudio separately
```bash
pip install pipwin
pipwin install pyaudio
```

### Issue: Microphone not detected
**Solution**: 
- Check system microphone permissions
- Try using the file upload option in call screen
- Restart the application

### Issue: Slow transcription
**Solution**: Use a smaller Whisper model
```python
WHISPER_MODEL = "tiny"  # Fastest but less accurate
```

### Issue: Out of memory with large models
**Solution**: Use smaller model or increase system RAM
```python
WHISPER_MODEL = "base"  # Default, balanced
```

### Issue: Audio quality is poor
**Solution**:
- Use a better microphone
- Record in a quieter environment
- Check microphone input levels

## 📈 Performance Metrics

Typical performance on standard hardware:

| Task | Time |
|------|------|
| Audio Recording | Real-time |
| Transcription (30 sec) | 10-15 seconds |
| Speech Analysis | < 1 second |
| Total Process | 15-20 seconds |

## 🚀 Future Improvements

- [ ] Multiple language support
- [ ] Accent detection
- [ ] Voice tone analysis
- [ ] Progress tracking across sessions
- [ ] Comparison with native speakers
- [ ] Advanced pronunciation feedback
- [ ] Custom speaking topics
- [ ] Leaderboard/gamification

## 📚 Resources

- [Whisper Model Docs](https://github.com/openai/whisper)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [English Speaking Tips](https://www.englishclub.com/speaking/)

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Improve documentation
- Submit pull requests

## 💬 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the configuration options
3. Check application logs for error messages

## 🎯 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
streamlit run main.py

# 3. Open browser
# Navigate to http://localhost:8501

# 4. Start practicing!
```

---

**Happy Speaking! 🗣️** Good luck with your English practice!
