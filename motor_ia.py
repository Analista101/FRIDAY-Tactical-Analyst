import streamlit as st
import google.generativeai as genai
import re

def procesar_relato_ia(relato):
    """
    FRIDAY: Procesa el relato usando la API Key oculta en Secrets.
    """
    try:
        # Recupera la API Key de forma segura desde el panel de Streamlit
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        return ["ERROR CONFIG", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", f"Falta API Key: {e}"]
    
    prompt = f"""
    Analiza el siguiente relato policial y extrae la información técnica solicitada.
    REGLAS ESTRICTAS:
    1. No incluyas nombres de personas ni RUTs.
    2. Responde exclusivamente con una lista de 12 valores separados por punto y coma (;).
    3. Todo el texto debe estar en MAYÚSCULAS.

    CAMPOS A EXTRAER:
    1. TIPO DE DELITO; 2. TRAMO HORARIO; 3. LUGAR; 4. GENERO VICTIMA; 5. RANGO ETARIO; 
    6. CLASE DE LUGAR; 7. ESPECIE; 8. PERFIL VICTIMARIO; 9. EDAD DELINCUENTE; 
    10. COMPLEXION; 11. MEDIO DE DESPLAZAMIENTO; 12. BREVE MODUS OPERANDI.

    RELATO:
    {relato}
    """

    try:
        response = model.generate_content(prompt)
        datos = response.text.strip().split(";")
        
        # Relleno de seguridad para evitar errores de desempaque en la tabla
        if len(datos) < 12:
            datos += ["DESCONOCIDO"] * (12 - len(datos))
        
        return [d.strip().upper() for d in datos[:12]]

    except Exception as e:
        return ["ERROR", "00:00", "DESCONOCIDO", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "FALLO MOTOR IA"]