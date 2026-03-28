# Installation Guide - AI Speaking Coach

Complete step-by-step guide to install and run the AI Speaking Coach.

## Prerequisites

Before you start, ensure you have:
- **Computer/Laptop** with microphone
- **Internet connection** (for first-time model download)
- **~2GB free disk space** (for Whisper model)
- **Operating System**: Windows, macOS, or Linux

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Processor**: Any modern CPU (Intel, AMD, Apple Silicon)
- **Storage**: 2GB for Whisper model + application files

## Installation Steps

### 1️⃣ Install Python

#### Windows
1. Visit https://www.python.org/downloads/
2. Download Python 3.11 or higher
3. Run the installer
4. **IMPORTANT**: Check "Add Python to PATH"
5. Click "Install Now"

#### macOS
Using Homebrew (recommended):
```bash
brew install python3
```

Or download from https://www.python.org/downloads/

#### Linux
```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-pip python3-venv

# Fedora
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python
```

### 2️⃣ Verify Python Installation

Open terminal/command prompt and run:
```bash
python --version
# or
python3 --version
```

Should output: `Python 3.8.x` or higher

### 3️⃣ Download/Clone the Project

**Option A: Download ZIP**
1. Download the project ZIP file
2. Extract it to your desired location
3. Open terminal in that folder

**Option B: Clone with Git**
```bash
git clone <repository-url>
cd ai_speaking_coach
```

### 4️⃣ Create Virtual Environment

A virtual environment keeps your dependencies isolated.

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

### 5️⃣ Install Dependencies

With the virtual environment activated:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- streamlit (UI framework)
- openai-whisper (speech recognition)
- pyaudio (microphone input)
- numpy, scipy, librosa (audio processing)
- And supporting libraries

**⏱️ This may take 2-5 minutes depending on internet speed**

### 6️⃣ Verify Installation

```bash
python -c "import streamlit; import whisper; import pyaudio; print('✅ All dependencies installed!')"
```

## Running the Application

### Quick Start (Easiest)

#### Windows
Double-click: `run.bat`

#### macOS/Linux
```bash
bash run.sh
```

Or make it executable first:
```bash
chmod +x run.sh
./run.sh
```

### Manual Start

1. Activate virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

2. Run the app:
```bash
streamlit run main.py
```

3. The app opens automatically at: `http://localhost:8501`

## First Run Setup

### Initial Download
On first run, Whisper will download its model (~140MB for 'base' model):
- **tiny**: 140MB (fastest)
- **base**: 140MB (default, balanced)
- **small**: 460MB (better accuracy)
- **medium**: 1.5GB (very accurate)
- **large**: 2.9GB (best accuracy)

⏱️ First run may take 1-5 minutes for model download.

### Microphone Setup

#### Windows
1. Right-click speaker icon in taskbar
2. Click "Open Sound settings"
3. Verify microphone is selected
4. Test in Settings > Privacy & Security > Microphone

#### macOS
1. System Preferences > Sound > Input
2. Select your microphone
3. Verify "Input Volume" is not at minimum

#### Linux
```bash
# Check microphone
pactl list sources | grep "Name:"

# Test audio
arecord -d 5 test.wav
```

## Troubleshooting

### Python Not Found
```
Error: 'python' is not recognized
```
**Solution:**
1. Verify Python installed: Check in Control Panel (Windows) or `/usr/bin/python3` (Linux)
2. Add to PATH manually
3. Use `python3` instead of `python`

### PyAudio Installation Fails

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

### Microphone Not Detected
1. Check system microphone settings
2. Grant microphone permissions to terminal
3. Try different audio input in settings
4. Restart the application

### "Port 8501 already in use"
```bash
# Use different port
streamlit run main.py --server.port 8502
```

### Out of Memory
Use smaller Whisper model in `config.py`:
```python
WHISPER_MODEL = "tiny"
```

### Slow Performance
- Use `tiny` or `base` Whisper model
- Close other applications
- Increase RAM if possible
- Use GPU if available

## Next Steps

1. **Read the README**: `README.md`
2. **Start practicing**: Run the app and click "Start Speaking Practice"
3. **Review tips**: Read the built-in tips and suggestions
4. **Practice regularly**: Daily practice improves results

## Getting Help

### Check These First
1. Look at README.md for feature details
2. Review config.py for settings
3. Check TROUBLESHOOTING in README.md

### Common Issues
- **Low accuracy**: Use larger Whisper model (small/medium)
- **Slow speed**: Use smaller model (tiny/base)
- **Memory issues**: Check available RAM

## Advanced Setup

### Using GPU for Faster Processing

**NVIDIA GPU (CUDA):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**AMD GPU (ROCm):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.7
```

**Apple Silicon (Metal):**
Uses CPU by default, Metal acceleration is automatic.

### Development Setup

If you want to modify the code:
```bash
pip install -r requirements.txt
pip install pytest black flake8  # For development
```

## Uninstalling

### Complete Removal
```bash
# Deactivate virtual environment
deactivate

# Delete virtual environment
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# Delete project folder
rm -rf ai_speaking_coach  # macOS/Linux
rmdir /s ai_speaking_coach  # Windows
```

## Verification Checklist

After installation, verify everything works:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed
- [ ] Microphone detected and working
- [ ] App runs without errors
- [ ] UI loads at localhost:8501
- [ ] Can record audio
- [ ] Whisper model downloaded
- [ ] Analysis works and shows results

## Support

If you encounter issues:
1. Check this installation guide
2. Review README.md troubleshooting section
3. Check Python and pip versions
4. Verify all dependencies installed: `pip list`
5. Check system audio settings

---

**🎉 You're ready to start practicing!**

Run the app and click "Start Speaking Practice" to begin.
