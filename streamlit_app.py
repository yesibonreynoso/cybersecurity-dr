from html import escape
import logging
from pathlib import Path
from typing import List

import streamlit as st

from herramientas import (
    build_answer_with_sources,
    discover_local_documents,
    format_chat_message,
    resolve_selected_sources,
    sanitize_question,
)

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Cybersecurity DR Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    *, *::before, *::after { box-sizing: border-box; }
    .stApp {
        background: linear-gradient(160deg, #060b13 0%, #0d1424 40%, #111827 100%);
        min-height: 100vh;
    }
    .block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1200px; }
    [data-testid="stSidebar"] { background: rgba(13, 20, 36, 0.95); }
    .stTextInput > div > div > input {
        border-radius: 14px;
        border: 1px solid rgba(79, 124, 255, 0.40);
        background: rgba(255,255,255,0.05);
        color: #e8ecf4;
        padding: 12px 16px;
        font-size: 0.95rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.20);
        transition: border-color 0.25s, box-shadow 0.25s;
    }
    .stTextInput > div > div > input:focus {
        border-color: rgba(79, 124, 255, 0.75);
        box-shadow: 0 0 0 3px rgba(79,124,255,0.15);
    }
    .stTextInput > label { color: #9fb7de; font-size: 0.85rem; }
    div[data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.04);
        border-radius: 14px;
        padding: 10px;
        border: 1px solid rgba(255,255,255,0.07);
    }
    .chat-shell {
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 18px;
        background: rgba(8, 13, 24, 0.70);
        box-shadow: 0 20px 50px rgba(0,0,0,0.30);
        backdrop-filter: blur(10px);
        margin-top: 12px;
        min-height: 400px;
    }
    .chat-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 4px 4px 14px 4px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 12px;
    }
    .chat-avatar {
        width: 44px; height: 44px; border-radius: 50%;
        background: linear-gradient(135deg, #4f7cff, #7c61ff, #a855f7);
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; font-size: 1.1rem; color: #fff;
        box-shadow: 0 4px 16px rgba(79,124,255,0.35);
    }
    .chat-bubble-user {
        background: linear-gradient(135deg, #4f7cff, #6c5ce7);
        color: #fff; padding: 11px 16px; border-radius: 18px 18px 4px 18px;
        margin: 10px 0 10px auto; max-width: 78%;
        box-shadow: 0 6px 20px rgba(79,124,255,0.20);
        font-size: 0.94rem; line-height: 1.55;
    }
    .chat-bubble-assistant {
        background: rgba(255,255,255,0.06);
        color: #e8ecf4; padding: 11px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 10px 0; max-width: 78%;
        border: 1px solid rgba(255,255,255,0.06);
        font-size: 0.94rem; line-height: 1.55;
    }
    .chat-empty {
        background: linear-gradient(135deg, rgba(79,124,255,0.12), rgba(255,255,255,0.03));
        color: #c4d4f0; padding: 16px 18px; border-radius: 16px;
        margin-bottom: 10px; border: 1px solid rgba(79,124,255,0.18);
        font-size: 0.92rem;
    }
    .pill {
        display: inline-block;
        background: rgba(79,124,255,0.14);
        color: #b8caf8;
        border: 1px solid rgba(79,124,255,0.28);
        padding: 5px 14px; border-radius: 999px;
        font-size: 0.88rem; font-weight: 500;
    }
    .source-tag {
        display: inline-block;
        background: rgba(79,124,255,0.10);
        color: #8ea6d8;
        border: 1px solid rgba(79,124,255,0.18);
        padding: 2px 8px; border-radius: 6px;
        font-size: 0.75rem; margin-top: 6px;
    }
    .follow-up-btn {
        background: rgba(79,124,255,0.12);
        color: #c4d6f5;
        border: 1px solid rgba(79,124,255,0.25);
        padding: 8px 16px; border-radius: 10px;
        font-size: 0.84rem; cursor: pointer;
        transition: all 0.2s; margin: 4px 4px 4px 0;
    }
    .follow-up-btn:hover {
        background: rgba(79,124,255,0.25);
        border-color: rgba(79,124,255,0.50);
        color: #fff;
    }
    .stButton > button {
        border-radius: 12px; font-weight: 600;
        background: linear-gradient(135deg, #4f7cff, #6c5ce7);
        color: #fff; border: none; padding: 8px 20px;
    }
    .stButton > button:hover { opacity: 0.92; }
    .stMarkdown h1 { color: #e8ecf4; font-size: 1.8rem; }
    .stMarkdown h2 { color: #c4d6f5; }
    .streaming-cursor { display: inline-block; width: 8px; height: 14px; background: #7c61ff; margin-left: 2px; border-radius: 2px; animation: blink 0.8s infinite; }
    @keyframes blink { 0%,100% { opacity:1; } 50% { opacity:0; } }
    .source-link { color: #7c9aff; text-decoration: underline; font-size: 0.82rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "sources" not in st.session_state:
    st.session_state.sources = []
if "active_sources" not in st.session_state:
    st.session_state.active_sources = []
if "typing" not in st.session_state:
    st.session_state.typing = False

base_sources = discover_local_documents()
if base_sources and not st.session_state.sources:
    st.session_state.sources = base_sources
if not st.session_state.active_sources and base_sources:
    st.session_state.active_sources = base_sources

st.markdown("<span class='pill'>🛡️ Asistente documental inteligente</span>", unsafe_allow_html=True)
st.title("Cybersecurity DR Assistant")
st.caption("Haz preguntas sobre tus documentos de ciberseguridad. Respuestas fundamentadas en tus fuentes.")

with st.sidebar:
    st.markdown("### 📂 Configuración de fuentes")
    st.caption("Formatos compatibles: PDF, Markdown, TXT, CSV")

    uploaded_files = st.file_uploader(
        "Sube documentos adicionales",
        type=["csv", "md", "markdown", "txt", "pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        help="Los archivos se guardan temporalmente en la sesión.",
    )

    if uploaded_files:
        new_added = False
        for uploaded_file in uploaded_files:
            name = uploaded_file.name
            try:
                from herramientas import validate_uploaded_filename
                safe_name = validate_uploaded_filename(name)
            except ValueError as exc:
                st.error(f"Archivo rechazado: {exc}")
                continue
            temp_path = Path("data") / safe_name
            temp_path.parent.mkdir(exist_ok=True)
            temp_path.write_bytes(uploaded_file.getvalue())
            if temp_path not in st.session_state.sources:
                st.session_state.sources.append(temp_path)
                new_added = True
        if new_added:
            st.success("Documentos cargados correctamente")

    if st.session_state.sources:
        label_names = [p.name for p in st.session_state.sources]
        selected = st.multiselect(
            "Fuentes activas",
            label_names,
            default=[p.name for p in st.session_state.active_sources],
            help="Selecciona las fuentes que deseas consultar.",
        )
        st.session_state.active_sources = resolve_selected_sources(selected, st.session_state.sources)

    st.markdown("---")
    st.markdown("### 📋 Preguntas sugeridas")
    suggested = [
        "¿Qué es el phishing?",
        "¿Cómo protegerme de un ransomware?",
        "¿Qué es la autenticación multifactor?",
        "¿Qué hacer si detecto un ataque?",
        "¿Qué servicios ofrece Cybersecurity DR?",
        "¿Cómo solicitar un presupuesto?",
    ]
    for q in suggested:
        if st.button(q, key=f"sug_{q[:20]}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": q})
            st.session_state.typing = True
            st.rerun()

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🗑️ Limpiar historial", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col_b:
        if st.session_state.messages:
            st.download_button(
                "📥 Exportar chat",
                data="\n".join(
                    f"[{m['role'].upper()}] {m['content']}" for m in st.session_state.messages
                ),
                file_name="conversacion_chat.txt",
                mime="text/plain",
                use_container_width=True,
            )

st.markdown("<div class='chat-shell'>", unsafe_allow_html=True)
st.markdown(
    "<div class='chat-header'><div class='chat-avatar'>DR</div><div><strong>Cybersecurity DR</strong><br><span style='color:#9fb7de'>Asistente documental</span></div></div>",
    unsafe_allow_html=True,
)

if not st.session_state.messages:
    st.markdown(
        "<div class='chat-empty'>👋 ¡Hola! Soy el asistente de ciberseguridad de Cybersecurity DR. "
        "Hazme una pregunta sobre nuestras políticas, servicios o documentos de seguridad.</div>",
        unsafe_allow_html=True,
    )

for message in st.session_state.messages:
    bubble_class = "chat-bubble-user" if message["role"] == "user" else "chat-bubble-assistant"
    if message["role"] == "assistant":
        rendered = format_chat_message(message["content"])
        source_info = message.get("sources", [])
        if source_info:
            source_names = ", ".join(s.name for s in source_info)
            rendered += f'<div class="source-tag">📄 Fuentes: {escape(source_names)}</div>'
        st.markdown(f"<div class='{bubble_class}'>{rendered}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='{bubble_class}'>{escape(message['content'])}</div>", unsafe_allow_html=True)

if st.session_state.typing:
    st.markdown(
        '<div class="chat-bubble-assistant"><span class="streaming-cursor"></span> Analizando documentos…</div>',
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

question = st.chat_input("Escribe tu pregunta aquí…")

if question and question.strip():
    question_text = sanitize_question(question.strip())
    if not question_text:
        st.warning("Por favor, introduce una pregunta válida.")
    else:
        st.session_state.messages.append({"role": "user", "content": question_text})
        st.session_state.typing = True
        st.rerun()

if st.session_state.typing and st.session_state.messages:
    last_user_msg = None
    for msg in reversed(st.session_state.messages):
        if msg["role"] == "user":
            last_user_msg = msg
            break
    if last_user_msg:
        try:
            combined_answer, used_sources = build_answer_with_sources(
                last_user_msg["content"], st.session_state.active_sources
            )
        except Exception as exc:
            logger.warning("Error generando respuesta: %s", exc)
            combined_answer = "Error al procesar las fuentes. Inténtalo de nuevo."
            used_sources = st.session_state.active_sources

        if not combined_answer or combined_answer.startswith("No se pudo"):
            combined_answer = "No pude encontrar una respuesta en las fuentes activas. Intenta con otra pregunta."

        knowledge_sources = [
            s for s in used_sources
            if s.parent.name in {"docs", "data", "knowledge"} or s.name == "README.md"
        ]
        if not knowledge_sources:
            knowledge_sources = used_sources
        st.session_state.messages.append({
            "role": "assistant",
            "content": combined_answer,
            "sources": knowledge_sources,
        })
        st.session_state.typing = False
        st.rerun()