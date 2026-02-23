import streamlit as st
from docxtpl import DocxTemplate, RichText
import io
from datetime import datetime
import os

# 1. CONFIGURACIÓN DEL SISTEMA
st.set_page_config(page_title="PROJECT JARVIS - 26ª Com. Pudahuel", page_icon="🟢", layout="wide")

# 2. INYECCIÓN DE ESTILO (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    
    /* BARRA LATERAL VERDE */
    [data-testid="stSidebar"] { background-color: #004A2F !important; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; font-weight: bold !important; }

    /* ETIQUETAS DE FORMULARIO EN NEGRO (Para que resalten en blanco) */
    .stApp label {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }

    /* BOTONES VERDES */
    div.stButton > button, .stFormSubmitButton > button {
        background-color: #004A2F !important;
        color: #FFFFFF !important;
        border: 2px solid #C5A059 !important;
        font-weight: bold !important;
        width: 100% !important;
    }

    /* PESTAÑAS */
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

# 3. BARRA LATERAL
with st.sidebar:
    # Carga del logo local para evitar imagen rota
    if os.path.exists("logo.png"):
        st.image("logo.png", width=160)
    else:
        st.error("Error: logo.png no encontrado en la carpeta.")
    
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

# 5. FUNCION DE GENERACIÓN DE FIRMA Y WORD
def generar_word(nombre_plantilla, datos):
    try:
        doc = DocxTemplate(nombre_plantilla)
        
        # PROTOCOLO DE FIRMA (IMAGEN 25fb57)
        rt = RichText()
        rt.add(datos['n'].upper(), bold=True)
        rt.add('\n')
        rt.add(datos['g'], bold=False)
        rt.add('\n')
        rt.add(datos['c'].upper(), bold=True)
        
        # Inyectar la firma en el diccionario de datos
        datos['firma_completa'] = rt
        
        now = datetime.now()
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        datos['fecha_fondo'] = f"PUDAHUEL, {now.day} DE {meses[now.month-1].upper()} DE {now.year}"
        
        doc.render(datos)
        output = io.BytesIO()
        doc.save(output)
        return output.getvalue()
    except Exception as e:
        st.error(f"Error en motor de firma: {e}")
        return None

# 6. PESTAÑAS
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

with tab1:
    with st.form("form_mensual"):
        st.markdown("### 📝 ACTA MENSUAL")
        col1, col2 = st.columns(2)
        with col1:
            sem = st.text_input("Semana de estudio")
            fec_s = st.text_input("Fecha de sesión")
        with col2:
            comp_c = st.text_input("Compromiso Carabineros")
        prob_d = st.text_area("Problemática Delictual 26ª Comisaría")
        btn_m = st.form_submit_button("🛡️ PROCESAR ACTA")

    if btn_m:
        val_comp = comp_c.upper() if comp_c else "SIN COMPROMISO"
        datos_m = {
            'semana': sem.upper(), 'fecha_sesion': fec_s.upper(),
            'c_carabineros': val_comp, 'problematica': prob_d.upper(),
            'n': n_f, 'g': g_f, 'c': c_f
        }
        archivo = generar_word("ACTA STOP MENSUAL.docx", datos_m)
        if archivo:
            st.download_button("⬇️ DESCARGAR WORD", archivo, f"ACTA_{sem}.docx", key="dw_m")

# (Se mantienen iguales tab2 y tab3 con sus respectivos diccionarios de datos)