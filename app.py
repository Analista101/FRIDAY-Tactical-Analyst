import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import datetime

# Configuración de F.R.I.D.A.Y.
st.set_page_config(page_title="F.R.I.D.A.Y. - Analista Criminal", page_icon="🟢")

st.markdown("""
    <style>
    .stButton>button { background-color: #004A2F; color: white; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🟢 F.R.I.D.A.Y.")
st.subheader("Unidad de Análisis Criminal - 26° Com. Pudahuel")

tipo_informe = st.selectbox("Seleccione el tipo de informe:", 
                            ["Acta STOP Mensual", "Acta STOP Trimestral", "Informe GEO"])

# Iniciamos el formulario
with st.form("formulario_analisis"):
    datos = {}
    
    if tipo_informe == "Acta STOP Mensual":
        st.info("Completando Acta STOP Mensual")
        datos['semana'] = st.text_input("Semana de estudio (ej: 01 al 07)")
        datos['fecha_sesion'] = st.text_input("Fecha de sesión")
        datos['problematica'] = st.text_area("Problemática 26ª Comisaría")
        datos['c_carabineros'] = st.text_input("Compromiso Carabineros")
        datos['c_muni'] = st.text_input("Compromiso Municipalidad")
        # Datos fijos para su firma
        datos['nom_oficial'] = "DIANA SANDOVAL ASTUDILLO"
        datos['grado_oficial'] = "C.P.R. Analista Social"
        datos['cargo_oficial'] = "OFICINA DE OPERACIONES"

    elif tipo_informe == "Acta STOP Trimestral":
        st.info("Completando Acta STOP Trimestral")
        datos['periodo'] = st.text_input("Periodo (ej: Octubre - Diciembre)")
        datos['cap_bustos'] = st.text_input("Nombre Capitán Comisario (S)")

    elif tipo_informe == "Informe GEO":
        st.info("Completando Informe Delictual GEO")
        datos['domicilio'] = st.text_input("Domicilio del análisis")
        datos['jurisdiccion'] = st.text_input("Unidad Jurisdiccional (ej: 26ª Comisaría)")
        datos['doe'] = st.text_input("N° de DOE")
        datos['fecha_doe'] = st.text_input("Fecha de DOE")
        datos['cuadrante'] = st.text_input("Cuadrante")
        datos['periodo_inicio'] = st.text_input("Fecha Inicio Análisis")
        datos['periodo_fin'] = st.text_input("Fecha Fin Análisis")
        datos['total_dmcs'] = st.text_input("Total de casos DMCS")
        datos['conclusion_ia'] = st.text_area("V.- CONCLUSIÓN")

    # BOTÓN DE ENVÍO (Debe estar dentro del 'with st.form')
    enviar = st.form_submit_button("GENERAR DOCUMENTO")

# Procesamiento fuera del formulario
if enviar:
    try:
        nombres_archivos = {
            "Acta STOP Mensual": "ACTA STOP MENSUAL.docx",
            "Acta STOP Trimestral": "ACTA STOP TRIMESTRAL.docx",
            "Informe GEO": "INFORME GEO.docx"
        }
        
        doc = DocxTemplate(nombres_archivos[tipo_informe])
        
        # Fechas automáticas según sus plantillas
        datos['fecha_hoy'] = datetime.now().strftime('%d/%m/%Y')
        datos['fecha_actual'] = datetime.now().strftime('%d/%m/%Y')
        
        doc.render(datos)
        
        output = io.BytesIO()
        doc.save(output)
        
        st.success(f"Sistema F.R.I.D.A.Y.: {tipo_informe} listo para descarga.")
        st.download_button(
            label="⬇️ DESCARGAR ARCHIVO OFICIAL",
            data=output.getvalue(),
            file_name=f"{tipo_informe}_{datetime.now().strftime('%Y%m%d')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"Error de acceso: Asegúrese de que el archivo '{nombres_archivos[tipo_informe]}' esté cargado en su GitHub.")