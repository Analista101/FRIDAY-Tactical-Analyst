import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="F.R.I.D.A.Y. - 26ª Com. Pudahuel", page_icon="🟢", layout="wide")

# 2. ESTILO TÁCTICO COMPACTO (CSS)
st.markdown("""
    <style>
    /* Eliminar espacio superior en blanco */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    
    .stApp { background-color: #FFFFFF !important; }
    
    /* BARRA LATERAL: Todo Blanco */
    [data-testid="stSidebar"] { background-color: #004A2F !important; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h4 {
        color: #FFFFFF !important;
        font-weight: bold !important;
        margin-bottom: 5px !important;
    }

    /* ENCABEZADO COMPACTO Y CENTRADO */
    .header-institucional {
        background-color: #004A2F;
        padding: 15px; /* Reducido para ahorrar espacio */
        border-radius: 10px;
        color: #FFFFFF !important;
        text-align: center;
        border: 2px solid #C5A059;
        margin-top: 0px !important;
    }
    
    /* TEXTO CUERPO: Verde Oscuro y Grueso */
    label, .stMarkdown p, .stTextInput label, .stTextArea label {
        color: #004A2F !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
    }

    /* BOTONES */
    div.stButton > button {
        background-color: #004A2F !important;
        color: #FFFFFF !important;
        border: 2px solid #C5A059 !important;
        font-weight: bold !important;
    }
    
    /* Pestañas */
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F; border-radius: 5px; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #C5A059 !important; color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL (Sidebar)
with st.sidebar:
    # Intentar cargar logo local desde GitHub, si no, usar respaldo
    try:
        st.image("logo.png", width=140)
    except:
        st.image("https://upload.wikimedia.org/wikipedia/commons/a/a2/Logotipo_de_Carabineros_de_Chile.svg", width=130)
    
    st.markdown("### 🟢 SISTEMA OPERATIVO")
    st.markdown("---")
    st.markdown("#### **UNIDAD:** 26ª Com. Pudahuel")
    st.markdown("#### **ANALISTA:** D. Sandoval A.")
    st.markdown(f"#### **FECHA:** {datetime.now().strftime('%d/%m/%Y')}")

# 4. CUERPO PRINCIPAL (Más arriba y centrado)
st.markdown("""
    <div class="header-institucional">
        <h2 style="color: white; margin:0; font-size: 1.8rem;">CARABINEROS DE CHILE</h2>
        <h3 style="color: #C5A059; margin:0; font-size: 1.2rem;">SISTEMA F.R.I.D.A.Y. | PREFECTURA OCCIDENTE</h3>
    </div>
    """, unsafe_allow_html=True)

# 5. PESTAÑAS
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

with tab1:
    with st.form("form_mensual"):
        c1, c2 = st.columns(2)
        with c1:
            semana = st.text_input("Semana de estudio", placeholder="Ej: 01 al 07")
            fecha_s = st.text_input("Fecha de sesión")
        with c2:
            c_carab = st.text_input("Compromiso Carabineros")
            c_muni = st.text_input("Compromiso Municipalidad")
        prob = st.text_area("Problemática Delictual 26ª Comisaría")
        if st.form_submit_button("🛡️ GENERAR ACTA"):
            st.success("Procesando...")

with tab2:
    with st.form("form_trimestral"):
        periodo = st.text_input("Periodo comprendido")
        cap_bustos = st.text_input("Comisario Subrogante")
        if st.form_submit_button("📊 GENERAR TRIMESTRAL"):
            st.info("Reporte en marcha...")

with tab3:
    with st.form("form_geo"):
        col_a, col_b = st.columns(2)
        with col_a:
            dom = st.text_input("Domicilio")
            doe_n = st.text_input("N° DOE")
        with col_b:
            p_ini = st.text_input("Inicio")
            total = st.text_input("Casos")
        concl = st.text_area("V.- CONCLUSIÓN")
        if st.form_submit_button("🗺️ GENERAR GEO"):
            st.success("Analizando...")