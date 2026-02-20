import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import datetime

# Configuración de Identidad
st.set_page_config(page_title="F.R.I.D.A.Y. - 26ª Com. Pudahuel", page_icon="🟢", layout="wide")

# Estilo Institucional Reforzado
st.markdown("""
    <style>
    /* Fondo general */
    .stApp { background-color: #FFFFFF; }
    
    /* Etiquetas de los campos (Label) en negro fuerte */
    label { 
        color: #000000 !important; 
        font-weight: bold !important; 
        font-size: 1.1rem !important;
    }
    
    /* Títulos */
    h1, h2, h3 { color: #004A2F !important; }
    
    /* Barra lateral */
    [data-testid="stSidebar"] { background-color: #004A2F; }
    [data-testid="stSidebar"] .stMarkdown p { color: white; font-weight: bold; }

    /* Ajuste de Tabs */
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        color: #004A2F;
        font-weight: bold;
        border: 1px solid #d3d3d3;
        padding: 8px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #004A2F !important;
        color: white !important;
        border-bottom: 4px solid #C5A059 !important;
    }

    /* Botones */
    div.stButton > button {
        background-color: #004A2F;
        color: white;
        border: 2px solid #C5A059;
        height: 3.5em;
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Encabezado (Corregido para que no se corte)
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    # Logo oficial de Carabineros
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/a2/Logotipo_de_Carabineros_de_Chile.svg", width=150)
with col_titulo:
    st.markdown("# CARABINEROS DE CHILE")
    st.markdown("### PREFECTURA SANTIAGO OCCIDENTE - 26ª COM. PUDAHUEL")
    st.write(f"**SISTEMA F.R.I.D.A.Y.** | Analista Civil: D. Sandoval | {datetime.now().strftime('%d/%m/%Y')}")

st.write("---")

# Sistema de Pestañas
tab1, tab2, tab3 = st.tabs(["📊 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- PESTAÑA 1: STOP MENSUAL ---
with tab1:
    st.markdown("### 📝 Ingreso de Datos: Acta STOP Mensual")
    with st.form("mensual"):
        c1, c2 = st.columns(2)
        with c1:
            semana = st.text_input("Semana de estudio analizada", placeholder="Ej: 01 al 07") [cite: 99]
            fecha_sesion = st.text_input("Fecha de sesión") [cite: 100]
        with c2:
            c_carabineros = st.text_input("Compromisos Institucionales") [cite: 119]
            c_muni = st.text_input("Compromiso Municipalidad") [cite: 121]
        
        problematica = st.text_area("Problemáticas Delictuales (26ª Comisaría)") [cite: 117]
        
        # Botón Institucional
        if st.form_submit_button("🛡️ GENERAR Y DESCARGAR ACTA MENSUAL"):
            st.success("Analizando datos... La descarga comenzará en breve.")

# --- PESTAÑA 2: STOP TRIMESTRAL ---
with tab2:
    st.markdown("### 📅 Análisis Operativo Trimestral")
    with st.form("trimestral"):
        periodo = st.text_input("Semana de estudio comprendida", placeholder="Ej: Octubre - Diciembre") [cite: 135]
        cap_bustos = st.text_input("Comisario Subrogante (Grado y Nombre)") [cite: 138]
        st.form_submit_button("💾 GENERAR ACTA TRIMESTRAL")

# --- PESTAÑA 3: INFORME GEO ---
with tab3:
    st.markdown("### 🗺️ Confección de Informe Delictual GEO")
    with st.form("geo"):
        c1, c2 = st.columns(2)
        with c1:
            domicilio = st.text_input("Domicilio del Análisis") [cite: 163]
            doe = st.text_input("N° de DOE") [cite: 170]
            cuadrante = st.text_input("Cuadrante") [cite: 173]
        with c2:
            p_inicio = st.text_input("Fecha Inicio Análisis") [cite: 172]
            p_fin = st.text_input("Fecha Fin Análisis") [cite: 172]
            total_dmcs = st.text_input("Total DMCS (Radio 300 mts)") [cite: 180]
        
        conclusion_ia = st.text_area("V.- CONCLUSIÓN") [cite: 186, 187]
        st.form_submit_button("🛰️ GENERAR INFORME GEODELICTUAL")

# Barra lateral de estado
st.sidebar.markdown("### 🟢 ESTADO OPERATIVO")
st.sidebar.write("**Unidad:** 26ª Com. Pudahuel") [cite: 162]
st.sidebar.write("**Sector:** Prefectura Occidente") [cite: 161]
st.sidebar.info("F.R.I.D.A.Y. lista para procesar informes.")