import streamlit as st

# Configuración de página para Móvil
st.set_page_config(page_title="Planilla ARI Digital", page_icon="📊")

st.title("📊 Calculadora ARI (ISLR)")
st.write("Complete los datos para calcular su porcentaje de retención.")

# --- ENTRADA DE DATOS ---
with st.expander("1. Datos de Remuneración", expanded=True):
    ut_valor = st.number_input("Valor de la Unidad Tributaria (Bs.)", value=0.02, format="%.4f")
    remuneracion = st.number_input("Remuneración Total Estimada (Anual)", min_value=0.0, step=1000.0)

with st.expander("2. Desgravámenes y Cargas"):
    tipo_desgravamen = st.radio("Tipo de Desgravamen", ["Único (774 UT)", "Detallado"])
    if tipo_desgravamen == "Único (774 UT)":
        monto_desgravamen = 774 * ut_valor
    else:
        monto_desgravamen = st.number_input("Monto Desgravamen Detallado", min_value=0.0)
    
    cargas_familiares = st.number_input("Número de Cargas Familiares (10 UT c/u)", min_value=0, step=1)

# --- LÓGICA DE CÁLCULO (Basada en tu Excel) ---
enriquecimiento_neto = max(0.0, remuneracion - monto_desgravamen)
enriquecimiento_ut = enriquecimiento_neto / ut_valor

# Escala de ISLR (Tarifa 1) extraída de tu planilla
if enriquecimiento_ut <= 1000:
    porcentaje = 0.06; sustraendo = 0
elif enriquecimiento_ut <= 1500:
    porcentaje = 0.09; sustraendo = 30
elif enriquecimiento_ut <= 2000:
    porcentaje = 0.12; sustraendo = 75
elif enriquecimiento_ut <= 2500:
    porcentaje = 0.16; sustraendo = 155
elif enriquecimiento_ut <= 3000:
    porcentaje = 0.20; sustraendo = 255
elif enriquecimiento_ut <= 4500:
    porcentaje = 0.24; sustraendo = 375
elif enriquecimiento_ut <= 6000:
    porcentaje = 0.29; sustraendo = 600
else:
    porcentaje = 0.34; sustraendo = 900

# Cálculo Final
impuesto_estimado_ut = (enriquecimiento_ut * porcentaje) - sustraendo
impuesto_con_cargas_ut = max(0.0, impuesto_estimado_ut - (cargas_familiares * 10) - 10) # 10 UT adicionales por el contribuyente
porcentaje_retencion = (impuesto_con_cargas_ut / enriquecimiento_ut * 100) if enriquecimiento_ut > 0 else 0

# --- RESULTADOS (Diseño Responsivo) ---
st.divider()
col1, col2 = st.columns(2)
col1.metric("Enriquecimiento (UT)", f"{enriquecimiento_ut:,.2f}")
col2.metric("Porcentaje de Retención", f"{porcentaje_retencion:.2f}%")

if porcentaje_retencion > 0:
    st.success(f"Usted debe aplicar un porcentaje de retención del **{porcentaje_retencion:.2f}%**")
else:
    st.info("Su enriquecimiento no alcanza el mínimo tributable.")
