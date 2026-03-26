class Evaluator:
    def analyze(self, text):
        # Mock analysis logic
        word_count = len(text.split())
        score = min(10, (word_count / 10)) # Simple logic for demo
        
        suggestions = [
            "Try to use more varied vocabulary.",
            "Watch your pace; you spoke quite quickly.",
            "Good job on clarity!"
        ]
        
        return {"score": round(score, 1), "suggestions": suggestions}