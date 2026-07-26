# Evidencia del proyecto

## Agente funcional

- El proyecto responde preguntas usando documentos CSV, Markdown, TXT y PDF.
- La interfaz web permite cargar documentos y conversar con el agente.
- El sistema está preparado para trabajar con múltiples documentos en una misma conversación.
- Las respuestas incluyen atribución de fuentes (nombre del documento origen).
- Las preguntas del usuario son sanitizadas antes del procesamiento (longitud máxima, caracteres peligrosos).
- Las subidas de archivo validan la extensión y el nombre del archivo.

## Pruebas

### Ejecución de pruebas unitarias
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
**Resultado:** 23 pruebas OK (todas pasan).

## Prueba realizada

### Comando ejecutado:
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### Resultado verificado: 23 pruebas OK.

## Evidencia de ejecución local

### Comando para lanzar la aplicación web:
```powershell
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py --server.headless true --server.port 8502
```

### Comando con Docker:
```powershell
docker build -t agente-ciberseguridad .
docker run -p 8501:8501 agente-ciberseguridad
```

La aplicación queda disponible en la URL local del entorno Streamlit (http://localhost:8502 o http://localhost:8501 con Docker).

## Despliegue en OCI

### Preparación para OCI:
1. La aplicación incluye un `Dockerfile` optimizado basado en `python:3.12-slim`.
2. Se incluye un `HEALTHCHECK` en el Dockerfile para monitoreo de salud del contenedor.
3. Se incluye `.dockerignore` para evitar copiar archivos innecesarios en la imagen.
4. El `README.md` incluye instrucciones completas de despliegue.

### Pasos para desplegar en OCI:
1. Construir la imagen Docker: `docker build -t agente-ciberseguridad .`
2. Ejecutar localmente: `docker run -p 8501:8501 agente-ciberseguridad`
3. Publicar la imagen en un registro de contenedores (OCI Container Registry).
4. Crear un instancia de cómputo en OCI (VM.Standard.E2.1.Micro o shape flexibles).
5. Configurar el security list para exponer el puerto 8501.
6. Opcional: configurar Nginx reverse proxy con SSL/TLS.
7. Verificar que la aplicación responda desde la URL pública asignada.

## Evaluación de las 11 dimensiones del proyecto

### 🔒 Seguridad
- Validación de longitud de entrada (máx. 500 caracteres).
- Sanitización de caracteres peligrosos en preguntas.
- Validación de extensiones de archivo en subidas.
- Protección contra path traversal en rutas de archivos.
- Los documentos subidos se limitan a extensiones permitidas.
- Las rutas de archivos se validan para estar dentro del directorio del proyecto.

### 📋 Usabilidad
- Instrucciones claras en la interfaz.
- Preguntas sugeridas para guiar al usuario.
- Mensajes de error descriptivos.
- Exportación de conversación en formato de texto.

### 🎨 UX (Experiencia de Usuario)
- Interfaz tipo chat con burbujas distinguidas para usuario y asistente.
- Indicador de "Analizando documentos…" mientras se procesa.
- Atribución de fuentes en cada respuesta.
- Diseño oscuro premium con gradientes.
- Botones de acción claros (limpiar, exportar).

### 🎭 Estilo
- CSS integrado con variables consistentes.
- Paleta de colores cohesionada (azul, violeta, fondo oscuro).
- Burbujas de chat con bordes redondeados y sombras.
- Tipografía consistente y legible.

### 🏗️ Estructura
- Código separado por responsabilidad (herramientas.py = lógica, streamlit_app.py = UI).
- Funciones modulares y reutilizables.
- Documentación de funciones con docstrings.
- Estructura de carpetas organizada (data/, docs/, tests/, herramientas.py, streamlit_app.py).

### ⚡ Dinamismo
- El agente responde en tiempo real según las fuentes activas.
- Soporte para múltiples documentos simultáneos.
- Búsqueda por relevancia dinámica.
- Seguimiento de estado de sesión (Streamlit session state).

### 🚀 Modernidad
- Python 3.12 con type hints.
- Dockerfile moderno con HEALTHCHECK.
- Streamlit con diseño responsive y contemporáneo.
- Código limpio sin dependencias muertas.

### 🔄 Interactividad
- Chat en tiempo real con historial de conversación.
- Selección dinámica de fuentes activas.
- Subida interactiva de documentos adicionales.
- Preguntas sugeridas con botones clickeables.
- Botón de limpiar historial y exportar conversación.

### 📱 Responsividad
- Streamlit se adapta automáticamente al tamaño de pantalla.
- Burbujas de chat con max-width controlado.
- Sidebar colapsable para configuración de fuentes.

### 🔧 Adaptabilidad
- Soporte para múltiples formatos de archivo (.csv, .md, .txt, .pdf).
- Descubrimiento automático de documentos en carpetas de conocimiento.
- Filtro de fuentes por nombre para personalizar el conjunto de datos.
- Función `discover_local_documents` flexible para cualquier directorio base.

### 📈 Escalabilidad
- Descubrimiento automático de documentos sin configuración manual.
- Dockerfile optimizado para despliegue en contenedor.
- Arquitectura modular que permite agregar nuevas fuentes fácilmente.
- Separación entre carga de documentos y motor de respuestas permite extensibilidad.