import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="F.R.I.D.A.Y. - 26ª Com. Pudahuel", page_icon="🟢", layout="wide")

# 2. ESTILO TÁCTICO COMPACTO (CSS)
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; }
    .stApp { background-color: #FFFFFF !important; }
    
    /* BARRA LATERAL */
    [data-testid="stSidebar"] { background-color: #004A2F !important; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; font-weight: bold !important; }

    /* ENCABEZADO */
    .header-institucional {
        background-color: #004A2F;
        padding: 15px;
        border-radius: 10px;
        color: #FFFFFF !important;
        text-align: center;
        border: 2px solid #C5A059;
    }
    
    /* TEXTO CUERPO */
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
        width: 100%;
    }
    
    /* PESTAÑAS */
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F; border-radius: 5px; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #C5A059 !important; color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL
with st.sidebar:
    try:
        st.image("logo.png", width=140)
    except:
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

# 5. SISTEMA DE PESTAÑAS
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

# --- FUNCION DE GENERACIÓN ---
def generar_word(nombre_plantilla, datos):
    try:
        doc = DocxTemplate(nombre_plantilla)
        datos['fecha_actual'] = datetime.now().strftime('%d/%m/%Y')
        doc.render(datos)
        output = io.BytesIO()
        doc.save(output)
        return output.getvalue()
    except Exception as e:
        st.error(f"Error: Asegúrese de que '{nombre_plantilla}' esté en GitHub.")
        return None

# --- PESTAÑA 1: STOP MENSUAL (CORREGIDA) ---
with tab1:
    with st.form("form_mensual"):
        c1, c2 = st.columns(2)
        with c1:
            semana = st.text_input("Semana de estudio", placeholder="Ej: 01 al 07")
            fecha_sesion = st.text_input("Fecha de sesión")
        with c2:
            c_carabineros = st.text_input("Compromiso Carabineros")
            # SE ELIMINÓ COMPROMISO MUNICIPAL
        
        problematica = st.text_area("Problemática Delictual 26ª Comisaría")
        submit_mensual = st.form_submit_button("🛡️ PROCESAR ACTA")

    if submit_mensual:
        datos = {
            'semana': semana,
            'fecha_sesion': fecha_sesion,
            'c_carabineros': c_carabineros,
            'problematica': problematica,
            'nom_oficial': "DIANA SANDOVAL ASTUDILLO",
            'grado_oficial': "C.P.R. Analista Social",
            'cargo_oficial': "OFICINA DE OPERACIONES"
        }
        archivo = generar_word("ACTA STOP MENSUAL.docx", datos)
        if archivo:
            st.download_button(label="⬇️ DESCARGAR ACTA (WORD)", data=archivo, file_name=f"ACTA_STOP_{semana}.docx")

# --- PESTAÑA 2: STOP TRIMESTRAL ---
with tab2:
    with st.form("form_trimestral"):
        periodo = st.text_input("Periodo comprendido")
        cap_bustos = st.text_input("Comisario Subrogante")
        submit_trim = st.form_submit_button("📊 PROCESAR TRIMESTRAL")
    
    if submit_trim:
        datos = {'periodo': periodo, 'cap_bustos': cap_bustos}
        archivo = generar_word("ACTA STOP TRIMESTRAL.docx", datos)
        if archivo:
            st.download_button(label="⬇️ DESCARGAR TRIMESTRAL", data=archivo, file_name="ACTA_TRIMESTRAL.docx")

# --- PESTAÑA 3: INFORME GEO ---
with tab3:
    with st.form("form_geo"):
        col_a, col_b = st.columns(2)
        with col_a:
            domicilio = st.text_input("Domicilio")
            doe = st.text_input("N° DOE")
        with col_b:
            p_inicio = st.text_input("Fecha Inicio")
            total_dmcs = st.text_input("Total Casos")
        conclusion = st.text_area("V.- CONCLUSIÓN")
        submit_geo = st.form_submit_button("🗺️ PROCESAR INFORME GEO")

    if submit_geo:
        datos = {'domicilio': domicilio, 'doe': doe, 'total_dmcs': total_dmcs, 'conclusion_ia': conclusion}
        archivo = generar_word("INFORME GEO.docx", datos)
        if archivo:
            st.download_button(label="⬇️ DESCARGAR INFORME GEO", data=archivo, file_name="INFORME_GEO.docx")