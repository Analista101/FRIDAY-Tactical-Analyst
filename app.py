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

if "key_carta" not in st.session_state:
    st.session_state.key_carta = 0

def limpiar_solo_carta():
    st.session_state.key_carta += 1

# --- 3. MOTOR DE INTELIGENCIA FRIDAY (CORRECCIÓN DE LUGARES Y PERFILES) ---
def procesar_relato_ia(texto):
    texto_u = texto.upper().replace("Aï¿½OS", "AÑOS").replace("N°", "NRO")
    an_actual = 2026 
    
    # 1. Tipificación
    tip_match = re.search(r'CODIGO DELITO\s?:\s?([^\n]+)', texto_u)
    tipificacion = tip_match.group(1).strip() if tip_match else "00842 ROBO DE ACCESORIOS DE VEHICULOS"

    # 2. Tramo Horario
    h_delito = re.search(r'HORA DEL DELITO\s?:\s?(\d{1,2})', texto_u)
    tramo_hora = f"{int(h_delito.group(1)):02d}:00 A {(int(h_delito.group(1))+1)%24:02d}:00 HRS" if h_delito else "00:00 A 01:00 HRS"

    # 3. Lugar de Ocurrencia (Dirección Exacta)
    dir_match = re.search(r'DIRECCIÓN\s?:\s?([^\n\r]+)', texto_u)
    lugar_ocurrencia = dir_match.group(1).strip() if dir_match else "INDICAR DIRECCIÓN"

    # 4. Perfil Víctima (Datos del Afectado)
    # Género
    gen_vic = "MASCULINO" if "SEXO : MASCULINO" in texto_u or "SR. " in texto_u else "FEMENINO"
    # Edad (Cálculo real desde fecha de nacimiento del afectado)
    edad_vic = "NO INDICA"
    f_nac_vic = re.search(r'FECHA NACIMIENTO\s?:\s?(\d{2})[-/](\d{2})[-/](\d{4})', texto_u)
    if f_nac_vic:
        edad_vic = f"DE {an_actual - int(f_nac_vic.group(3))} AÑOS"
    
    # Tipo de Lugar (Recinto)
    tipo_lugar = "VIA PUBLICA"
    if "SERVICENTRO" in texto_u or "ESTACION DE SERVICIO" in texto_u: tipo_lugar = "SERVICENTRO"
    elif "DOMICILIO" in texto_u: tipo_lugar = "DOMICILIO PARTICULAR"

    # Especie (Limpieza)
    especies = []
    if "CELULAR" in texto_u: especies.append("01 TELEFONO CELULAR")
    if "MALETA" in texto_u: especies.append("01 MALETA")
    if "BOLSO" in texto_u: especies.append("01 BOLSO")
    if "MOCHILA" in texto_u: especies.append("01 MOCHILA")
    if "VEHICULO" in texto_u and "ROBO DE VEHICULO" in tipificacion: especies.append("01 VEHICULO")
    especie_sust = " / ".join(especies) if especies else "ACCESORIOS VARIOS"

    # 5. Perfil Delincuente
    # Género Victimario
    if "DESCENDIO UN SUJETO" in texto_u or "UN HOMBRE" in texto_u: gen_del = "MASCULINO"
    elif "UNA MUJER" in texto_u: gen_del = "FEMENINO"
    else: gen_del = "NO INDICA"

    # Edad Delincuente
    edad_del = "NO INDICA"
    detenido_nac = re.search(r'DETENIDO[\s\S]*?NACIMIENTO\s?:\s?(\d{2})[-/](\d{2})[-/](\d{4})', texto_u)
    if detenido_nac: edad_del = f"{an_actual - int(detenido_nac.group(3))} AÑOS"

    # Características Físicas
    caract = "NO INDICA"
    if "VESTIMENTA OSCURA" in texto_u: caract = "VESTIMENTA OSCURA"
    elif "POLERA" in texto_u: caract = "VESTIMENTA INFORMAL"

    # Medio Desplazamiento
    medio = "NO INDICA"
    m_match = re.search(r'VEHICULO MARCA\s?(\w+)', texto_u)
    if m_match and "VICTIMA" not in texto_u[m_match.start()-20:m_match.start()]:
        medio = f"01 VEHICULO {m_match.group(1)}"
    elif "A PIE" in texto_u: medio = "A PIE"

    # 6. Modus Operandi (MAYÚSCULAS Y ANÓNIMO)
    modus = f"VICTIMA DEJO ESTACIONADO SU VEHICULO EN {tipo_lugar}, MOMENTOS EN QUE {gen_del} QUE SE DESPLAZABA EN {medio} QUIEBRA VENTANAL Y SUSTRAE {especie_sust} PARA LUEGO DARSE A LA FUGA."
    
    return tipificacion, tramo_hora, lugar_ocurrencia, gen_vic, edad_vic, tipo_lugar, especie_sust, gen_del, edad_del, caract, medio, modus.upper()

# --- 4. INTERFAZ (PESTAÑAS INTACTAS) ---
st.markdown('<div class="section-header">🧠 FRIDAY: COMANDO CENTRAL DE INTELIGENCIA</div>', unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["📄 ACTA STOP", "📈 STOP TRIMESTRAL", "📍 INFORME GEO", "📋 CARTA DE SITUACIÓN"])

with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_acta"):
        st.text_input("Semana de estudio", value="SEMANA 08")
        st.form_submit_button("🛡️ GENERAR ACTA")

with t2:
    st.markdown('<div class="section-header">📈 STOP TRIMESTRAL</div>', unsafe_allow_html=True)
    with st.form("form_trim"):
        st.text_input("Periodo", value="DIC-ENE-FEB")
        st.form_submit_button("🛡️ GENERAR")

with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO: CLONACIÓN NIVEL PREFECTURA</div>', unsafe_allow_html=True)
    with st.form("form_geo"):
        st.text_input("DOE N°", value="247205577")
        st.form_submit_button("🛡️ EJECUTAR CLONACIÓN")

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