import streamlit as st
import os
import tempfile
import json
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

st.set_page_config(page_title="MatriVaani AI", layout="wide", page_icon="📚")

@st.cache_resource
def get_asr_service():
    from app.services.asr_service import ASRService
    return ASRService()

@st.cache_resource
def get_translation_service():
    from app.services.translation_service import TranslationService
    return TranslationService()

@st.cache_resource
def get_llm_service():
    from app.services.llm_service import LLMService
    return LLMService()

@st.cache_resource
def get_offline_service():
    from app.services.offline_service import OfflineService
    return OfflineService()

if "mode" not in st.session_state:
    st.session_state.mode = "ONLINE"
if "language" not in st.session_state:
    st.session_state.language = "Santhali"

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("MATRI VAANI")
st.sidebar.subheader("Mother Tongue Learning Assistant")

st.sidebar.markdown("---")
st.session_state.mode = st.sidebar.radio("System Mode", ["ONLINE", "OFFLINE"])
st.session_state.language = st.sidebar.selectbox("Target Language", ["Santhali", "Ho", "Mundari"])

if st.session_state.language != "Santhali":
    st.sidebar.warning(f"Language resources for {st.session_state.language} not yet available.")

st.sidebar.markdown("---")
navigation = st.sidebar.radio("Navigation", [
    "HOME",
    "CLASSROOM ASSISTANT",
    "CLASSROOM VOICE MODE",
    "LESSON GENERATOR",
    "WORKSHEETS",
    "FLASHCARDS",
    "OFFLINE CONTENT",
    "SETTINGS"
])

def check_online_required():
    if st.session_state.mode == "OFFLINE":
        st.warning("This feature requires synchronization before offline use.")
        st.stop()

if navigation == "HOME":
    st.title("MATRI VAANI")
    st.subheader("AI-Powered Mother Tongue Learning Assistant")
    st.write(f"**Current language:** {st.session_state.language}")
    st.write(f"**System mode:** {st.session_state.mode}")
    
    col1, col2, col3 = st.columns(3)
    col1.info("🎤 Voice Classroom\n\nRecord/Upload audio, get translation & teaching scripts.")
    col2.info("📚 Lesson Generator\n\nGenerate NIPUN-aligned bilingual lesson plans.")
    col3.info("📝 Worksheets\n\nCreate bilingual matching & Q/A worksheets.")
    
    col4, col5, col6 = st.columns(3)
    col4.info("🃏 Flashcards\n\nVisual vocabulary building.")
    col5.info("🔊 Language Audio\n\nText-to-Speech (NOT AVAILABLE).")
    col6.info("📦 Offline Content\n\nAccess previously generated content offline.")

elif navigation == "CLASSROOM ASSISTANT":
    st.title("CLASSROOM ASSISTANT")
    st.write(f"**Target language:** [ {st.session_state.language} ]")
    
    uploaded_file = st.file_uploader("Upload Audio", type=['wav', 'flac', 'mp3'])
    
    for key in ["ca_transcript", "ca_translation", "ca_script", "ca_edited_script", "ca_latencies"]:
        if key not in st.session_state:
            st.session_state[key] = None

    if st.button("Reset Pipeline"):
        for key in ["ca_transcript", "ca_translation", "ca_script", "ca_edited_script", "ca_latencies"]:
            st.session_state[key] = None
        st.rerun()
        
    if uploaded_file is not None:
        st.audio(uploaded_file)
        
        if st.session_state.ca_transcript is None:
            if st.button("🎤 Process Audio"):
                with st.spinner("Running local ASR (Offline capable)..."):
                    try:
                        t0 = time.time()
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                            tmp.write(uploaded_file.getvalue())
                            tmp_path = tmp.name
                        asr = get_asr_service()
                        result = asr.transcribe(tmp_path)
                        transcript = result["transcript"] if isinstance(result, dict) else result
                        os.unlink(tmp_path)
                        t1 = time.time()
                        
                        st.session_state.ca_transcript = transcript
                        st.session_state.ca_latencies = {"ASR": t1 - t0}
                        st.rerun()
                    except Exception as e:
                        st.error("Unable to process this audio.")
        else:
            st.success(f"ASR Complete! ({st.session_state.ca_latencies.get('ASR', 0):.2f}s)")
            st.info(st.session_state.ca_transcript)
            
            if st.session_state.ca_translation is None:
                if st.button("Translate to Hindi"):
                    check_online_required()
                    with st.spinner("Translating..."):
                        t0 = time.time()
                        trans = get_translation_service().translate(st.session_state.ca_transcript, "santali", "hi")
                        t1 = time.time()
                        st.session_state.ca_translation = trans
                        st.session_state.ca_latencies["Translation"] = t1 - t0
                        st.rerun()
            else:
                st.success(f"Translation Complete! ({st.session_state.ca_latencies.get('Translation', 0):.2f}s)")
                st.info(st.session_state.ca_translation)
                
                if st.session_state.ca_script is None:
                    if st.button("Generate Teaching Script"):
                        check_online_required()
                        with st.spinner("Generating script..."):
                            t0 = time.time()
                            script = get_llm_service().generate_script(st.session_state.ca_translation)
                            t1 = time.time()
                            st.session_state.ca_script = script
                            st.session_state.ca_latencies["Scriptwriter"] = t1 - t0
                            st.rerun()
                else:
                    st.success(f"Script Generated! ({st.session_state.ca_latencies.get('Scriptwriter', 0):.2f}s)")
                    st.json(st.session_state.ca_script)
                    
                    if st.session_state.ca_edited_script is None:
                        if st.button("Polish Script"):
                            check_online_required()
                            with st.spinner("Polishing script..."):
                                t0 = time.time()
                                edited = get_llm_service().copy_edit(json.dumps(st.session_state.ca_script, ensure_ascii=False))
                                t1 = time.time()
                                st.session_state.ca_edited_script = edited
                                st.session_state.ca_latencies["CopyEditor"] = t1 - t0
                                
                                try:
                                    get_offline_service().save_content("script", "Audio Script", st.session_state.language, {"script": edited})
                                except Exception:
                                    pass
                                st.rerun()
                    else:
                        st.success(f"Script Polished! ({st.session_state.ca_latencies.get('CopyEditor', 0):.2f}s)")
                        st.markdown(st.session_state.ca_edited_script)
                        total_time = sum(st.session_state.ca_latencies.values())
                        st.write(f"**Total Pipeline Latency:** {total_time:.2f}s")
                        if total_time <= 3.0:
                            st.success("SUB-3-SECOND REQUIREMENT ACHIEVED!")
                        else:
                            st.warning("SUB-3-SECOND REQUIREMENT NOT YET ACHIEVED")

elif navigation == "CLASSROOM VOICE MODE":
    st.title("CLASSROOM VOICE MODE")
    st.write("Real-Time Voice Translation Prototype")
    
    st.write(f"**Target Language:** {st.session_state.language}")
    
    # Built-in Streamlit microphone input
    audio_bytes = st.audio_input("Record Audio")
    
    if audio_bytes is not None:
        with st.spinner("Processing..."):
            try:
                t_asr_start = time.time()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(audio_bytes.getvalue())
                    tmp_path = tmp.name
                
                # 1. ASR
                asr = get_asr_service()
                result = asr.transcribe(tmp_path)
                transcript = result["transcript"] if isinstance(result, dict) else result
                os.unlink(tmp_path)
                t_asr_end = time.time()
                
                st.write("**Recognized:**")
                st.info(transcript)
                st.caption(f"ASR Latency: {t_asr_end - t_asr_start:.2f}s")
                
                # 2. Translation
                if st.session_state.mode == "OFFLINE":
                    st.warning("Translation requires online synchronization.")
                else:
                    t_trans_start = time.time()
                    trans = get_translation_service().translate(transcript, "santali", "hi")
                    t_trans_end = time.time()
                    
                    st.write("**Translation (Hindi):**")
                    st.info(trans)
                    st.caption(f"Translation Latency: {t_trans_end - t_trans_start:.2f}s")
                    
                    total = (t_asr_end - t_asr_start) + (t_trans_end - t_trans_start)
                    st.write(f"**Total Latency (ASR+Translation):** {total:.2f}s")
                    if total <= 3.0:
                        st.success("SUB-3-SECOND ACHIEVED!")
                    else:
                        st.warning("SUB-3-SECOND NOT ACHIEVED")
                    
                    # 3. TTS
                    st.write("**Audio Playback:**")
                    st.warning("TTS NOT AVAILABLE (No offline model available for Santhali)")
                        
            except Exception as e:
                st.error(f"Processing failed: {e}")

elif navigation == "LESSON GENERATOR":
    st.title("LESSON GENERATOR")
    st.write("NIPUN Bharat Aligned Lesson Plans")
    
    cls = st.selectbox("Class", ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5"])
    sub = st.selectbox("Subject", ["Foundational Literacy", "Numeracy", "Environmental Studies"])
    top = st.text_input("Topic", "Animals")
    lo = st.text_input("Learning Objective (NIPUN Aligned)", "Recognize common animal names.")
    
    if st.button("GENERATE LESSON"):
        check_online_required()
        with st.spinner("Generating lesson..."):
            try:
                res = get_llm_service().generate_lesson(cls, sub, top, lo, st.session_state.language)
                st.session_state.last_lesson = res
                get_offline_service().save_content("lesson", top, st.session_state.language, res)
            except Exception as e:
                st.error("Failed to generate lesson.")
                
    if "last_lesson" in st.session_state:
        st.json(st.session_state.last_lesson)

elif navigation == "WORKSHEETS":
    st.title("BILINGUAL WORKSHEET GENERATOR")
    
    cls = st.selectbox("Class", ["Class 1", "Class 2", "Class 3"])
    top = st.text_input("Topic", "Animals")
    diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    num = st.slider("Number of Questions", 3, 10, 5)
    
    if st.button("GENERATE WORKSHEET"):
        check_online_required()
        with st.spinner("Generating worksheet..."):
            try:
                res = get_llm_service().generate_worksheet(cls, "Literacy", top, st.session_state.language, diff, num)
                st.session_state.last_worksheet = res
                get_offline_service().save_content("worksheet", top, st.session_state.language, res)
            except Exception as e:
                st.error("Failed to generate worksheet.")
                
    if "last_worksheet" in st.session_state:
        st.json(st.session_state.last_worksheet)

elif navigation == "FLASHCARDS":
    st.title("VISUAL FLASHCARDS")
    
    cls = st.selectbox("Class", ["Class 1", "Class 2"])
    top = st.text_input("Topic", "Animals")
    
    if st.button("GENERATE FLASHCARDS"):
        check_online_required()
        with st.spinner("Generating flashcards..."):
            try:
                res = get_llm_service().generate_flashcards(cls, top, st.session_state.language)
                st.session_state.last_flashcards = res
                get_offline_service().save_content("flashcard", top, st.session_state.language, res)
            except Exception as e:
                st.error("Failed to generate flashcards.")
                
    if "last_flashcards" in st.session_state:
        cards = st.session_state.last_flashcards.get("flashcards", [])
        for c in cards:
            with st.container():
                st.markdown(f"### {c.get('emoji', '')} {c.get('target_word', '')} ({c.get('hindi_word', '')})")
                st.write(f"Pronunciation: {c.get('pronunciation', '')}")
                if st.button(f"🔊 Play Audio", key=f"tts_{c.get('target_word','')}"):
                    st.warning("TTS NOT AVAILABLE")

elif navigation == "OFFLINE CONTENT":
    st.title("OFFLINE CONTENT")
    st.write("Access previously generated and synchronized content.")
    
    ctype = st.selectbox("Content Type", ["lesson", "worksheet", "flashcard", "script"])
    if st.button("LOAD CONTENT"):
        items = get_offline_service().get_content(ctype)
        if items:
            for item in items:
                with st.expander(f"{item['topic']} ({item['created_at'][:10]}) - {item['language']}"):
                    st.json(item['data'])
        else:
            st.info("No content found.")

elif navigation == "SETTINGS":
    st.title("SETTINGS")
    st.write("**ASR:** Local checkpoint-1500")
    st.write(f"**Language:** {st.session_state.language}")
    st.write("**Translation:** Groq")
    st.write("**Scriptwriter:** Groq")
    st.write("**Copy Editor:** Groq")
    st.write("**Offline Storage:** SQLite (content/matrivaani_offline.db)")

