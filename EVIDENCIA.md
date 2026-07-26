# Evidencia del proyecto

## Agente funcional

- El proyecto responde preguntas usando documentos CSV, Markdown, TXT y PDF.
- La interfaz web permite cargar documentos y conversar con el agente.
- El sistema está preparado para trabajar con múltiples documentos en una misma conversación.

## Prueba realizada

- Comando ejecutado:
  ```powershell
  .\.venv\Scripts\python.exe -m unittest discover -s tests -v
  ```
- Resultado verificado: 3 pruebas OK.

## Evidencia de ejecución local

- Comando para lanzar la aplicación web:
  ```powershell
  .\.venv\Scripts\python.exe -m streamlit run streamlit_app.py --server.headless true --server.port 8502
  ```
- La interfaz queda disponible en la URL local del entorno Streamlit.

## Despliegue

- El proyecto está preparado para desplegarse con Docker y Streamlit.
- Comando de ejecución local:
  ```powershell
  streamlit run streamlit_app.py
  ```
- Comando de contenedor:
  ```powershell
  docker build -t agente-ciberseguridad .
  docker run -p 8501:8501 agente-ciberseguridad
  ```

## Nota para la presentación

Este proyecto demuestra un agente conversacional funcional, con soporte para documentos de conocimiento y una interfaz lista para evaluación y posterior despliegue en la nube.
