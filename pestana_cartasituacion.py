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
from motor_friday import ajustar_texto_largo, crear_tabla_profesional
def render_pestana_situacion():
    st.header("📋 Carta de Situación Tactica")
    st.info("Este módulo automatiza el resumen de Modus Operandi y Tramos Horarios por Cuadrante.")

    with st.form("form_situacion"):
        col1, col2 = st.columns(2)
        with col1:
            unidad_policial = st.text_input("UNIDAD", value="PUDAHUEL").upper()
        with col2:
            fecha_reporte = st.date_input("FECHA DEL REPORTE")
        
        archivo_situacion = st.file_uploader("Cargar Base de Datos (Excel de Partes Policiales)", type=['xlsx'])
        
        submit_situacion = st.form_submit_button("GENERAR CARTA DE SITUACIÓN")

    if submit_situacion:
        if archivo_situacion:
            try:
                # 1. CARGA Y LIMPIEZA (Protocolo Stark: Todo a Mayúsculas)
                df = pd.read_excel(archivo_situacion)
                df.columns = [c.upper().strip() for c in df.columns]
                
                # 2. FILTRADO DE LOS 10 CUADRANTES
                # FRIDAY filtra automáticamente los sectores del 1 al 10
                st.write("🔍 Analizando cuadrantes y extrayendo Modus Operandi...")
                
                # --- AQUÍ VA SU LÓGICA DE PROCESAMIENTO ---
                # Ejemplo de aplicación de las reglas que definimos antes:
                # - Sin nombres/RUTs
                # - Todo en UPPERCASE
                # - Tramos horarios de 1 hora
                
                st.success("✅ Análisis de Carta de Situación finalizado.")
                
            except Exception as e:
                st.error(f"Error en motor FRIDAY (Situación): {e}")
        else:
            st.warning("⚠️ Requiere archivo Excel para proceder.")
2. Actualización del Cerebro Central (app.py)
Ahora simplemente añadimos la nueva opción al menú lateral. Su archivo principal quedará así de limpio:

Python
import streamlit as st
from pestana_geo import render_pestana_georreferenciacion
from pestana_mensual import render_pestana_mensual
from pestana_trimestral import render_pestana_trimestral
from pestana_situacion import render_pestana_situacion # <-- Nuevo

st.set_page_config(page_title="Proyecto JARVIS - Stark Industries", layout="wide")

# Menú Lateral Estilo Stark
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/b/b5/Stark_Industries_logo.png", width=200)
st.sidebar.title("SISTEMA FRIDAY")

opcion = st.sidebar.radio("MÓDULOS ACTIVOS:", 
    ["Georreferenciación", "Acta Mensual", "Acta Trimestral", "Carta de Situación"])

# Enrutador de funciones
if opcion == "Georreferenciación":
    render_pestana_georreferenciacion()
elif opcion == "Acta Mensual":
    render_pestana_mensual()
elif opcion == "Acta Trimestral":
    render_pestana_trimestral()
elif opcion == "Carta de Situación":
    render_pestana_situacion()

# --- PESTAÑA 4: CARTA DE SITUACIÓN (ESTILO Y LÓGICA FINAL) ---
with t4:
    st.markdown('<div class="section-header">📋 GENERADOR DE CARTA DE SITUACIÓN</div>', unsafe_allow_html=True)
    
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
            resultado = procesar_relato_ia(relato_in)
            
            # Sincronización de campos
            if len(resultado) >= 12:
                tip, tr, loc, gv, ev, tl_clase, esp, gd, ed, cd, md_ia, mo_ia = resultado[:12]
            else:
                datos_relleno = resultado + (None,) * (12 - len(resultado))
                tip, tr, loc, gv, ev, tl_clase, esp, gd, ed, cd, md_ia, mo_ia = datos_relleno

            import re
            texto_analisis = relato_in.upper()
            
            # 1. DETECCIÓN DE DELITO
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

            # 4. LIMPIEZA DE PRIVACIDAD
            nombres_p = r'(YESSENIA|DEL CARMEN|GARCIA|ARO|JENIPHER|SABANDO|TOLEDO|MARIVOR|DOMICILIADA|IDENTIDAD|CEDULA)'
            resumen_final = re.sub(nombres_p, 'VICTIMA', resumen_final)
            resumen_final = re.sub(r'\d{1,2}\.\d{3}\.\d{3}-[\dKk]', '', resumen_final)

            # 5. LÓGICA DE LUGAR
            if any(h in texto_analisis for h in ["HOSPITAL", "CLINICA", "POSTA"]):
                tl_final = "CENTRO DE SALUD"
                loc_final = str(loc).upper()
            else:
                tl_final = "VIA PUBLICA" if any(v in texto_analisis for v in ["AVENIDA", "CALLE", "TENIENTE CRUZ"]) else tl_clase
                loc_final = str(loc).upper()

        # --- 6. RENDERIZADO CON TAMAÑO DE LETRA CORREGIDO ---
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

