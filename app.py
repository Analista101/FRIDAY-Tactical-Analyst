import streamlit as st
from docxtpl import DocxTemplate, RichText
import io
from datetime import datetime
import os

# 1. CONFIGURACIÓN DEL SISTEMA JARVIS
st.set_page_config(page_title="PROJECT JARVIS - 26ª Com. Pudahuel", page_icon="🟢", layout="wide")

# 2. INYECCIÓN DE ESTILO (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #004A2F !important; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; font-weight: bold !important; }

    /* ETIQUETAS EN NEGRO PARA RESALTAR EN FONDO BLANCO */
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
        text-transform: uppercase;
    }

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

# 3. BARRA LATERAL (Solo para información de Unidad)
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=160)
    else:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Logotipo_de_Carabineros_de_Chile.svg/640px-Logotipo_de_Carabineros_de_Chile.svg.png", width=140)
    
    st.markdown("---")
    st.markdown("#### **UNIDAD:**")
    st.write("26ª Comisaría Pudahuel") 
    st.markdown(f"#### **FECHA:** {datetime.now().strftime('%d/%m/%Y')}")

# 4. ENCABEZADO
st.markdown('<div class="stark-header"><h2>CARABINEROS DE CHILE</h2><h3>SISTEMA F.R.I.D.A.Y. | PREFECTURA OCCIDENTE</h3></div>', unsafe_allow_html=True)

# 5. FUNCION DE GENERACIÓN DE WORD
def generar_word(nombre_plantilla, datos):
    try:
        doc = DocxTemplate(nombre_plantilla)
        
        # PROTOCOLO DE FIRMA (IMAGEN 25fb57): Negrita-Normal-Negrita
        rt = RichText()
        rt.add(datos['n_oficial'].upper(), bold=True)
        rt.add('\n')
        rt.add(datos['g_oficial'], bold=False)
        rt.add('\n')
        rt.add(datos['c_oficial'].upper(), bold=True)
        
        datos['firma_completa'] = rt
        
        # Fecha fondo para el pie del documento
        now = datetime.now()
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        datos['fecha_fondo'] = f"PUDAHUEL, {now.day} DE {meses[now.month-1].upper()} DE {now.year}"
        
        doc.render(datos)
        output = io.BytesIO()
        doc.save(output)
        return output.getvalue()
    except Exception as e:
        st.error(f"Error en motor JARVIS: {e}")
        return None

# 6. PESTAÑAS
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

with tab1:
    with st.form("form_mensual"):
        st.markdown("### 📋 DATOS DEL ACTA")
        c1, c2 = st.columns(2)
        with c1:
            semana = st.text_input("Semana de estudio")
            fecha_s = st.text_input("Fecha de sesión")
        with c2:
            comp_c = st.text_input("Compromiso Carabineros")
        
        problema = st.text_area("Problemática Delictual 26ª Comisaría")
        
        st.markdown("---")
        st.markdown("### 🖋️ CONFIGURACIÓN DE FIRMA (PIE DE PÁGINA)")
        cf1, cf2 = st.columns(2)
        with cf1:
            nom = st.text_input("Nombre del Oficial", value="DIANA SANDOVAL ASTUDILLO")
            gra = st.text_input("Grado", value="C.P.R. Analista Social")
        with cf2:
            car = st.text_input("Cargo", value="OFICINA DE OPERACIONES")
            
        submit = st.form_submit_button("🛡️ PROCESAR Y GENERAR DOCUMENTO")

    if submit:
        # Validación y Mayúsculas
        datos_finales = {
            'semana': semana.upper(),
            'fecha_sesion': fecha_s.upper(),
            'c_carabineros': (comp_c.upper() if comp_c else "SIN COMPROMISO"),
            'problematica': problema.upper(),
            'n_oficial': nom,
            'g_oficial': gra,
            'c_oficial': car
        }
        
        archivo_word = generar_word("ACTA STOP MENSUAL.docx", datos_finales)
        if archivo_word:
            st.success("Firma procesada correctamente.")
            st.download_button("⬇️ DESCARGAR ACTA", archivo_word, f"ACTA_{semana}.docx")