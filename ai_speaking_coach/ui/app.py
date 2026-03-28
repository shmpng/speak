import streamlit as st
from ui.screens import home, call_screen, result_screen
from ai.coach import SpeakingCoach
import time

def run_app():
    """Main app controller"""
    
    # Page configuration
    st.set_page_config(
        page_title="AI Speaking Coach",
        page_icon="🗣️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    if "screen" not in st.session_state:
        st.session_state.screen = "home"
    
    if "last_result" not in st.session_state:
        st.session_state.last_result = {}
    
    # Route to appropriate screen
    if st.session_state.screen == "home":
        home.show()
    
    elif st.session_state.screen == "call":
        call_screen.show()
    
    elif st.session_state.screen == "processing":
        show_processing_screen()
    
    elif st.session_state.screen == "result":
        result_screen.show()


def show_processing_screen():
    """Show processing screen while analyzing speech"""
    
    st.title("⏳ Analyzing Your Speech...")
    st.markdown("---")
    
    # Progress indicator
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    with progress_placeholder.container():
        progress_bar = st.progress(0)
    
    try:
        audio_path = st.session_state.get("audio_path")
        
        if not audio_path:
            st.error("❌ No audio file found. Please record your speech again.")
            if st.button("🔄 Go Back to Recording"):
                st.session_state.screen = "call"
                st.rerun()
            return
        
        # Initialize coach
        coach = SpeakingCoach()
        
        # Step 1: Transcribe
        with status_placeholder.container():
            st.info("📝 Step 1/3: Transcribing your speech...")
        progress_bar.progress(33)
        time.sleep(0.5)
        
        # Step 2: Analyze
        with status_placeholder.container():
            st.info("🔍 Step 2/3: Analyzing speech quality...")
        progress_bar.progress(66)
        
        # Process the session
        result = coach.process_session(audio_path)
        
        # Step 3: Complete
        with status_placeholder.container():
            st.info("✅ Step 3/3: Generating results...")
        progress_bar.progress(100)
        time.sleep(0.5)
        
        # Store results and navigate
        st.session_state.last_result = result
        st.session_state.screen = "result"
        
        progress_placeholder.empty()
        status_placeholder.empty()
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error during processing: {str(e)}")
        
        if st.button("🔄 Go Back to Recording"):
            st.session_state.screen = "call"
            st.rerun()


if __name__ == "__main__":
    run_app()
