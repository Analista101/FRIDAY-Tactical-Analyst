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

import streamlit as st
from pestana_geo import render_pestana_georreferenciacion

# Configuración de la interfaz JARVIS
st.set_page_config(page_title="Proyecto JARVIS", layout="wide")

st.title("SISTEMA DE INTELIGENCIA FRIDAY")

# Selector de Pestañas en la barra lateral o superior
tabs = st.tabs(["GEORREFERENCIACIÓN", "ANÁLISIS CRIMINAL", "CONFIGURACIÓN"])

with tabs[0]:
    # Llamamos a la función del archivo externo
    render_pestana_georreferenciacion()

with tabs[1]:
    st.info("Módulo de Análisis Criminal en desarrollo...")

with tabs[2]:
    st.write("Configuraciones del sistema Stark.")


# --- ESTRUCTURA DE LA PESTAÑA INFORME GEO ---
with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO: GENERACIÓN PROFESIONAL</div>', unsafe_allow_html=True)
    
    with st.form("form_geo_final"):
        col1, col2, col3 = st.columns(3)
        # DOE y Fechas
        doe_n = col1.text_input("DOE N°", value="248812153")
        doe_fecha = col1.text_input("Fecha DOE", value="03-03-2026")
        inf_fecha = col1.text_input("Fecha Informe", value="03 de marzo de 2026")
        
        # Funcionario
        funcionario = col2.text_input("Funcionario", value="JUAN ANDRES URRUTIA LOBOS")
        grado = col2.text_input("Grado", value="SARGENTO 2°")
        unidad = col2.text_input("Unidad", value="GRUPO DE ADIESTRAMIENTO CANINO")
        
        # Ubicación
        domicilio = col3.text_input("Domicilio", value="PASAJE PILCOMAYO 8501")
        subcomisaria = col3.text_input("Subcomisaría", value="26A COMISARIA PUDAHUEL")
        cuadrante = col3.text_input("Cuadrante", value="232-A")
        
        cp1, cp2, cp3 = st.columns([2, 1, 1])
        periodo_txt = cp1.text_input("Periodo", value="03-12-2025 al 03-03-2026")
        mapa_img = cp2.file_uploader("SUBIR MAPA SAIT", type=['png', 'jpg'])
        excel_geo = cp3.file_uploader("SUBIR EXCEL/CSV", type=['xlsx', 'csv'])
        
        submit_geo = st.form_submit_button("🛡️ GENERAR INFORME GEO")

## --- FUNCIÓN DE SOPORTE (Asegúrese de que esté definida antes del bloque principal) ---
def ajustar_texto_largo(texto, ancho=35):
    """Divide el texto para evitar desbordamientos en las tablas del informe."""
    import textwrap
    if not isinstance(texto, str):
        texto = str(texto)
    return "\n".join(textwrap.wrap(texto, width=ancho))

# --- LÓGICA DE PROCESAMIENTO (Fuera del Form, dependiente del botón) ---
if submit_geo:
    if not mapa_img or not excel_geo:
        st.error("❌ Faltan archivos (Mapa o Excel) para procesar.")
    else:
        try:
            # 1. PROCESAMIENTO DE DATOS
            # Soporte para CSV y Excel con limpieza de cabeceras
            df = pd.read_csv(excel_geo) if excel_geo.name.endswith('csv') else pd.read_excel(excel_geo)
            df.columns = [c.upper().strip() for c in df.columns]
            total_casos = len(df)

            # Inicializar variables de seguridad
            resumen_dmcs = pd.DataFrame()
            dia_frec, hora_frec = "NO IDENTIFICADO", "NO IDENTIFICADO"

            if 'DELITO' in df.columns:
                df['DELITO'] = df['DELITO'].astype(str).str.upper()
                resumen_dmcs = df['DELITO'].value_counts().reset_index()
                resumen_dmcs.columns = ['TIPO DE DELITO (DMCS)', 'CANTIDAD']
                
                # Aplicación corregida de la función de ajuste (usando 'ancho')
                resumen_dmcs_tabla = resumen_dmcs.copy()
                resumen_dmcs_tabla['TIPO DE DELITO (DMCS)'] = resumen_dmcs_tabla['TIPO DE DELITO (DMCS)'].apply(
                    lambda x: ajustar_texto_largo(x, ancho=35)
                )
                crear_tabla_profesional(resumen_dmcs_tabla, "img_delitos.png", ancho_pulgadas=12)

            if 'DIA' in df.columns and 'RANGO HORA' in df.columns:
                resumen_tramos = df.groupby(['DIA', 'RANGO HORA']).size().reset_index(name='CANTIDAD')
                resumen_tramos = resumen_tramos.sort_values(by=['CANTIDAD', 'DIA'], ascending=[False, True]).head(10)
                resumen_tramos.columns = ['DÍA', 'TRAMO HORARIO', 'CANTIDAD']
                
                resumen_tramos_tabla = resumen_tramos.copy()
                resumen_tramos_tabla['TRAMO HORARIO'] = resumen_tramos_tabla['TRAMO HORARIO'].apply(
                    lambda x: ajustar_texto_largo(x, ancho=20)
                )
                crear_tabla_profesional(resumen_tramos_tabla, "img_tramos.png", ancho_pulgadas=10)
                
                dia_frec = df['DIA'].mode()[0] if not df['DIA'].empty else "N/A"
                hora_frec = df['RANGO HORA'].mode()[0] if not df['RANGO HORA'].empty else "N/A"
            
            # Variables para el análisis
            delito_principal = resumen_dmcs.iloc[0]['TIPO DE DELITO (DMCS)'] if not resumen_dmcs.empty else "DMCS"
            cantidad_real = resumen_dmcs.iloc[0]['CANTIDAD'] if not resumen_dmcs.empty else 0

            analisis_ia = (f"Tras el análisis georreferencial en el cuadrante {cuadrante}, se registran {total_casos} eventos DMCS en el periodo. "
                           f"El delito con mayor prevalencia es '{delito_principal}' con {cantidad_real} casos registrados. "
                           f"La criticidad se concentra los días {dia_frec} en el tramo {hora_frec}. "
                           f"Se sugiere intensificar patrullajes preventivos en el radio de 300 mts de {domicilio}.")

            # 2. GENERACIÓN DEL DOCUMENTO WORD
            doc = DocxTemplate("INFORME GEO.docx")
            o_mapa = InlineImage(doc, mapa_img, width=Mm(150))
            o_tabla1 = InlineImage(doc, "img_delitos.png", width=Mm(145))
            o_tabla2 = InlineImage(doc, "img_tramos.png", width=Mm(130))

            # Manejo seguro del periodo
            p_split = periodo_txt.split(" al ")
            p_inicio = p_split[0] if len(p_split) > 0 else "INICIO"
            p_fin = p_split[1] if len(p_split) > 1 else "FIN"

            contexto = {
                "domicilio": domicilio.upper(), "jurisdiccion": subcomisaria.upper(), "fecha_actual": inf_fecha.upper(),
                "doe": doe_n, "fecha_doe": doe_fecha, "grado_solic": grado.upper(),
                "solicitante": funcionario.upper(), "unidad_solic": unidad.upper(),
                "periodo_inicio": p_inicio, "periodo_fin": p_fin,
                "cuadrante": cuadrante, "mapa": o_mapa, "total_dmcs": total_casos,
                "tabla": o_tabla1, "tabla_horarios": o_tabla2,
                "dia_max": dia_frec, "hora_max": hora_frec, "conclusion_ia": analisis_ia.upper()
            }

            doc.render(contexto)
            
            # Guardado en memoria
            output = io.BytesIO()
            doc.save(output)
            output.seek(0)

            st.success("✅ Informe generado exitosamente.")
            st.download_button(
                label="📥 DESCARGAR INFORME OFICIAL",
                data=output,
                file_name=f"Informe_Geo_{cuadrante}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        except Exception as e:
            st.error(f"Error en el motor FRIDAY: {e}")


                </td>
                <td class="resumen-texto">{resumen_final}</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)