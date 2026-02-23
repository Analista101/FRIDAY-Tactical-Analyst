import streamlit as st
from docxtpl import DocxTemplate, RichText
import io
from datetime import datetime
import os

# 1. CONFIGURACIÓN DEL SISTEMA JARVIS
st.set_page_config(page_title="PROJECT JARVIS - 26ª Com. Pudahuel", page_icon="🟢", layout="wide")

# 2. INYECCIÓN DE ESTILO TÁCTICO REFINADO
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }

    /* TEXTO NEGRO CON MARGEN VERDE SOBRE BLANCO */
    .stApp label { color: #000000 !important; font-weight: bold !important; }
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        color: #000000 !important;
        border: 2px solid #004A2F !important;
        border-radius: 5px;
    }

    /* BARRA LATERAL E INSTITUCIONAL */
    [data-testid="stSidebar"] { background-color: #004A2F !important; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    [data-testid="stSidebar"] button { border: 2px solid #28a745 !important; background-color: rgba(255,255,255,0.1) !important; }

    /* TEXTO BLANCO SOBRE FONDO VERDE (Header y Tabs) */
    .stark-header {
        background-color: #004A2F;
        padding: 15px;
        border-radius: 10px;
        color: #FFFFFF !important;
        text-align: center;
        border: 2px solid #C5A059;
        margin-bottom: 25px;
    }
    .stark-header h2, .stark-header h3 { color: #FFFFFF !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; }

    /* BOTONES DE PROCESAMIENTO */
    div.stButton > button, .stFormSubmitButton > button {
        background-color: #004A2F !important;
        color: #FFFFFF !important;
        border: 2px solid #C5A059 !important;
        font-weight: bold !important;
        width: 100% !important;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. MOTOR DE GENERACIÓN CON FIRMA BOOKMAN 11
def generar_word(nombre_plantilla, datos):
    try:
        doc = DocxTemplate(nombre_plantilla)
        rt = RichText()
        # Protocolo: Negrita-Normal-Negrita (Bookman Old Style 11pt)
        rt.add(datos['n_oficial'].upper(), bold=True, font='Bookman Old Style', size=22)
        rt.add('\n')
        rt.add(datos['g_oficial'], bold=False, font='Bookman Old Style', size=22)
        rt.add('\n')
        rt.add(datos['c_oficial'].upper(), bold=True, font='Bookman Old Style', size=22)
        datos['firma_completa'] = rt
        
        now = datetime.now()
        meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
        datos['fecha_fondo'] = f"PUDAHUEL, {now.day} DE {meses[now.month-1]} DE {now.year}"
        
        doc.render(datos)
        output = io.BytesIO()
        doc.save(output)
        return output.getvalue()
    except Exception as e:
        st.error(f"Fallo en los sistemas: {e}")
        return None

# 4. BARRA LATERAL
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=160)
    st.markdown("---")
    st.write("UNIDAD: 26ª Comisaría Pudahuel")
    st.write(f"FECHA: {datetime.now().strftime('%d/%m/%Y')}")

# 5. ENCABEZADO
st.markdown('<div class="stark-header"><h2>CARABINEROS DE CHILE</h2><h3>SISTEMA F.R.I.D.A.Y. | PREFECTURA OCCIDENTE</h3></div>', unsafe_allow_html=True)

# 6. PESTAÑAS DE OPERACIÓN
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

with tab2: # Módulo Trimestral solicitado
    with st.form("form_trimestral"):
        st.markdown("### 📊 ANÁLISIS STOP TRIMESTRAL")
        col1, col2 = st.columns(2)
        with col1:
            periodo = st.text_input("Periodo de estudio (Semana comprendida)") [cite: 8]
            fec_sesion = st.text_input("Fecha de la sesión") [cite: 30]
        with col2:
            asistente = st.text_input("Asistente Institucional (Nombre)") [cite: 10]
            grado_asist = st.text_input("Grado Asistente") [cite: 10]
        
        st.markdown("---")
        st.markdown("### 🖋️ CONFIGURACIÓN DE FIRMA")
        cf1, cf2 = st.columns(2)
        with cf1:
            nom = st.text_input("Nombre del Oficial", value="DIANA SANDOVAL ASTUDILLO", key="n_trim")
            gra = st.text_input("Grado", value="C.P.R. Analista Social", key="g_trim")
        with cf2:
            car = st.text_input("Cargo", value="OFICINA DE OPERACIONES", key="c_trim")
            
        btn_trim = st.form_submit_button("📊 GENERAR ACTA TRIMESTRAL")

    if btn_trim:
        datos_t = {
            'periodo': periodo.upper(),
            'fecha_sesion': fec_sesion.upper(),
            'asistente': asistente.upper(),
            'grado': grado_asist.upper(),
            'n_oficial': nom,
            'g_oficial': gra,
            'c_oficial': car
        }
        archivo = generar_word("ACTA STOP TRIMESTRAL.docx", datos_t)
        if archivo:
            st.success("Acta Trimestral procesada correctamente.")
            st.download_button("⬇️ DESCARGAR TRIMESTRAL", archivo, "ACTA_TRIMESTRAL.docx")