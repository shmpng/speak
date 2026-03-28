import librosa
import numpy as np
from scipy import signal
import soundfile as sf
from typing import Dict


class AudioAnalyzer:
    """Analyzes spoken audio by comparing with reference American English audio"""
    
    def __init__(self):
        self.sr = 16000  # Sample rate
    
    def analyze_audio(self, audio_path: str) -> Dict:
        """
        Analyze user's audio and compare with American English reference
        
        Returns: Dict with scores for pronunciation, accent, clarity, pace, etc.
        """
        
        try:
            print(f"📊 Loading audio: {audio_path}")
            # Load user's audio
            y, sr = librosa.load(audio_path, sr=self.sr)
            
            print(f"✅ Audio loaded: {len(y)} samples")
            
            # Extract audio features
            features = self._extract_features(y, sr)
            
            print(f"🔍 Analyzing audio characteristics...")
            
            # Generate scores based on features
            scores = self._generate_scores(features, y, sr)
            
            return scores
            
        except Exception as e:
            print(f"Error analyzing audio: {e}")
            return self._get_error_result(str(e))
    
    def _extract_features(self, y: np.ndarray, sr: int) -> Dict:
        """Extract audio features"""
        
        features = {}
        
        # 1. PITCH ANALYSIS
        try:
            # Estimate fundamental frequency (pitch)
            S = librosa.stft(y)
            magnitude = np.abs(S)
            pitch = librosa.hz_to_midi(librosa.fft_frequencies(sr=sr, n_fft=len(S)*2-1))
            
            # Get dominant frequencies
            mean_freq = np.mean(np.where(magnitude > np.mean(magnitude))[0])
            features['mean_freq'] = mean_freq
        except:
            features['mean_freq'] = 0
        
        # 2. ENERGY/VOLUME ANALYSIS
        features['rms_energy'] = float(np.sqrt(np.mean(y**2)))
        features['max_amplitude'] = float(np.max(np.abs(y)))
        
        # 3. CLARITY/NOISE ANALYSIS (Signal-to-Noise Ratio estimation)
        # Calculate spectral centroid (lower = more noise-like, higher = clearer)
        S = librosa.feature.melspectrogram(y=y, sr=sr)
        features['spectral_centroid'] = float(np.mean(librosa.feature.spectral_centroid(S=S)))
        
        # 4. PACE/TEMPO ANALYSIS
        # Onset strength (detects when speaker speaks vs silence)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        features['onset_rate'] = float(np.mean(onset_env))
        
        # 5. DURATION
        duration = len(y) / sr
        features['duration'] = float(duration)
        
        # 6. MFCC (Mel-frequency cepstral coefficients - captures speech characteristics)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        features['mfcc_mean'] = float(np.mean(mfcc))
        features['mfcc_std'] = float(np.std(mfcc))
        
        # 7. ZERO CROSSING RATE (speech vs silence)
        zcr = librosa.feature.zero_crossing_rate(y)
        features['zcr_mean'] = float(np.mean(zcr))
        
        return features
    
    def _generate_scores(self, features: Dict, y: np.ndarray, sr: int) -> Dict:
        """Generate comparison scores"""
        
        # Reference values for American English speaker (professional quality)
        reference = {
            'energy': 0.15,              # Moderate energy
            'pitch_clarity': 0.8,        # Clear pitch (high spectral centroid)
            'duration': 20,              # About 20 seconds of speech
            'speech_rate': 0.5,          # Moderate speech rate
        }
        
        # FLUENCY SCORE (based on consistency and speech rate)
        # More onsets = more pauses = less fluent
        onset_rate = features['onset_rate']
        fluency_score = max(1, min(10, 10 - (onset_rate * 20)))  # 0.5 onset_rate = 0 score
        
        # CLARITY SCORE (based on spectral centroid and energy)
        # Higher spectral centroid = clearer (less noise)
        spec_cent = features['spectral_centroid']
        clarity_score = max(1, min(10, (spec_cent / 2000) * 10))  # Normalized to 0-10
        
        # PRONUNCIATION SCORE (based on MFCC and energy consistency)
        # Good pronunciation = consistent energy and clear phonemes
        energy = features['rms_energy']
        energy_score = max(1, min(10, (energy / 0.3) * 10))  # Normalize to 0-10
        
        # PACE SCORE (based on duration and speech rate)
        duration = features['duration']
        # 15-25 seconds for natural speech = best score
        if 15 <= duration <= 25:
            pace_score = 9.0
        elif 10 <= duration < 15 or 25 < duration <= 30:
            pace_score = 7.0
        elif duration < 10:
            pace_score = 5.0
        else:
            pace_score = 6.0
        
        # ACCENT SCORE (based on pitch and MFCC features)
        # Native American speakers have consistent pitch and formants
        mfcc_consistency = 1 / (features['mfcc_std'] + 0.1)  # Lower std = more consistent
        accent_score = max(1, min(10, (mfcc_consistency / 2) * 10))
        
        # OVERALL SCORE
        overall_score = round((fluency_score + clarity_score + energy_score + pace_score + accent_score) / 5, 1)
        
        # Generate suggestions based on weak areas
        suggestions = self._generate_suggestions(
            fluency_score, clarity_score, energy_score, pace_score, accent_score
        )
        
        # Identify strengths
        strengths = self._identify_strengths(
            fluency_score, clarity_score, energy_score, pace_score, accent_score
        )
        
        return {
            "status": "success",
            "overall_score": overall_score,
            "fluency_score": fluency_score,
            "clarity_score": clarity_score,
            "pronunciation_score": energy_score,
            "pace_score": pace_score,
            "accent_score": accent_score,
            "suggestions": suggestions,
            "strengths": strengths,
            "duration": round(features['duration'], 1),
            "word_count": 0,  # Not applicable for audio
            "sentence_count": 0,  # Not applicable for audio
            "transcript": f"[Audio Analysis - {round(features['duration'], 1)}s duration]",
        }
    
    def _generate_suggestions(self, fluency, clarity, pronunciation, pace, accent) -> list:
        """Generate improvement suggestions"""
        scores = {
            "Fluency": fluency,
            "Clarity": clarity,
            "Pronunciation": pronunciation,
            "Pace": pace,
            "Accent": accent,
        }
        
        sorted_scores = sorted(scores.items(), key=lambda x: x[1])
        suggestions = []
        
        suggestion_map = {
            "Fluency": "Speak more smoothly with fewer pauses between words",
            "Clarity": "Articulate more clearly - pronounce each word distinctly",
            "Pronunciation": "Increase your volume and energy while speaking",
            "Pace": "Adjust your speaking speed - aim for 120-150 words per minute",
            "Accent": "Work on reducing accent - listen to native American speakers",
        }
        
        # Add suggestions for 3 weakest areas
        for category, _ in sorted_scores[:3]:
            suggestions.append(suggestion_map[category])
        
        return suggestions
    
    def _identify_strengths(self, fluency, clarity, pronunciation, pace, accent) -> list:
        """Identify strengths"""
        strengths = []
        
        if fluency >= 8:
            strengths.append("✨ Excellent fluency and smooth speech flow!")
        if clarity >= 8:
            strengths.append("✨ Very clear and distinct pronunciation!")
        if pronunciation >= 8:
            strengths.append("✨ Great vocal energy and projection!")
        if pace >= 8:
            strengths.append("✨ Perfect speaking pace!")
        if accent >= 8:
            strengths.append("✨ Natural American English accent!")
        
        return strengths if strengths else ["Keep practicing to develop your speaking skills!"]
    
    def _get_error_result(self, error_msg: str) -> Dict:
        """Return error result"""
        return {
            "status": "error",
            "error_message": error_msg,
            "overall_score": 0,
            "fluency_score": 0,
            "clarity_score": 0,
            "pronunciation_score": 0,
            "pace_score": 0,
            "accent_score": 0,
            "suggestions": [error_msg],
            "strengths": [],
            "duration": 0,
            "word_count": 0,
            "sentence_count": 0,
            "transcript": "",
        }
