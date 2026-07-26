# Agente de Ciberseguridad

Este proyecto implementa un agente conversacional capaz de responder preguntas sobre ciberseguridad utilizando un documento oficial de Cybersecurity DR como base principal y permitiendo además agregar documentos adicionales como contexto. La solución está preparada para ejecutarse desde consola y también como una interfaz web con Streamlit, con una experiencia visual más atractiva y organizada.

## Descripción general

El agente carga documentos de conocimiento, extrae su contenido, divide el texto en fragmentos, identifica los segmentos más relevantes para la consulta del usuario y devuelve una respuesta basada en esa información. También permite trabajar con múltiples documentos en una sola conversación.

## Arquitectura de la solución

- Documento oficial: el sistema puede usar un documento principal de Cybersecurity DR como fuente base.
- Documentos adicionales: cualquier persona puede subir archivos extra para enriquecer el contexto de las respuestas.
- Carga de documentos: el sistema acepta archivos CSV, Markdown, TXT y PDF.
- Procesamiento del texto: el contenido se divide en fragmentos pequeños para facilitar la recuperación.
- Recuperación de contexto: se comparan palabras clave de la pregunta con los fragmentos disponibles.
- Generación de respuesta: se devuelve la respuesta más relevante para la consulta del usuario.
- Interfaz web: Streamlit ofrece una experiencia conversacional, visual y fácil de usar.

## Tecnologías y herramientas

- Python 3.14
- Streamlit para la interfaz web
- PyMuPDF para lectura de PDF
- CSV, Markdown y TXT como fuentes de conocimiento
- unittest para pruebas
- Docker para despliegue portable

## Estructura del proyecto

- data/: documentos y recursos de conocimiento
- data/knowledge/docs/: documentos de referencia
- data/knowledge/text/: textos y materiales de apoyo
- data/knowledge/images/: imágenes de apoyo
- tests/: pruebas básicas del agente
- docs/: documentación adicional de despliegue

## Ejecución local

1. Activar el entorno virtual:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
2. Instalar dependencias:
   ```powershell
   python -m pip install -r requirements.txt
   ```
3. Ejecutar la versión de consola:
   ```powershell
   python app.py
   ```
4. Ejecutar la interfaz web:
   ```powershell
   streamlit run streamlit_app.py
   ```

## Ejemplos de preguntas

- ¿Qué es phishing?
- ¿Cómo puedo protegerme de un phishing?
- ¿Qué hacer si detecto un ataque de ransomware?
- ¿Qué es la autenticación multifactor?
- ¿Qué medidas tomar ante un incidente de seguridad?

## Ejemplos de respuestas generadas

- El phishing es un ataque de ingeniería social que intenta engañar a las personas para que compartan credenciales o datos sensibles.
- Verifica la URL, no hagas clic en enlaces sospechosos, activa la autenticación multifactor y reporta correos dudosos.
- La autenticación multifactor exige más de un factor para verificar la identidad del usuario.

## Uso para profesores y evaluadores

Para usar el agente con material propio, basta con colocar los archivos en las carpetas de apoyo:

- Documentos: data/knowledge/docs
- Texto: data/knowledge/text
- Imágenes: data/knowledge/images

Luego, en la interfaz se pueden subir o seleccionar esos recursos para que el agente responda preguntas sobre ellos.

## Despliegue en OCI

La aplicación está preparada para desplegarse en OCI mediante Docker o un servicio de aplicaciones web. La guía de despliegue se encuentra en docs/deploy-oci.md.

```powershell
docker build -t agente-ciberseguridad .
docker run -p 8501:8501 agente-ciberseguridad
```

## Evidencia de funcionamiento

El proyecto incluye pruebas básicas que validan la carga del documento y la recuperación de contexto.

```powershell
python -m unittest discover -s tests -v
```
