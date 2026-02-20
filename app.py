import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="F.R.I.D.A.Y. - 26ª Com. Pudahuel", page_icon="🟢", layout="wide")

# 2. ESTILO TÁCTICO (CSS)
st.markdown("""
    <style>
    /* Estilo de la Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #004A2F !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Letras de los formularios en NEGRO */
    .stMarkdown p, label, .stTextInput label, .stTextArea label {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 1.1rem;
    }
    
    /* Botones Estilo Institucional */
    div.stButton > button {
        background-color: #004A2F;
        color: white;
        border: 2px solid #C5A059;
        border-radius: 5px;
        font-weight: bold;
        width: 100%;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL (Sidebar)
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/a2/Logotipo_de_Carabineros_de_Chile.svg", width=100)
    st.markdown("### 🟢 ESTADO: OPERATIVO")
    st.write("**Unidad:** 26ª Comisaría")
    st.write("**Analista:** D. Sandoval A.")
    st.write(f"**Fecha:** {datetime.now().strftime('%d/%m/%Y')}")

# 4. ENCABEZADO PRINCIPAL
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/a2/Logotipo_de_Carabineros_de_Chile.svg", width=120)
with col2:
    st.title("CARABINEROS DE CHILE")
    st.subheader("SISTEMA F.R.I.D.A.Y. - PREFECTURA OCCIDENTE")

# 5. SISTEMA DE PESTAÑAS
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- PESTAÑA 1: STOP MENSUAL ---
with tab1:
    with st.form("form_mensual"):
        st.markdown("### DATOS ACTA STOP MENSUAL")
        c1, c2 = st.columns(2)
        with c1:
            semana = st.text_input("Semana de estudio analizada", placeholder="Ej: 01 al 07")
            fecha_sesion = st.text_input("Fecha de sesión")
        with c2:
            c_carabineros = st.text_input("Compromiso Carabineros")
            c_muni = st.text_input("Compromiso Municipalidad")
        
        problematica = st.text_area("Problemática 26ª Comisaría")
        
        # EL BOTÓN DEBE ESTAR DENTRO DEL FORMULARIO
        submit_mensual = st.form_submit_button("GENERAR ACTA MENSUAL")
        
        if submit_mensual:
            st.success("Procesando Acta Mensual...")

# --- PESTAÑA 2: STOP TRIMESTRAL ---
with tab2:
    with st.form("form_trimestral"):
        st.markdown("### DATOS STOP TRIMESTRAL")
        periodo = st.text_input("Semana de estudio comprendida", placeholder="Ej: Octubre - Diciembre")
        cap_bustos = st.text_input("Nombre Comisario Subrogante")
        
        submit_trimestral = st.form_submit_button("GENERAR ACTA TRIMESTRAL")

# --- PESTAÑA 3: INFORME GEO ---
with tab3:
    with st.form("form_geo"):
        st.markdown("### DATOS INFORME GEO")
        col_a, col_b = st.columns(2)
        with col_a:
            domicilio = st.text_input("Domicilio del análisis")
            doe = st.text_input("N° de DOE")
            cuadrante = st.text_input("Cuadrante")
        with col_b:
            p_inicio = st.text_input("Fecha Inicio")
            p_fin = st.text_input("Fecha Fin")
            total_dmcs = st.text_input("Total DMCS")
        
        conclusion_ia = st.text_area("V.- CONCLUSIÓN")
        
        submit_geo = st.form_submit_button("GENERAR INFORME GEO")