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
from motor_ia import procesar_relato_ia
from motor_friday import ajustar_texto_largo, crear_tabla_profesional

def render_pestana_situacion():
    st.markdown('<div class="section-header">📋 GENERADOR DE CARTA DE SITUACIÓN</div>', unsafe_allow_html=True)
    
    # Manejo de estado para el botón borrar
    if 'key_relato' not in st.session_state:
        st.session_state.key_relato = 0

    relato_in = st.text_area(
        "PEGUE EL PARTE POLICIAL AQUÍ:", 
        height=250, 
        key=f"relato_area_{st.session_state.key_relato}"
    )
    
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        enviar = st.button("⚡ GENERAR ANÁLISIS TÁCTICO")
    with col_btn2:
        if st.button("🗑️ BORRAR RELATO"):
            st.session_state.key_relato += 1
            st.rerun()

    if enviar and relato_in:
        with st.status("🤖 FRIDAY: Analizando naturaleza del procedimiento...", expanded=False):
            # Asumimos que procesar_relato_ia está definida en su motor
            try:
                from motor_ia import procesar_relato_ia
                resultado = procesar_relato_ia(relato_in)
            except ImportError:
                st.error("Error: No se encontró la función procesar_relato_ia")
                return

            # Sincronización de campos (Manejo de tuplas)
            if len(resultado) >= 12:
                tip, tr, loc, gv, ev, tl_clase, esp, gd, ed, cd, md_ia, mo_ia = resultado[:12]
            else:
                datos_relleno = resultado + (None,) * (12 - len(resultado))
                tip, tr, loc, gv, ev, tl_clase, esp, gd, ed, cd, md_ia, mo_ia = datos_relleno

            texto_analisis = relato_in.upper()
            
            # 1. DETECCIÓN DE DELITO (Protocolo Lesiones)
            es_lesion = any(x in texto_analisis for x in ["LESION", "GOLPE", "AGRESION", "RIÑA", "PUÑO", "PATADA"])
            
            # 2. SINCRONIZACIÓN DE MEDIO DE DESPLAZAMIENTO
            md_final = "MOTOCICLETA" if "MOTO" in texto_analisis else "A PIE"
            sujeto_v = f"UN SUJETO EN MOTOCICLETA" if md_final == "MOTOCICLETA" else "UN SUJETO"

            # 3. CONSTRUCCIÓN DEL RESUMEN TÁCTICO
            if es_lesion:
                accion_v = "PROPINA GOLPES A LA VÍCTIMA" if "GOLPE" in texto_analisis else "AGREDE FÍSICAMENTE A LA VÍCTIMA"
                resumen_final = f"VICTIMA SE ENCONTRABA EN LA VIA PUBLICA, MOMENTOS EN QUE ES ABORDADA POR {sujeto_v}, QUIEN SIN PROVOCACION PREVIA {accion_v}, RESULTANDO ESTA CON LESIONES DE DIVERSA CONSIDERACION, PARA LUEGO DARSE A LA FUGA."
                especie_display = "NO REGISTRA (PROCEDIMIENTO POR LESIONES)"
            else:
                transporte_v = "A PIE"
                if "BUS" in texto_analisis or "MICRO" in texto_analisis: transporte_v = "EN TRANSPORTE PUBLICO"
                elif "VEHICULO" in texto_analisis: transporte_v = "EN SU VEHICULO"
                
                accion_v = "LE ARREBATA" if "ARREBATA" in texto_analisis else "SUSTRAE"
                especie_v = str(esp).upper() if esp else "ESPECIES"
                resumen_final = f"VICTIMA TRANSITABA {transporte_v} POR LA VIA PUBLICA, MOMENTOS EN QUE ES ABORDADA POR {sujeto_v}, QUIEN {accion_v} {especie_v}, DÁNDOSE POSTERIORMENTE A LA FUGA."
                especie_display = esp if esp else "SIN ESPECIFICAR"

            # 4. LIMPIEZA DE PRIVACIDAD (PII)
            nombres_p = r'(YESSENIA|DEL CARMEN|GARCIA|ARO|JENIPHER|SABANDO|TOLEDO|MARIVOR|DOMICILIADA|IDENTIDAD|CEDULA)'
            resumen_final = re.sub(nombres_p, 'VICTIMA', resumen_final)
            resumen_final = re.sub(r'\d{1,2}\.\d{3}\.\d{3}-[\dKk]', '', resumen_final)

            # 5. LÓGICA DE LUGAR (Prioridad lugar de ocurrencia)
            if any(h in texto_analisis for h in ["HOSPITAL", "CLINICA", "POSTA"]):
                tl_final = "CENTRO DE SALUD"
                loc_final = str(loc).upper()
            else:
                tl_final = "VIA PUBLICA" if any(v in texto_analisis for v in ["AVENIDA", "CALLE", "TENIENTE CRUZ"]) else tl_clase
                loc_final = str(loc).upper()

        # 6. RENDERIZADO HTML/CSS
        st.markdown(f"""
        <style>
            .tabla-final {{ width: 100%; border-collapse: collapse; font-family: 'Arial', sans-serif; color: black; border: 1px solid #333; }}
            .tabla-final td {{ border: 1px solid #333; padding: 10px; font-size: 14px !important; vertical-align: middle; background-color: white; }}
            .encabezado-verde {{ background-color: #1E7421 !important; color: white !important; text-align: center; font-weight: bold; font-size: 15px !important; }}
            .sub-encabezado {{ background-color: #D7E4BD !important; text-align: center; font-weight: bold; font-size: 14px !important; }}
            .perfil-header {{ background-color: #EBF1DE !important; text-align: center; font-weight: bold; font-size: 14px !important; }}
            .dato-negrita {{ font-weight: bold; font-size: 14px !important; }}
            .resumen-texto {{ text-align: justify; line-height: 1.5; font-size: 13px !important; }}
        </style>

        <table class="tabla-final">
            <tr>
                <td rowspan="2" class="encabezado-verde" style="width: 35%;">{tip}</td>
                <td class="sub-encabezado" style="width: 30%;">TRAMO</td>
                <td class="sub-encabezado" style="width: 35%;">LUGAR OCURRENCIA</td>
            </tr>
            <tr>
                <td style="text-align: center; height: 50px;" class="dato-negrita">{tr}</td>
                <td style="text-align: center;" class="dato-negrita">{loc_final}</td>
            </tr>
            <tr>
                <td class="perfil-header">PERFIL VÍCTIMA</td>
                <td class="perfil-header">PERFIL DELINCUENTE</td>
                <td class="perfil-header">MODUS OPERANDI</td>
            </tr>
            <tr>
                <td style="vertical-align: top;">
                    <span class="dato-negrita">GENERO:</span> {gv}<br>
                    <span class="dato-negrita">RANGO:</span> {ev}<br>
                    <span class="dato-negrita">LUGAR:</span> <span style="color:green; font-weight:bold;">{tl_final}</span><br>
                    <span class="dato-negrita">ESPECIE:</span> {especie_display}
                </td>
                <td style="vertical-align: top;">
                    <span class="dato-negrita">VICTIMARIO:</span> {gd}<br>
                    <span class="dato-negrita">EDAD:</span> {ed}<br>
                    <span class="dato-negrita">FISICO:</span> {cd}<br>
                    <span class="dato-negrita">MED. DESPL.:</span> {md_final}
                </td>
                <td class="resumen-texto">{resumen_final}</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)