import re
from typing import Dict, List, Tuple
from config import RATING_SCALE
import statistics


class AdvancedEvaluator:
    """
    Analyzes spoken text for fluency, clarity, grammar, vocabulary, and pace
    """
    
    def __init__(self):
        self.rating_scale = RATING_SCALE
        # Common grammar mistakes patterns
        self.grammar_patterns = {
            r'\b(is|are|was|were)\s+(\w+)\s+\1\b': 'Subject-verb repetition',
            r'\b(and|but|or)\s+\1\b': 'Conjunction repetition',
        }
    
    def analyze(self, text: str, duration_seconds: int = 0) -> Dict:
        """
        Comprehensive speech analysis
        
        Args:
            text: Transcribed text from speech
            duration_seconds: Length of the speech
        
        Returns:
            Dictionary with rating, suggestions, and detailed analysis
        """
        
        if not text or len(text.strip()) == 0:
            return self._get_empty_result()
        
        analysis = {
            "fluency_score": self._analyze_fluency(text, duration_seconds),
            "clarity_score": self._analyze_clarity(text),
            "grammar_score": self._analyze_grammar(text),
            "vocabulary_score": self._analyze_vocabulary(text),
            "pace_score": self._analyze_pace(text, duration_seconds),
            "overall_score": 0,  # Will be calculated below
        }
        
        # Calculate overall score
        scores = [
            analysis["fluency_score"],
            analysis["clarity_score"],
            analysis["grammar_score"],
            analysis["vocabulary_score"],
            analysis["pace_score"]
        ]
        analysis["overall_score"] = round(sum(scores) / len(scores), 1)
        
        # Generate suggestions based on weakest areas
        analysis["suggestions"] = self._generate_suggestions(analysis)
        analysis["strengths"] = self._identify_strengths(analysis)
        analysis["transcript"] = text
        analysis["word_count"] = len(text.split())
        analysis["sentence_count"] = len(re.split(r'[.!?]+', text))
        
        return analysis
    
    def _analyze_fluency(self, text: str, duration_seconds: int) -> float:
        """
        Evaluate fluency based on:
        - Speech rate (words per minute)
        - Sentence complexity
        - Filler words (um, uh, like)
        """
        words = text.split()
        word_count = len(words)
        
        # Estimate fluency from word count
        base_score = min(10, (word_count / 10))
        
        # Penalize filler words
        filler_words = ['um', 'uh', 'like', 'you know', 'basically', 'literally']
        filler_count = sum(text.lower().count(f) for f in filler_words)
        filler_penalty = (filler_count * 0.2)
        
        # Penalize very short responses
        if word_count < 5:
            base_score = 2
        elif word_count < 15:
            base_score = 4
        
        fluency_score = max(1, min(10, base_score - filler_penalty))
        return round(fluency_score, 1)
    
    def _analyze_clarity(self, text: str) -> float:
        """
        Evaluate clarity based on:
        - Capitalization (proper use)
        - Punctuation
        - Repetitions
        """
        words = text.split()
        if not words:
            return 1.0
        
        # Base score
        clarity_score = 8.0
        
        # Check for repetitive words
        word_freq = {}
        for word in words:
            clean_word = word.lower().strip('.,!?;:')
            word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
        
        # Penalize excessive repetition
        repetition_count = sum(1 for count in word_freq.values() if count > 3)
        clarity_score -= (repetition_count * 0.5)
        
        # Check for proper sentence structure
        sentences = re.split(r'[.!?]+', text)
        avg_sentence_length = len(words) / max(len(sentences), 1)
        
        if avg_sentence_length < 3:
            clarity_score -= 1  # Very short fragments
        elif avg_sentence_length > 25:
            clarity_score -= 0.5  # Very long run-ons
        
        return round(max(1, min(10, clarity_score)), 1)
    
    def _analyze_grammar(self, text: str) -> float:
        """
        Evaluate grammar based on:
        - Common mistakes patterns
        - Subject-verb agreement indicators
        - Tense consistency
        """
        grammar_score = 8.0
        
        # Check for common patterns
        for pattern, error_type in self.grammar_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                grammar_score -= 1
        
        # Basic subject-verb checks (simple heuristics)
        singular_subjects = ['he', 'she', 'it', 'this', 'that']
        plural_subjects = ['they', 'we', 'you', 'these', 'those']
        
        # Check for 'is' vs 'are' usage
        is_count = len(re.findall(r'\bis\b', text, re.IGNORECASE))
        are_count = len(re.findall(r'\bare\b', text, re.IGNORECASE))
        
        if is_count + are_count > 0:
            # Simple validation - may have false positives
            pass
        
        # Check for consistent tense
        past_tense = len(re.findall(r'\b(was|were|did|went|said)\b', text, re.IGNORECASE))
        present_tense = len(re.findall(r'\b(is|are|do|go|say)\b', text, re.IGNORECASE))
        
        # If speaker switches between tenses frequently, it's a sign of inconsistency
        if past_tense > 0 and present_tense > 0:
            grammar_score -= 0.5
        
        return round(max(1, min(10, grammar_score)), 1)
    
    def _analyze_vocabulary(self, text: str) -> float:
        """
        Evaluate vocabulary based on:
        - Word diversity
        - Use of complex words
        - Repetition of simple words
        """
        words = [w.lower().strip('.,!?;:') for w in text.split()]
        
        if not words:
            return 1.0
        
        # Calculate lexical diversity (type-token ratio)
        unique_words = len(set(words))
        total_words = len(words)
        
        if total_words == 0:
            return 1.0
        
        diversity_ratio = unique_words / total_words
        
        # Score based on diversity
        if diversity_ratio > 0.7:
            vocab_score = 9.0
        elif diversity_ratio > 0.5:
            vocab_score = 7.5
        elif diversity_ratio > 0.3:
            vocab_score = 5.0
        else:
            vocab_score = 3.0
        
        # Check for use of common words
        simple_words = {'the', 'a', 'is', 'and', 'to', 'of', 'in', 'it'}
        simple_word_ratio = sum(1 for w in words if w in simple_words) / total_words
        
        if simple_word_ratio > 0.5:
            vocab_score -= 1.5  # Too many simple words
        
        return round(max(1, min(10, vocab_score)), 1)
    
    def _analyze_pace(self, text: str, duration_seconds: int) -> float:
        """
        Evaluate pace based on:
        - Words per minute
        - Speech rate (typically 120-150 WPM is ideal)
        """
        words = len(text.split())
        
        if duration_seconds == 0:
            # Estimate based on typical speaking pace
            estimated_duration = words / 2.5  # ~150 WPM
            duration_seconds = estimated_duration
        
        if duration_seconds == 0:
            return 5.0
        
        wpm = (words / duration_seconds) * 60
        
        # Ideal pace is 120-150 WPM
        if 120 <= wpm <= 150:
            pace_score = 10.0
        elif 100 <= wpm < 120 or 150 < wpm <= 170:
            pace_score = 8.0
        elif 80 <= wpm < 100 or 170 < wpm <= 190:
            pace_score = 6.0
        elif wpm < 80:
            pace_score = 4.0  # Too slow
        else:
            pace_score = 5.0  # Too fast
        
        return round(pace_score, 1)
    
    def _generate_suggestions(self, analysis: Dict) -> List[str]:
        """Generate improvement suggestions based on analysis"""
        suggestions = []
        
        # Sort by weakest areas
        scores = {
            'fluency': analysis['fluency_score'],
            'clarity': analysis['clarity_score'],
            'grammar': analysis['grammar_score'],
            'vocabulary': analysis['vocabulary_score'],
            'pace': analysis['pace_score'],
        }
        
        sorted_scores = sorted(scores.items(), key=lambda x: x[1])
        
        suggestion_map = {
            'fluency': [
                "Practice longer passages to improve fluency.",
                "Try to minimize filler words like 'um' and 'like'.",
                "Record yourself and listen for areas to improve.",
            ],
            'clarity': [
                "Avoid repeating the same words too frequently.",
                "Break up long sentences for better clarity.",
                "Speak with clear enunciation of each word.",
            ],
            'grammar': [
                "Review subject-verb agreement in your sentences.",
                "Maintain consistent verb tense throughout.",
                "Use correct article usage (a/an/the).",
            ],
            'vocabulary': [
                "Expand your vocabulary by reading more.",
                "Use synonyms to avoid word repetition.",
                "Practice using more varied and descriptive words.",
            ],
            'pace': [
                "Slow down slightly to ensure clarity.",
                "Speed up to maintain listener engagement.",
                "Practice speaking at a consistent pace.",
            ],
        }
        
        # Add suggestions for 3 weakest areas
        for category, _ in sorted_scores[:3]:
            tips = suggestion_map[category]
            suggestions.append(tips[0])
        
        return suggestions
    
    def _identify_strengths(self, analysis: Dict) -> List[str]:
        """Identify and highlight speaker's strengths"""
        strengths = []
        
        if analysis['vocabulary_score'] >= 8:
            strengths.append("✨ Excellent vocabulary diversity!")
        if analysis['clarity_score'] >= 8:
            strengths.append("✨ Clear and well-structured speech!")
        if analysis['grammar_score'] >= 9:
            strengths.append("✨ Excellent grammar and syntax!")
        if analysis['fluency_score'] >= 8:
            strengths.append("✨ Smooth and fluent delivery!")
        if analysis['pace_score'] >= 8:
            strengths.append("✨ Great speaking pace!")
        
        return strengths if strengths else ["Keep practicing to develop your speaking skills!"]
    
    def _get_empty_result(self) -> Dict:
        """Return empty analysis result"""
        return {
            "overall_score": 0,
            "fluency_score": 0,
            "clarity_score": 0,
            "grammar_score": 0,
            "vocabulary_score": 0,
            "pace_score": 0,
            "suggestions": ["Please record some speech to get analysis."],
            "strengths": [],
            "transcript": "",
            "word_count": 0,
            "sentence_count": 0,
        }


# Keep backward compatibility
class Evaluator(AdvancedEvaluator):
    """Backward compatible wrapper"""
    pass
