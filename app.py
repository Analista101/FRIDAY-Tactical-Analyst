import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="F.R.I.D.A.Y. - 26ª Com. Pudahuel", page_icon="🟢", layout="wide")

# 2. ESTILO INSTITUCIONAL DE ALTO CONTRASTE
st.markdown("""
    <style>
    /* Fondo Blanco Puro */
    .stApp {
        background-color: #FFFFFF !important;
    }
    
    /* Barra Lateral Verde JARVIS */
    [data-testid="stSidebar"] {
        background-color: #004A2F !important;
    }
    
    /* LETRAS EN VERDE OSCURO, NEGRITAS Y GRUESAS */
    label, .stMarkdown p, .stTextInput label, .stTextArea label, h1, h2, h3 {
        color: #004A2F !important;
        font-weight: 900 !important; /* Grosor máximo */
        font-family: 'Arial', sans-serif !important;
    }

    /* Input text color para que lo que escribas se vea negro */
    input {
        color: #000000 !important;
        font-weight: bold !important;
    }

    /* Botones */
    div.stButton > button {
        background-color: #004A2F;
        color: white;
        border: 3px solid #C5A059;
        font-weight: bold;
        height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL (Sidebar)
with st.sidebar:
    # Logo alternativo para evitar link roto
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Logotipo_de_Carabineros_de_Chile.svg/1200px-Logotipo_de_Carabineros_de_Chile.svg.png", width=120)
    st.markdown("### 🟢 SISTEMA ACTIVO")
    st.write("**Unidad:** 26ª Comisaría")
    st.write("**Analista:** D. Sandoval A.")
    st.write(f"**Fecha:** {datetime.now().strftime('%d/%m/%Y')}")

# 4. ENCABEZADO PRINCIPAL (Logo corregido)
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Logotipo_de_Carabineros_de_Chile.svg/1200px-Logotipo_de_Carabineros_de_Chile.svg.png", width=150)
with col2:
    st.markdown("# CARABINEROS DE CHILE")
    st.markdown("## SISTEMA F.R.I.D.A.Y. | PREFECTURA OCCIDENTE")

st.write("---")

# 5. SISTEMA DE PESTAÑAS
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- PESTAÑA 1: STOP MENSUAL ---
with tab1:
    with st.form("form_mensual"):
        st.markdown("### 📝 DATOS PARA ACTA STOP MENSUAL") [cite: 1, 2]
        c1, c2 = st.columns(2)
        with c1:
            semana = st.text_input("Semana de estudio analizada", placeholder="Ej: 01 al 07") [cite: 4]
            fecha_sesion = st.text_input("Fecha de sesión") [cite: 5]
        with c2:
            c_carabineros = st.text_input("Compromiso Carabineros") [cite: 24]
            c_muni = st.text_input("Compromiso Municipalidad") [cite: 26]
        
        problematica = st.text_area("Problemática 26ª Comisaría Pudahuel") [cite: 22]
        
        if st.form_submit_button("🛡️ GENERAR ACTA STOP"):
            st.success("Escribiendo documento...")

# --- PESTAÑA 2: STOP TRIMESTRAL ---
with tab2:
    with st.form("form_trimestral"):
        st.markdown("### 📊 DATOS STOP TRIMESTRAL") [cite: 39]
        periodo = st.text_input("Semana de estudio comprendida", placeholder="Ej: Octubre - Diciembre") [cite: 40]
        cap_bustos = st.text_input("Nombre Comisario Subrogante") [cite: 43]
        
        st.form_submit_button("📊 GENERAR TRIMESTRAL")

# --- PESTAÑA 3: INFORME GEO ---
with tab3:
    with st.form("form_geo"):
        st.markdown("### 📍 DATOS INFORME DELICTUAL GEO") [cite: 72]
        col_a, col_b = st.columns(2)
        with col_a:
            domicilio = st.text_input("Domicilio del análisis") [cite: 68]
            doe = st.text_input("N° de DOE") [cite: 75]
            cuadrante = st.text_input("Cuadrante") [cite: 78]
        with col_b:
            p_inicio = st.text_input("Fecha Inicio Análisis") [cite: 77]
            p_fin = st.text_input("Fecha Fin Análisis") [cite: 77]
            total_dmcs = st.text_input("Total DMCS") [cite: 85]
        
        conclusion_ia = st.text_area("V.- CONCLUSIÓN") [cite: 91, 92]
        
        st.form_submit_button("🗺️ GENERAR INFORME GEO")