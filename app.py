import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="F.R.I.D.A.Y. - 26ª Com. Pudahuel", page_icon="🟢", layout="wide")

# 2. ESTILO DE CONTRASTES DINÁMICOS (CSS)
st.markdown("""
    <style>
    /* Fondo General Blanco */
    .stApp {
        background-color: #FFFFFF !important;
    }
    
    /* BARRA LATERAL: Fondo Verde, Letra Blanca */
    [data-testid="stSidebar"] {
        background-color: #004A2F !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
        font-weight: bold !important;
    }

    /* ENCABEZADOS Y TÍTULOS: Fondo Verde, Letra Blanca */
    .header-verde {
        background-color: #004A2F;
        padding: 20px;
        border-radius: 10px;
        color: #FFFFFF !important;
        margin-bottom: 20px;
        border: 2px solid #C5A059;
    }
    
    /* LETRAS DONDE EL FONDO ES BLANCO: Verde Oscuro y Negrita */
    label, .stMarkdown p, .stTextInput label, .stTextArea label {
        color: #004A2F !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
    }

    /* BOTONES: Fondo Verde, Letra Blanca */
    div.stButton > button {
        background-color: #004A2F !important;
        color: #FFFFFF !important;
        border: 2px solid #C5A059 !important;
        font-weight: bold !important;
        height: 3.5em !important;
        width: 100% !important;
        text-transform: uppercase;
    }
    
    /* Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F; border-radius: 5px; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #C5A059 !important; color: #000000 !important; }

    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL
with st.sidebar:
    # Usando el logo con un parámetro para forzar la carga
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Logotipo_de_Carabineros_de_Chile.svg/800px-Logotipo_de_Carabineros_de_Chile.svg.png", width=120)
    st.markdown("### 🟢 UNIDAD ACTIVA")
    st.write("26ª Comisaría Pudahuel")
    st.write(f"Analista: D. Sandoval\n{datetime.now().strftime('%d/%m/%Y')}")

# 4. ENCABEZADO CON FONDO VERDE
st.markdown("""
    <div class="header-verde">
        <h1 style="color: white; margin:0;">CARABINEROS DE CHILE</h1>
        <h3 style="color: white; margin:0;">SISTEMA F.R.I.D.A.Y. | PREFECTURA OCCIDENTE</h3>
    </div>
    """, unsafe_allow_html=True)

# 5. PESTAÑAS
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- PESTAÑA 1: STOP MENSUAL ---
with tab1:
    with st.form("form_mensual"):
        st.markdown("### 📝 COMPLETAR ACTA STOP MENSUAL")
        c1, c2 = st.columns(2)
        with c1:
            semana = st.text_input("Semana de estudio", placeholder="Ej: 01 al 07")
            fecha_s = st.text_input("Fecha de sesión")
        with c2:
            c_carab = st.text_input("Compromiso Carabineros")
            c_muni = st.text_input("Compromiso Municipalidad")
        
        prob = st.text_area("Problemática Delictual Detectada")
        
        if st.form_submit_button("GENERAR DOCUMENTO"):
            st.success("Analizando datos para el Acta...")

# --- PESTAÑA 2: STOP TRIMESTRAL ---
with tab2:
    with st.form("form_trimestral"):
        st.markdown("### 📊 COMPLETAR STOP TRIMESTRAL")
        periodo = st.text_input("Periodo (Meses)", placeholder="Ej: Enero a Marzo")
        capitan = st.text_input("Comisario Subrogante")
        
        if st.form_submit_button("GENERAR TRIMESTRAL"):
            st.info("Preparando análisis trimestral...")

# --- PESTAÑA 3: INFORME GEO ---
with tab3:
    with st.form("form_geo"):
        st.markdown("### 📍 COMPLETAR INFORME GEO")
        col_a, col_b = st.columns(2)
        with col_a:
            dom = st.text_input("Domicilio Análisis")
            doe_n = st.text_input("N° DOE")
        with col_b:
            cuad = st.text_input("Cuadrante")
            casos = st.text_input("Total DMCS")
        
        conclusion = st.text_area("V.- CONCLUSIÓN TÁCTICA")
        
        if st.form_submit_button("GENERAR INFORME GEO"):
            st.success("Geolocalizando datos...")