import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import datetime
import locale

# Configuración de idioma para fecha en español
try:
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
except:
    pass # Respaldo si el servidor no tiene el locale instalado

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="F.R.I.D.A.Y. - 26ª Com. Pudahuel", page_icon="🟢", layout="wide")

# 2. ESTILO TÁCTICO (CSS)
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; }
    .stApp { background-color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #004A2F !important; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; font-weight: bold !important; }
    .header-institucional {
        background-color: #004A2F;
        padding: 15px;
        border-radius: 10px;
        color: #FFFFFF !important;
        text-align: center;
        border: 2px solid #C5A059;
    }
    label, .stMarkdown p, .stTextInput label, .stTextArea label {
        color: #004A2F !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
    }
    div.stButton > button {
        background-color: #004A2F !important;
        color: #FFFFFF !important;
        border: 2px solid #C5A059 !important;
        font-weight: bold !important;
    }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F; border-radius: 5px; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #C5A059 !important; color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/a2/Logotipo_de_Carabineros_de_Chile.svg", width=130)
    st.markdown("### 🟢 SISTEMA OPERATIVO")
    st.markdown("---")
    st.markdown("#### **UNIDAD:** 26ª Com. Pudahuel")
    st.markdown("#### **ANALISTA:** D. Sandoval A.")
    st.markdown(f"#### **FECHA:** {datetime.now().strftime('%d/%m/%Y')}")

# 4. ENCABEZADO
st.markdown("""
    <div class="header-institucional">
        <h2 style="color: white; margin:0; font-size: 1.8rem;">CARABINEROS DE CHILE</h2>
        <h3 style="color: #C5A059; margin:0; font-size: 1.2rem;">SISTEMA F.R.I.D.A.Y. | PREFECTURA OCCIDENTE</h3>
    </div>
    """, unsafe_allow_html=True)

# 5. LÓGICA DE GENERACIÓN
def generar_word(nombre_plantilla, datos):
    try:
        doc = DocxTemplate(nombre_plantilla)
        # Fecha completa para el fondo del documento
        fecha_larga = datetime.now().strftime('%d de %B de %Y')
        datos['fecha_fondo'] = f"Pudahuel, {fecha_larga}".upper()
        
        doc.render(datos)
        output = io.BytesIO()
        doc.save(output)
        return output.getvalue()
    except:
        st.error(f"Error: No se encontró el archivo '{nombre_plantilla}' en el repositorio.")
        return None

# 6. PESTAÑAS
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

with tab1:
    with st.form("form_mensual"):
        c1, c2 = st.columns(2)
        with c1:
            semana = st.text_input("Semana de estudio")
            fecha_sesion = st.text_input("Fecha de sesión")
        with c2:
            c_carabineros = st.text_input("Compromiso Carabineros")
        problematica = st.text_area("Problemática Delictual 26ª Comisaría")
        submit_mensual = st.form_submit_button("🛡️ PROCESAR ACTA MENSUAL")

    if submit_mensual:
        # TODO A MAYÚSCULAS PARA EL ACTA MENSUAL
        datos = {
            'semana': semana.upper(),
            'fecha_sesion': fecha_sesion.upper(),
            'c_carabineros': (c_carabineros if c_carabineros else "SIN COMPROMISO").upper(),
            'problematica': problematica.upper(),
            'nom_oficial': "DIANA SANDOVAL ASTUDILLO",
            'grado_oficial': "C.P.R. Analista Social",
            'cargo_oficial': "OFICINA DE OPERACIONES"
        }
        archivo = generar_word("ACTA STOP MENSUAL.docx", datos)
        if archivo:
            st.download_button(label="⬇️ DESCARGAR ACTA EN MAYÚSCULAS", data=archivo, file_name=f"ACTA_STOP_{semana}.docx")

with tab2:
    with st.form("form_trimestral"):
        periodo = st.text_input("Periodo comprendido")
        cap_bustos = st.text_input("Nombre Comisario Subrogante")
        c_otros = st.text_input("Otros Compromisos")
        submit_trim = st.form_submit_button("📊 PROCESAR TRIMESTRAL")
    
    if submit_trim:
        datos = {
            'periodo': periodo, 
            'cap_bustos': cap_bustos,
            'compromiso': c_otros if c_otros else "SIN COMPROMISO" # Defecto si está vacío
        }
        archivo = generar_word("ACTA STOP TRIMESTRAL.docx", datos)
        if archivo:
            st.download_button(label="⬇️ DESCARGAR TRIMESTRAL", data=archivo, file_name="ACTA_TRIMESTRAL.docx")

with tab3:
    # Lógica similar para Informe GEO...
    st.info("Módulo GEO listo para transcripción.")