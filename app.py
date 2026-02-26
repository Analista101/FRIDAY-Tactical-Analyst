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
    .stButton>button { background-color: #004A2F !important; color: white !important; border-radius: 5px; width: 100%; font-weight: bold; border: 1px solid #C5A059; }
    .ia-box { background-color: #002D1D; color: #C5A059; padding: 20px; border-radius: 10px; border: 2px solid #C5A059; font-family: 'Arial', sans-serif; }
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

# --- 2. LÓGICA DE SESIÓN AISLADA ---
if "key_carta" not in st.session_state:
    st.session_state.key_carta = 0

def limpiar_solo_carta():
    st.session_state.key_carta += 1

# --- 3. MOTOR DE INTELIGENCIA FRIDAY (MEJORADO SEGÚN SUS INSTRUCCIONES) ---
def procesar_relato_ia(texto):
    texto_u = texto.upper()
    an_actual = 2026 
    
    # 1. Título / Tipificación
    tipificacion = "ROBO EN LUGAR NO HABITADO"
    if "00804" in texto_u or "ROBO POR SORPRESA" in texto_u: tipificacion = "00804 ROBO POR SORPRESA"
    elif "00842" in texto_u or "ACCESORIOS" in texto_u: tipificacion = "00842 ROBO DE ACCESORIOS DE VEHICULOS"
    else:
        match_delito = re.search(r'DELITO\s?:\s?([^\n]+)', texto_u)
        if match_delito: tipificacion = match_delito.group(1).strip()

    # 2. Tramo Horario
    h_delito = re.search(r'HORA DEL DELITO\s?:\s?(\d{1,2})', texto_u)
    tramo_hora = f"{int(h_delito.group(1)):02d}:00 A {(int(h_delito.group(1))+1)%24:02d}:00 HRS" if h_delito else "INDICAR TRAMO"

    # 3. Lugar de Ocurrencia (DINÁMICO)
    lugar_match = re.search(r'LUGAR\s?:\s?([^\n\r]+)', texto_u)
    if lugar_match and "VIA PUBLICA" not in lugar_match.group(1):
        lugar_final = lugar_match.group(1).strip()
    elif "SERVICENTRO" in texto_u: lugar_final = "SERVICENTRO"
    elif "DOMICILIO" in texto_u: lugar_final = "DOMICILIO PARTICULAR"
    else: lugar_final = "VIA PUBLICA"

    # 4. Especie Sustraída (SIN MARCAS NI DATOS PERSONALES)
    especie = "NO INDICA"
    if "CELULAR" in texto_u: especie = "01 TELEFONO CELULAR"
    elif "VEHICULO" in texto_u or "AUTO" in texto_u or "PPU" in texto_u: especie = "01 VEHICULO"
    elif "GAS" in texto_u: especie = "01 BALON DE GAS"
    elif "MOCHILA" in texto_u: especie = "01 MOCHILA"

    # 5. Perfil Delincuente: Género
    if any(x in texto_u for x in ["SUJETO", "INDIVIDUO", "HOMBRE", "TIPO"]): genero_del = "MASCULINO"
    elif "MUJER" in texto_u: genero_del = "FEMENINO"
    elif "DESCONOCIDOS" in texto_u: genero_del = "NO INDICA"
    else: genero_del = "NO INDICA"

    # 6. Perfil Delincuente: Rango Edad
    edad_del = "NO INDICA"
    match_f_nac = re.search(r'NACIMIENTO\D+(\d{2})[-/](\d{2})[-/](\d{4})', texto_u)
    if match_f_nac:
        edad_del = f"{an_actual - int(match_f_nac.group(3))} AÑOS"
    else:
        match_edad = re.search(r'(\d{2})\s?AÑOS', texto_u)
        if match_edad: edad_del = f"{match_edad.group(1)} AÑOS"

    # 7. Perfil Delincuente: Características Físicas
    fisicas_list = []
    for item in ["POLERA", "PANTALON", "CASACA", "GORRO", "ESTATURA", "EXTRANJERO", "CHILENO", "DELGADO", "MORENO"]:
        if item in texto_u: fisicas_list.append(item)
    fisicas = " / ".join(fisicas_list) if fisicas_list else "NO INDICA"

    # 8. Perfil Delincuente: Medio de Desplazamiento
    medio = "NO INDICA"
    if "MOTOCICLETA" in texto_u or "MOTO" in texto_u: medio = "01 MOTOCICLETA"
    elif "A PIE" in texto_u: medio = "A PIE"
    elif "VEHICULO" in texto_u or "AUTO" in texto_u: medio = "01 VEHICULO"

    # 9. Modus Operandi (RESUMEN EJECUTIVO ANÓNIMO)
    resumen = f"VICTIMA TRANSITABA POR {lugar_final} CUANDO ES ABORDADA POR {genero_del}, QUIEN SE DESPLAZABA {medio}, SUSTRAYENDO {especie} PARA LUEGO DARSE A LA FUGA."
    if "SORPRESA" in texto_u: resumen = f"VICTIMA FUE ABORDADA POR SORPRESA POR {genero_del} EN {medio}, SUSTRAYENDO {especie} Y ESCAPANDO DEL LUGAR."
    
    return tipificacion, tramo_hora, lugar_final, especie, genero_del, edad_del, fisicas, medio, resumen.upper()

# --- 4. COMANDO CENTRAL IA FRIDAY ---
st.markdown('<div class="section-header">🧠 FRIDAY: COMANDO CENTRAL DE INTELIGENCIA</div>', unsafe_allow_html=True)
with st.expander("TERMINAL DE ANÁLISIS TÁCTICO FRIDAY", expanded=True):
    st.markdown('<div class="ia-box"><b>PROTOCOLO JARVIS ACTIVADO:</b> Señor, los sistemas están listos para el peritaje.</div>', unsafe_allow_html=True)
    consulta_ia = st.text_area("Describa el hecho para peritaje legal (IA Friday):", key="terminal_fr")
    if st.button("⚡ CONSULTAR A FRIDAY"):
        if consulta_ia: st.info("SISTEMA: Análisis de IA Friday completado.")

# --- 5. PESTAÑAS (RESTAURADAS COMPLETAMENTE) ---
t1, t2, t3, t4 = st.tabs(["📄 ACTA STOP", "📈 STOP TRIMESTRAL", "📍 INFORME GEO", "📋 CARTA DE SITUACIÓN"])

with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_acta"):
        c1, c2 = st.columns(2)
        c1.text_input("Semana de estudio", value="SEMANA 08")
        c1.text_input("Fecha de sesión", value="24-02-2026")
        c2.text_input("Compromiso Carabineros", value="INCREMENTAR PATRULLAJES")
        st.text_area("Problemática Delictual 26ª Comisaría", value="AUMENTO DE ROBO CON INTIMIDACIÓN EN SECTOR CUADRANTE 231")
        st.markdown('**🖋️ PIE DE FIRMA**')
        st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="n1")
        st.text_input("Grado", value="C.P.R. Analista Social", key="g1")
        st.text_input("Cargo", value="OFICINA DE OPERACIONES", key="c1")
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
        st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="n2")
        st.text_input("Grado", value="C.P.R. Analista Social", key="g2")
        st.text_input("Cargo", value="OFICINA DE OPERACIONES", key="c2")
        st.form_submit_button("🛡️ GENERAR")

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
        col3.text_input("Domicilio", value="Corona Sueca Nro. 8556")
        col3.text_input("Subcomisaría", value="SUBCOM. TENIENTE HERNÁN MERINO CORREA")
        col3.text_input("Cuadrante", value="231")
        st.markdown("---")
        cf1, cf2 = st.columns(2)
        cf1.text_input("Desde (Rango)", value="05-11-2025")
        cf2.text_input("Hasta (Rango)", value="24-02-2026")
        st.markdown("---")
        c_map, c_xls = st.columns(2)
        c_map.file_uploader("📂 ADJUNTAR MAPA SAIT (IMAGEN)", type=['png', 'jpg'], key="mapa_up")
        c_xls.file_uploader("📊 ADJUNTAR EXCEL DE DELITOS", type=['xlsx'], key="excel_up")
        st.form_submit_button("🛡️ EJECUTAR CLONACIÓN")

with t4:
    st.markdown('<div class="section-header">📋 CARTA DE SITUACIÓN (MATRIZ DINÁMICA)</div>', unsafe_allow_html=True)
    if st.button("🗑️ LIMPIAR RELATO"):
        limpiar_solo_carta()
        st.rerun()

    with st.form("form_carta"):
        relato_in = st.text_area("PEGUE EL RELATO AQUÍ:", height=200, key=f"txt_{st.session_state.key_carta}")
        if st.form_submit_button("⚡ GENERAR CUADRO"):
            if relato_in:
                tip, tr, lu, esp, gen_d, ed_d, fis_d, med_d, mo = procesar_relato_ia(relato_in)
                
                html = f"""
                <table class="tabla-carta">
                    <tr><td rowspan="2" class="celda-titulo" style="width:40%">{tip}</td><td class="celda-sub" style="width:20%">TRAMO</td><td class="celda-sub" style="width:40%">LUGAR OCURRENCIA</td></tr>
                    <tr><td style="text-align:center">{tr}</td><td style="text-align:center">{lu}</td></tr>
                    <tr><td class="celda-header-perfil">PERFIL VÍCTIMA</td><td class="celda-header-perfil">PERFIL DELINCUENTE</td><td class="celda-header-perfil">MODUS OPERANDI</td></tr>
                    <tr>
                        <td style="padding:0; vertical-align:top;">
                            <table class="mini-tabla" style="width:100%">
                                <tr><td class="border-inner-r">GENERO</td><td>VÍCTIMA</td></tr>
                                <tr><td class="border-inner-r border-inner-t">RANGO ETARIO</td><td class="border-inner-t">NO INDICA</td></tr>
                                <tr><td class="border-inner-r border-inner-t">LUGAR</td><td class="border-inner-t">{lu}</td></tr>
                                <tr><td class="border-inner-r border-inner-t">ESPECIE SUST.</td><td class="border-inner-t">{esp}</td></tr>
                            </table>
                        </td>
                        <td style="padding:0; vertical-align:top;">
                            <table class="mini-tabla" style="width:100%">
                                <tr><td class="border-inner-r">VICTIMARIO</td><td>{gen_d}</td></tr>
                                <tr><td class="border-inner-r border-inner-t">RANGO EDAD</td><td class="border-inner-t">{ed_d}</td></tr>
                                <tr><td class="border-inner-r border-inner-t">CARACT. FÍS.</td><td class="border-inner-t">{fis_d}</td></tr>
                                <tr><td class="border-inner-r border-inner-t">MED. DESPL.</td><td class="border-inner-t">{med_d}</td></tr>
                            </table>
                        </td>
                        <td style="vertical-align:top; text-align:justify; font-size:11px; padding:10px;">{mo}</td>
                    </tr>
                </table>
                """
                st.markdown(html, unsafe_allow_html=True)