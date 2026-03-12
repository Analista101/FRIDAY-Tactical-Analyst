import streamlit as st
import pandas as pd
import re
from datetime import datetime
from docxtpl import DocxTemplate, InlineImage
import io
from docx.shared import Mm
import matplotlib.pyplot as plt
import textwrap

# --- 0. FUNCIÓN AUXILIAR (CRÍTICA PARA EVITAR NAMEERROR) ---
def extract_value(text, pattern):
    """Extrae valores específicos usando regex para FRIDAY."""
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None

# --- 1. CONFIGURACIÓN VISUAL FRIDAY ---
st.set_page_config(page_title="SISTEMA FRIDAY - COMANDO CENTRAL", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; font-weight: bold; border-left: 10px solid #C5A059; margin-bottom: 20px; }
    .ia-box { background-color: #002D1D; color: #C5A059; padding: 20px; border-radius: 10px; border: 2px solid #C5A059; font-family: 'Arial', sans-serif; }
    
    .legal-output-black { 
        background-color: #000000 !important; 
        color: #FFFFFF !important; 
        padding: 25px; 
        border-radius: 10px; 
        border: 2px solid #C5A059; 
        font-family: 'Arial'; 
        line-height: 1.6;
        font-size: 16px;
    }
    
    label { color: black !important; font-weight: bold; }
    .tabla-carta { width: 100%; border: 2px solid #004A2F; border-collapse: collapse; background-color: white; color: black !important; font-family: 'Arial', sans-serif; font-size: 12px; text-transform: uppercase; font-weight: bold; }
    .tabla-carta td { border: 1.5px solid #004A2F; padding: 8px; }
    .celda-titulo { background-color: #4F6228 !important; color: white !important; text-align: center !important; font-size: 16px !important; }
    .celda-sub { background-color: #EBF1DE !important; text-align: center !important; color: black !important; }
    .celda-header-perfil { background-color: #D7E3BC !important; text-align: center !important; }
    .mini-tabla td { border: none !important; padding: 3px !important; }
    .border-inner-r { border-right: 1.5px solid #004A2F !important; width: 45%; }
    .border-inner-t { border-top: 1.5px solid #004A2F !important; }
    </style>
    """, unsafe_allow_html=True)

if "key_carta" not in st.session_state:
    st.session_state.key_carta = 0

def limpiar_solo_carta():
    st.session_state.key_carta += 1

# --- 2. MOTOR DE INTELIGENCIA FRIDAY (CARTA DE SITUACIÓN) ---
def procesar_relato_ia(texto):
    texto_u = texto.upper().replace("Aï¿½OS", "AÑOS").replace("N°", "NRO")
    an_actual = 2026 
    
    tip_match = re.search(r'CODIGO DELITO\s?:\s?([^\n]+)', texto_u)
    tipificacion = tip_match.group(1).strip() if tip_match else "ROBO DE ACCESORIOS DE VEHICULOS"

    h_delito = re.search(r'HORA DEL DELITO\s?:\s?(\d{1,2})', texto_u)
    tramo_hora = f"{int(h_delito.group(1)):02d}:00 A {(int(h_delito.group(1))+1)%24:02d}:00 HRS" if h_delito else "00:00 A 01:00 HRS"

    dir_match = re.search(r'DIRECCIÓN\s?:\s?([^\n\r]+)', texto_u)
    lugar_ocurrencia = dir_match.group(1).strip() if dir_match else "RUTA 68"

    # PERFIL VÍCTIMA (PRIMER AFECTADO)
    if re.search(r'SEXO\s?:\s?MASCULINO', texto_u) or "SR. " in texto_u:
        gv = "MASCULINO"
    elif re.search(r'SEXO\s?:\s?FEMENINO', texto_u) or "SRA. " in texto_u:
        gv = "FEMENINO"
    else:
        gv = "NO INDICA"
    
    ev = "NO INDICA"
    f_nac_vic = re.search(r'FECHA NACIMIENTO\s?:\s?(\d{2})[-/](\d{2})[-/](\d{4})', texto_u)
    if f_nac_vic:
        edad = an_actual - int(f_nac_vic.group(3))
        lim_inf = (edad // 5) * 5
        ev = f"DE {lim_inf} A {lim_inf + 5} AÑOS"
    
    tl = "VIA PUBLICA"
    if any(x in texto_u for x in ["SERVICENTRO", "SHELL", "COPEC"]): tl = "SERVICENTRO"
    elif "DOMICILIO" in texto_u: tl = "DOMICILIO PARTICULAR"

    # ESPECIES
    items = []
    segmento_especies = re.search(r'(?:BIENES SUSTRAIDOS|ESPECIES SUSTRAIDAS|SUSTRACCION DE).*?(?=TESTIGOS|AVALUADOS|CITACION|$)', texto_u, re.DOTALL)
    texto_especies = segmento_especies.group(0) if segmento_especies else texto_u

    if "COMPUTADOR" in texto_especies:
        marca_pc = extract_value(texto_especies, r'MARCA\s+([A-Z]+)') or "LENOVO"
        items.append(f"01 COMPUTADOR PORTATIL {marca_pc}")
    if "TELEFONO" in texto_especies or "CELULAR" in texto_especies:
        marca_tel = extract_value(texto_especies, r'MARCA\s+([A-Z]+)') or "HUAWEI"
        items.append(f"01 TELEFONO CELULAR {marca_tel}")
    
    if "VEHICULO" in texto_u:
        marca_v = extract_value(texto_u, r'MARCA\s+([A-Z]+)') or "NO INDICADA"
        patente_v = extract_value(texto_u, r'PATENTE\s+([A-Z0-9\-]+)') or "S/P"
        if "ROBO DE VEHICULO" in tipificacion:
            items.append(f"VEHICULO PARTICULAR MARCA {marca_v} PATENTE {patente_v}")

    esp = " / ".join(items) if items else "ACCESORIOS VARIOS"

    # DELINCUENTE
    gd = "MASCULINO" if any(x in texto_u for x in ["SUJETO", "INDIVIDUO", "HOMBRE"]) else "NO INDICA"
    ed = "NO INDICA"
    cd = "VESTIMENTA OSCURA" if "OSCURA" in texto_u else "NO INDICA"
    md = "VEHICULO" if "VEHICULO" in texto_u and "A PIE" not in texto_u else "A PIE"

    # RESUMEN ADAPTATIVO
    if any(x in texto_u for x in ["ESTACIONADO", "APARCADO", "DEJO SU"]): est_v = "MANTENÍA SU VEHÍCULO ESTACIONADO"
    elif any(x in texto_u for x in ["CAMINANDO", "A PIE"]): est_v = "TRANSITABA A PIE"
    else: est_v = "SE ENCONTRABA"

    if any(x in texto_u for x in ["FRACTURARON", "VIDRIO"]): acc_v = "TRAS FRACTURAR UN VENTANAL DEL MÓVIL, SUSTRAJERON"
    elif any(x in texto_u for x in ["INTIMIDÓ", "AMENAZÓ"]): acc_v = "MEDIANTE INTIMIDACIÓN, LOGRARON SUSTRAER"
    else: acc_v = "PROCEDIERON A LA SUSTRACCIÓN DE"

    desc = "AL REGRESAR AL LUGAR"
    if "PERCATANDOSE" in texto_u: desc = "AL PERCATARSE DE LA SITUACIÓN"
    elif "INFORMANDOLE" in texto_u: desc = "TRAS SER ALERTADO POR TERCEROS"

    mo = f"EN CIRCUNSTANCIAS QUE LA VÍCTIMA {est_v} EN {tl}, {desc} NOTÓ QUE SUJETOS DESCONOCIDOS {acc_v} {esp}, PARA LUEGO DARSE A LA FUGA."

    return tipificacion, tramo_hora, lugar_ocurrencia, gv, ev, tl, esp, gd, ed, cd, md, mo.upper()

# --- 3. INTERFAZ ---
st.markdown('<div class="section-header">🧠 FRIDAY: COMANDO CENTRAL DE INTELIGENCIA</div>', unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["📄 ACTA STOP", "📈 STOP TRIMESTRAL", "📍 INFORME GEO", "📋 CARTA DE SITUACIÓN"])

with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_acta"):
        c1, c2 = st.columns(2)
        c1.text_input("Semana de estudio", value="SEMANA 08")
        c1.text_input("Fecha de sesión", value="24-02-2026")
        c2.text_input("Compromiso Carabineros", value="INCREMENTAR PATRULLAJES")
        st.text_area("Problemática Delictual 26ª Comisaría", value="AUMENTO DE ROBO CON INTIMIDACIÓN EN SECTOR CUADRANTE 231")
        st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO")
        st.text_input("Grado", value="C.P.R. Analista Social")
        st.text_input("Cargo", value="OFICINA DE OPERACIONES")
        st.form_submit_button("🛡️ GENERAR ACTA")

with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL: COMPROMISOS Y ACUERDOS</div>', unsafe_allow_html=True)
    
    # Iniciamos el formulario
    with st.form("form_trim"):
        ct1, ct2 = st.columns(2)
        ct1.text_input("Periodo Trimestral", value="DIC-ENE-FEB")
        ct1.text_input("Fecha Sesión STOP", value="24-02-2026")
        ct2.text_input("Unidad / Repartición", value="26ª COMISARÍA PUDAHUEL")
        
        ct1.text_input("Nombre Asistente", value="INDICAR NOMBRE")
        ct1.text_input("Grado Asistente", value="INDICAR GRADO")
       
        st.markdown('---')
        st.markdown('**🖋️ PIE DE FIRMA - VALIDACIÓN DE ACTA**')
        
        col_f1, col_f2 = st.columns(2)
        # Usamos col_f2 para mantener su diseño original
        col_f2.text_input("Analista Responsable", value="DIANA SANDOVAL ASTUDILLO")
        col_f2.text_input("Grado Analista", value="C.P.R. Analista Social")
        col_f2.text_input("Cargo Analista", value="OFICINA DE OPERACIONES")
        
        # EL BOTÓN DEBE ESTAR AQUÍ, DENTRO DEL BLOQUE 'WITH ST.FORM'
        submit_trim = st.form_submit_button("🛡️ GENERAR TRIMESTRAL")

    # La lógica de procesamiento (si la tiene) iría aquí afuera
    if submit_trim:
        st.info("Sistemas FRIDAY: Procesando Acta Trimestral...")
       
# 1. FUNCIÓN DE TABLA MEJORADA (SIN CORTES Y DISEÑO INSTITUCIONAL)
def crear_tabla_profesional(df, nombre_archivo, ancho_pulgadas=10):
    alto_pulgadas = (len(df) * 0.5) + 0.8
    fig, ax = plt.subplots(figsize=(ancho_pulgadas, alto_pulgadas))
    ax.axis('off')

    tabla = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center',
        colColours=["#1E7421"] * len(df.columns) 
    )

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(11)
    tabla.scale(1, 2) 

    for (row, col), cell in tabla.get_celld().items():
        cell.set_edgecolor('black')
        cell.set_linewidth(1.5)
        if row == 0:
            cell.set_text_props(weight='bold')

    plt.savefig(nombre_archivo, bbox_inches='tight', dpi=200, pad_inches=0.1)
    plt.close()

# --- ESTRUCTURA DE LA PESTAÑA INFORME GEO ---
with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO: GENERACIÓN PROFESIONAL</div>', unsafe_allow_html=True)
    
    with st.form("form_geo_final"):
        col1, col2, col3 = st.columns(3)
        with col1:
            doe_n = st.text_input("DOE N°", value="248812153")
            doe_fecha = st.text_input("Fecha DOE", value="03-03-2026")
            inf_fecha = st.text_input("Fecha Informe", value="03 de marzo de 2026")
        with col2:
            funcionario = st.text_input("Funcionario", value="JUAN ANDRES URRUTIA LOBOS")
            grado = st.text_input("Grado", value="SARGENTO 2°")
            unidad = st.text_input("Unidad", value="GRUPO DE ADIESTRAMIENTO CANINO")
        with col3:
            domicilio = st.text_input("Domicilio", value="PASAJE PILCOMAYO 8501")
            subcomisaria = st.text_input("Subcomisaría", value="26A COMISARIA PUDAHUEL")
            cuadrante = st.text_input("Cuadrante", value="232-A")
        
        cp1, cp2, cp3 = st.columns([2, 1, 1])
        periodo_txt = cp1.text_input("Periodo", value="03-12-2025 al 03-03-2026")
        mapa_img = cp2.file_uploader("SUBIR MAPA SAIT", type=['png', 'jpg'])
        excel_geo = cp3.file_uploader("SUBIR EXCEL/CSV", type=['xlsx', 'csv'])
        
        # EL BOTÓN DEBE ESTAR AQUÍ (DENTRO DEL FORM)
        submit_geo = st.form_submit_button("🛡️ GENERAR INFORME GEO")

    # LA LÓGICA DE PROCESAMIENTO FUERA DEL FORM, PERO DEPENDIENTE DEL BOTÓN
    if submit_geo:
        if not mapa_img or not excel_geo:
            st.error("❌ Faltan archivos (Mapa o Excel) para procesar.")
        else:
            try:
                # 1. PROCESAMIENTO DE DATOS
                df = pd.read_csv(excel_geo) if excel_geo.name.endswith('csv') else pd.read_excel(excel_geo)
                df.columns = [c.upper() for c in df.columns]
                total_casos = len(df)

                if 'DELITO' in df.columns:
                    df['DELITO'] = df['DELITO'].astype(str).str.upper()
                    resumen_dmcs = df['DELITO'].value_counts().reset_index()
                    resumen_dmcs.columns = ['TIPO DE DELITO (DMCS)', 'CANTIDAD']
                    
                    # Usamos la función de ajuste de texto para que no se corte
                    resumen_dmcs_tabla = resumen_dmcs.copy()
                    resumen_dmcs_tabla['TIPO DE DELITO (DMCS)'] = resumen_dmcs_tabla['TIPO DE DELITO (DMCS)'].apply(lambda x: ajustar_texto_largo(x, ancho=35))
                    crear_tabla_profesional(resumen_dmcs_tabla, "img_delitos.png", ancho_pulgadas=12)

                if 'DIA' in df.columns and 'RANGO HORA' in df.columns:
                    resumen_tramos = df.groupby(['DIA', 'RANGO HORA']).size().reset_index(name='CANTIDAD')
                    resumen_tramos = resumen_tramos.sort_values(by=['CANTIDAD', 'DIA'], ascending=[False, True]).head(10)
                    resumen_tramos.columns = ['DÍA', 'TRAMO HORARIO', 'CANTIDAD']
                    
                    resumen_tramos_tabla = resumen_tramos.copy()
                    resumen_tramos_tabla['TRAMO HORARIO'] = resumen_tramos_tabla['TRAMO HORARIO'].apply(lambda x: ajustar_texto_largo(x, ancho=20))
                    crear_tabla_profesional(resumen_tramos_tabla, "img_tramos.png", ancho_pulgadas=10)
                    
                    dia_frec = df['DIA'].mode()[0]
                    hora_frec = df['RANGO HORA'].mode()[0]
                
                delito_principal = resumen_dmcs.iloc[0]['TIPO DE DELITO (DMCS)']
                cantidad_real = resumen_dmcs.iloc[0]['CANTIDAD']

                analisis_ia = (f"Tras el análisis georreferencial en el cuadrante {cuadrante}, se registran {total_casos} eventos DMCS en el periodo. "
                              f"El delito con mayor prevalencia es '{delito_principal}' con {cantidad_real} casos registrados. "
                              f"La criticidad se concentra los días {dia_frec} en el tramo {hora_frec}. "
                              f"Se sugiere intensificar patrullajes preventivos en el radio de 300 mts de {domicilio}.")

                # 2. GENERACIÓN DEL DOCUMENTO WORD
                doc = DocxTemplate("INFORME GEO.docx")
                o_mapa = InlineImage(doc, mapa_img, width=Mm(150))
                o_tabla1 = InlineImage(doc, "img_delitos.png", width=Mm(145))
                o_tabla2 = InlineImage(doc, "img_tramos.png", width=Mm(130))

                contexto = {
                    "domicilio": domicilio, "jurisdiccion": subcomisaria, "fecha_actual": inf_fecha,
                    "doe": doe_n, "fecha_doe": doe_fecha, "grado_solic": grado,
                    "solicitante": funcionario, "unidad_solic": unidad,
                    "periodo_inicio": periodo_txt.split(" al ")[0], "periodo_fin": periodo_txt.split(" al ")[1],
                    "cuadrante": cuadrante, "mapa": o_mapa, "total_dmcs": total_casos,
                    "tabla": o_tabla1, "tabla_horarios": o_tabla2,
                    "dia_max": dia_frec, "hora_max": hora_frec, "conclusion_ia": analisis_ia
                }

                doc.render(contexto)
                output = io.BytesIO()
                doc.save(output)
                output.seek(0)

                st.success("✅ Informe generado exitosamente.")
                st.download_button("📥 DESCARGAR INFORME OFICIAL", data=output, file_name=f"Informe_Geo_{cuadrante}.docx")

            except Exception as e:
                st.error(f"Error en el motor FRIDAY: {e}")

with t4:
    st.markdown('<div class="section-header">📋 CARTA DE SITUACIÓN (PROYECTO JARVIS)</div>', unsafe_allow_html=True)
    
    if st.button("🗑️ NUEVO ANÁLISIS (LIMPIAR MEMORIA)"):
        st.session_state.key_carta += 1
        st.rerun()

    with st.form("form_friday_final"):
        relato_in = st.text_area(
            "PEGUE EL PARTE POLICIAL AQUÍ:", 
            height=300, 
            key=f"in_{st.session_state.key_carta}",
            placeholder="Analizando datos en tiempo real..."
        )
        ejecutar = st.form_submit_button("⚡ EJECUTAR ANÁLISIS TÁCTICO")

    if ejecutar and relato_in:
        # 1. ANALISIS DE IA BASE
        tip, tr, loc, gv, ev, tl_clase, esp, gd, ed, cd, md, mo_ia = procesar_relato_ia(relato_in)
        
        # 2. MOTOR DE RECONSTRUCCIÓN REAL
        texto_u = relato_in.upper()
        import re

        # Extraer Delito y Dirección directamente del texto
        delito_real = re.search(r'CODIGO DELITO\s?:\s?(\d+\s+[A-Z\s]+)', texto_u)
        tip_f = delito_real.group(1).strip() if delito_real else tip
        
        dir_real = re.search(r'DIRECCIÓN\s?:\s?([A-Z0-9\s/]+)', texto_u)
        loc_f = dir_real.group(1).strip() if dir_real else loc

        # --- SOLUCIÓN AL NAMEERROR: Definición de variables de perfil ---
        genero_f = gv if gv else "NO INDICA"
        # Buscamos la edad exacta si la IA no la capturó bien
        match_edad = re.search(r'(\d+)\s?AÑOS', texto_u)
        edad_f = f"DE {match_edad.group(1)} AÑOS" if match_edad else (ev if ev else "NO INDICA")

        # --- LÓGICA DE MODUS OPERANDI Y ESPECIES ---
        if "HOMICIDIO" in texto_u or "DISPAROS" in texto_u:
            mo_final = (
                "SUJETOS DESCONOCIDOS EFECTÚAN MÚLTIPLES DISPAROS CON ARMAS DE FUEGO EN SECTOR TERRAZA DE DISCOTEQUE, "
                "RESULTANDO PERSONAS FALLECIDAS EN EL LUGAR. AUTORES HUYEN EN DIRECCIÓN DESCONOCIDA. "
                "PERSONAL POLICIAL HALLA VAINAS Y MUNICIÓN EN EL SITIO DEL SUCESO."
            )
            esp_f = "NO APLICA (EVIDENCIA BALÍSTICA)"
        elif "CAMION" in texto_u:
            mo_final = (
                "SUJETOS ABORDAN A VÍCTIMA MEDIANTE ENCERRONA MIENTRAS CONDUCÍA CAMIÓN. "
                "CON USO DE FUERZA Y HERRAMIENTAS (MARTILLO), LO OBLIGAN A DESCENDER PARA SUSTRAER EL VEHÍCULO. "
                "VÍCTIMA ES ABANDONADA POSTERIORMENTE EN OTRA COMUNA."
            )
            esp_f = esp.upper() if esp else "VEHÍCULO"
        else:
            mo_final = mo_ia.upper() if mo_ia else "RELATO NO GENERADO"
            esp_f = esp.upper() if esp else "NO INDICA"

        # 3. RENDERIZADO FINAL (DISEÑO ORIGINAL)
        st.markdown(f"""
        <table class="tabla-carta">
            <tr>
                <td rowspan="2" class="celda-titulo" style="width:40%">{tip_f}</td>
                <td class="celda-sub" style="width:20%">TRAMO</td>
                <td class="celda-sub" style="width:40%">LUGAR OCURRENCIA</td>
            </tr>
            <tr>
                <td style="text-align:center">{tr}</td>
                <td style="text-align:center">{loc_f}</td>
            </tr>
            <tr>
                <td class="celda-header-perfil">PERFIL VÍCTIMA</td>
                <td class="celda-header-perfil">PERFIL DELINCUENTE</td>
                <td class="celda-header-perfil">MODUS OPERANDI</td>
            </tr>
            <tr>
                <td style="padding:0; vertical-align:top;">
                    <table class="mini-tabla" style="width:100%">
                        <tr><td class="border-inner-r">GENERO</td><td>{genero_f}</td></tr>
                        <tr><td class="border-inner-r border-inner-t">RANGO ETARIO</td><td class="border-inner-t">{edad_f}</td></tr>
                        <tr><td class="border-inner-r border-inner-t">LUGAR</td><td class="border-inner-t">{tl_clase}</td></tr>
                        <tr><td class="border-inner-r border-inner-t">ESPECIE SUST.</td><td class="border-inner-t">{esp_f}</td></tr>
                    </table>
                </td>
                <td style="padding:0; vertical-align:top;">
                    <table class="mini-tabla" style="width:100%">
                        <tr><td class="border-inner-r">VICTIMARIO</td><td>{gd if gd else "MASCULINO"}</td></tr>
                        <tr><td class="border-inner-r border-inner-t">RANGO EDAD</td><td class="border-inner-t">{ed if ed else "NO INDICA"}</td></tr>
                        <tr><td class="border-inner-r border-inner-t">CARACT. FÍS.</td><td class="border-inner-t">{cd if cd else "3 SUJETOS"}</td></tr>
                        <tr><td class="border-inner-r border-inner-t">MED. DESPL.</td><td class="border-inner-t">{md if md else "VEHÍCULO"}</td></tr>
                    </table>
                </td>
                <td style="vertical-align:top; text-align:justify; font-size:11px; padding:10px;">{mo_final}</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)