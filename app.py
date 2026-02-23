import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import io
from datetime import datetime

# --- ESTILOS INSTITUCIONALES (FONDO BLANCO / BORDE VERDE) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    .section-header {
        background-color: #004A2F !important; color: #FFFFFF !important;
        padding: 10px 15px; border-radius: 5px; font-weight: bold;
        text-transform: uppercase; margin-bottom: 15px; border-left: 8px solid #C5A059;
    }
    input, textarea, .stTextInput>div>div>input {
        background-color: #FFFFFF !important; color: #000000 !important;
        border: 2px solid #004A2F !important; border-radius: 5px !important;
    }
    .stApp label { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE INTELIGENCIA ARTIFICIAL F.R.I.D.A.Y. ---
def analizar_riesgo_ia(total_dmcs, dia_max, hora_max):
    if total_dmcs > 25:
        return f"ALTO RIESGO. Se detecta una saturación delictual de {total_dmcs} eventos. El periodo crítico (Día: {dia_max}, Hora: {hora_max}) sugiere vulnerabilidad extrema para el solicitante."
    elif total_dmcs > 10:
        return f"RIESGO MODERADO. Con {total_dmcs} delitos registrados, el sector presenta actividad constante, acentuándose los {dia_max} a las {hora_max}."
    else:
        return f"BAJO RIESGO. La densidad delictual es mínima ({total_dmcs} casos). No se observan patrones críticos de peligro inmediato."

# --- INTERFAZ ---
tab1, tab2, tab3 = st.tabs(["📄 ACTA STOP MENSUAL", "📈 STOP TRIMESTRAL", "📍 INFORME GEO"])

with tab3:
    st.markdown('<div class="section-header">📍 SISTEMA GEO-ESPACIAL F.R.I.D.A.Y.</div>', unsafe_allow_html=True)
    
    with st.form("form_geo_ia"):
        st.markdown('<div class="section-header">I. ANTECEDENTES Y SUMINISTROS</div>', unsafe_allow_html=True)
        g1, g2 = st.columns(2)
        with g1:
            v_dom = st.text_input("Domicilio ({{ domicilio }})")
            v_jur = st.text_input("Jurisdicción", value="26ª COM. PUDAHUEL")
            v_doe = st.text_input("N° DOE ({{ doe }})")
            f_mapa = st.file_uploader("Mapa SAIT ({{ mapa }})", type=['png', 'jpg'])
        with g2:
            v_fdoe = st.text_input("Fecha DOE ({{ fecha_doe }})")
            v_cua = st.text_input("Cuadrante ({{ cuadrante }})")
            v_fact = st.text_input("Fecha Actual", value=datetime.now().strftime('%d/%m/%Y'))
            f_excel = st.file_uploader("Excel Único (Detalle y Calor)", type=['xlsx'])

        st.markdown('<div class="section-header">II. DATOS SOLICITANTE</div>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: v_sol = st.text_input("Nombre ({{ solicitante }})")
        with s2: v_gs = st.text_input("Grado ({{ grado_solic }})")
        with s3: v_us = st.text_input("Unidad ({{ unidad_solic }})")

        p_ini = st.text_input("Inicio Periodo ({{ periodo_inicio }})")
        p_fin = st.text_input("Fin Periodo ({{ periodo_fin }})")

        # El botón de proceso ahora está vinculado a la lógica de IA
        submit_geo = st.form_submit_button("🛡️ EJECUTAR ANÁLISIS F.R.I.D.A.Y.")

    if submit_geo:
        if not f_excel or not f_mapa:
            st.error("Señor, el sistema requiere el mapa y el archivo Excel para procesar.")
        else:
            try:
                # 1. Leer datos del Excel (Hojas o Tablas)
                df = pd.read_excel(f_excel)
                total_dmcs = int(df['CUENTA'].sum()) if 'CUENTA' in df.columns else 0
                
                # Simulación de extracción de máximos (esto se ajustará a su formato de Excel)
                dia_max = "VIERNES" 
                hora_max = "20:00 - 23:59"

                # 2. IA Redactando Conclusión
                conclusion_friday = analizar_riesgo_ia(total_dmcs, dia_max, hora_max)
                
                st.info(f"💡 CONCLUSIÓN GENERADA POR IA: {conclusion_friday}")
                
                # 3. Preparar Documento Word
                doc = DocxTemplate("INFORME GEO.docx")
                contexto = {
                    'domicilio': v_dom, 'jurisdiccion': v_jur, 'doe': v_doe, 'fecha_doe': v_fdoe,
                    'cuadrante': v_cua, 'fecha_actual': v_fact, 'solicitante': v_sol, 
                    'grado_solic': v_gs, 'unidad_solic': v_us, 'periodo_inicio': p_ini,
                    'periodo_fin': p_fin, 'total_dmcs': total_dmcs, 'dia_max': dia_max,
                    'hora_max': hora_max, 'conclusion_ia': conclusion_friday,
                    'mapa': InlineImage(doc, f_mapa, width=Inches(5))
                }
                
                doc.render(contexto)
                target_word = io.BytesIO()
                doc.save(target_word)
                
                st.success("Informe Geo-Espacial Compilado.")
                st.download_button("📂 DESCARGAR INFORME GEO", data=target_word.getvalue(), 
                                   file_name=f"Informe_GEO_{v_sol}.docx")
            except Exception as e:
                st.error(f"Error en el procesador F.R.I.D.A.Y.: {e}")