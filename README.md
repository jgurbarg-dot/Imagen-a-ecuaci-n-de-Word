# App: Imagen a Ecuación Word
Esta aplicación en Streamlit utiliza la API de Google Gemini para leer imágenes de ecuaciones (por ejemplo, recortes de Mathcad) y Pandoc para generar un archivo `.docx` con las fórmulas matemáticas nativas de Word.

## Archivos clave:
- `app.py`: La lógica principal de la aplicación.
- `requirements.txt`: Librerías de Python requeridas (Streamlit, SDK de Gemini, PyPandoc).
- `packages.txt`: Dependencias del sistema (Pandoc). **Crucial para Streamlit Community Cloud**.
