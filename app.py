import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# --- 1. AJUSTE DE COLORIMETRÍA (VERDE OPACO) ---
st.set_page_config(page_title="PROYECTO F.R.I.D.A.Y.", layout="wide")

st.markdown("""
    <style>
    /* Fondo Verde Claro Opaco para descanso visual */
    .stApp { background-color: #D1D8C4 !important; }
    
    /* Pestañas (Fondo Verde Oscuro Institucional) */
    .stTabs [data-baseweb="tab-list"] { 
        background-color: #004A2F !important; 
        border-radius: 5px;
    }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; }

    /* Encabezados Tácticos */
    .section-header {
        background-color: #004A2F !important; color: #FFFFFF !important;
        padding: 10px 15px; border-radius: 5px; font-weight: bold;
        text-transform: uppercase; margin-bottom: 15px; border-left: 8px solid #C5A059;
    }

    /* Cuadros de entrada: Fondo Blanco para escritura clara / Borde Verde */
    input, textarea, [data-baseweb="input"] {
        background-color: #FFFFFF !important; 
        color: #000000 !important;
        border: 2px solid #004A2F !important; 
        border-radius: 5px !important;
    }
    label { color: #000000 !important; font-weight: bold !important; }
    
    /* Botones de Procesamiento */
    .stButton>button {
        background-color: #004A2F !important;
        color: white !important;
        border: 2px solid #C5A059 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE IA F.R.I.D.A.Y. ---
def motor_ia_friday(df):
    total = int(df['CUENTA'].sum()) if 'CUENTA' in df.columns else 0
    dia_critico = "VIERNES" 
    hora_critica = "20:00 - 23:59"
    
    if total > 25:
        conclusion = f"ALTO RIESGO. Se detecta una saturación delictual de {total} eventos. El periodo crítico (Día: {dia_critico}, Hora: {hora_critica}) sugiere vulnerabilidad extrema."
    else:
        conclusion = f"RIESGO MODERADO. Con {total} delitos registrados, el sector presenta actividad constante."
    return total, dia_critico, hora_critica, conclusion

# --- 3. INTERFAZ INTEGRAL ---
t1, t2, t3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_mensual_v2"):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Semana de estudio")
            st.text_input("Fecha de sesión")
        with c2:
            st.text_input("Compromiso Carabineros")
        st.text_area("Problemática Delictual 26ª Comisaría")
        
        st.markdown('<div class="section-header">🖋️ FIRMA</div>', unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        with f1:
            st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="nm_v2")
            st.text_input("Grado", value="C.P.R. Analista Social", key="gm_v2")
        with f2:
            st.text_input("Cargo", value="OFICINA DE OPERACIONES", key="cm_v2")
        st.form_submit_button("🛡️ GENERAR ACTA MENSUAL")

with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO-ESPACIAL (IA F.R.I.D.A.Y.)</div>', unsafe_allow_html=True)
    with st.form("form_geo_v2"):
        st.markdown('<div class="section-header">I. ANTECEDENTES Y SUMINISTROS</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            v_dom = st.text_input("Domicilio ({{ domicilio }})")
            v_jur = st.text_input("Jurisdicción", value="26ª COM. PUDAHUEL")
            v_doe = st.text_input("N° DOE ({{ doe }})")
            f_mapa = st.file_uploader("Mapa SAIT ({{ mapa }})", type=['png', 'jpg'])
        with col2:
            v_fdoe = st.text_input("Fecha DOE ({{ fecha_doe }})")
            v_cua = st.text_input("Cuadrante ({{ cuadrante }})")
            v_fact = st.text_input("Fecha Actual", value=datetime.now().strftime('%d/%m/%Y'))
            f_excel = st.file_uploader("Excel Único (Detalle y Calor)", type=['xlsx'])

        st.markdown('<div class="section-header">II. DATOS SOLICITANTE</div>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: v_sol = st.text_input("Nombre ({{ solicitante }})")
        with s2: v_gs = st.text_input("Grado ({{ grado_solic }})")
        with s3: v_us = st.text_input("Unidad ({{ unidad_solic }})")

        p_ini = st.text_input("Inicio Periodo ({{ periodo_inicio }})")
        p_fin = st.text_input("Fin Periodo ({{ periodo_fin }})")

        btn_run = st.form_submit_button("🛡️ EJECUTAR ANÁLISIS FINAL")

    if btn_run:
        if f_excel and f_mapa:
            with st.spinner("F.R.I.D.A.Y. Generando informe..."):
                df_data = pd.read_excel(f_excel)
                total, dia, hora, concl = motor_ia_friday(df_data)
                
                doc = DocxTemplate("INFORME GEO.docx")
                context = {
                    'domicilio': v_dom, 'jurisdiccion': v_jur, 'doe': v_doe, 'fecha_doe': v_fdoe,
                    'cuadrante': v_cua, 'fecha_actual': v_fact, 'solicitante': v_sol,
                    'grado_solic': v_gs, 'unidad_solic': v_us, 'periodo_inicio': p_ini,
                    'periodo_fin': p_fin, 'total_dmcs': total, 'dia_max': dia,
                    'hora_max': hora, 'conclusion_ia': concl,
                    'mapa': InlineImage(doc, f_mapa, width=Inches(5))
                }
                doc.render(context)
                
                output = io.BytesIO()
                doc.save(output)
                st.success(f"Análisis completado: {total} delitos detectados.")
                st.download_button("📂 DESCARGAR INFORME GEO", data=output.getvalue(), 
                                   file_name=f"Informe_GEO_{v_sol}.docx")