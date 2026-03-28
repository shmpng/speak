import streamlit as st
import time

def show():
    """Display results screen with analysis"""
    
    st.title("📊 Speech Analysis Results")
    st.markdown("---")
    
    # Get results from session state
    result = st.session_state.get("last_result", {})
    
    if result.get("status") == "error":
        st.error(f"❌ Error: {result.get('error_message', 'Unknown error')}")
    else:
        # Overall Score - Large display
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            score = result.get("overall_score", 0)
            
            # Color coding based on score
            if score >= 8:
                score_color = "green"
                emoji = "🌟"
            elif score >= 6:
                score_color = "orange"
                emoji = "👍"
            else:
                score_color = "red"
                emoji = "💪"
            
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;">
                <h1 style="color: {score_color}; margin: 0;">{emoji} {score}/10</h1>
                <p style="font-size: 1.2rem; color: #555;">Overall Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Detailed Scores
        st.subheader("📈 Detailed Breakdown")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        metrics = [
            ("Fluency", result.get("fluency_score", 0), "🗣️"),
            ("Clarity", result.get("clarity_score", 0), "📢"),
            ("Grammar", result.get("grammar_score", 0), "📝"),
            ("Vocabulary", result.get("vocabulary_score", 0), "📚"),
            ("Pace", result.get("pace_score", 0), "⏱️"),
        ]
        
        cols = [col1, col2, col3, col4, col5]
        
        for (metric_name, score, emoji), col in zip(metrics, cols):
            with col:
                st.metric(metric_name, f"{score}/10", f"{emoji}")
        
        st.markdown("---")
        
        # Strengths
        strengths = result.get("strengths", [])
        if strengths:
            st.subheader("✨ Your Strengths")
            for strength in strengths:
                st.success(strength)
            st.markdown("")
        
        # Suggestions
        suggestions = result.get("suggestions", [])
        if suggestions:
            st.subheader("💡 Suggestions for Improvement")
            for i, suggestion in enumerate(suggestions, 1):
                st.info(f"**Tip {i}:** {suggestion}")
            st.markdown("")
        
        st.markdown("---")
        
        # Speech Statistics
        st.subheader("📊 Speech Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Word Count", result.get("word_count", 0), "words")
        
        with col2:
            st.metric("Sentence Count", result.get("sentence_count", 0), "sentences")
        
        with col3:
            if result.get("word_count", 0) > 0:
                avg_words = round(result.get("word_count", 0) / max(result.get("sentence_count", 1), 1), 1)
                st.metric("Avg Words/Sentence", avg_words, "words")
        
        st.markdown("---")
        
        # Transcript
        with st.expander("📄 Full Transcript"):
            transcript = result.get("transcript", "")
            if transcript:
                st.text(transcript)
            else:
                st.info("No transcript available")
        
        st.markdown("---")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🔁 Try Again", use_container_width=True):
                st.session_state.screen = "call"
                st.session_state.recording_started = False
                st.session_state.audio_path = None
                st.rerun()
        
        with col3:
            if st.button("🏠 Back to Home", use_container_width=True, type="primary"):
                # Clear all session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.session_state.screen = "home"
                st.rerun()
        
        st.markdown("---")
        
        # Tips for next session
        with st.expander("🚀 Tips for Your Next Session"):
            st.markdown("""
            - **Practice daily** for consistent improvement
            - **Record yourself** and compare over time
            - **Focus on weak areas** mentioned in suggestions
            - **Read aloud** to improve fluency and clarity
            - **Listen to native speakers** for pronunciation models
            - **Join speaking groups** for real conversation practice
            - **Watch videos** and try to mimic the speech patterns
            - **Stay consistent** - Small improvements add up!
            """)
