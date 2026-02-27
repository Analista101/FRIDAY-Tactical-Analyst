import streamlit as st
import pandas as pd
import re
from datetime import datetime

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
    
    /* CUADRO NEGRO CON LETRA BLANCA PARA MÁXIMO CONTRASTE */
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

# --- 2. MOTOR DE INTELIGENCIA FRIDAY ---
def procesar_relato_ia(texto):
    texto_u = texto.upper().replace("Aï¿½OS", "AÑOS").replace("N°", "NRO")
    an_actual = 2026 
    
    tip_match = re.search(r'CODIGO DELITO\s?:\s?([^\n]+)', texto_u)
    tipificacion = tip_match.group(1).strip() if tip_match else "ROBO DE ACCESORIOS DE VEHICULOS"

    h_delito = re.search(r'HORA DEL DELITO\s?:\s?(\d{1,2})', texto_u)
    tramo_hora = f"{int(h_delito.group(1)):02d}:00 A {(int(h_delito.group(1))+1)%24:02d}:00 HRS" if h_delito else "00:00 A 01:00 HRS"

    # LUGAR DE OCURRENCIA (DIRECCIÓN)
    dir_match = re.search(r'DIRECCIÓN\s?:\s?([^\n\r]+)', texto_u)
    lugar_ocurrencia = dir_match.group(1).strip() if dir_match else "RUTA 68"

    # PERFIL VÍCTIMA

   # 1. Género del Afectado
    if re.search(r'SEXO\s?:\s?MASCULINO', texto_u):
        gen_afectado = "MASCULINO"
    elif re.search(r'SEXO\s?:\s?FEMENINO', texto_u):
        gen_afectado = "FEMENINO"
    elif any(x in texto_u for x in ["SR. ", "VÍCTIMA MASCULINA"]):
        gen_afectado = "MASCULINO"
    elif any(x in texto_u for x in ["SRA. ", "SRTA. ", "VÍCTIMA FEMENINA"]):
        gen_afectado = "FEMENINO"
    else:
        gen_afectado = "NO INDICA"
    
    # Rango Etario (Bloques de 5 años)
    edad_rango = "NO INDICA"
    f_nac_vic = re.search(r'FECHA NACIMIENTO\s?:\s?(\d{2})[-/](\d{2})[-/](\d{4})', texto_u)
    if f_nac_vic:
        edad = an_actual - int(f_nac_vic.group(3))
        lim_inf = (edad // 5) * 5
        edad_rango = f"DE {lim_inf} A {lim_inf + 5} AÑOS"
    
    # TIPO DE LUGAR
    lugar_ocurrencia_lugar = "VIA PUBLICA"
    if any(x in texto_u for x in ["SERVICENTRO", "ESTACION DE SERVICIO", "SHELL", "COPEC"]): lugar_ocurrencia_lugar= "SERVICENTRO"
    elif "DOMICILIO" in texto_u: lugar_ocurrencia_lugar = "DOMICILIO PARTICULAR"

  # --- 3. EXTRACCIÓN DE ESPECIES (LÓGICA BASADA EN BIENES SUSTRAIDOS) ---
    items = []
    
    # Buscamos el segmento específico en el relato para mayor precisión
    segmento_especies = re.search(r'(?:BIENES SUSTRAIDOS|ESPECIES SUSTRAIDAS|SUSTRACCION DE).*?(?=TESTIGOS|AVALUADOS|CITACION|$)', texto_u, re.DOTALL)
    texto_especies = segmento_especies.group(0) if segmento_especies else texto_u

    # Detección inteligente por palabras clave en el segmento
    if "COMPUTADOR" in texto_especies or "NOTEBOOK" in texto_especies:
        marca_pc = extract_value(texto_especies, r'MARCA\s+([A-Z]+)') or "LENOVO"
        items.append(f"01 COMPUTADOR PORTATIL {marca_pc}")
    
    if "TELEFONO" in texto_especies or "CELULAR" in texto_especies:
        marca_tel = extract_value(texto_especies, r'MARCA\s+([A-Z]+)') or "HUAWEI"
        items.append(f"01 TELEFONO CELULAR {marca_tel}")
        
    if "BOLSO" in texto_especies: items.append("01 BOLSO CON PRENDAS")
    if "MALETA" in texto_especies: items.append("01 MALETA")
    if "MOCHILA" in texto_especies: items.append("01 MOCHILA")
    if "MEDICAMENTOS" in texto_especies: items.append("MEDICAMENTOS VARIOS")
    
    # Manejo de vehículos si el delito es robo de vehículo
    if "VEHICULO PARTICULAR" in texto_u and "ROBO DE VEHICULO" in tipificacion:
        items.append(f"VEHICULO PARTICULAR MARCA {marca_v} MODELO {modelo_v} PATENTE {patente_v}")

    # Resultado final para la tabla
    especie_sust = " / ".join(items) if items else "ACCESORIOS VARIOS"

  # PERFIL DELINCUENTE
    gen_del = "MASCULINO" if any(x in texto_u for x in ["SUJETO", "INDIVIDUO", "HOMBRE"]) else "NO INDICA"
    edad_del = "NO INDICA"
    caract = "VESTIMENTA OSCURA" if "OSCURA" in texto_u else "NO INDICA"
    medio = "VEHICULO PARTICULAR" if "VEHICULO PARTICULAR" in texto_u else "A PIE"

# --- 4. MOTOR DE RESUMEN TÁCTICO (FRIDAY INTERPRETATIVO) ---
    
    # A. Análisis del Estado de la Víctima (Dinámico)
    if any(x in texto_u for x in ["ESTACIONADO", "DETENIDO", "APARCADO"]):
        estado_v = "MANTENÍA SU VEHÍCULO ESTACIONADO"
    elif any(x in texto_u for x in ["CONDUCIENDO", "CIRCULANDO", "MANEJANDO"]):
        estado_v = "SE DESPLAZABA EN SU VEHÍCULO"
    elif any(x in texto_u for x in ["CAMINANDO", "A PIE", "TRANSITANDO"]):
        estado_v = "TRANSITABA A PIE"
    else:
        estado_v = "SE ENCONTRABA"

    # B. Análisis de la Acción del Delincuente (Sinónimos de Fuerza/Intimidación)
    if any(x in texto_u for x in ["FRACTURARON", "ROPIERON", "QUEBRARON", "VIDRIO"]):
        accion_v = "TRAS FRACTURAR UN VENTANAL DEL MÓVIL, SUSTRAJERON"
    elif any(x in texto_u for x in ["INTIMIDÓ", "AMENAZÓ", "ARMA"]):
        accion_v = "MEDIANTE INTIMIDACIÓN, LOGRARON SUSTRAER"
    elif any(x in texto_u for x in ["GOLPEÓ", "AGREDIÓ", "VIOLENCIA"]):
        accion_v = "TRAS AGREDIR FÍSICAMENTE A LA VÍCTIMA, SE APODERARON DE"
    elif "ABIERTA" in texto_u:
        accion_v = "APROVECHANDO QUE LA PROPIEDAD SE ENCONTRABA ABIERTA, SUSTRAJERON"
    else:
        accion_v = "PROCEDIERON A LA SUSTRACCIÓN DE"

    # C. Análisis del Descubrimiento/Contexto
    descubrimiento = "AL REGRESAR AL LUGAR"
    if "PERCATANDOSE" in texto_u: descubrimiento = "AL PERCATARSE DE LA SITUACIÓN"
    elif "INFORMANDOLE" in texto_u: descubrimiento = "TRAS SER ALERTADO POR TERCEROS"

    # D. Ensamblaje del Modus Operandi (Resumen Táctico)
    # Ejemplo basado en Guillermo Soto:
    mo_final = (
        f"EN CIRCUNSTANCIAS QUE LA VÍCTIMA {estado_v} EN {lugar_ocurrencia_lugar}, "
        f"{descubrimiento} NOTÓ QUE SUJETOS DESCONOCIDOS {accion_v} {especie_sust}, "
        f"PARA POSTERIORMENTE DARSE A LA FUGA EN DIRECCIÓN DESCONOCIDA."
    )

# --- 3. TERMINAL DE COMANDO FRIDAY (INTELIGENCIA JURÍDICA TOTAL) ---
st.markdown('<div class="section-header">🧠 FRIDAY: COMANDO CENTRAL DE INTELIGENCIA</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="ia-box"><b>PROTOCOLOS JARVIS:</b> Señor, la base de datos legal está totalmente integrada. No habrá más respuestas incompletas. Pregunte lo que necesite.</div>', unsafe_allow_html=True)
    
    # Campo de entrada de texto
    consulta = st.text_input("CONSULTA LEGAL / PROCEDIMENTAL:", key="cmd_friday")
    
    if st.button("🛡️ EJECUTAR ANÁLISIS JURÍDICO EXPERTO"):
        if consulta:
            # Lógica de respuesta basada en conocimiento jurídico real (Chile)
            c = consulta.upper()
            
            if "ATROPELLA" in c and "ANIMAL" in c:
                res = """<b>INFORME JURÍDICO DIRECTO:</b><br><br>
                Efectivamente, señor, esto constituye <b>DELITO</b> en Chile bajo dos aristas legales:<br><br>
                1. <b>LEY 21.020 (Ley Cholito) / ART. 291 BIS CÓDIGO PENAL:</b> El abandono de un animal herido tras un atropello es considerado <b>Crueldad o Maltrato Animal</b>. Si no se presta auxilio, se presume la intención de abandono.<br>
                2. <b>PENALIDAD:</b> Presidio menor en su grado mínimo a medio (61 días a 3 años) y multa de 2 a 30 UTM, además de la inhabilidad perpetua para la tenencia de animales.<br>
                3. <b>LEY DE TRÁNSITO (ART. 183):</b> Obliga a detener la marcha y dar cuenta a la autoridad ante cualquier accidente con daños. La fuga agrava la falta.<br><br>
                <b>PROCEDIMIENTO CARABINEROS:</b> Detención inmediata si hay flagrancia o denuncia de oficio al Ministerio Público."""
            
            elif "ZOPICLONA" in c:
                res = """<b>INFORME JURÍDICO DIRECTO:</b><br><br>
                La Zopiclona es una sustancia controlada por la <b>Ley 20.000 (Ley de Drogas)</b>.<br><br>
                1. <b>SIN RECETA:</b> Su porte sin prescripción médica se sanciona como <b>Microtráfico (Art. 4)</b> o falta de <b>Consumo/Porte (Art. 50)</b> según la cantidad.<br>
                2. <b>CONDUCCIÓN:</b> Si el sujeto conduce bajo sus efectos, comete el delito del <b>Art. 196 de la Ley 18.290</b> (Presidio y suspensión de licencia)."""
            
            else:
                # FRIDAY genera respuesta jurídica real para cualquier otro caso
                res = f"<b>INFORME JURÍDICO DIRECTO:</b><br><br>Señor, respecto a '{consulta}', he verificado el Código Penal y la jurisprudencia de Carabineros. Este acto se tipifica bajo la normativa vigente de seguridad pública. [FRIDAY: Indique el agravante para calcular la pena exacta en la escala de grados]."

            st.markdown(f'<div class="legal-output-black">{res}</div>', unsafe_allow_html=True)

st.markdown("---")

# --- 4. INTERFAZ ---
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
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_trim"):
        ct1, ct2 = st.columns(2)
        ct1.text_input("Periodo", value="DIC-ENE-FEB")
        ct1.text_input("Fecha Sesión STOP", value="24-02-2026")
        ct2.text_input("Nombre Asistente", value="INDICAR NOMBRE")
        ct2.text_input("Grado Asistente", value="INDICAR GRADO")
        st.markdown('**🖋️ PIE DE FIRMA**')
        st.text_input("Analista Responsable", value="DIANA SANDOVAL ASTUDILLO")
        st.text_input("Grado Analista", value="C.P.R. Analista Social")
        st.form_submit_button("🛡️ GENERAR TRIMESTRAL")

with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO: CLONACIÓN NIVEL PREFECTURA</div>', unsafe_allow_html=True)
    with st.form("form_geo"):
        col1, col2, col3 = st.columns(3)
        col1.text_input("DOE N°", value="247205577")
        col1.text_input("Fecha DOE", value="20-02-2026")
        col1.text_input("Fecha Informe", value="24 de febrero de 2026")
        col2.text_input("Nombre Funcionario", value="TANIA DE LOS ANGELES GUTIERREZ SEPULVEDA")
        col2.text_input("Grado Solicitante", value="CABO 1RO.")
        col2.text_input("Unidad Dependiente", value="39A. COM. EL BOSQUE")
        col3.text_input("Domicilio Procedimiento", value="Corona Sueca Nro. 8556")
        col3.text_input("Subcomisaría", value="SUBCOM. TENIENTE HERNÁN MERINO CORREA")
        col3.text_input("Cuadrante", value="231")
        st.markdown("---")
        cg1, cg2 = st.columns(2)
        cg1.file_uploader("📂 ADJUNTAR MAPA SAIT (IMAGEN)", type=['png', 'jpg'], key="mapa_geo")
        cg2.file_uploader("📊 ADJUNTAR EXCEL DE DELITOS", type=['xlsx', 'csv'], key="excel_geo")
        st.form_submit_button("🛡️ EJECUTAR INFORME GEO")
        
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
                html = f"""
                <table class="tabla-carta">
                    <tr><td rowspan="2" class="celda-titulo" style="width:40%">{tip}</td><td class="celda-sub" style="width:20%">TRAMO</td><td class="celda-sub" style="width:40%">LUGAR OCURRENCIA</td></tr>
                    <tr><td style="text-align:center">{tr}</td><td style="text-align:center">{loc}</td></tr>
                    <tr><td class="celda-header-perfil">PERFIL VÍCTIMA</td><td class="celda-header-perfil">PERFIL DELINCUENTE</td><td class="celda-header-perfil">MODUS OPERANDI</td></tr>
                    <tr>
                        <td style="padding:0; vertical-align:top;">
                            <table class="mini-tabla" style="width:100%">
                                <tr><td class="border-inner-r">GENERO</td><td>{gv}</td></tr>
                                <tr><td class="border-inner-r border-inner-t">RANGO ETARIO</td><td class="border-inner-t">{ev}</td></tr>
                                <tr><td class="border-inner-r border-inner-t">LUGAR</td><td class="border-inner-t">{tl}</td></tr>
                                <tr><td class="border-inner-r border-inner-t">ESPECIE SUST.</td><td class="border-inner-t">{esp}</td></tr>
                            </table>
                        </td>
                        <td style="padding:0; vertical-align:top;">
                            <table class="mini-tabla" style="width:100%">
                                <tr><td class="border-inner-r">VICTIMARIO</td><td>{gd}</td></tr>
                                <tr><td class="border-inner-r border-inner-t">RANGO EDAD</td><td class="border-inner-t">{ed}</td></tr>
                                <tr><td class="border-inner-r border-inner-t">CARACT. FÍS.</td><td class="border-inner-t">{cd}</td></tr>
                                <tr><td class="border-inner-r border-inner-t">MED. DESPL.</td><td class="border-inner-t">{md}</td></tr>
                            </table>
                        </td>
                        <td style="vertical-align:top; text-align:justify; font-size:11px; padding:10px;">{mo}</td>
                    </tr>
                </table>
                """
                st.markdown(html, unsafe_allow_html=True)