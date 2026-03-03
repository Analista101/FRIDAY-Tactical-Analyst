import streamlit as st
import pandas as pd
import re
from datetime import datetime
from docxtpl import DocxTemplate, InlineImage
import io
from docx.shared import Mm
import matplotlib.pyplot as plt

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
    with st.form("form_trim"):
        ct1, ct2 = st.columns(2)
        ct1.text_input("Periodo Trimestral", value="DIC-ENE-FEB")
        ct1.text_input("Fecha Sesión STOP", value="24-02-2026")
        ct2.text_input("Unidad / Repartición", value="26ª COMISARÍA PUDAHUEL")
        ct2.text_input("Nivel de Cumplimiento (%)", value="100%")
        
        st.text_area("Compromisos Adquiridos", value="1. Aumento de patrullajes preventivos.\n2. Focalización de delitos en Cuadrante 231.")

        st.markdown('---')
        st.markdown('**🖋️ PIE DE FIRMA - VALIDACIÓN DE ACTA**')
        f1, f2 = st.columns(2)
        f1.text_input("Nombre Asistente", value="INDICAR NOMBRE")
        f1.text_input("Grado Asistente", value="INDICAR GRADO")
        f2.text_input("Analista Responsable", value="DIANA SANDOVAL ASTUDILLO")
        f2.text_input("Grado Analista", value="C.P.R. Analista Social")
        
        st.form_submit_button("🛡️ GENERAR TRIMESTRAL")


# 1. FUNCIÓN PARA CREAR TABLAS CON ESTILO INSTITUCIONAL (COMO IMAGEN)
def crear_tabla_img(df, nombre_archivo, color_header='#2E5A27'): # Verde Institucional
    fig, ax = plt.subplots(figsize=(8, len(df) * 0.4 + 0.7))
    ax.axis('off')
    
    # Crear la tabla
    mpl_table = ax.table(
        cellText=df.values, 
        colLabels=df.columns, 
        cellLoc='center', 
        loc='center',
        colColours=[color_header] * len(df.columns)
    )
    
    # Estilo de fuente y bordes
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(9)
    mpl_table.scale(1.1, 1.4)
    
    for (row, col), cell in mpl_table.get_celld().items():
        cell.set_edgecolor('#D3D3D3') # Gris claro para bordes
        if row == 0:
            cell.set_text_props(weight='bold', color='white') # Texto blanco en encabezado
        else:
            cell.set_facecolor('white')

    plt.savefig(nombre_archivo, bbox_inches='tight', dpi=200)
    plt.close()

with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO: GENERACIÓN INSTITUCIONAL</div>', unsafe_allow_html=True)
    
    with st.form("form_geo"):
        col1, col2, col3 = st.columns(3)
        with col1:
            doe_n = st.text_input("DOE N°", value="248812153")
            doe_fecha = st.text_input("Fecha DOE", value="03-03-2026")
            inf_fecha = st.text_input("Fecha Informe", value="03 de marzo de 2026")
        with col2:
            funcionario = st.text_input("Nombre Funcionario", value="JUAN ANDRES URRUTIA LOBOS")
            grado = st.text_input("Grado", value="SARGENTO 2°")
            unidad = st.text_input("Unidad", value="GRUPO DE ADIESTRAMIENTO CANINO")
        with col3:
            domicilio = st.text_input("Domicilio", value="PASAJE PILCOMAYO 8501")
            subcomisaria = st.text_input("Subcomisaría", value="26A COMISARIA PUDAHUEL")
            cuadrante = st.text_input("Cuadrante", value="232-A")
        
        cp1, cp2, cp3 = st.columns([2, 1, 1])
        periodo_txt = cp1.text_input("Periodo", value="03-12-2025 al 03-03-2026")
        mapa_img = cp2.file_uploader("MAPA SAIT", type=['png', 'jpg'])
        excel_geo = cp3.file_uploader("EXCEL DELITOS", type=['xlsx', 'csv'])
        
        submit_geo = st.form_submit_button("🛡️ GENERAR INFORME OFICIAL")

    # --- INICIO DEL PROCESAMIENTO ---
    if submit_geo:
        if not mapa_img or not excel_geo:
            st.error("Error: Se requiere el Mapa SAIT y el archivo de datos.")
            st.stop()

        try:
            # 1. CARGA DE DATOS Y CONTEO EXACTO
            df = pd.read_csv(excel_geo) if excel_geo.name.endswith('csv') else pd.read_excel(excel_geo)
            
            # Tabla 2: Delitos DMCS
            res_dmcs = df['DELITO'].value_counts().reset_index()
            res_dmcs.columns = ['DELITOS DMCS', 'CANTIDAD']
            crear_tabla_img(res_dmcs, "t_dmcs.png")

            # Tabla 3: Tramos Horarios (Ordenada por mayor a menor)
            res_tramos = df.groupby(['DIA', 'RANGO HORA']).size().reset_index(name='CANTIDAD')
            res_tramos = res_tramos.sort_values('CANTIDAD', ascending=False).head(10)
            res_tramos.columns = ['DÍA', 'TRAMO HORARIO', 'CANTIDAD']
            crear_tabla_img(res_tramos, "t_tramos.png", color_header='#555555') # Gris oscuro

            # 2. IA: CONCLUSIÓN BASADA EN DATOS REALES
            total_casos = len(df)
            top_delito = res_dmcs.iloc[0]['DELITOS DMCS']
            top_cant = res_dmcs.iloc[0]['CANTIDAD'] # CASOS REALES (5 en tu ejemplo)
            dia_max = df['DIA'].mode()[0]
            hora_max = df['RANGO HORA'].mode()[0]

            conclusion_final = (f"Tras el análisis georreferencial en el cuadrante {cuadrante}, se registran {total_casos} eventos DMCS. "
                                f"El delito con mayor prevalencia es '{top_delito}' con un total de {top_cant} casos. "
                                f"La criticidad se concentra los días {dia_max} en el tramo {hora_max}. "
                                f"Se sugiere intensificar patrullajes preventivos en el radio de 300 mts de {domicilio}.")

            # 3. RENDERIZADO EN WORD (IMÁGENES CENTRADAS)
            doc = DocxTemplate("INFORME GEO.docx")
            
            # Objetos de imagen (Ancho controlado para centrado visual)
            o_mapa = InlineImage(doc, mapa_img, width=Mm(145))
            o_dmcs = InlineImage(doc, "t_dmcs.png", width=Mm(130))
            o_tramos = InlineImage(doc, "t_tramos.png", width=Mm(130))

            contexto = {
                "domicilio": domicilio, "jurisdiccion": subcomisaria, "fecha_actual": inf_fecha,
                "doe": doe_n, "fecha_doe": doe_fecha, "grado_solic": grado,
                "solicitante": funcionario, "unidad_solic": unidad,
                "periodo_inicio": periodo_txt.split(" al ")[0], "periodo_fin": periodo_txt.split(" al ")[1],
                "cuadrante": cuadrante,
                "mapa": o_mapa,
                "total_dmcs": total_casos,
                "tabla": o_dmcs,         # SE INSERTA COMO IMAGEN
                "tabla_horarios": o_tramos, # SE INSERTA COMO IMAGEN
                "dia_max": dia_max, "hora_max": hora_max,
                "conclusion_ia": conclusion_final
            }

            doc.render(contexto)
            output = io.BytesIO()
            doc.save(output)
            output.seek(0)

            st.success("✅ Informe generado. Las tablas han sido insertadas como imágenes institucionales.")
            st.download_button("📥 DESCARGAR INFORME FINAL", data=output, file_name=f"Informe_Geo_{cuadrante}.docx")

        except Exception as e:
            st.error(f"Error técnico en FRIDAY: {e}")

with t4:
    st.markdown('<div class="section-header">📋 CARTA DE SITUACIÓN (MATRIZ DINÁMICA)</div>', unsafe_allow_html=True)
    if st.button("🗑️ LIMPIAR RELATO"):
        limpiar_solo_carta()
        st.rerun()
    with st.form("form_carta"):
        relato_in = st.text_area("PEGUE EL RELATO AQUÍ:", height=250, key=f"txt_{st.session_state.key_carta}")
        if st.form_submit_button("⚡ GENERAR CUADRO"):
            if relato_in:
                tip, tr, loc, gv, ev, tl, esp, gd, ed, cd, md, mo = procesar_relato_ia(relato_in)
                st.markdown(f"""
                <table class="tabla-carta">
                    <tr><td rowspan="2" class="celda-titulo" style="width:40%">{tip}</td><td class="celda-sub" style="width:20%">TRAMO</td><td class="celda-sub" style="width:40%">LUGAR OCURRENCIA</td></tr>
                    <tr><td style="text-align:center">{tr}</td><td style="text-align:center">{loc}</td></tr>
                    <tr><td class="celda-header-perfil">PERFIL VÍCTIMA</td><td class="celda-header-perfil">PERFIL DELINCUENTE</td><td class="celda-header-perfil">MODUS OPERANDI</td></tr>
                    <tr>
                        <td style="padding:0; vertical-align:top;"><table class="mini-tabla" style="width:100%">
                            <tr><td class="border-inner-r">GENERO</td><td>{gv}</td></tr>
                            <tr><td class="border-inner-r border-inner-t">RANGO ETARIO</td><td class="border-inner-t">{ev}</td></tr>
                            <tr><td class="border-inner-r border-inner-t">LUGAR</td><td class="border-inner-t">{tl}</td></tr>
                            <tr><td class="border-inner-r border-inner-t">ESPECIE SUST.</td><td class="border-inner-t">{esp}</td></tr>
                        </table></td>
                        <td style="padding:0; vertical-align:top;"><table class="mini-tabla" style="width:100%">
                            <tr><td class="border-inner-r">VICTIMARIO</td><td>{gd}</td></tr>
                            <tr><td class="border-inner-r border-inner-t">RANGO EDAD</td><td class="border-inner-t">{ed}</td></tr>
                            <tr><td class="border-inner-r border-inner-t">CARACT. FÍS.</td><td class="border-inner-t">{cd}</td></tr>
                            <tr><td class="border-inner-r border-inner-t">MED. DESPL.</td><td class="border-inner-t">{md}</td></tr>
                        </table></td>
                        <td style="vertical-align:top; text-align:justify; font-size:11px; padding:10px;">{mo}</td>
                    </tr>
                </table>""", unsafe_allow_html=True)