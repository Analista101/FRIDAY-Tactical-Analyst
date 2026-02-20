import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import datetime

# Configuración de página con estética institucional
st.set_page_config(page_title="F.R.I.D.A.Y. - Analista Criminal", page_icon="🟢")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { background-color: #004A2F; color: white; width: 100%; }
    </style>
    """, unsafe_allow_index=True)

st.title("🟢 F.R.I.D.A.Y.")
st.subheader("Unidad de Análisis Criminal - 26° Com. Pudahuel")

# Selección de Informe
tipo_informe = st.selectbox("Seleccione el tipo de informe a generar:", 
                            ["Acta STOP Mensual", "Acta STOP Trimestral", "Informe GEO"])

with st.form("datos_informe"):
    datos = {}
    
    if tipo_informe == "Acta STOP Mensual":
        datos['semana'] = st.text_input("Semana de estudio (ej: 01 al 07)") [cite: 4]
        datos['fecha_sesion'] = st.text_input("Fecha de sesión") [cite: 5]
        datos['problematica'] = st.text_area("Problemática detectada") [cite: 22]
        datos['c_carabineros'] = st.text_input("Compromiso Carabineros") [cite: 24]
        datos['nom_oficial'] = "DIANA SANDOVAL ASTUDILLO" # Por defecto según su perfil [cite: 93]

    elif tipo_informe == "Acta STOP Trimestral":
        datos['periodo'] = st.text_input("Periodo (ej: Octubre - Diciembre)") [cite: 40]
        datos['cap_bustos'] = st.text_input("Nombre Comisario Subrogante") [cite: 43]

    elif tipo_informe == "Informe GEO":
        datos['domicilio'] = st.text_input("Domicilio del análisis") [cite: 68]
        datos['doe'] = st.text_input("Número de DOE") [cite: 75]
        datos['cuadrante'] = st.text_input("Cuadrante") [cite: 78]
        datos['total_dmcs'] = st.number_input("Total DMCS detectados", step=1) [cite: 85]
        datos['conclusion_ia'] = st.text_area("Conclusión del Analista") [cite: 91]

    submitted = st.form_submit_button("PROCESAR DOCUMENTO")

    if submitted:
        # Mapeo de archivos según su selección
        archivos = {
            "Acta STOP Mensual": "ACTA STOP MENSUAL.docx",
            "Acta STOP Trimestral": "ACTA STOP TRIMESTRAL.docx",
            "Informe GEO": "INFORME GEO.docx"
        }
        
        try:
            doc = DocxTemplate(archivos[tipo_informe])
            datos['fecha_hoy'] = datetime.now().strftime('%d/%m/%Y') [cite: 29, 62]
            datos['fecha_actual'] = datetime.now().strftime('%d/%m/%Y') [cite: 69]
            
            doc.render(datos)
            
            # Guardar en memoria para descarga
            bio = io.BytesIO()
            doc.save(bio)
            
            st.success(f"✅ {tipo_informe} generado con éxito.")
            st.download_button(
                label="⬇️ DESCARGAR WORD",
                data=bio.getvalue(),
                file_name=f"Generado_{tipo_informe}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        except Exception as e:
            st.error(f"Error: Asegúrese de que el archivo {archivos[tipo_informe]} esté en el mismo nivel que app.py")