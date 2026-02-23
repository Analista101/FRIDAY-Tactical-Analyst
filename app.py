import streamlit as st
from docxtpl import DocxTemplate, RichText
import io
from datetime import datetime
import os

# 1. CONFIGURACIÓN DEL SISTEMA
st.set_page_config(page_title="PROJECT JARVIS - 26ª Com. Pudahuel", page_icon="🟢", layout="wide")

# 2. INYECCIÓN DE ESTILO TÁCTICO (FUERZA BRUTA)
st.markdown("""
    <style>
    /* FONDO GENERAL BLANCO */
    .stApp { background-color: #FFFFFF !important; }

    /* TODO EL TEXTO EN FONDO BLANCO A NEGRO (Headers, etiquetas, inputs) */
    .stApp, .stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp span {
        color: #000000 !important;
        font-weight: bold !important;
    }

    /* BARRA LATERAL (Mantiene su estilo institucional) */
    [data-testid="stSidebar"] { background-color: #004A2F !important; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }

    /* BOTONES VERDES CON LETRA BLANCA (REPARACIÓN CRÍTICA) */
    div.stButton > button, .stFormSubmitButton > button {
        background-color: #004A2F !important;
        color: #FFFFFF !important; /* Letra blanca en botón */
        border: 2px solid #C5A059 !important;
        font-weight: bold !important;
        width: 100% !important;
        height: 3.5em !important;
        text-transform: uppercase;
    }

    /* PESTAÑAS (TABS) */
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; }
    
    /* ENCABEZADO STARK */
    .stark-header {
        background-color: #004A2F;
        padding: 15px;
        border-radius: 10px;
        color: #FFFFFF !important; /* Letra blanca en fondo verde */
        text-align: center;
        border: 2px solid #C5A059;
        margin-bottom: 25px;
    }
    .stark-header h2, .stark-header h3 { color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL
with st.sidebar:
    # Intento de carga de logo local
    if os.path.exists("logo.png"):
        st.image("logo.png", width=160)
    else:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Logotipo_de_Carabineros_de_Chile.svg/640px-Logotipo_de_Carabineros_de_Chile.svg.png", width=140)
    
    st.markdown("---")
    st.markdown("#### **UNIDAD:**")
    st.write("26ª Comisaría Pudahuel") 
    st.write(f"FECHA: {datetime.now().strftime('%d/%m/%Y')}")

# 4. ENCABEZADO
st.markdown('<div class="stark-header"><h2>CARABINEROS DE CHILE</h2><h3>SISTEMA F.R.I.D.A.Y. | PREFECTURA OCCIDENTE</h3></div>', unsafe_allow_html=True)

# 5. MOTOR DE GENERACIÓN JARVIS
def generar_word(nombre_plantilla, datos):
    try:
        doc = DocxTemplate(nombre_plantilla)
        
        # PROTOCOLO DE FIRMA (IMAGEN 25fb57)
        # 1. Opción RichText (Para mantener negritas)
        rt = RichText()
        rt.add(datos['n_oficial'].upper(), bold=True)
        rt.add('\n')
        rt.add(datos['g_oficial'], bold=False)
        rt.add('\n')
        rt.add(datos['c_oficial'].upper(), bold=True)
        
        # 2. Opción Texto Plano (Si el RichText falla en su Word)
        firma_texto = f"{datos['n_oficial'].upper()}\n{datos['g_oficial']}\n{datos['c_oficial'].upper()}"
        
        # Inyectamos ambas para seguridad
        datos['firma_completa'] = rt
        datos['firma_simple'] = firma_texto
        
        now = datetime.now()
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        datos['fecha_fondo'] = f"PUDAHUEL, {now.day} DE {meses[now.month-1].upper()} DE {now.year}"
        
        doc.render(datos)
        output = io.BytesIO()
        doc.save(output)
        return output.getvalue()
    except Exception as e:
        st.error(f"Error en renderizado: {e}")
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
        st.markdown("### 🖋️ CONFIGURACIÓN DE FIRMA")
        cf1, cf2 = st.columns(2)
        with cf1:
            nom = st.text_input("Nombre del Oficial", value="DIANA SANDOVAL ASTUDILLO")
            gra = st.text_input("Grado", value="C.P.R. Analista Social")
        with cf2:
            car = st.text_input("Cargo", value="OFICINA DE OPERACIONES")
            
        submit = st.form_submit_button("🛡️ PROCESAR ACTA")

    if submit:
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
            st.success("Documento generado con éxito.")
            st.download_button("⬇️ DESCARGAR WORD", archivo_word, f"ACTA_{semana}.docx")