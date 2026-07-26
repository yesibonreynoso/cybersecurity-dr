from __future__ import annotations

import csv
from pathlib import Path
from typing import List, Sequence

try:
    import fitz  # PyMuPDF
except Exception:  # pragma: no cover
    fitz = None


DEFAULT_DOCUMENT = Path(__file__).resolve().parent / "data" / "ciberseguridad.csv"


def load_document(path: Path | str) -> str:
    """Carga documentos CSV, Markdown o PDF como fuente de conocimiento."""
    document_path = Path(path)
    if not document_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {document_path}")

    suffix = document_path.suffix.lower()

    if suffix == ".csv":
        with document_path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            raise ValueError("El documento no contiene registros válidos")

        sections: List[str] = []
        for row in rows:
            question = (row.get("pregunta") or "").strip()
            answer = (row.get("respuesta") or "").strip()
            if question and answer:
                sections.append(f"Pregunta: {question}\nRespuesta: {answer}")
        return "\n\n".join(sections)

    if suffix in {".md", ".markdown", ".txt"}:
        return document_path.read_text(encoding="utf-8")

    if suffix == ".pdf":
        if fitz is None:
            raise RuntimeError("PyMuPDF no está instalado. Instálalo con pip install pymupdf")
        with fitz.open(document_path) as doc:
            texts = [page.get_text() for page in doc]
        return "\n\n".join(text for text in texts if text).strip()

    raise ValueError(f"Formato no soportado: {suffix}")


def chunk_text(text: str, chunk_size: int = 300) -> List[str]:
    """Divide el texto en fragmentos manejables."""
    words = text.split()
    chunks: List[str] = []
    current: List[str] = []

    for word in words:
        current.append(word)
        if len(current) >= chunk_size:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks


def retrieve_relevant_chunks(query: str, chunks: Sequence[str], top_k: int = 3) -> List[str]:
    """Selecciona los fragmentos más relevantes por coincidencia simple de palabras."""
    query_terms = {term.lower() for term in query.split() if term.isalnum()}
    scored: List[tuple[int, str]] = []

    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = sum(1 for term in query_terms if term in chunk_lower)
        if score:
            scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in scored[:top_k]]


def answer_question(question: str, knowledge_base: str) -> str:
    """Responde una pregunta utilizando el conocimiento disponible."""
    chunks = chunk_text(knowledge_base)
    relevant = retrieve_relevant_chunks(question, chunks, top_k=3)

    if not relevant:
        return "No encontré información suficiente en la base de conocimiento para responder esa pregunta."

    for chunk in relevant:
        if "Respuesta:" in chunk:
            return chunk.split("Respuesta:", 1)[1].strip()

    return relevant[0].strip()


def build_answer(question: str, document_path: Path | str) -> str:
    """Ruta útil para construir respuestas a partir de un documento."""
    knowledge = load_document(document_path)
    return answer_question(question, knowledge)
