import pandas as pd
import re
from datetime import datetime
from docxtpl import DocxTemplate, InlineImage
import io
from docx.shared import Mm
import matplotlib.pyplot as plt
import textwrap
import streamlit as st
import json
import os
import requests
import streamlit as st
import json
import os
import re
import google.generativeai as genai
from motor_friday import ajustar_texto_largo, crear_tabla_profesional

def procesar_relato_ia(relato):
    """
    FRIDAY: Procesa el relato usando la API Key oculta en Secrets.
    """
    # Recupera la API Key de forma segura
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        return ["ERROR CONFIG", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", f"Falta API Key en Secrets: {e}"]
    
    prompt = f"""
    Analiza el siguiente relato policial y extrae la información técnica solicitada.
    REGLAS ESTRICTAS:
    1. No incluyas nombres de personas ni RUTs.
    2. Responde exclusivamente con una lista de 12 valores separados por punto y coma (;).
    3. Todo el texto debe estar en MAYÚSCULAS.

    CAMPOS A EXTRAER:
    1. TIPO DE DELITO (Ej: ROBO CON VIOLENCIA, LESIONES)
    2. TRAMO HORARIO (Ej: 14:00 - 15:00)
    3. LUGAR (Dirección o intersección)
    4. GENERO VICTIMA (MASCULINO/FEMENINO/DESCONOCIDO)
    5. RANGO ETARIO VICTIMA (ADULTO/MENOR/TERCERA EDAD)
    6. CLASE DE LUGAR (VIA PUBLICA/CENTRO DE SALUD/DOMICILIO)
    7. ESPECIE SUSTRAIDA (Si no hay, poner NO REGISTRA)
    8. PERFIL VICTIMARIO (Ej: 01 SUJETO)
    9. EDAD ESTIMADA DELINCUENTE (Ej: 20 A 25 AÑOS)
    10. COMPLEXION FISICA (Ej: DELGADA/ATLETICA)
    11. MEDIO DE DESPLAZAMIENTO (A PIE/MOTOCICLETA/VEHICULO)
    12. BREVE MODUS OPERANDI (Máximo 10 palabras)

    RELATO:
    {relato}
    """

    try:
        response = model.generate_content(prompt)
        # Limpieza de la respuesta para obtener la lista
        datos = response.text.strip().split(";")
        
        # Asegurar que siempre devuelva 12 elementos para evitar errores de desempaque
        if len(datos) < 12:
            datos += ["DESCONOCIDO"] * (12 - len(datos))
        
        # Limpieza final de espacios
        return [d.strip().upper() for d in datos[:12]]

    except Exception as e:
        # En caso de fallo, FRIDAY devuelve valores por defecto
        return ["ERROR", "00:00", "DESCONOCIDO", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "FALLO MOTOR IA"]