import pandas as pd
import re
from datetime import datetime
from docxtpl import DocxTemplate, InlineImage
import io
from docx.shared import Mm
import matplotlib.pyplot as plt
import textwrap
import streamlit as st
import json
import os
import requests

# --- 1. NÚCLEO DE MEMORIA Y EVOLUCIÓN (SISTEMA INTEGRAL) ---
def cargar_memoria_nube():
    archivo = 'memoria_evolutiva.json'
    if os.path.exists(archivo):
        try:
            with open(archivo, 'r') as f:
                contenido = f.read().strip()
                return json.loads(contenido) if contenido else []
        except: return []
    return []

def guardar_en_nube(nueva_leccion):
    archivo = 'memoria_evolutiva.json'
    datos = cargar_memoria_nube()
    datos.append(nueva_leccion)
    with open(archivo, 'w') as f:
        json.dump(datos, f)

def aplicar_evolucion_universal():
    memoria = cargar_memoria_nube()
    if not memoria: return
    adn = " ".join(memoria).upper()
    
    if "INVESTIGA" in adn or "BUSCA" in adn:
        termino = adn.split("INVESTIGA")[-1].strip() if "INVESTIGA" in adn else adn.split("BUSCA")[-1].strip()
        st.sidebar.info(f"🌐 FRIDAY EN LA RED: {termino}")
        if "DIRECCION" in adn or "MAPA" in adn:
            st.sidebar.markdown(f"📍 [Ver en Google Maps](https://www.google.com/maps/search/{termino.replace(' ', '+')})")
    
    if "AGREGA BOTON" in adn:
        nombre_b = adn.split("AGREGA BOTON")[-1].strip().split()[0]
        if st.sidebar.button(f"🔘 {nombre_b}"): st.toast(f"Acción: {nombre_b}")

# --- 2. FUNCIONES DE APOYO (ESTADÍSTICA Y FORMATO) ---
def ajustar_texto_largo(texto, ancho=35):
    return "\n".join(textwrap.wrap(str(texto), width=ancho))

def extract_value(text, pattern):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None

def crear_tabla_profesional(df, nombre_archivo, ancho_pulgadas=10):
    alto_pulgadas = (len(df) * 0.5) + 0.8
    fig, ax = plt.subplots(figsize=(ancho_pulgadas, alto_pulgadas))
    ax.axis('off')
    tabla = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colColours=["#1E7421"] * len(df.columns))
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(11)
    tabla.scale(1, 2)
    for (row, col), cell in tabla.get_celld().items():
        cell.set_edgecolor('black')
        cell.set_linewidth(1.5)
        if row == 0: cell.set_text_props(weight='bold', color='white')
    plt.savefig(nombre_archivo, bbox_inches='tight', dpi=200, pad_inches=0.1)
    plt.close()

def obtener_base_legal(delito):
    leyes = {
        "ROBO CON INTIMIDACION": "Art. 436 inciso 1º del Código Penal",
        "ROBO EN LUGAR NO HABITADO": "Art. 442 del Código Penal",
        "ROBO DE ACCESORIOS": "Art. 443 del Código Penal (Ley 20.931)",
        "HURTO": "Art. 446 del Código Penal",
        "RECEPTACION": "Art. 456 bis A del Código Penal"
    }
    for clave, articulo in leyes.items():
        if clave in delito.upper(): return articulo
    return "Artículo a determinar según relato (Revisión requerida)"

# --- 3. CONFIGURACIÓN VISUAL Y ESTILO ---
st.set_page_config(page_title="SISTEMA FRIDAY - COMANDO CENTRAL", layout="wide")
aplicar_evolucion_universal()

st.markdown("""
    <style>
    .stApp { background-color: #D1D8C4 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .section-header { 
        background-color: #004A2F !important; color: white; padding: 10px; 
        border-radius: 5px; font-weight: bold; border-left: 10px solid #C5A059; margin-bottom: 20px; 
    }
    .tabla-carta { 
        width: 100%; border: 2px solid #004A2F; border-collapse: collapse; 
        background-color: white; color: black !important; font-family: 'Arial'; 
        font-size: 12px; text-transform: uppercase; font-weight: bold; 
    }
    .tabla-carta td { border: 1.5px solid #004A2F; padding: 8px; }
    .celda-titulo { background-color: #4F6228 !important; color: white !important; text-align: center; font-size: 16px; }
    .celda-sub { background-color: #EBF1DE !important; text-align: center; color: black !important; }
    .celda-header-perfil { background-color: #D7E3BC !important; text-align: center; }
    .mini-tabla td { border: none !important; padding: 2px !important; }
    .border-inner-r { border-right: 1.5px solid #004A2F !important; width: 45%; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. MOTOR DE INTELIGENCIA FRIDAY ---
def procesar_relato_ia(texto):
    texto_u = texto.upper().replace("Aï¿½OS", "AÑOS")
    
    # Extracción de Datos
    tip_match = re.search(r'CODIGO DELITO\s?:\s?([^\n]+)', texto_u)
    tip = tip_match.group(1).strip() if tip_match else "ROBO DE ACCESORIOS DE VEHICULOS"
    
    h_delito = re.search(r'HORA DEL DELITO\s?:\s?(\d{1,2})', texto_u)
    tr = f"{int(h_delito.group(1)):02d}:00 A {(int(h_delito.group(1))+1)%24:02d}:00 HRS" if h_delito else "00:00 A 01:00 HRS"

    loc = extract_value(texto_u, r'DIRECCIÓN\s?:\s?([^\n\r]+)') or "SECTOR JURISDICCIONAL"
    gv = "MASCULINO" if "MASCULINO" in texto_u or "SR. " in texto_u else "FEMENINO" if "FEMENINO" in texto_u else "NO INDICA"
    esp = extract_value(texto_u, r'SUSTRACCION DE\s+([^\.]+)') or "ACCESORIOS VARIOS"
    
    # Delincuente y MO
    vest = "VESTIMENTA OSCURA" if "OSCURA" in texto_u else "NO INDICA"
    movil = "VEHICULO" if "VEHICULO" in texto_u else "A PIE"
    mo = f"EN CIRCUNSTANCIAS QUE LA VÍCTIMA SE ENCONTRABA EN {loc}, SUJETOS DESCONOCIDOS PROCEDIERON A LA SUSTRACCIÓN DE {esp}, PARA LUEGO DARSE A LA FUGA."
    
    return tip, tr, loc, gv, esp, vest, movil, mo.upper(), obtener_base_legal(tip)

# --- 5. INTERFAZ MULTI-MÓDULO ---
st.markdown('<div class="section-header">🧠 FRIDAY: COMANDO CENTRAL DE INTELIGENCIA</div>', unsafe_allow_html=True)
t1, t2, t3, t4 = st.tabs(["📄 ACTA STOP", "📈 STOP TRIMESTRAL", "📍 INFORME GEO", "📋 CARTA DE SITUACIÓN"])

with t1:
    st.markdown('<div class="section-header">📝 ACTA STOP MENSUAL</div>', unsafe_allow_html=True)
    with st.form("form_acta"):
        c1, c2 = st.columns(2)
        sem = c1.text_input("Semana de estudio", value="SEMANA 08")
        fec = c1.text_input("Fecha de sesión", value="24-02-2026")
        comp = c2.text_input("Compromiso Carabineros", value="INCREMENTAR PATRULLAJES")
        prob = st.text_area("Problemática Delictual", value="AUMENTO DE ROBO CON INTIMIDACIÓN EN SECTOR CUADRANTE 231")
        nom = st.text_input("Nombre", value="DIANA SANDOVAL ASTUDILLO")
        st.form_submit_button("🛡️ GENERAR ACTA")

with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO: GENERACIÓN PROFESIONAL</div>', unsafe_allow_html=True)
    with st.form("form_geo_final"):
        col1, col2, col3 = st.columns(3)
        doe_n = col1.text_input("DOE N°", "248812153")
        funcionario = col2.text_input("Funcionario", "JUAN ANDRES URRUTIA LOBOS")
        domicilio = col3.text_input("Domicilio", "PASAJE PILCOMAYO 8501")
        mapa_img = st.file_uploader("SUBIR MAPA SAIT", type=['png', 'jpg'])
        excel_geo = st.file_uploader("SUBIR EXCEL/CSV", type=['xlsx', 'csv'])
        if st.form_submit_button("🛡️ GENERAR INFORME GEO") and mapa_img and excel_geo:
            # Lógica completa de procesamiento de Excel y Word aquí...
            st.success("Analizando datos georreferenciales...")

with t4:
    st.markdown('<div class="section-header">📋 CARTA DE SITUACIÓN (PROYECTO FRIDAY)</div>', unsafe_allow_html=True)
    with st.expander("🗣️ CONSOLA DE ÓRDENES", expanded=True):
        col_o1, col_o2 = st.columns([4, 1])
        nueva_orden = col_o1.text_input("INSTRUCCIÓN PARA FRIDAY:")
        if col_o2.button("🚀 EVOLUCIONAR"):
            if nueva_orden: guardar_en_nube(nueva_orden.upper()); st.rerun()

    relato_in = st.text_area("PEGUE EL PARTE POLICIAL AQUÍ:", height=250)
    if st.button("⚡ ANALIZAR CON MEMORIA ACTIVA") and relato_in:
        tip, tr, loc, gv, esp, vest, movil, mo_ia, legal = procesar_relato_ia(relato_in)
        
        st.markdown(f"""
        <table class="tabla-carta">
            <tr style="background-color: #000000; color: #C5A059;">
                <td colspan="3" style="text-align: center; font-size: 11px;">⚠️ PROTOCOLO LEGAL ACTIVO: {legal}</td>
            </tr>
            <tr>
                <td rowspan="2" class="celda-titulo" style="width:40%">{tip}</td>
                <td class="celda-sub" style="width:20%">TRAMO</td>
                <td class="celda-sub" style="width:40%">LUGAR OCURRENCIA</td>
            </tr>
            <tr>
                <td style="text-align:center">{tr}</td>
                <td style="text-align:center">{loc}</td>
            </tr>
            <tr>
                <td class="celda-header-perfil">PERFIL VÍCTIMA</td>
                <td class="celda-header-perfil">PERFIL DELINCUENTE</td>
                <td class="celda-header-perfil">MODUS OPERANDI</td>
            </tr>
            <tr>
                <td style="padding:0; vertical-align:top;">
                    <table class="mini-tabla" style="width:100%">
                        <tr><td class="border-inner-r">GENERO</td><td>{gv}</td></tr>
                        <tr><td class="border-inner-r" style="border-top:1.5px solid #004A2F">ESPECIE</td><td style="border-top:1.5px solid #004A2F">{esp}</td></tr>
                    </table>
                </td>
                <td style="padding:0; vertical-align:top;">
                    <table class="mini-tabla" style="width:100%">
                        <tr><td class="border-inner-r">VESTIMENTA</td><td>{vest}</td></tr>
                        <tr><td class="border-inner-r" style="border-top:1.5px solid #004A2F">MOVIL</td><td style="border-top:1.5px solid #004A2F">{movil}</td></tr>
                    </table>
                </td>
                <td style="vertical-align:top; text-align:justify; font-size:11px; padding:10px;">{mo_ia}</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)