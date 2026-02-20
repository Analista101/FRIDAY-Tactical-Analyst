import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import datetime

# Configuración Superior del Sistema
st.set_page_config(
    page_title="F.R.I.D.A.Y. - Análisis Criminal",
    page_icon="🟢",
    layout="wide"
)

# Inyección de Estilo Institucional (Verde y Dorado)
st.markdown("""
    <style>
    /* Fondo y contenedores */
    .stApp { background-color: #F4F4F4; }
    
    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: #004A2F;
        color: white;
    }
    
    /* Títulos y Subtítulos */
    h1, h2, h3 { color: #004A2F; font-family: 'Arial Black', sans-serif; }
    
    /* Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #E0E0E0;
        border-radius: 5px 5px 0px 0px;
        padding: 10px 25px;
        color: #004A2F;
        font-weight: bold;
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
        border-radius: 5px;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #C5A059;
        color: #004A2F;
        border: 2px solid #004A2F;
    }
    </style>
    """, unsafe_allow_html=True)

# Encabezado con Identidad
col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/a2/Logotipo_de_Carabineros_de_Chile.svg", width=120)
with col_titulo:
    st.title("CARABINEROS DE CHILE")
    st.subheader("SISTEMA F.R.I.D.A.Y. - PREFECTURA SANTIAGO OCCIDENTE")

st.write("---")

# Navegación por Pestañas
tab1, tab2, tab3 = st.tabs(["📝 ACTA STOP MENSUAL", "📅 STOP TRIMESTRAL", "🗺️ INFORME GEO"])

# --- PESTAÑA 1: STOP MENSUAL ---
with tab1:
    st.markdown("### 📄 Formulario: Acta de Sesión Mensual")
    with st.form("mensual"):
        c1, c2 = st.columns(2)
        with c1:
            semana = st.text_input("Semana de estudio analizada", placeholder="Ej: 05 al 11")
            fecha_s = st.text_input("Fecha de sesión")
        with c2:
            c_carab = st.text_input("Compromisos Institucionales")
            c_muni = st.text_input("Compromisos Municipalidad")
        prob = st.text_area("Problemáticas Delictuales Analizadas (26ª Comisaría)")
        
        btn_stop = st.form_submit_button("GENERAR DOCUMENTO OFICIAL")
        
        if btn_stop:
            # Aquí iría la lógica de renderizado que ya tenemos
            st.info("Generando documento... Verifique los campos en el Word.")

# --- PESTAÑA 2: STOP TRIMESTRAL ---
with tab2:
    st.markdown("### 📅 Formulario: Análisis Operativo Trimestral")
    with st.form("trimestral"):
        periodo = st.text_input("Periodo (Meses)", placeholder="Ej: Enero - Marzo")
        cap_bustos = st.text_input("Nombre Comisario Subrogante")
        btn_trim = st.form_submit_button("GENERAR ACTA TRIMESTRAL")

# --- PESTAÑA 3: INFORME GEO ---
with tab3:
    st.markdown("### 🗺️ Formulario: Informe Delictual GEO")
    with st.form("geo"):
        c1, c2, c3 = st.columns(3)
        with c1:
            domicilio = st.text_input("Domicilio Análisis")
            doe = st.text_input("N° DOE")
        with c2:
            cuadrante = st.text_input("Cuadrante")
            total_dmcs = st.text_input("Total DMCS")
        with c3:
            p_inicio = st.text_input("Fecha Inicio")
            p_fin = st.text_input("Fecha Fin")
            
        conclusion = st.text_area("V.- CONCLUSIÓN")
        btn_geo = st.form_submit_button("GENERAR INFORME GEO")

# Barra Lateral (Sidebar) de Estado
st.sidebar.markdown("### 🟢 ESTADO DEL SISTEMA")
st.sidebar.write("**Unidad:** 26ª Com. Pudahuel")
st.sidebar.write("**Analista:** D. Sandoval A.")
st.sidebar.write(f"**Fecha:** {datetime.now().strftime('%d/%m/%Y')}")
st.sidebar.write("---")
st.sidebar.info("F.R.I.D.A.Y. está conectada a la base de datos local.")