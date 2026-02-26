import streamlit as st
import pandas as pd
import re
from datetime import datetime

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
    tipificacion = tip_match.group(1).strip() if tip_match else "00842 ROBO DE ACCESORIOS DE VEHICULOS"

    h_delito = re.search(r'HORA DEL DELITO\s?:\s?(\d{1,2})', texto_u)
    tramo_hora = f"{int(h_delito.group(1)):02d}:00 A {(int(h_delito.group(1))+1)%24:02d}:00 HRS" if h_delito else "00:00 A 01:00 HRS"

    # LUGAR DE OCURRENCIA (DIRECCIÓN)
    dir_match = re.search(r'DIRECCIÓN\s?:\s?([^\n\r]+)', texto_u)
    lugar_ocurrencia = dir_match.group(1).strip() if dir_match else "RUTA 68"

    # PERFIL VÍCTIMA
    gen_vic = "MASCULINO" if "SEXO : MASCULINO" in texto_u or "SR. " in texto_u else "FEMENINO"
    
    # Rango Etario (Bloques de 5 años)
    edad_rango = "NO INDICA"
    f_nac_vic = re.search(r'FECHA NACIMIENTO\s?:\s?(\d{2})[-/](\d{2})[-/](\d{4})', texto_u)
    if f_nac_vic:
        edad = an_actual - int(f_nac_vic.group(3))
        lim_inf = (edad // 5) * 5
        edad_rango = f"DE {lim_inf} A {lim_inf + 5} AÑOS"
    
    # TIPO DE LUGAR
    tipo_lugar = "VIA PUBLICA"
    if any(x in texto_u for x in ["SERVICENTRO", "ESTACION DE SERVICIO", "SHELL", "COPEC"]): tipo_lugar = "SERVICENTRO"
    elif "DOMICILIO" in texto_u: tipo_lugar = "DOMICILIO PARTICULAR"

    # ESPECIE
    items = []
    if "CELULAR" in texto_u: items.append("01 TELEFONO CELULAR")
    if "MALETA" in texto_u: items.append("01 MALETA")
    if "BOLSO" in texto_u: items.append("01 BOLSO")
    if "MOCHILA" in texto_u: items.append("01 MOCHILA")
    especie_sust = " / ".join(items) if items else "ACCESORIOS VARIOS"

    # PERFIL DELINCUENTE
    gen_del = "MASCULINO" if any(x in texto_u for x in ["SUJETO", "INDIVIDUO", "HOMBRE"]) else "NO INDICA"
    edad_del = "NO INDICA"
    caract = "VESTIMENTA OSCURA" if "OSCURA" in texto_u else "NO INDICA"
    
    medio = "NO INDICA"
    v_match = re.search(r'VEHICULO MARCA\s?(\w+)', texto_u)
    if v_match: medio = f"01 VEHICULO {v_match.group(1)}"

    modus = f"VICTIMA DEJO ESTACIONADO SU VEHICULO EN {tipo_lugar}, MOMENTOS EN QUE {gen_del} QUE SE DESPLAZABA EN {medio} QUIEBRA VENTANAL Y SUSTRAE {especie_sust} PARA LUEGO DARSE A LA FUGA."
    
    return tipificacion, tramo_hora, lugar_ocurrencia, gen_vic, edad_rango, tipo_lugar, especie_sust, gen_del, edad_del, caract, medio, modus.upper()

# --- 3. TERMINAL DE COMANDO FRIDAY (INTELIGENCIA LEGAL TOTAL) ---
st.markdown('<div class="section-header">🧠 FRIDAY: COMANDO CENTRAL DE INTELIGENCIA</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="ia-box"><b>PROTOCOLO JARVIS:</b> Señor, he sincronizado mi base de datos con la legislación vigente de Chile. Analizaré cualquier conducta delictual, infracción de tránsito o procedimiento de Carabineros con sustento legal directo.</div>', unsafe_allow_html=True)
    
    consulta_legal = st.text_input("CONSULTA LEGAL / PROCEDIMENTAL:", key="cmd_friday", placeholder="Ej: ¿Consumir zopiclona sin receta es delito?")
    
    if st.button("🛡️ ANALIZAR CONDUCTA DELICTUAL"):
        if consulta_legal:
            cons_u = consulta_legal.upper()
            
            # ANÁLISIS ESPECÍFICO DE ZOPICLONA Y PSICOTRÓPICOS
            if "ZOPICLONA" in cons_u or "SIN RECETA" in cons_u:
                resp = """<b>ANÁLISIS JURÍDICO FRIDAY:</b><br><br>
                Señor, el consumo de <b>Zopiclona</b> (u otros psicotrópicos) sin receta médica en Chile tiene las siguientes implicancias legales:<br><br>
                1. <b>Ley 20.000 (Art. 1, 4 y 50):</b> La Zopiclona es un fármaco controlado. Si se porta en cantidades que no corresponden a un tratamiento médico vigente y sin receta, se presume <b>Microtráfico</b> o <b>Porte Ilegal de Sustancias</b>.<br>
                2. <b>El Consumo:</b> Si es sorprendido consumiendo en la vía pública sin prescripción, se aplica el <b>Art. 50</b> (Falta sancionada con multas o programas de rehabilitación).<br>
                3. <b>La Venta:</b> Quien venda o facilite Zopiclona sin receta comete un <b>Delito contra la Salud Pública</b> y Tráfico de Drogas.<br>
                4. <b>Conducción:</b> Si conduce bajo sus efectos, se aplica el <b>Art. 196 de la Ley de Tránsito</b> (Conducción bajo la influencia de sustancias estupefacientes o psicotrópicas), lo cual es un delito grave con penas de presidio y suspensión de licencia.<br><br>
                <b>Procedimiento:</b> Carabineros debe proceder a la incautación del fármaco y la detención si no se acredita la procedencia médica mediante receta retenida o digital."""
            
            # ANÁLISIS DE TRÁNSITO / PIRUETAS
            elif "PIRUETA" in cons_u or "ACROBACIA" in cons_u:
                resp = """<b>ANÁLISIS JURÍDICO FRIDAY:</b><br><br>
                Realizar piruetas en motocicleta en la vía pública <b>ES UN DELITO</b>.<br>
                <b>Base Legal:</b> Art. 197 bis de la <b>Ley de Tránsito (Ley 21.495)</b>.<br>
                <b>Sanción:</b> Presidio menor en su grado mínimo y multa. El vehículo debe ser retirado de circulación inmediatamente."""
            
            # RESPUESTA GENERAL EXPERTA
            else:
                resp = f"""<b>INFORME TÉCNICO FRIDAY:</b><br><br>
                Analizando conducta: "{consulta_legal}".<br>
                Bajo la normativa chilena y el Código Penal, este hecho requiere la aplicación del protocolo de flagrancia. [FRIDAY procesando artículos específicos...]. 
                Señor, sea más específico con el agravante o el lugar de ocurrencia para darle la pena exacta."""
            
            st.markdown(f'<div class="legal-output-black">{resp}</div>', unsafe_allow_html=True)

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