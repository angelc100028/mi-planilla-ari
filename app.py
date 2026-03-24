import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA Y PARCHE DE PRIVACIDAD
st.set_page_config(page_title="Planilla ARI - Calculadora", page_icon="📝", layout="centered")

# CSS para ocultar el botón de GitHub, el menú de Streamlit y el pie de página
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QS1h {display: none;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 2. TÍTULO Y PRESENTACIÓN
st.title("📲 Planilla ARI Digital")
st.subheader("Cálculo de Porcentaje de Retención (ISLR)")
st.write("Herramienta interactiva para la estimación de retención salarial.")

# 3. ENTRADA DE DATOS (Interactivo para móvil)
st.info("Complete los campos a continuación:")

with st.container():
    # Valor de la UT (Variable según el año actual)
    ut_valor = st.number_input("Valor de la UT Vigente (Bs.)", value=0.40, format="%.2f", help="Ajuste el valor según la Gaceta Oficial vigente.")
    
    # Remuneración
    remuneracion = st.number_input("Remuneración Total Estimada para el Año (Bs.)", min_value=0.0, step=1000.0)
    
    # Cargas Familiares
    cargas = st.number_input("Número de Cargas Familiares (Ascendientes/Descendientes)", min_value=0, max_value=20, step=1)

    # Desgravamen
    des_tipo = st.selectbox("Tipo de Desgravamen", ["Único (774 UT)", "Detallado (Soportado)"])
    if des_tipo == "Único (774 UT)":
        des_monto = 774 * ut_valor
    else:
        des_monto = st.number_input("Monto Total de Desgravámenes Detallados (Bs.)", min_value=0.0)

# 4. LÓGICA DE CÁLCULO FISCAL
enriquecimiento_neto = max(0.0, remuneracion - des_monto)
enriquecimiento_ut = enriquecimiento_neto / ut_valor

# Tabla de Tarifas (Tarifa 1 - Personas Naturales)
if enriquecimiento_ut <= 1000:
    p = 0.06; s = 0
elif enriquecimiento_ut <= 1500:
    p = 0.09; s = 30
elif enriquecimiento_ut <= 2000:
    p = 0.12; s = 75
elif enriquecimiento_ut <= 2500:
    p = 0.16; s = 155
elif enriquecimiento_ut <= 3000:
    p = 0.20; s = 255
elif enriquecimiento_ut <= 4500:
    p = 0.24; s = 375
elif enriquecimiento_ut <= 6000:
    p = 0.29; s = 600
else:
    p = 0.34; s = 900

# Cálculo final del impuesto
impuesto_bruto_ut = (enriquecimiento_ut * p) - s
rebaja_personal = 10 # 10 UT por ser persona natural
rebaja_familia = cargas * 10
impuesto_neto_ut = max(0.0, impuesto_bruto_ut - rebaja_personal - rebaja_familia)

# Porcentaje de Retención Final
if enriquecimiento_neto > 0:
    porcentaje_final = (impuesto_neto_ut * ut_valor / remuneracion) * 100
else:
    porcentaje_final = 0.0

# 5. RESULTADOS VISUALES
st.divider()
st.write("### Resultado de la Estimación:")

col1, col2 = st.columns(2)
with col1:
    st.metric("Base Gravable (UT)", f"{enriquecimiento_ut:,.2f}")
with col2:
    st.metric("Porcentaje de Retención", f"{porcentaje_final:.2f} %")

if porcentaje_final > 0:
    st.success(f"Usted debe declarar un **{porcentaje_final:.2f}%** de retención.")
else:
    st.warning("Su nivel de ingresos no genera retención de ISLR para los parámetros ingresados.")

st.caption("Nota: Esta calculadora es una herramienta de apoyo y no sustituye la asesoría legal o contable formal.")
