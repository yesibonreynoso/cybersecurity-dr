import unittest
from pathlib import Path

from herramientas import chunk_text, load_document, retrieve_relevant_chunks


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


if __name__ == "__main__":
    unittest.main()
