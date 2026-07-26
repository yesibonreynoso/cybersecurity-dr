# Cybersecurity DR Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.44%2B-ff4b4b)](https://streamlit.io/)
[![PyMuPDF](https://img.shields.io/badge/PyMuPDF-1.26%2B-blue)](https://pymupdf.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Agente inteligente de ciberseguridad que responde preguntas basadas en el contenido de documentos locales (CSV, Markdown, TXT, PDF). Interfaz web interactiva construida con Streamlit.

## 📖 Descripción general

Cybersecurity DR Assistant es un agente conversacional que permite consultar información de seguridad almacenada en documentos locales. El usuario puede hacer preguntas en lenguaje natural y el agente busca en las fuentes activas para generar respuestas fundamentadas. El sistema soporta múltiples formatos de documento, selección dinámica de fuentes, y ofrece historial de conversación con atribución de fuentes.

## 🏗️ Arquitectura de la solución

```
┌─────────────────────────────────────────────────────┐
│              Streamlit Web Interface                │
│  ┌──────────┐  ┌───────────┐  ┌─────────────────┐ │
│  │ Chat UI  │  │ Source    │  │ Follow-up       │ │
│  │          │  │ Manager   │  │ Suggestions     │ │
│  └────┬─────┘  └─────┬─────┘  └─────────────────┘ │
│       │               │                             │
│       ▼               ▼                             │
│  ┌──────────────────────────────────────────────┐  │
│  │            herramientas.py (Core)           │  │
│  │  ┌─────────┐ ┌──────────┐ ┌─────────────┐ │  │
│  │  │ Sanitize│ │ Chunking │ │ Relevance   │ │  │
│  │  │ Input   │ │          │ │ Scoring     │ │  │
│  │  └─────────┘ └──────────┘ └─────────────┘ │  │
│  │  ┌─────────┐ ┌──────────────┐ ┌──────────┐│  │
│  │  │Load CSV/│ │Load PDF/MD   │ │Answer    ││  │
│  │  │TXT/PDF  │ │TXT           │ │Engine    ││  │
│  │  └─────────┘ └──────────────┘ └──────────┘│  │
│  └──────────────────────────────────────────────┘  │
│       │               │                             │
│       ▼               ▼                             │
│  ┌──────────┐  ┌──────────────┐                    │
│  │ data/    │  │ docs/        │   Archivos de    │
│  │ ciberseg │  │ 01_Politica  │   conocimiento   │
│  │ .csv/.md │  │ 02_Plan_DR   │                    │
│  │          │  │ 03_FAQ       │                    │
│  └──────────┘  └──────────────┘                    │
└─────────────────────────────────────────────────────┘
```

### Flujo de trabajo

1. El usuario envía una pregunta desde la interfaz web.
2. `streamlit_app.py` recibe la pregunta y la limpia mediante `sanitize_question()`.
3. Se obtienen las fuentes activas seleccionadas (CSV, MD, PDF, TXT).
4. Cada fuente se carga con `load_document()` y se combina en un corpus de conocimiento.
5. `answer_question()` segmenta el texto en fragmentos (`chunk_text()`), los puntúa por relevancia (`retrieve_relevant_chunks()`) y genera una respuesta.
6. La respuesta se muestra con atribución de fuentes (nombre del documento origen).

## 🛠️ Tecnologías y herramientas

| Componente              | Tecnología                 |
| ----------------------- | -------------------------- |
| Interfaz web            | Streamlit 1.44+            |
| Backend                 | Python 3.10+ (stdlib)      |
| Parsing CSV             | `csv` (stdlib)             |
| Parsing PDF             | PyMuPDF (fitz)             |
| Parsing Markdown/TXT    | `pathlib` + encoding UTF-8 |
| Containerización        | Docker (python:3.12-slim)  |
| Pruebas                 | `unittest` (stdlib)        |
| Gestión de dependencias | `requirements.txt`         |

## ▶️ Instrucciones de ejecución

### Requisitos previos

- Python 3.10 o superior
- pip

### Instalación local

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Ejecución de la aplicación

```bash
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py --server.headless true --server.port 8502
```

La aplicación quedará disponible en `http://localhost:8502`.

### Ejecución con Docker

```bash
docker build -t agente-ciberseguridad .
docker run -p 8501:8501 agente-ciberseguridad
```

### Ejecución de pruebas

```bash
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## 💡 Ejemplos de preguntas y respuestas

### Preguntas frecuentes soportadas por el documento base:

**Pregunta:** ¿Qué es phishing?
**Respuesta generada:** El phishing es un ataque de ingeniería social que intenta engañar a las personas para que compartan credenciales o datos sensibles.

**Pregunta:** ¿Cómo puedo protegerme de un phishing?
**Respuesta generada:** Verifica la URL, no hagas clic en enlaces sospechosos, activa la autenticación multifactor y reporta correos dudosos.

**Pregunta:** ¿Qué hacer si detecto un ataque de ransomware?
**Respuesta generada:** Aísla el equipo de la red, desconecta el cable de red o Wi‑Fi, notifica al área de seguridad y sigue los protocolos de respuesta.

**Pregunta:** ¿Qué es la autenticación multifactor?
**Respuesta generada:** Es un mecanismo de seguridad que exige más de un factor para verificar la identidad del usuario.

**Pregunta:** ¿Qué es la seguridad de datos?
**Respuesta generada:** La seguridad de datos protege la información frente a accesos no autorizados, pérdida o alteración.

**Pregunta:** ¿Qué es Cybersecurity DR?
**Respuesta generada:** Cybersecurity DR es una empresa especializada en ciberseguridad que ofrece servicios de respuesta a incidentes, recuperación ante desastres, consultoría, auditoría, pentesting y operaciones de seguridad gestionadas.

## 📸 Evidencia de despliegue

### Despliegue en OCI

La aplicación está preparada para desplegarse en Oracle Cloud Infrastructure (OCI) mediante Docker:

1. Construir la imagen: `docker build -t agente-ciberseguridad .`
2. Ejecutar: `docker run -p 8501:8501 agente-ciberseguridad`
3. La aplicación queda disponible en el puerto 8501 del contenedor.

Para producción en OCI, se recomienda:

- Usar una instancia VM.Standard.E2.1.Micro (nivel Always Free) o un shape flexibles.
- Exponer el puerto 8501 en el security list del VCN.
- Configurar un reverse proxy (Nginx) con SSL/TLS para acceso HTTPS.

## 🔒 Seguridad

- Validación de longitud de entrada (máximo 500 caracteres por pregunta).
- Sanitización de caracteres peligrosos en preguntas del usuario.
- Validación de extensiones de archivo en subidas.
- Protección contra path traversal en rutas de archivos.
- Los documentos subidos se limitan a extensiones permitidas (.csv, .md, .txt, .pdf).

## 📚 Documentos incluidos

- `data/ciberseguridad.csv` — Preguntas y respuestas de ciberseguridad básica.
- `data/ciberseguridad.md` — Guía de seguridad de la información.
- `docs/01_Politica_Seguridad_CybersecurityDR.md` — Política de seguridad de la información.
- `docs/02_Plan_Incidentes_DR_CybersecurityDR.md` — Plan de respuesta a incidentes y DR.
- `docs/03_FAQ_Servicios_CybersecurityDR.md` — FAQ y catálogo de servicios.
- `docs/04_Inventario_Activos_CybersecurityDR.csv` — Inventario de activos de TI.
- `docs/05_Controles_Seguridad_CybersecurityDR.csv` — Controles de seguridad NIST.
- `data/knowledge/` — Carpeta de conocimiento con documentos de referencia.

## 👤 Autor

Proyecto desarrollado para el Challenge Alura Agente — Cybersecurity DR.
