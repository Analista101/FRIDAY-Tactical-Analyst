import streamlit as st
import pandas as pd
import re

# --- 1. CONFIGURACIÓN VISUAL FRIDAY ---
st.set_page_config(page_title="SISTEMA FRIDAY - COMANDO CENTRAL", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .section-header { background-color: #004A2F !important; color: white; padding: 10px; border-radius: 5px; font-weight: bold; border-left: 10px solid #C5A059; margin-bottom: 20px; }
    .stButton>button { background-color: #004A2F !important; color: white !important; border-radius: 5px; width: 100%; font-weight: bold; border: 1px solid #C5A059; }
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

# --- 2. MOTOR DE INTELIGENCIA FRIDAY (REFINADO) ---
def procesar_relato_ia(texto):
    # Tipificación (Solo toma lo que viene después de Codigo Delito)
    tipo_match = re.search(r'Codigo Delito\s?:\s?\d+\s?([^:\n\r]+)', texto, re.I)
    tipificacion = tipo_match.group(1).strip().upper() if tipo_match else "DELITO NO ESPECIFICADO"

    # Dirección (Mejorada para capturar intersecciones)
    dir_match = re.search(r'Dirección\s?:\s?([^\n\r]+)', texto, re.I)
    lugar = dir_match.group(1).strip().upper() if dir_match else "VIA PUBLICA"

    # Tramo Horario (Hora del Delito)
    h_delito = re.search(r'Hora del Delito\s?:\s?(\d{1,2})[:.](\d{2})', texto, re.I)
    if h_delito:
        h = int(h_delito.group(1))
        tramo_hora = f"{h:02d}:00 A {(h+1)%24:02d}:00 HRS"
    else:
        tramo_hora = "INDICAR TRAMO"

    # Especie (Si es vehículo: MARCA, MODELO, PPU. Si es celular: Solo tipo)
    es_vehiculo = any(x in texto.upper() for x in ["VEHICULO", "AUTOMOVIL", "CAMIONETA", "PPU"])
    if es_vehiculo:
        especie = "VEHÍCULO (MARCA/MODELO/PPU A EXTRAER)" # Aquí se añadiría regex de PPU
    else:
        especie = "01 TELÉFONO CELULAR"

    # Género y Edad
    genero = "FEMENINO" if "FEMENINO" in texto.upper() else "MASCULINO" if "MASCULINO" in texto.upper() else "NO INDICA"
    edad_match = re.search(r'(\d{2})\s?(AÑOS|Aï¿½OS)', texto, re.I)
    edad = f"DE {edad_match.group(1)} AÑOS" if edad_match else "NO INDICA"

    # Medio de Desplazamiento (Búsqueda limpia)
    v_match = re.search(r'DESPLAZABA EN (UN|UNA)\s?([^,.]+)', texto, re.I)
    v_transporte = v_match.group(2).strip().upper() if v_match else "A PIE / NO INDICA"

    # Modus Operandi (Sin detalles personales de especies)
    huida = re.search(r'HUYO EN DIRECCION ([^.]+)', texto, re.I)
    dir_huida = f" PARA LUEGO ESCAPAR EN DIRECCIÓN {huida.group(1).strip().upper()}." if huida else "."
    modus = f"LA VÍCTIMA TRANSITABA POR LA VÍA PÚBLICA CUANDO FUE ABORDADA POR UN SUJETO, QUIEN MEDIANTE EL USO DE SORPRESA PROCEDIÓ A SUSTRAERLE SU EQUIPO TELEFÓNICO{dir_huida}"
    
    return tipificacion, tramo_hora, lugar, genero, edad, especie, v_transporte, modus

# --- 3. PESTAÑAS ---
st.markdown('<div class="section-header">🧠 FRIDAY: COMANDO CENTRAL DE INTELIGENCIA</div>', unsafe_allow_html=True)
t1, t2, t3, t4 = st.tabs(["📄 ACTA STOP", "📈 STOP TRIMESTRAL", "📍 INFORME GEO", "📋 CARTA DE SITUACIÓN"])

with t3: # PESTAÑA GEO SIN CAMBIOS PARA INTEGRIDAD
    st.markdown('<div class="section-header">📍 INFORME GEO</div>', unsafe_allow_html=True)
    with st.form("geo_form"):
        st.text_input("DOE N°", value="247205577")
        st.file_uploader("📂 ADJUNTAR MAPA SAIT", type=['png', 'jpg'])
        st.form_submit_button("🛡️ EJECUTAR")

with t4:
    st.markdown('<div class="section-header">📋 CARTA DE SITUACIÓN (SISTEMA DE PRECISIÓN)</div>', unsafe_allow_html=True)
    if st.button("🗑️ LIMPIAR RELATO"):
        limpiar_solo_carta()
        st.rerun()

    with st.form("form_carta"):
        relato_input = st.text_area("PEGUE EL RELATO AQUÍ:", height=200, key=f"txt_{st.session_state.key_carta}")
        if st.form_submit_button("⚡ GENERAR CUADRO"):
            if relato_input:
                tip, tr, lu, ge, ed, es, vt, mo = procesar_relato_ia(relato_input)
                html = f"""
                <table class="tabla-carta">
                    <tr><td rowspan="2" class="celda-titulo" style="width:40%">{tip}</td><td class="celda-sub" style="width:20%">TRAMO</td><td class="celda-sub" style="width:40%">LUGAR OCURRENCIA</td></tr>
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
                st.markdown(html, unsafe_allow_html=True)