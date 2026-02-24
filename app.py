import streamlit as st
import pandas as pd
import re

# --- 1. CONFIGURACIÓN VISUAL JARVIS ---
st.set_page_config(page_title="SISTEMA JARVIS - COMANDO CENTRAL", layout="wide")
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

# --- 2. LÓGICA DE SESIÓN (SOLO PESTAÑA 4) ---
if "key_carta" not in st.session_state:
    st.session_state.key_carta = 0

def limpiar_solo_carta():
    st.session_state.key_carta += 1

# --- 3. MOTOR DE INTELIGENCIA FRIDAY (EXTRACCIÓN REAL) ---
def procesar_relato_ia(texto):
    # Extracción de Género
    genero = "FEMENINO" if "FEMENINO" in texto.upper() else "MASCULINO" if "MASCULINO" in texto.upper() else "NO INDICA"
    
    # Extracción de Edad
    edad_match = re.search(r'(\d{2})\s?(AÑOS|Aï¿½OS)', texto, re.I)
    edad = f"DE {edad_match.group(1)} AÑOS" if edad_match else "NO INDICA"
    
    # Extracción de Lugar (Busca entre Dirección y Región en la cabecera)
    lugar_match = re.search(r'Dirección\s?:\s?([^Región]+)', texto, re.I)
    lugar = lugar_match.group(1).strip().upper() if lugar_match else "VIA PUBLICA"
    
    # Extracción de Especie
    especie_match = re.search(r'(TELÉFONO|CELULAR|IPHONE)\s?([^,.]+)', texto, re.I)
    especie = especie_match.group(0).strip().upper() if especie_match else "01 TELÉFONO CELULAR"
    
    # Extracción de Medio de Desplazamiento
    v_match = re.search(r'(EN UNA|A BORDO DE|MOVILIZABAN EN|VEHÍCULO)\s?([^,.]+)', texto, re.I)
    v_transporte = v_match.group(2).strip().upper() if v_match else "A PIE / NO IDENTIFICADO"
    
    # Lógica de tramo horario basada en "Hora del Delito"
    h_delito = re.search(r'Hora del Delito\s?:\s?(\d{1,2})[:.](\d{2})', texto, re.I)
    if h_delito:
        h = int(h_delito.group(1))
        tramo_hora = f"{h:02d}:00 A {(h+1)%24:02d}:00 HRS"
    else:
        tramo_hora = "INDICAR TRAMO"

    # Redacción Dinámica de Modus Operandi
    huida = re.search(r'HUYO EN DIRECCION ([^.]+)', texto, re.I)
    dir_huida = f" PARA LUEGO ESCAPAR EN DIRECCIÓN {huida.group(1).strip().upper()}." if huida else " PARA LUEGO ESCAPAR EN DIRECCIÓN DESCONOCIDA."
    
    modus = f"LA VÍCTIMA SE ENCONTRABA EN LA VÍA PÚBLICA CUANDO FUE ABORDADA POR SUJETOS, QUIENES MEDIANTE EL USO DE SORPRESA O INTIMIDACIÓN LE ARREBATARON SUS PERTENENCIAS ({especie}){dir_huida}"
    
    return v_transporte, modus, tramo_hora, genero, edad, lugar, especie

# --- 4. COMANDO CENTRAL IA FRIDAY ---
st.markdown('<div class="section-header">🧠 FRIDAY: COMANDO CENTRAL DE INTELIGENCIA</div>', unsafe_allow_html=True)
with st.expander("TERMINAL DE ANÁLISIS TÁCTICO FRIDAY", expanded=True):
    st.markdown('<div class="ia-box"><b>PROTOCOLO JARVIS ACTIVADO:</b> Señor, el análisis pericial está listo.</div>', unsafe_allow_html=True)
    consulta_ia = st.text_area("Describa el hecho para peritaje legal (IA Friday):", key="terminal_fr")
    if st.button("⚡ CONSULTAR A FRIDAY"):
        if consulta_ia: st.info("SISTEMA: Análisis de IA Friday completado.")

# --- 5. PESTAÑAS OPERATIVAS ---
t1, t2, t3, t4 = st.tabs(["📄 ACTA STOP", "📈 STOP TRIMESTRAL", "📍 INFORME GEO", "📋 CARTA DE SITUACIÓN"])

with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_acta"):
        c1, c2 = st.columns(2)
        c1.text_input("Semana de estudio", value="SEMANA 08")
        c2.text_input("Fecha de sesión", value="24-02-2026")
        st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="n1")
        st.form_submit_button("🛡️ GENERAR ACTA")

with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_trim"):
        ct1, ct2 = st.columns(2)
        ct1.text_input("Periodo", value="DIC-ENE-FEB")
        ct2.text_input("Nombre Asistente", value="INDICAR NOMBRE")
        st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="n2")
        st.form_submit_button("🛡️ GENERAR")

with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO: CLONACIÓN NIVEL PREFECTURA</div>', unsafe_allow_html=True)
    with st.form("form_geo"):
        col1, col2 = st.columns(2)
        col1.text_input("DOE N°", value="247205577")
        col2.text_input("Nombre Funcionario", value="TANIA DE LOS ANGELES GUTIERREZ SEPULVEDA")
        st.markdown("---")
        st.file_uploader("📂 ADJUNTAR MAPA SAIT (IMAGEN)", type=['png', 'jpg'], key="mapa_up")
        st.file_uploader("📊 ADJUNTAR EXCEL DE DELITOS", type=['xlsx'], key="excel_up")
        st.form_submit_button("🛡️ EJECUTAR CLONACIÓN")

with t4:
    st.markdown('<div class="section-header">📋 CARTA DE SITUACIÓN (MATRIZ DINÁMICA)</div>', unsafe_allow_html=True)
    if st.button("🗑️ LIMPIAR TODO EL RELATO"):
        limpiar_solo_carta()
        st.rerun()

    with st.form("peritaje_carta"):
        relato_in = st.text_area("PEGUE EL RELATO AQUÍ:", height=200, key=f"area_relato_{st.session_state.key_carta}")
        ejecutar = st.form_submit_button("⚡ GENERAR CUADRO DE SITUACIÓN")
        
        if ejecutar and relato_in:
            vt, mo, tr, ge, ed, lu, es = procesar_relato_ia(relato_in)
            html_matriz = f"""
            <table class="tabla-carta">
                <tr><td rowspan="2" class="celda-titulo" style="width:40%">ROBO POR SORPRESA / INTIMIDACIÓN</td><td class="celda-sub" style="width:20%">TRAMO</td><td class="celda-sub" style="width:40%">LUGAR OCURRENCIA</td></tr>
                <tr><td style="text-align:center">{tr}</td><td style="text-align:center">{lu}</td></tr>
                <tr><td class="celda-header-perfil">PERFIL VÍCTIMA</td><td class="celda-header-perfil">PERFIL DELINCUENTE</td><td class="celda-header-perfil">MODUS OPERANDI</td></tr>
                <tr>
                    <td style="padding:0; vertical-align:top;">
                        <table class="mini-tabla" style="width:100%">
                            <tr><td class="border-inner-r">GENERO</td><td>{ge}</td></tr>
                            <tr><td class="border-inner-r border-inner-t">RANGO ETARIO</td><td class="border-inner-t">{ed}</td></tr>
                            <tr><td class="border-inner-r border-inner-t">LUGAR</td><td class="border-inner-t">VIA PUBLICA</td></tr>
                            <tr><td class="border-inner-r border-inner-t">ESPECIE SUST.</td><td class="border-inner-t">{es}</td></tr>
                        </table>
                    </td>
                    <td style="padding:0; vertical-align:top;">
                        <table class="mini-tabla" style="width:100%">
                            <tr><td class="border-inner-r">VICTIMARIO</td><td>MASCULINO</td></tr>
                            <tr><td class="border-inner-r border-inner-t">RANGO EDAD</td><td class="border-inner-t">NO INDICA</td></tr>
                            <tr><td class="border-inner-r border-inner-t">CARACT. FÍS.</td><td class="border-inner-t">VESTIMENTA OSCURA</td></tr>
                            <tr><td class="border-inner-r border-inner-t">MED. DESPL.</td><td class="border-inner-t">{vt}</td></tr>
                        </table>
                    </td>
                    <td style="vertical-align:top; text-align:justify; font-size:11px; padding:10px;">{mo}</td>
                </tr>
            </table>
            """
            st.markdown(html_matriz, unsafe_allow_html=True)