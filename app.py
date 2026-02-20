import streamlit as st
from docxtpl import DocxTemplate, RichText
import io
from datetime import datetime

# 1. CONFIGURACIÓN DEL SISTEMA
st.set_page_config(page_title="PROJECT JARVIS - 26ª Com. Pudahuel", page_icon="🟢", layout="wide")

# 2. INYECCIÓN DE ESTILO TÁCTICO (FUERZA BRUTA PARA COLORES)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #004A2F !important; }
    
    /* TEXTO UNIDAD EN BLANCO */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] span {
        color: #FFFFFF !important;
        font-weight: bold !important;
    }

    /* BOTONES VERDES */
    div.stButton > button, .stFormSubmitButton > button {
        background-color: #004A2F !important;
        color: #FFFFFF !important;
        border: 2px solid #C5A059 !important;
        font-weight: bold !important;
        width: 100% !important;
        height: 3.5em !important;
        text-transform: uppercase;
    }

    /* PESTAÑAS (TABS) */
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; border-radius: 5px; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; font-weight: bold !important; }
    .stTabs [aria-selected="true"] { background-color: #C5A059 !important; color: #000000 !important; }

    .stark-header {
        background-color: #004A2F;
        padding: 15px;
        border-radius: 10px;
        color: #FFFFFF;
        text-align: center;
        border: 2px solid #C5A059;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL (Panel de Firma)
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Logotipo_de_Carabineros_de_Chile.svg/640px-Logotipo_de_Carabineros_de_Chile.svg.png", width=140)
    st.markdown("### 🟢 CONFIGURACIÓN DE FIRMA")
    n_f = st.text_input("Nombre Oficial", value="DIANA SANDOVAL ASTUDILLO")
    g_f = st.text_input("Grado", value="C.P.R. Analista Social")
    c_f = st.text_input("Cargo", value="OFICINA DE OPERACIONES")
    st.markdown("---")
    st.markdown("#### **UNIDAD:**")
    st.write("26ª Comisaría Pudahuel") 
    st.markdown(f"#### **FECHA:** {datetime.now().strftime('%d/%m/%Y')}")

# 4. ENCABEZADO
st.markdown('<div class="stark-header"><h2>CARABINEROS DE CHILE</h2><h3>SISTEMA F.R.I.D.A.Y. | PREFECTURA OCCIDENTE</h3></div>', unsafe_allow_html=True)

# 5. PESTAÑAS RESTAURADAS
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- FUNCION DE GENERACIÓN ---
def generar_word(nombre_plantilla, datos):
    try:
        doc = DocxTemplate(nombre_plantilla)
        # Formato de firma solicitado: Negrita-Normal-Negrita
        rt = RichText()
        rt.add(datos['n'].upper(), bold=True)
        rt.add('\n')
        rt.add(datos['g'], bold=False)
        rt.add('\n')
        rt.add(datos['c'].upper(), bold=True)
        datos['firma_completa'] = rt
        
        # Fecha fondo
        now = datetime.now()
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        datos['fecha_fondo'] = f"PUDAHUEL, {now.day} DE {meses[now.month-1].upper()} DE {now.year}"
        
        doc.render(datos)
        output = io.BytesIO()
        doc.save(output)
        return output.getvalue()
    except:
        return None

# --- PESTAÑA 1: ACTA MENSUAL ---
with tab1:
    with st.form("form_mensual"):
        st.markdown("### 📝 FORMULARIO ACTA MENSUAL")
        col1, col2 = st.columns(2)
        with col1:
            sem = st.text_input("Semana de estudio")
            fec_sesion = st.text_input("Fecha de sesión")
        with col2:
            comp_carab = st.text_input("Compromiso Carabineros")
        
        prob_delictual = st.text_area("Problemática Delictual 26ª Comisaría")
        btn_m = st.form_submit_button("🛡️ PROCESAR ACTA MENSUAL")

    if btn_m:
        datos_m = {