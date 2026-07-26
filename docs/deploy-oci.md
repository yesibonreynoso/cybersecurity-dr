# Despliegue en OCI

1. Construye la imagen Docker desde la raíz del proyecto:
   ```powershell
   docker build -t agente-ciberseguridad .
   ```
2. Ejecuta la imagen localmente para comprobar que el servicio responde:
   ```powershell
   docker run -p 8501:8501 agente-ciberseguridad
   ```
3. Publica la imagen en un registro de contenedores accesible desde OCI.
4. Crea un despliegue en OCI con exposición del puerto 8501.
5. Verifica que la aplicación responda desde la URL pública asignada.

## Nota de presentación

Este proyecto está preparado para un despliegue sencillo en la nube, utilizando Docker y Streamlit como base de ejecución.
