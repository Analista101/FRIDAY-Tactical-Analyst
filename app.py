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

# --- 1. PRIMERO DEFINIMOS CÓMO FUNCIONA LA MEMORIA ---
def cargar_memoria_nube():
    archivo = 'memoria_evolutiva.json'
    if os.path.exists(archivo):
        try:
            with open(archivo, 'r') as f:
                contenido = f.read().strip()
                if not contenido: 
                    return []
                return json.loads(contenido)
        except (json.JSONDecodeError, Exception):
            # Si el archivo está corrupto, FRIDAY lo ignora para no romperse
            return []
    return []

def guardar_en_nube(nueva_leccion):
    archivo = 'memoria_evolutiva.json'
    datos = cargar_memoria_nube()
    datos.append(nueva_leccion)
    with open(archivo, 'w') as f:
        json.dump(datos, f)

# --- 2. DESPUÉS CARGAMOS LA MEMORIA Y EL ESTILO ---
memoria_historia = cargar_memoria_nube()
color_texto = "white" # <--- Este valor cambia 'dinámicamente'

for leccion in memoria_historia:
    if "LETRA NEGRA" in leccion:
        color_texto = "black" # <--- Aquí ocurre el cambio de estado

def aplicar_evolucion_universal():
    memoria = cargar_memoria_nube()
    if not memoria: return
    
    adn = " ".join(memoria).upper()

    # --- A. PROTOCOLO DE BÚSQUEDA (INTERNET) ---
    if "INVESTIGA" in adn or "BUSCA" in adn:
        termino = adn.split("INVESTIGA")[-1].strip() if "INVESTIGA" in adn else adn.split("BUSCA")[-1].strip()
        st.sidebar.info(f"🌐 FRIDAY EN LA RED: Buscando '{termino}'...")
        if "DIRECCION" in adn or "MAPA" in adn:
            st.sidebar.markdown(f"📍 [Ver ubicación en Maps](https://www.google.com/maps/search/{termino.replace(' ', '+')})")

    # --- B. PROTOCOLO DE CREACIÓN DE INTERFAZ (AUTOPROGRAMACIÓN) ---
    if "AGREGA BOTON" in adn:
        nombre_b = adn.split("AGREGA BOTON")[-1].strip().split()[0]
        if st.sidebar.button(f"🔘 {nombre_b}"):
            st.toast(f"Acción ejecutada: {nombre_b}")

    # --- C. PROTOCOLO DE ELIMINACIÓN (REESTRUCTURACIÓN) ---
    if "BORRA PESTAÑA" in adn:
        st.sidebar.warning("⚠️ FRIDAY ha modificado la estructura de pestañas por orden superior.")

# Aplicamos el estilo que FRIDAY decidió basándose en su memoria
st.markdown(f"""
    <style>
    .stApp {{
        color: {color_texto};
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 0. FUNCIÓN AUXILIAR (CRÍTICA PARA EVITAR NAMEERROR) ---
def extract_value(text, pattern):
    """Extrae valores específicos usando regex para FRIDAY."""
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None

# --- 1. CONFIGURACIÓN VISUAL FRIDAY (SISTEMA REPARADO) ---
# Nota: st.set_page_config DEBE ser el primer comando de Streamlit. 
# Si da error, asegúrese de que no haya otros st. antes de este.
if 'config_ejecutada' not in st.session_state:
    st.set_page_config(page_title="SISTEMA FRIDAY - COMANDO CENTRAL", layout="wide")
    st.session_state.config_ejecutada = True

# FRIDAY revisa sus órdenes universales antes de mostrar nada
aplicar_evolucion_universal()

# Unificamos todo el CSS en un solo bloque seguro
st.markdown("""
    <style>
    /* Fondo y Base */
    .stApp { background-color: #D1D8C4 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #004A2F !important; }
    .reportview-container .main .block-container { padding: 25px; }
    
    /* Encabezados y Cajas de IA */
    .section-header { 
        background-color: #004A2F !important; 
        color: white; 
        padding: 10px; 
        border-radius: 5px; 
        font-weight: bold; 
        border-left: 10px solid #C5A059; 
        margin-bottom: 20px; 
    }
    .ia-box { 
        background-color: #002D1D; 
        color: #C5A059; 
        padding: 20px; 
        border-radius: 10px; 
        border: 2px solid #C5A059; 
        font-family: 'Arial', sans-serif; 
    }
    
    /* Output Legal (Corregido) */
    .legal-output-black { 
        background-color: #000000 !important; 
        color: #FFFFFF !important; 
        border-radius: 10px; 
        border: 2px solid #C5A059; 
        font-family: 'Arial'; 
        line-height: 1.6;
        font-size: 16px;
        padding: 15px;
    }
    
    /* Etiquetas y Tablas */
    label { color: black !important; font-weight: bold; }
    .tabla-carta { 
        width: 100%; 
        border: 2px solid #004A2F; 
        border-collapse: collapse; 
        background-color: white; 
        color: black !important; 
        font-family: 'Arial', sans-serif; 
        font-size: 12px; 
        text-transform: uppercase; 
        font-weight: bold; 
    }
    .tabla-carta td { border: 1.5px solid #004A2F; padding: 8px; }
    .celda-titulo { background-color: #4F6228 !important; color: white !important; text-align: center !important; font-size: 16px !important; }
    .celda-sub { background-color: #EBF1DE !important; text-align: center !important; color: black !important; }
    .celda-header-perfil { background-color: #D7E3BC !important; text-align: center !important; }
    .mini-tabla td { border: none !important; padding: 3px !important; }
    .border-inner-r { border-right: 1.5px solid #004A2F !important; width: 45%; }
    .border-inner-t { border-top: 1.5px solid #004A2F !important; }
    </style>
    """, unsafe_allow_html=True)

# --- PROTOCOLO DE SALUDO FRIDAY ---
if memoria_historia:
    st.sidebar.success(f"✅ NÚCLEO ACTIVO: {len(memoria_historia)} LECCIONES CARGADAS")
    st.sidebar.info(f"ÚLTIMO RECUERDO: {memoria_historia[-1]}")
else:
    st.sidebar.warning("⚠️ NÚCLEO VACÍO: Esperando instrucciones iniciales, Srta. Diana.")

# --- 2. GESTIÓN DE ESTADO ---
if "key_carta" not in st.session_state:
    st.session_state.key_carta = 0

def limpiar_solo_carta():
    st.session_state.key_carta += 1

# --- 2. MOTOR DE INTELIGENCIA FRIDAY (CARTA DE SITUACIÓN) ---
def procesar_relato_ia(texto):
    # Limpieza inicial y normalización
    texto_u = texto.upper().replace("Aï¿½OS", "AÑOS").replace("N°", "NRO")
    an_actual = 2026 
    
    # 1. TIPIFICACIÓN
    tip_match = re.search(r'CODIGO DELITO\s?:\s?([^\n]+)', texto_u)
    tipificacion = tip_match.group(1).strip() if tip_match else "ROBO DE ACCESORIOS DE VEHICULOS"

    # 2. TRAMO HORARIO
    h_delito = re.search(r'HORA DEL DELITO\s?:\s?(\d{1,2})', texto_u)
    tramo_hora = f"{int(h_delito.group(1)):02d}:00 A {(int(h_delito.group(1))+1)%24:02d}:00 HRS" if h_delito else "00:00 A 01:00 HRS"

    # 3. LUGAR DE OCURRENCIA
    dir_match = re.search(r'DIRECCIÓN\s?:\s?([^\n\r]+)', texto_u)
    lugar_ocurrencia = dir_match.group(1).strip() if dir_match else "RUTA 68"

    # 4. FUNCIÓN INTERNA: BASE LEGAL (Corregida Indentación)
    def obtener_base_legal(delito):
        # Diccionario dinámico de leyes chilenas (Base: Código Penal)
        leyes = {
            "ROBO CON INTIMIDACION": "Art. 436 inciso 1º del Código Penal",
            "ROBO EN LUGAR NO HABITADO": "Art. 442 del Código Penal",
            "ROBO DE ACCESORIOS": "Art. 443 del Código Penal (Ley 20.931)",
            "HURTO": "Art. 446 del Código Penal",
            "RECEPTACION": "Art. 456 bis A del Código Penal"
        }
        
        delito_u = delito.upper()
        for clave, articulo in leyes.items():
            if clave in delito_u:
                return articulo
        return "Artículo a determinar según relato (Revisión requerida)"

    # Ejecución de base legal
    base_legal_resultado = obtener_base_legal(tipificacion)

    # 5. PERFIL VÍCTIMA (PRIMER AFECTADO)
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

    # 6. ESPECIES
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

    # 7. DELINCUENTE
    gd = "MASCULINO" if any(x in texto_u for x in ["SUJETO", "INDIVIDUO", "HOMBRE"]) else "NO INDICA"
    ed = "NO INDICA"
    cd = "VESTIMENTA OSCURA" if "OSCURA" in texto_u else "NO INDICA"
    md = "VEHICULO" if "VEHICULO" in texto_u and "A PIE" not in texto_u else "A PIE"

    # 8. RESUMEN ADAPTATIVO (MODUS OPERANDI)
    if any(x in texto_u for x in ["ESTACIONADO", "APARCADO", "DEJO SU"]): est_v = "MANTENÍA SU VEHÍCULO ESTACIONADO"
    elif any(x in texto_u for x in ["CAMINANDO", "A PIE"]): est_v = "TRANSITABA A PIE"
    else: est_v = "SE ENCONTRABA"

    if any(x in texto_u for x in ["FRACTURARON", "VIDRIO"]): acc_v = "TRAS FRACTURAR UN VENTANAL DEL MÓVIL, SUSTRAJERON"
    elif any(x in texto_u for x in ["INTIMIDÓ", "AMENAZÓ"]): acc_v = "MEDIANTE INTIMIDACIÓN, LOGRARON SUSTRAER"
    else: acc_v = "PROCEDIERON A LA SUSTRACCIÓN DE"

    desc = "AL REGRESAR AL LUGAR"
    if "PERCATANDOSE" in texto_u: desc = "AL PERCATARSE DE LA SITUACIÓN"
    elif "INFORMANDOLE" in texto_u: desc = "TRAS SER ALERTADO POR TERCEROS"

    mo_final = f"EN CIRCUNSTANCIAS QUE LA VÍCTIMA {est_v} EN {tl}, {desc} NOTÓ QUE SUJETOS DESCONOCIDOS {acc_v} {esp}, PARA LUEGO DARSE A LA FUGA."

    # Retornamos 13 valores (incluyendo base legal al final)
    return tipificacion, tramo_hora, lugar_ocurrencia, gv, ev, tl, esp, gd, ed, cd, md, mo_final.upper(), base_legal_resultado

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
        
        submit_trim = st.form_submit_button("🛡️ GENERAR TRIMESTRAL")

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
            cell.set_text_props(weight='bold', color='white')

    plt.savefig(nombre_archivo, bbox_inches='tight', dpi=200, pad_inches=0.1)
    plt.close()

# --- ESTRUCTURA DE LA PESTAÑA INFORME GEO ---
with t3:
    st.markdown('<div class="section-header">📍 INFORME GEO: GENERACIÓN PROFESIONAL</div>', unsafe_allow_html=True)
    
    with st.form("form_geo_final"):
        col1, col2, col3 = st.columns(3)
        # DOE y Fechas
        doe_n = col1.text_input("DOE N°", value="248812153")
        doe_fecha = col1.text_input("Fecha DOE", value="03-03-2026")
        inf_fecha = col1.text_input("Fecha Informe", value="03 de marzo de 2026")
        
        # Funcionario
        funcionario = col2.text_input("Funcionario", value="JUAN ANDRES URRUTIA LOBOS")
        grado = col2.text_input("Grado", value="SARGENTO 2°")
        unidad = col2.text_input("Unidad", value="GRUPO DE ADIESTRAMIENTO CANINO")
        
        # Ubicación
        domicilio = col3.text_input("Domicilio", value="PASAJE PILCOMAYO 8501")
        subcomisaria = col3.text_input("Subcomisaría", value="26A COMISARIA PUDAHUEL")
        cuadrante = col3.text_input("Cuadrante", value="232-A")
        
        cp1, cp2, cp3 = st.columns([2, 1, 1])
        periodo_txt = cp1.text_input("Periodo", value="03-12-2025 al 03-03-2026")
        mapa_img = cp2.file_uploader("SUBIR MAPA SAIT", type=['png', 'jpg'])
        excel_geo = cp3.file_uploader("SUBIR EXCEL/CSV", type=['xlsx', 'csv'])
        
        submit_geo = st.form_submit_button("🛡️ GENERAR INFORME GEO")

# LA LÓGICA DE PROCESAMIENTO FUERA DEL FORM, PERO DEPENDIENTE DEL BOTÓN
    if submit_geo:
        if not mapa_img or not excel_geo:
            st.error("❌ Faltan archivos (Mapa o Excel) para procesar.")
        else:
            try:
                # 1. PROCESAMIENTO DE DATOS
                df = pd.read_csv(excel_geo) if excel_geo.name.endswith('csv') else pd.read_excel(excel_geo)
                df.columns = [c.upper().strip() for c in df.columns]
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
                else:
                    dia_frec, hora_frec = "NO IDENTIFICADO", "NO IDENTIFICADO"
                
                delito_principal = resumen_dmcs.iloc[0]['TIPO DE DELITO (DMCS)'] if not resumen_dmcs.empty else "DMCS"
                cantidad_real = resumen_dmcs.iloc[0]['CANTIDAD'] if not resumen_dmcs.empty else 0

                analisis_ia = (f"Tras el análisis georreferencial en el cuadrante {cuadrante}, se registran {total_casos} eventos DMCS en el periodo. "
                              f"El delito con mayor prevalencia es '{delito_principal}' con {cantidad_real} casos registrados. "
                              f"La criticidad se concentra los días {dia_frec} en el tramo {hora_frec}. "
                              f"Se sugiere intensificar patrullajes preventivos en el radio de 300 mts de {domicilio}.")

                # 2. GENERACIÓN DEL DOCUMENTO WORD (Procesamiento de Imágenes)
                doc = DocxTemplate("INFORME GEO.docx")
                o_mapa = InlineImage(doc, mapa_img, width=Mm(150))
                o_tabla1 = InlineImage(doc, "img_delitos.png", width=Mm(145))
                o_tabla2 = InlineImage(doc, "img_tramos.png", width=Mm(130))

                # Manejo seguro del periodo
                p_split = periodo_txt.split(" al ")
                p_inicio = p_split[0] if len(p_split) > 0 else "INICIO"
                p_fin = p_split[1] if len(p_split) > 1 else "FIN"

                contexto = {
                    "domicilio": domicilio.upper(), "jurisdiccion": subcomisaria.upper(), "fecha_actual": inf_fecha.upper(),
                    "doe": doe_n, "fecha_doe": doe_fecha, "grado_solic": grado.upper(),
                    "solicitante": funcionario.upper(), "unidad_solic": unidad.upper(),
                    "periodo_inicio": p_inicio, "periodo_fin": p_fin,
                    "cuadrante": cuadrante, "mapa": o_mapa, "total_dmcs": total_casos,
                    "tabla": o_tabla1, "tabla_horarios": o_tabla2,
                    "dia_max": dia_frec, "hora_max": hora_frec, "conclusion_ia": analisis_ia.upper()
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
    
    # --- CONSOLA DE ÓRDENES ---
    with st.expander("🗣️ CONSOLA DE ÓRDENES (HABLAR CON FRIDAY)", expanded=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            nueva_orden = st.text_input("INSTRUCCIÓN PARA EL SISTEMA:", placeholder="FRIDAY, cambia tu código para...")
        with col2:
            st.write("") 
            if st.button("🚀 EVOLUCIONAR Y APLICAR"):
                if nueva_orden:
                    guardar_en_nube(nueva_orden.upper())
                    st.success("SISTEMA ACTUALIZADO. REINICIANDO...")
                    st.rerun()

    # --- FORMULARIO DE ANÁLISIS ---
    with st.form("form_friday_final", clear_on_submit=False):
        # Usamos la key dinámica para poder limpiar el área de texto
        relato_in = st.text_area(
            "PEGUE EL PARTE POLICIAL AQUÍ:", 
            height=250, 
            key=f"relato_{st.session_state.key_carta}"
        )
        
        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            ejecutar = st.form_submit_button("⚡ ANALIZAR CON MEMORIA ACTIVA")
        with col_btn2:
            # Este es el botón que usted solicitó en su instrucción
            limpiar = st.form_submit_button("🗑️ LIMPIAR RELATO")

    # Lógica del botón Limpiar (fuera del diseño, pero activa)
    if limpiar:
        st.session_state.key_carta += 1
        st.rerun()

    if ejecutar and relato_in:
        # 1. EXTRACCIÓN Y PROCESAMIENTO
        tip, tr, loc, gv, ev, tl_clase, esp, gd, ed, cd, md, mo_ia, base_legal_res = procesar_relato_ia(relato_in)
        
        # --- (El resto del código de la tabla HTML sigue igual aquí abajo) ---