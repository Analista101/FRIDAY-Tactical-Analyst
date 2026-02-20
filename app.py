import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import datetime

# Configuración de Identidad Visual
st.set_page_config(page_title="F.R.I.D.A.Y. - Tactical Unit", page_icon="🟢", layout="wide")

# Estilo Stark-Institucional
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; white-space: pre-wrap; background-color: #004A2F;
        border-radius: 5px; color: white; font-weight: bold; padding: 10px;
    }
    .stTabs [aria-selected="true"] { background-color: #C5A059 !important; color: black !important; }
    div.stButton > button {
        background-color: #004A2F; color: white; border: 2px solid #C5A059;
        border-radius: 10px; height: 3em; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ F.R.I.D.A.Y. | Analista Civil")
st.write("---")

# Creación de Pestañas
tab1, tab2, tab3 = st.tabs(["📊 ACTA STOP MENSUAL", "📅 STOP TRIMESTRAL", "🗺️ INFORME GEO"])

# --- PESTAÑA 1: STOP MENSUAL ---
with tab1:
    st.header("Sesión Táctica Operativa Mensual")
    with st.form("form_mensual"):
        c1, c2 = st.columns(2)
        with c1:
            semana = st.text_input("Semana de estudio", placeholder="Ej: 01 al 07")
            fecha_s = st.text_input("Fecha de sesión")
        with c2:
            c_carab = st.text_input("Compromiso Carabineros")
            c_muni = st.text_input("Compromiso Municipalidad")
        
        prob = st.text_area("Problemática Delictual Analizada")
        
        btn_stop = st.form_submit_button("GENERAR ACTA MENSUAL")
        if btn_stop:
            # Lógica de renderizado (se repite la del post anterior)
            st.info("Procesando datos institucionales...")

# --- PESTAÑA 2: STOP TRIMESTRAL ---
with tab2:
    st.header("Análisis Operativo Trimestral")
    with st.form("form_trimestral"):
        periodo = st.text_input("Periodo Comprendido", placeholder="Ej: Octubre - Diciembre")
        cap_b = st.text_input("Capitán Comisario (S)")
        btn_trim = st.form_submit_button("GENERAR ACTA TRIMESTRAL")

# --- PESTAÑA 3: INFORME GEO ---
with tab3:
    st.header("Análisis Geodelictual")
    with st.form("form_geo"):
        col_a, col_b = st.columns(2)
        with col_a:
            dom = st.text_input("Domicilio del Análisis")
            doe_n = st.text_input("N° de DOE")
        with col_b:
            cuad = st.text_input("Cuadrante")
            casos = st.text_input("Total DMCS")
        
        conc = st.text_area("Conclusión del Analista")
        btn_geo = st.form_submit_button("GENERAR INFORME GEO")

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/a/a2/Logotipo_de_Carabineros_de_Chile.svg", width=100)
st.sidebar.write("**Estado del Sistema:** Operativo")
st.sidebar.write("**Usuario:** D. Sandoval")