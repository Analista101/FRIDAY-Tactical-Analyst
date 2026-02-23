import streamlit as st
from docxtpl import DocxTemplate, RichText
import io
from datetime import datetime
import os

# 1. CONFIGURACIÓN DEL SISTEMA F.R.I.D.A.Y.
st.set_page_config(page_title="SISTEMA F.R.I.D.A.Y. - 26ª Com. Pudahuel", page_icon="🟢", layout="wide")

# 2. ESTILO TÁCTICO (Letra negra sobre blanco, márgenes verdes, encabezados blancos)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    .stApp label { color: #000000 !important; font-weight: bold !important; }
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        color: #000000 !important;
        border: 2px solid #004A2F !important;
        border-radius: 5px;
    }
    [data-testid="stSidebar"] { background-color: #004A2F !important; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    .stark-header {
        background-color: #004A2F; padding: 15px; border-radius: 10px;
        color: #FFFFFF !important; text-align: center; border: 2px solid #C5A059; margin-bottom: 25px;
    }
    .stark-header h2, .stark-header h3 { color: #FFFFFF !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; }
    div.stButton > button, .stFormSubmitButton > button {
        background-color: #004A2F !important; color: #FFFFFF !important;
        border: 2px solid #C5A059 !important; font-weight: bold !important; width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. MOTOR DE RENDERIZADO (Firma Bookman Old Style 11)
def generar_word(nombre_plantilla, datos):
    try:
        doc = DocxTemplate(nombre_plantilla)
        rt = RichText()
        rt.add(datos['n_oficial'].upper(), bold=True, font='Bookman Old Style', size=22)
        rt.add('\n')
        rt.add(datos['g_oficial'], bold=False, font='Bookman Old Style', size=22)
        rt.add('\n')
        rt.add(datos['c_oficial'].upper(), bold=True, font='Bookman Old Style', size=22)
        datos['firma_completa'] = rt
        
        now = datetime.now()
        meses_n = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
        datos['fecha_fondo'] = f"PUDAHUEL, {now.day} DE {meses_n[now.month-1]} DE {now.year}"
        
        doc.render(datos)
        output = io.BytesIO()
        doc.save(output)
        return output.getvalue()
    except Exception as e:
        st.error(f"Falla en F.R.I.D.A.Y.: {e}")
        return None

# 4. BARRA LATERAL
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=160)
    st.markdown("---")
    st.write("UNIDAD: 26ª Comisaría Pudahuel")
    st.write(f"FECHA: {datetime.now().strftime('%d/%m/%Y')}")

# 5. ENCABEZADO
st.markdown('<div class="stark-header"><h2>CARABINEROS DE CHILE</h2><h3>SISTEMA F.R.I.D.A.Y. | PREFECTURA OCCIDENTE</h3></div>', unsafe_allow_html=True)

# 6. PESTAÑAS
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

with tab1:
    st.info("Módulo de Acta Mensual bloqueado y operativo.")

with tab2:
    with st.form("form_stop_trimestral"):
        st.markdown("### 📈 ANÁLISIS STOP TRIMESTRAL")
        col1, col2 = st.columns(2)
        with col1:
            val_periodo = st.text_input("Periodo (Meses comprendidos entre...)")
            val_fecha_s = st.text_input("Fecha de la Sesión")
        with col2:
            val_asistente = st.text_input("Nombre Asistente Institucional")
            val_grado_as = st.text_input("Grado Asistente")

        st.markdown("---")
        st.markdown("### 🖋️ CONFIGURACIÓN DE FIRMA")
        cf1, cf2 = st.columns(2)
        with cf1:
            nom = st.text_input("Nombre Oficial", value="DIANA SANDOVAL ASTUDILLO", key="n_t")
            gra = st.text_input("Grado", value="C.P.R. Analista Social", key="g_t")
        with cf2:
            car = st.text_input("Cargo", value="OFICINA DE OPERACIONES", key="c_t")

        btn_submit_t = st.form_submit_button("🛡️ GENERAR ACTA TRIMESTRAL")

    if btn_submit_t:
        # Diccionario limpio sin etiquetas de referencia internas
        datos_t = {
            'periodo': val_periodo.upper(),
            'fecha_sesion': val_fecha_s.upper(),
            'asistente': val_asistente.upper(),
            'grado': val_grado_as.upper(),
            'n_oficial': nom,
            'g_oficial': gra,
            'c_oficial': car
        }
        archivo_t = generar_word("ACTA STOP TRIMESTRAL.docx", datos_t)
        if archivo_t:
            st.success("Acta Trimestral generada correctamente.")
            st.download_button("⬇️ DESCARGAR DOCUMENTO", archivo_t, "ACTA_TRIMESTRAL.docx")