import streamlit as st
import google.generativeai as genai
import pypandoc
import os
from PIL import Image

st.set_page_config(page_title="Img to Word Math", page_icon="📐")

st.title("📸 a 📝 Generador de Ecuaciones Word")
st.markdown("Sube imágenes (de Mathcad, libros, apuntes) y descarga un archivo `.docx` con las ecuaciones nativas listas para Word.")

# Sidebar para la API Key
st.sidebar.header("Configuración")
api_key = st.sidebar.text_input("Ingresa tu API Key de Gemini:", type="password")
st.sidebar.markdown("[Obtén tu API Key aquí](https://aistudio.google.com/app/apikey)")

# Subida de múltiples archivos
uploaded_files = st.file_uploader("Sube tus imágenes con ecuaciones", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if st.button("Generar Documento Word"):
    if not api_key:
        st.error("Por favor, ingresa tu API Key en el menú lateral.")
    elif not uploaded_files:
        st.warning("Sube al menos una imagen antes de continuar.")
    else:
        genai.configure(api_key=api_key)
        
        # ESTA ES LA LÍNEA CORREGIDA PARA EVITAR EL ERROR 404:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        with st.spinner("Procesando imágenes con IA y construyendo el documento..."):
            md_content = "# Ecuaciones Extraídas\n\n"
            
            for i, file in enumerate(uploaded_files):
                img = Image.open(file)
                st.image(img, caption=f"Imagen {i+1}", width=400)
                
                # Prompt estricto para obtener solo LaTeX
                prompt = "Extrae las ecuaciones matemáticas de esta imagen. Devuelve ÚNICAMENTE el código LaTeX de la ecuación, encerrado entre doble signo de dólar ($$ecuacion$$). No agregues texto extra, ni explicaciones, solo el bloque de la ecuación."
                
                try:
                    response = model.generate_content([prompt, img])
                    latex_code = response.text.strip()
                    md_content += f"**Ecuación de la Imagen {i+1}:**\n\n{latex_code}\n\n"
                except Exception as e:
                    st.error(f"Error interpretando la imagen {i+1}: {e}")
            
            # Guardamos el markdown temporal
            md_filename = "temp_ecuaciones.md"
            docx_filename = "Ecuaciones_Nativas.docx"
            
            with open(md_filename, "w", encoding="utf-8") as f:
                f.write(md_content)
            
            try:
                # Pandoc es el motor que convierte el LaTeX del markdown a la ecuación nativa de Word
                pypandoc.convert_file(md_filename, 'docx', outputfile=docx_filename)
                
                with open(docx_filename, "rb") as f:
                    st.download_button(
                        label="📥 Descargar Archivo Word",
                        data=f,
                        file_name="Tus_Ecuaciones.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                st.success("¡Documento generado con éxito! Haz clic en el botón de arriba para descargarlo.")
            except Exception as e:
                st.error(f"Error en la conversión a Word. ¿Está Pandoc instalado?: {e}")
