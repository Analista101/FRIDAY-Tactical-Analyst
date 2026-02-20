import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="F.R.I.D.A.Y. - 26ª Com. Pudahuel", page_icon="🟢", layout="wide")

# 2. ESTILO DE CONTRASTES Y ALINEACIÓN (CSS)
st.markdown("""
    <style>
    /* Fondo General Blanco */
    .stApp { background-color: #FFFFFF !important; }
    
    /* BARRA LATERAL: Fondo Verde, Letras Blancas */
    [data-testid="stSidebar"] {
        background-color: #004A2F !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
        font-weight: bold !important;
    }

    /* ENCABEZADO CENTRADO: Fondo Verde, Letra Blanca */
    .header-institucional {
        background-color: #004A2F;
        padding: 30px;
        border-radius: 15px;
        color: #FFFFFF !important;
        text-align: center; /* CENTRADO TOTAL */
        margin-bottom: 25px;
        border: 3px solid #C5A059;
    }
    
    /* LETRAS EN CUERPO (Fondo Blanco): Verde Oscuro y Muy Negritas */
    label, .stMarkdown p, .stTextInput label, .stTextArea label {
        color: #004A2F !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
    }

    /* BOTONES: Verdes con Letra Blanca */
    div.stButton > button {
        background-color: #004A2F !important;
        color: #FFFFFF !important;
        border: 2px solid #C5A059 !important;
        font-weight: bold !important;
        height: 3.5em !important;
        width: 100% !important;
    }
    
    /* Pestañas */
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F; border-radius: 5px; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #C5A059 !important; color: #000000 !important; }

    /* Ajuste para centrar la imagen del logo en el cuerpo */
    .img-centered {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 150px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL (Sidebar)
with st.sidebar:
    # ESCUDO DE CARABINEROS EN LA BARRA LATERAL
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Logotipo_de_Carabineros_de_Chile.svg/800px-Logotipo_de_Carabineros_de_Chile.svg.png", width=150)
    st.markdown("### 🟢 SISTEMA OPERATIVO")
    st.write("---")
    st.write("**UNIDAD:** 26ª Comisaría Pudahuel")
    st.write(f"**ANALISTA:** D. Sandoval A.")
    st.write(f"**FECHA:** {datetime.now().strftime('%d/%m/%Y')}")
    st.write("---")
    st.info("F.R.I.D.A.Y. conectada al servidor institucional.")

# 4. CUERPO PRINCIPAL: LOGO Y CABECERA CENTRADOS
# Usamos HTML para asegurar el centrado perfecto
st.markdown("""
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Logotipo_de_Carabineros_de_Chile.svg/800px-Logotipo_de_Carabineros_de_Chile.svg.png" class="img-centered">
    <div class="header-institucional">
        <h1 style="color: white; margin:0;">CARABINEROS DE CHILE</h1>
        <h2 style="color: white; margin:0;">SISTEMA F.R.I.D.A.Y.</h2>
        <p style="color: #C5A059; margin:0; font-weight: bold;">PREFECTURA SANTIAGO OCCIDENTE</p>
    </div>
    """, unsafe_allow_html=True)

# 5. SISTEMA DE PESTAÑAS
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- PESTAÑA 1: STOP MENSUAL ---
with tab1:
    with st.form("form_mensual"):
        st.markdown("### 📝 DATOS PARA ACTA STOP MENSUAL")
        c1, c2 = st.columns(2)
        with c1:
            semana = st.text_input("Semana de estudio", placeholder="Ej: 01 al 07")
            fecha_s = st.text_input("Fecha de sesión")
        with c2:
            c_carab = st.text_input("Compromiso Carabineros")
            c_muni = st.text_input("Compromiso Municipalidad")
        
        prob = st.text_area("Problemática Delictual 26ª Comisaría")
        
        if st.form_submit_button("🛡️ GENERAR ACTA STOP"):
            st.success("Procesando información institucional...")

# --- PESTAÑA 2: STOP TRIMESTRAL ---
with tab2:
    with st.form("form_trimestral"):
        st.markdown("### 📊 DATOS STOP TRIMESTRAL")
        periodo = st.text_input("Periodo comprendido", placeholder="Ej: Octubre - Diciembre")
        cap_bustos = st.text_input("Nombre Comisario Subrogante")
        
        if st.form_submit_button("📊 GENERAR TRIMESTRAL"):
            st.info("Preparando reporte trimestral...")

# --- PESTAÑA 3: INFORME GEO ---
with tab3:
    with st.form("form_geo"):
        st.markdown("### 📍 DATOS INFORME DELICTUAL GEO")
        col_a, col_b = st.columns(2)
        with col_a:
            dom = st.text_input("Domicilio del análisis")
            doe_n = st.text_input("N° de DOE")
            cuadrante = st.text_input("Cuadrante")
        with col_b:
            p