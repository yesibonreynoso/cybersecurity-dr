import tempfile
import unittest
from pathlib import Path

from herramientas import (
    answer_question,
    build_answer,
    build_answer_with_sources,
    chunk_text,
    discover_local_documents,
    discover_primary_sources,
    format_chat_message,
    load_document,
    resolve_selected_sources,
    retrieve_relevant_chunks,
    sanitize_question,
    validate_file_path,
    validate_uploaded_filename,
)


class AgentTests(unittest.TestCase):
    def test_load_document_from_csv(self):
        text = load_document(Path("data/ciberseguridad.csv"))
        self.assertIn("phishing", text.lower())

    def test_load_document_from_markdown(self):
        text = load_document(Path("data/ciberseguridad.md"))
        self.assertIn("phishing", text.lower())

    def test_retrieve_relevant_chunks(self):
        text = load_document(Path("data/ciberseguridad.csv"))
        chunks = chunk_text(text, chunk_size=250)
        ranked = retrieve_relevant_chunks("¿Qué hacer si detecto un phishing?", chunks)
        self.assertTrue(ranked)

    def test_discover_local_documents_from_knowledge_folders(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            base = Path(tmp_dir)
            docs_dir = base / "docs"
            text_dir = base / "text"
            docs_dir.mkdir(parents=True)
            text_dir.mkdir(parents=True)
            (docs_dir / "manual.md").write_text("# Manual\n\nTexto de prueba", encoding="utf-8")
            (text_dir / "notas.txt").write_text("Notas adicionales", encoding="utf-8")
            (base / "ignored.bin").write_bytes(b"no")

            discovered = discover_local_documents(base)
            self.assertEqual({path.name for path in discovered}, {"manual.md", "notas.txt"})

    def test_discover_local_documents_from_nested_data_folders(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            base = Path(tmp_dir)
            (base / "docs").mkdir(parents=True)
            (base / "data" / "knowledge" / "docs").mkdir(parents=True)
            (base / "docs" / "empresa.md").write_text("# Cybersecurity DR\n\nEmpresa de ciberseguridad", encoding="utf-8")
            (base / "data" / "knowledge" / "docs" / "guia.txt").write_text("Guía de seguridad", encoding="utf-8")

            discovered = discover_local_documents(base)
            self.assertEqual({path.name for path in discovered}, {"empresa.md", "guia.txt"})

    def test_answer_question_about_company(self):
        knowledge = "# Cybersecurity DR\n\nCybersecurity DR es una empresa especializada en ciberseguridad."
        answer = answer_question("¿Qué es esta empresa?", knowledge)
        self.assertIn("Cybersecurity DR", answer)

    def test_format_chat_message_with_markup(self):
        formatted = format_chat_message("**Respuesta breve**\n- SOC gestionado\n- Auditorías")
        self.assertIn("<strong>Respuesta breve</strong>", formatted)
        self.assertIn("<ul>", formatted)

    def test_discover_local_documents_ignores_readme_and_examples(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            base = Path(tmp_dir)
            (base / "docs").mkdir(parents=True)
            (base / "data" / "knowledge" / "docs").mkdir(parents=True)
            (base / "README.md").write_text("README del proyecto", encoding="utf-8")
            (base / "EVIDENCIA.md").write_text("Evidencia", encoding="utf-8")
            (base / "data" / "knowledge" / "docs" / "README.md").write_text("README de ejemplo", encoding="utf-8")
            (base / "data" / "knowledge" / "docs" / "ejemplo_ciberseguridad.md").write_text("Ejemplo", encoding="utf-8")
            (base / "docs" / "empresa.md").write_text("# Cybersecurity DR", encoding="utf-8")

            discovered = discover_local_documents(base)
            self.assertEqual({path.name for path in discovered}, {"empresa.md"})

    def test_discover_primary_sources_includes_root_readme(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            base = Path(tmp_dir)
            (base / "docs").mkdir(parents=True)
            (base / "README.md").write_text("README del proyecto", encoding="utf-8")
            (base / "docs" / "politica.md").write_text("Política de seguridad", encoding="utf-8")
            discovered = discover_primary_sources(base)
            names = [path.name for path in discovered]
            self.assertIn("README.md", names)
            self.assertIn("politica.md", names)

    def test_resolve_selected_sources_uses_real_paths(self):
        available_sources = [Path("data/ciberseguridad.csv"), Path("docs/01_Politica.md")]
        resolved = resolve_selected_sources(["01_Politica.md"], available_sources)
        self.assertEqual(resolved, [Path("docs/01_Politica.md")])

    def test_sanitize_question_trims_long_input(self):
        long_question = "A" * 600
        result = sanitize_question(long_question)
        self.assertLessEqual(len(result), 500)

    def test_sanitize_question_strips_html_tag_delimiters(self):
        result = sanitize_question("<script>alert('xss')</script>")
        self.assertNotIn("<", result)
        self.assertNotIn(">", result)
        self.assertNotIn(";", result)

    def test_sanitize_question_preserves_normal_text(self):
        result = sanitize_question("¿Qué es el phishing?")
        self.assertEqual(result, "¿Qué es el phishing?")

    def test_validate_uploaded_filename_accepts_valid(self):
        result = validate_uploaded_filename("mi_documento.csv")
        self.assertEqual(result, "mi_documento.csv")

    def test_validate_uploaded_filename_rejects_invalid_extension(self):
        with self.assertRaises(ValueError):
            validate_uploaded_filename("malware.exe")

    def test_validate_uploaded_filename_rejects_too_long(self):
        long_name = "a" * 130 + ".csv"
        with self.assertRaises(ValueError):
            validate_uploaded_filename(long_name)

    def test_validate_file_path_within_project(self):
        result = validate_file_path(Path("data/ciberseguridad.csv"))
        self.assertTrue(result.exists())

    def test_build_answer_returns_string(self):
        result = build_answer("¿Qué es phishing?", Path("data/ciberseguridad.csv"))
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_build_answer_with_sources_returns_tuple(self):
        sources = [Path("data/ciberseguridad.csv")]
        answer, used = build_answer_with_sources("¿Qué es phishing?", sources)
        self.assertIsInstance(answer, str)
        self.assertIsInstance(used, list)
        self.assertTrue(len(used) > 0)

    def test_answer_question_no_match_returns_first_chunk(self):
        knowledge = "Información sin relación con la consulta de phishing."
        answer = answer_question("¿Qué es la fotosíntesis?", knowledge)
        self.assertIsInstance(answer, str)
        self.assertTrue(len(answer) > 0)

    def test_chunk_text_splits_correctly(self):
        text = "word " * 400
        chunks = chunk_text(text, chunk_size=100)
        self.assertEqual(len(chunks), 4)

    def test_retrieve_relevant_chunks_returns_top_k(self):
        text = load_document(Path("data/ciberseguridad.csv"))
        chunks = chunk_text(text, chunk_size=250)
        ranked = retrieve_relevant_chunks("ransomware", chunks, top_k=2)
        self.assertLessEqual(len(ranked), 2)

    def test_discover_local_documents_skips_unsupported_extensions(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            base = Path(tmp_dir)
            (base / "imagen.png").write_bytes(b"fake image data")
            (base / "script.py").write_text("print('hola')", encoding="utf-8")
            (base / "notas.md").write_text("# Notas", encoding="utf-8")

            discovered = discover_local_documents(base)
            names = {path.name for path in discovered}
            self.assertIn("notas.md", names)
            self.assertNotIn("imagen.png", names)
            self.assertNotIn("script.py", names)


if __name__ == "__main__":
    unittest.main()