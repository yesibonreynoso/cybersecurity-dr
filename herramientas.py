from __future__ import annotations

import csv
import re
import logging
from html import escape
from pathlib import Path
from typing import List, Sequence

try:
    import fitz  # PyMuPDF
except Exception:  # pragma: no cover
    fitz = None

logger = logging.getLogger(__name__)

MAX_INPUT_LENGTH = 500
MAX_FILENAME_LENGTH = 128
DEFAULT_DOCUMENT = Path(__file__).resolve().parent / "data" / "ciberseguridad.csv"
SUPPORTED_EXTENSIONS = {".csv", ".md", ".markdown", ".txt", ".pdf"}
ALLOWED_UPLOAD_EXTENSIONS = {".csv", ".md", ".markdown", ".txt", ".pdf"}

IGNORED_PREFIXES = ("readme", "evidencia", "ejemplo")

PROJECT_ROOT = Path(__file__).resolve().parent


def discover_local_documents(base_path: Path | str | None = None) -> List[Path]:
    """Busca documentos compatibles en las carpetas locales de conocimiento."""
    base = Path(base_path) if base_path is not None else Path(__file__).resolve().parent

    candidate_roots = [
        base,
        base / "data",
        base / "data" / "knowledge",
        base / "docs",
    ]

    discovered: List[Path] = []
    seen: set[Path] = set()

    for root in candidate_roots:
        if not root.exists() or not root.is_dir():
            continue

        folders_to_scan = [root]
        for subdir_name in ["docs", "text", "images"]:
            subdir = root / subdir_name
            if subdir.exists() and subdir.is_dir():
                folders_to_scan.append(subdir)

        for folder in folders_to_scan:
            for path in sorted(folder.iterdir()):
                if not path.is_file():
                    continue
                if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                    continue
                name_lower = path.name.lower()
                if any(name_lower.startswith(prefix) for prefix in IGNORED_PREFIXES):
                    continue
                if path not in seen:
                    discovered.append(path)
                    seen.add(path)

    return discovered


def discover_primary_sources(base_path: Path | str | None = None) -> List[Path]:
    """Prioriza los documentos de docs y el README raíz como fuentes principales."""
    base = Path(base_path) if base_path is not None else Path(__file__).resolve().parent
    sources = []
    root_readme = base / "README.md"
    if root_readme.is_file():
        sources.append(root_readme)
    for path in discover_local_documents(base):
        name_lower = path.name.lower()
        if path.is_file() and path.parent.name == "docs":
            sources.append(path)
    return sources


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
    """Selecciona los fragmentos más relevantes por coincidencia de palabras y frases clave."""
    query_terms = [term.lower() for term in re.split(r"[^a-z0-9]+", query.lower()) if term]
    scored: List[tuple[int, str]] = []

    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = 0
        for term in query_terms:
            if term in chunk_lower:
                score += 2
            if re.search(rf"\b{re.escape(term)}\b", chunk_lower):
                score += 1
        if score:
            scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in scored[:top_k]]


def answer_question(question: str, knowledge_base: str) -> str:
    """Responde una pregunta utilizando el conocimiento disponible."""
    normalized = question.strip().lower()
    if "qué es" in normalized or "que es" in normalized or "quién" in normalized or "quien" in normalized or "describe" in normalized:
        if "empresa" in normalized or "cybersecurity" in normalized:
            if "cybersecurity dr" in knowledge_base.lower() or "empresa" in knowledge_base.lower():
                return "Cybersecurity DR es una empresa especializada en ciberseguridad que ofrece servicios de respuesta a incidentes, recuperación ante desastres, consultoría, auditoría, pentesting y operaciones de seguridad gestionadas."

    chunks = chunk_text(knowledge_base)
    relevant = retrieve_relevant_chunks(question, chunks, top_k=3)

    if not relevant:
        return "No encontré información suficiente en la base de conocimiento para responder esa pregunta."

    for chunk in relevant:
        if "Respuesta:" in chunk:
            return chunk.split("Respuesta:", 1)[1].strip()

    return relevant[0].strip()


def format_chat_message(text: str) -> str:
    """Convierte texto simple en HTML básico con estilo de chat."""
    cleaned = text.replace("\r\n", "\n").strip()
    if not cleaned:
        return ""

    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    html_parts: List[str] = []
    in_list = False

    for line in lines:
        if line.startswith("- "):
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            html_parts.append(f"<li>{escape(line[2:].strip())}</li>")
        else:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            if line.startswith("**") and line.endswith("**"):
                html_parts.append(f"<strong>{escape(line[2:-2])}</strong>")
            else:
                html_parts.append(escape(line))

    if in_list:
        html_parts.append("</ul>")

    return "<br>".join(html_parts)


def resolve_selected_sources(selected_names: Sequence[str], available_sources: Sequence[Path]) -> List[Path]:
    """Convierte los nombres seleccionados en rutas reales del proyecto, validando seguridad."""
    available_by_name = {path.name: path for path in available_sources if path.name}
    resolved: List[Path] = []
    for name in selected_names:
        sanitized_name = validate_uploaded_filename(name) if "/" not in name and "\\" not in name else name
        if sanitized_name in available_by_name:
            resolved.append(available_by_name[sanitized_name])
        else:
            candidate = Path(sanitized_name)
            if candidate.exists():
                try:
                    resolved.append(validate_file_path(candidate))
                except PermissionError:
                    logger.warning("Ruta rechazada por seguridad: %s", candidate)
                    continue
            else:
                data_candidate = PROJECT_ROOT / "data" / sanitized_name
                try:
                    resolved.append(validate_file_path(data_candidate))
                except PermissionError:
                    logger.warning("Ruta rechazada por seguridad: %s", data_candidate)
                    continue
    return resolved


def build_answer(question: str, document_path: Path | str) -> str:
    """Ruta útil para construir respuestas a partir de un documento."""
    sanitized = sanitize_question(question)
    knowledge = load_document(document_path)
    return answer_question(sanitized, knowledge)


def build_answer_with_sources(question: str, source_paths: Sequence[Path]) -> tuple[str, list[Path]]:
    """Construye una respuesta combinando múltiples fuentes y devuelve las fuentes usadas."""
    sanitized = sanitize_question(question)
    combined_knowledge_parts: List[str] = []
    used_sources: List[Path] = []

    for source in source_paths:
        try:
            knowledge = load_document(source)
            combined_knowledge_parts.append(knowledge)
            used_sources.append(source)
        except Exception as exc:
            logger.warning("No se pudo cargar la fuente %s: %s", source, exc)

    if not combined_knowledge_parts:
        return "No se pudo cargar ninguna fuente de conocimiento.", used_sources

    combined_knowledge = "\n\n".join(combined_knowledge_parts)
    answer = answer_question(sanitized, combined_knowledge)
    return answer, used_sources


def sanitize_question(question: str) -> str:
    """Valida y limpia la pregunta del usuario."""
    cleaned = question.strip()
    if len(cleaned) > MAX_INPUT_LENGTH:
        cleaned = cleaned[:MAX_INPUT_LENGTH]
    cleaned = cleaned.replace("\x00", "")
    cleaned = re.sub(r"[<>&'\";\\]", "", cleaned)
    return cleaned.strip()


def validate_file_path(file_path: Path | str, base: Path | None = None) -> Path:
    """Valida que una ruta de archivo esté dentro del directorio permitido."""
    resolved_base = (base or PROJECT_ROOT).resolve()
    resolved_path = Path(file_path).resolve()
    try:
        resolved_path.relative_to(resolved_base)
    except ValueError:
        raise PermissionError(
            f"Acceso denegado: '{resolved_path}' está fuera del directorio permitido."
        )
    return resolved_path


def validate_uploaded_filename(filename: str) -> str:
    """Valida el nombre de un archivo subido por el usuario."""
    if len(filename) > MAX_FILENAME_LENGTH:
        raise ValueError(f"El nombre del archivo excede los {MAX_FILENAME_LENGTH} caracteres.")
    sanitized = re.sub(r"[^\w\.\-]", "_", filename)
    suffix = Path(sanitized).suffix.lower()
    if suffix not in ALLOWED_UPLOAD_EXTENSIONS:
        raise ValueError(f"Extensión '{suffix}' no permitida. Extensiones válidas: {', '.join(sorted(ALLOWED_UPLOAD_EXTENSIONS))}.")
    return sanitized
