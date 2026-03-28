import streamlit as st

def show():
    """Display home screen"""
    
    # Custom styling
    st.markdown("""
    <style>
    .big-title {
        font-size: 3.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size: 1.3rem;
        text-align: center;
        color: #555;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="big-title">🗣️ AI Speaking Coach</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="subtitle">Improve your English speaking skills with real-time AI feedback</div>', unsafe_allow_html=True)
    
    # Info cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📝 **Real-time Analysis**\nGet instant feedback on your speech")
    
    with col2:
        st.info("🎯 **Detailed Scoring**\nFluency, clarity, grammar & more")
    
    with col3:
        st.info("💡 **Smart Suggestions**\nPersonalized improvement tips")
    
    st.markdown("---")
    
    # Start button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Speaking Practice", use_container_width=True, key="start_call"):
            st.session_state.screen = "call"
            st.session_state.recording_started = False
            st.session_state.audio_path = None
            st.session_state.recording_time = 0
            st.rerun()
    
    st.markdown("---")
    
    # How it works section
    st.subheader("📚 How It Works")
    
    steps = [
        ("1️⃣", "Click **Start Speaking Practice**", "Begin your practice session"),
        ("2️⃣", "**Record your speech**", "Speak naturally about any topic (max 2 minutes)"),
        ("3️⃣", "**Wait for analysis**", "AI analyzes your speech instantly"),
        ("4️⃣", "**Get results**", "Receive a detailed score and improvement suggestions"),
    ]
    
    for step_num, title, desc in steps:
        col1, col2 = st.columns([0.3, 3])
        with col1:
            st.markdown(f"## {step_num}")
        with col2:
            st.markdown(f"**{title}**  \n{desc}")
    
    st.markdown("---")
    
    # Tips section
    with st.expander("💡 Tips for Better Results"):
        st.markdown("""
        - **Choose a quiet environment** - Background noise affects transcription
        - **Speak clearly** - Enunciate words properly
        - **Speak naturally** - Avoid reading, aim for conversational speech
        - **Take your time** - Don't rush, maintain a steady pace
        - **Use varied vocabulary** - Try to use diverse words and expressions
        - **Complete sentences** - Structure your thoughts in complete sentences
        """)
    
    with st.expander("❓ Scoring Criteria"):
        st.markdown("""
        - **Fluency** (0-10): How smoothly and naturally you speak
        - **Clarity** (0-10): How clear and understandable your speech is
        - **Grammar** (0-10): Correct usage of grammar and syntax
        - **Vocabulary** (0-10): Variety and appropriateness of words used
        - **Pace** (0-10): Speaking speed and consistency (ideal: 120-150 WPM)
        
        **Overall Score** = Average of all 5 criteria
        """)
