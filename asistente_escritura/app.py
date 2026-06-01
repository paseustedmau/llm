import streamlit as st
import google.generativeai as genai
import os

# Configuración básica de la página
st.set_page_config(page_title="Asistente de Escritura", page_icon="✍️", layout="centered")

st.title("✍️ Asistente de Escritura Automática")
st.write("¡Hola! Soy tu asistente de escritura. Puedo ayudarte a sugerir oraciones, corregir tu gramática, mejorar tu estilo o incluso redactar textos completos.")

# Configurar API Key
api_key = st.text_input("Ingresa tu Google Gemini API Key para empezar:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # Seleccionar la tarea
    tarea = st.selectbox(
        "¿En qué te puedo ayudar hoy?",
        ("Mejorar redacción y ortografía", "Sugerir continuación", "Escribir un texto desde cero")
    )
    
    # Opciones dependiendo de la tarea
    if tarea == "Mejorar redacción y ortografía":
        texto_usuario = st.text_area("Pega aquí tu texto:", height=150)
        if st.button("Mejorar texto"):
            if texto_usuario:
                with st.spinner("Revisando tu texto..."):
                    try:
                        model = genai.GenerativeModel('gemini-1.5-pro')
                        prompt = f"Corrige la ortografía y mejora la redacción y estilo del siguiente texto. Devuelve solo el texto corregido:\n\n{texto_usuario}"
                        response = model.generate_content(prompt)
                        st.subheader("Texto Mejorado:")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Por favor, ingresa un texto para mejorar.")
                
    elif tarea == "Sugerir continuación":
        texto_usuario = st.text_area("Escribe el inicio de tu texto aquí:", height=150)
        if st.button("Sugerir continuación"):
            if texto_usuario:
                with st.spinner("Pensando en ideas..."):
                    try:
                        model = genai.GenerativeModel('gemini-1.5-pro')
                        prompt = f"Continúa escribiendo el siguiente texto de forma coherente y creativa (agrega un párrafo más):\n\n{texto_usuario}"
                        response = model.generate_content(prompt)
                        st.subheader("Sugerencia:")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Por favor, ingresa el inicio de tu texto.")
                
    elif tarea == "Escribir un texto desde cero":
        tema = st.text_input("¿Sobre qué tema quieres escribir? (Ej. Un correo pidiendo vacaciones, un artículo sobre IA, etc.)")
        tono = st.selectbox("Elige el tono del texto:", ("Profesional", "Casual", "Creativo", "Persuasivo"))
        
        if st.button("Generar texto"):
            if tema:
                with st.spinner("Escribiendo..."):
                    try:
                        model = genai.GenerativeModel('gemini-1.5-pro')
                        prompt = f"Escribe un texto sobre: '{tema}'. El tono del texto debe ser {tono.lower()}."
                        response = model.generate_content(prompt)
                        st.subheader("Texto Generado:")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Por favor, ingresa un tema.")
else:
    st.info("Para usar el asistente, necesitas una API Key de Google Gemini. Puedes obtenerla en Google AI Studio.")
