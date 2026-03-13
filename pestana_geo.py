import streamlit as st
import pandas as pd
import io
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from motor_friday import ajustar_texto_largo, crear_tabla_profesional

def render_pestana_georreferenciacion():
    st.markdown('### 📍 INFORME GEO: GENERACIÓN PROFESIONAL')
    
    with st.form("form_geo_final"):
        col1, col2, col3 = st.columns(3)
        doe_n = col1.text_input("DOE N°", value="248812153")
        doe_fecha = col1.text_input("Fecha DOE", value="03-03-2026")
        inf_fecha = col1.text_input("Fecha Informe", value="03 de marzo de 2026")
        
        funcionario = col2.text_input("Funcionario", value="JUAN ANDRES URRUTIA LOBOS")
        grado = col2.text_input("Grado", value="SARGENTO 2°")
        unidad = col2.text_input("Unidad", value="GRUPO DE ADIESTRAMIENTO CANINO")
        
        domicilio = col3.text_input("Domicilio", value="PASAJE PILCOMAYO 8501")
        subcomisaria = col3.text_input("Subcomisaría", value="26A COMISARIA PUDAHUEL")
        cuadrante = col3.text_input("Cuadrante", value="232-A")
        
        cp1, cp2, cp3 = st.columns([2, 1, 1])
        periodo_txt = cp1.text_input("Periodo", value="03-12-2025 al 03-03-2026")
        mapa_img = cp2.file_uploader("SUBIR MAPA SAIT", type=['png', 'jpg'])
        excel_geo = cp3.file_uploader("SUBIR EXCEL/CSV", type=['xlsx', 'csv'])
        
        submit_geo = st.form_submit_button("🛡️ GENERAR INFORME GEO")

    if submit_geo:
        if not mapa_img or not excel_geo:
            st.error("❌ Faltan archivos (Mapa o Excel) para procesar.")
        else:
            try:
                # PROCESAMIENTO
                df = pd.read_csv(excel_geo) if excel_geo.name.endswith('csv') else pd.read_excel(excel_geo)
                df.columns = [c.upper().strip() for c in df.columns]
                
                # ... (Aquí sigue su lógica de filtrado y generación de Word) ...
                st.success("✅ Informe procesado por FRIDAY.")
                
            except Exception as e:
                st.error(f"Error en el motor FRIDAY: {e}")