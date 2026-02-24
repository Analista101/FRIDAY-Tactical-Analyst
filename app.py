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

# --- 2. LÓGICA DE SESIÓN (PROTECCIÓN CONTRA DATOS ANTIGUOS) ---
if "key_control" not in st.session_state:
    st.session_state.key_control = 0

def limpiar_sistema_total():
    st.session_state.key_control += 1
    # Forzamos la eliminación de datos previos en el búfer
    for key in list(st.session_state.keys()):
        if "resultado_" in key:
            del st.session_state[key]
    st.rerun()

# --- 3. MOTOR DE INTELIGENCIA FRIDAY (RECALIBRADO) ---
def procesar_relato_ia(texto):
    # Detección de vehículo (Medio de desplazamiento)
    v_match = re.search(r'(EN UN|A BORDO DE|MOVILIZABAN EN|VEHÍCULO)\s?([^,.]+)', texto, re.I)
    v_transporte = v_match.group(2).strip().upper() if v_match else "VEHÍCULO NO IDENTIFICADO"
    
    # LÓGICA DE TRAMO HORARIO (Ej: 13:15 -> 13:00 A 14:00)
    h_match = re.search(r'(\d{1,2})[:.](\d{2})', texto)
    if h_match:
        hora_base = int(h_match.group(1))
        tramo_hora = f"{hora_base:02d}:00 A {(hora_base + 1):02d}:00 HRS"
    else:
        tramo_hora = "INDICAR TRAMO"
    
    modus = "LA VÍCTIMA TRANSITABA POR LA VÍA PÚBLICA CUANDO FUE ABORDADA POR SUJETOS DESCONOCIDOS, QUIENES MEDIANTE EL USO DE INTIMIDACIÓN O VIOLENCIA LE ARREBATARON SUS PERTENENCIAS PARA LUEGO ESCAPAR EN DIRECCIÓN DESCONOCIDA."
    return v_transporte, modus, tramo_hora

# --- 4. COMANDO CENTRAL IA FRIDAY ---
st.markdown('<div class="section-header">🧠 FRIDAY: COMANDO CENTRAL DE INTELIGENCIA</div>', unsafe_allow_html=True)

# --- 5. PESTAÑAS ---
t1, t2, t3, t4 = st.tabs(["📄 ACTA STOP", "📈 STOP TRIMESTRAL", "📍 INFORME GEO", "📋 CARTA DE SITUACIÓN"])

with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_trim"):
        st.text_input("Periodo (Ej: Nov-Dic-Ene)")
        st.text_input("Fecha Sesión STOP")
        st.markdown('**🖋️ PIE DE FIRMA TRIMESTRAL**')
        st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO", key="f_nom")
        st.text_input("Grado", value="C.P.R. Analista Social", key="f_grad")
        st.text_input("Cargo", value="OFICINA DE OPERACIONES", key="f_carg")
        st.form_submit_button("🛡️ GENERAR")

with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO: CLONACIÓN NIVEL PREFECTURA</div>', unsafe_allow_html=True)
    with st.form("form_geo"):
        col1, col2, col3 = st.columns(3)
        col1.text_input("DOE N°", value="247205577")
        col1.text_input("Fecha DOE", value="20-02-2026")
        col2.text_input("Nombre Funcionario", value="TANIA DE LOS ANGELES GUTIERREZ SEPULVEDA")
        col3.text_input("Cuadrante", value="231")
        st.markdown("---")
        c_map, c_xls = st.columns(2)
        c_map.file_uploader("📂 ADJUNTAR MAPA SAIT", type=['png', 'jpg'])
        c_xls.file_uploader("📊 ADJUNTAR EXCEL DE DELITOS", type=['xlsx'])
        st.form_submit_button("🛡️ EJECUTAR")

with t4:
    st.markdown('<div class="section-header">📋 CARTA DE SITUACIÓN (MATRIZ COLUMNAS)</div>', unsafe_allow_html=True)
    
    c_izq, c_der = st.columns([5, 1])
    with c_der:
        # BOTÓN LIMPIAR TOTAL
        st.button("🗑️ LIMPIAR", on_click=limpiar_sistema_total)
    
    # Key dinámica para forzar vacío
    relato_actual = st.text_area("PEGUE EL RELATO AQUÍ:", 
                                height=200, 
                                key=f"input_relato_{st.session_state.key_control}")

    if st.button("⚡ GENERAR CUADRO"):
        if relato_actual:
            v_traslado, v_modus, v_tramo = procesar_relato_ia(relato_actual)
            
            # Guardamos el resultado con una key única del proceso actual
            st.session_state[f"resultado_{st.session_state.key_control}"] = True
            
            html_matriz = f"""
            <table class="tabla-carta">
                <tr><td rowspan="2" class="celda-titulo" style="width:40%">ROBO CON INTIMIDACIÓN</td><td class="celda-sub" style="width:20%">TRAMO</td><td class="celda-sub" style="width:40%">LUGAR OCURRENCIA</td></tr>
                <tr><td style="text-align:center">{v_tramo}</td><td style="text-align:center">AVENIDA GENERAL OSCAR BONILLA / LOS EDILES</td></tr>
                <tr><td class="celda-header-perfil">PERFIL VÍCTIMA</td><td class="celda-header-perfil">PERFIL DELINCUENTE</td><td class="celda-header-perfil">MODUS OPERANDI</td></tr>
                <tr>
                    <td style="padding:0; vertical-align:top;">
                        <table class="mini-tabla" style="width:100%">
                            <tr><td class="border-inner-r">GENERO</td><td>MASCULINO</td></tr>
                            <tr><td class="border-inner-r border-inner-t">RANGO ETARIO</td><td class="border-inner-t">DE 30 A 35 AÑOS</td></tr>
                            <tr><td class="border-inner-r border-inner-t">LUGAR</td><td class="border-inner-t">VIA PUBLICA</td></tr>
                            <tr><td class="border-inner-r border-inner-t">ESPECIE SUST.</td><td class="border-inner-t">01 TELÉFONO CELULAR</td></tr>
                        </table>
                    </td>
                    <td style="padding:0; vertical-align:top;">
                        <table class="mini-tabla" style="width:100%">
                            <tr><td class="border-inner-r">VICTIMARIO</td><td>MASCULINO</td></tr>
                            <tr><td class="border-inner-r border-inner-t">RANGO EDAD</td><td class="border-inner-t">NO INDICA</td></tr>
                            <tr><td class="border-inner-r border-inner-t">CARACT. FÍS.</td><td class="border-inner-t">VESTIMENTA OSCURA</td></tr>
                            <tr><td class="border-inner-r border-inner-t">MED. DESPL.</td><td class="border-inner-t">{v_traslado}</td></tr>
                        </table>
                    </td>
                    <td style="vertical-align:top; text-align:justify; font-size:11px; padding:10px;">{v_modus}</td>
                </tr>
            </table>
            """
            st.markdown(html_matriz, unsafe_allow_html=True)