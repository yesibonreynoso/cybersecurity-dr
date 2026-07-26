from pathlib import Path

import streamlit as st

from herramientas import build_answer

st.set_page_config(page_title="Agente de Ciberseguridad", page_icon="🛡️", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(135deg, #060b13 0%, #121b2e 100%); }
    .block-container { padding-top: 1rem; }
    .stTextInput > div > div > input { border-radius: 12px; border: 1px solid #4f7cff; background: rgba(255,255,255,0.04); color: white; }
    .stButton > button { border-radius: 999px; background: linear-gradient(90deg, #4f7cff, #7b61ff); color: white; }
    div[data-testid="stFileUploader"] { background: rgba(255,255,255,0.06); border-radius: 16px; padding: 10px; }
    .chat-bubble-user { background: linear-gradient(90deg, #4f7cff, #7b61ff); color: white; padding: 12px 14px; border-radius: 16px 16px 4px 16px; margin-bottom: 8px; animation: fadeIn 0.35s ease-out; }
    .chat-bubble-assistant { background: rgba(255,255,255,0.08); color: #f3f7ff; padding: 12px 14px; border-radius: 16px 16px 16px 4px; margin-bottom: 8px; border: 1px solid rgba(255,255,255,0.08); animation: fadeIn 0.35s ease-out; }
    .chat-bubble-typing { background: rgba(255,255,255,0.06); color: #dceaff; padding: 12px 14px; border-radius: 16px; margin-bottom: 8px; font-style: italic; }
    .card { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 12px; margin-bottom: 10px; transition: transform 0.25s ease, box-shadow 0.25s ease; }
    .card:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.2); }
    .sidebar .block-container { background: rgba(255,255,255,0.04); border-radius: 18px; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(3px);} to { opacity: 1; transform: translateY(0);} }
    </style>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "sources" not in st.session_state:
    st.session_state.sources = [Path("data/ciberseguridad.csv")]
if "active_sources" not in st.session_state:
    st.session_state.active_sources = [Path("data/ciberseguridad.csv")]
if "pending_question" not in st.session_state:
    st.session_state.pending_question = ""
if "processing" not in st.session_state:
    st.session_state.processing = False

st.title("🛡️ Cybersecurity DR Assistant")
st.caption("Asistente conversacional basado en un documento oficial de Cybersecurity DR y con capacidad para incorporar documentos adicionales como contexto.")

with st.sidebar:
    st.markdown("## 📚 Resumen de recursos")
    st.markdown("- Documento oficial: base principal del conocimiento")
    st.markdown("- Documentos adicionales: aportan contexto extra para responder mejor")
    st.markdown("- Formatos soportados: CSV, Markdown, TXT y PDF")
    st.markdown("- Imágenes y texto: también pueden usarse como material de apoyo")
    st.markdown("---")
    st.markdown("### 🗂️ Estructura recomendada")
    st.code("data/knowledge/docs\ndata/knowledge/text\ndata/knowledge/images")

with st.container():
    st.markdown("<div class='card'>📄 Documento oficial</div>", unsafe_allow_html=True)
    st.caption("Este es el documento base principal del asistente.")
    uploaded_files = st.file_uploader(
        "Sube documentos de conocimiento",
        type=["csv", "md", "markdown", "txt", "pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            temp_path = Path("data") / uploaded_file.name
            temp_path.parent.mkdir(exist_ok=True)
            temp_path.write_bytes(uploaded_file.getvalue())
            if temp_path not in st.session_state.sources:
                st.session_state.sources.append(temp_path)
        st.success("Documentos cargados correctamente")

    st.markdown("<div class='card'>🧠 Contexto adicional</div>", unsafe_allow_html=True)
    st.caption("Puedes agregar documentos extra para enriquecer las respuestas.")

    st.markdown("<div class='card'>🔗 Fuentes activas</div>", unsafe_allow_html=True)
    source_labels = [path.name for path in st.session_state.sources]
    selected_sources = st.multiselect(
        "Activa las fuentes que quieras usar",
        source_labels,
        default=[path.name for path in st.session_state.active_sources],
    )
    st.session_state.active_sources = [Path("data") / name for name in selected_sources]

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'>🧑 {message['content']}</div>", unsafe_allow_html=True)
    elif message["role"] == "assistant":
        bubble_type = "chat-bubble-typing" if message["content"].startswith("✍️") else "chat-bubble-assistant"
        st.markdown(f"<div class='{bubble_type}'>🤖 {message['content']}</div>", unsafe_allow_html=True)

question = st.text_input("Escribe tu pregunta", placeholder="Ej. ¿Qué hacer si detecto un phishing?")

if st.button("Responder", use_container_width=True) and question.strip():
    st.session_state.pending_question = question.strip()
    st.session_state.messages.append({"role": "user", "content": question.strip()})
    st.session_state.messages.append({"role": "assistant", "content": "✍️ Escribiendo..."})
    st.session_state.processing = True
    st.rerun()

if st.session_state.processing and st.session_state.pending_question:
    answers = []
    for source in st.session_state.active_sources:
        if source.exists():
            answers.append(build_answer(st.session_state.pending_question, source))

    combined = "\n\n".join([answer for answer in answers if answer]).strip()
    if not combined:
        combined = "No pude encontrar una respuesta en las fuentes activas."

    if st.session_state.messages:
        st.session_state.messages[-1] = {"role": "assistant", "content": combined}
    st.session_state.pending_question = ""
    st.session_state.processing = False
    st.rerun()

if st.button("Limpiar historial", use_container_width=True):
    st.session_state.messages = []
    st.session_state.pending_question = ""
    st.session_state.processing = False
    st.rerun()
