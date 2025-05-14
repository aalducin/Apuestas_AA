
import streamlit as st

def calcular_probabilidad_implicita(cuota):
    try:
        if cuota > 0:
            return 1 / cuota
        else:
            return 0
    except ZeroDivisionError:
        return 0

def calcular_ev(probabilidad, cuota):
    return (probabilidad * cuota) - (1 - probabilidad)

def calcular_fraccion_kelly(probabilidad, cuota):
    return probabilidad - ((1 - probabilidad) / cuota)

def calcular_ganancia_potencial(apuesta, cuota):
    return apuesta * cuota

def calcular_apuesta_recomendada(apuesta, fraccion_kelly):
    return apuesta * fraccion_kelly

st.title("Calculadora de Apuestas")

tipo_apuesta = st.selectbox("Tipo de apuesta", ["Individual", "Parlay"])

if tipo_apuesta == "Individual":
    cuota = st.number_input("Cuota", min_value=0.01)
    probabilidad = st.number_input("Probabilidad (dejar en blanco para calcular automáticamente)", min_value=0.0, max_value=1.0, value=0.0)
    if probabilidad == 0.0:
        probabilidad = calcular_probabilidad_implicita(cuota)
    apuesta = st.number_input("Monto de la apuesta", min_value=0.01)
    
    ev = calcular_ev(probabilidad, cuota)
    fraccion_kelly = calcular_fraccion_kelly(probabilidad, cuota)
    ganancia_potencial = calcular_ganancia_potencial(apuesta, cuota)
    apuesta_recomendada = calcular_apuesta_recomendada(apuesta, fraccion_kelly)
    
    st.write(f"Valor Esperado (EV): {ev:.2f}")
    st.write(f"Fracción de Kelly: {fraccion_kelly:.2f}")
    st.write(f"Ganancia Potencial: {ganancia_potencial:.2f}")
    st.write(f"Apuesta Recomendada: {apuesta_recomendada:.2f}")

elif tipo_apuesta == "Parlay":
    num_apuestas = st.number_input("Número de apuestas en el parlay", min_value=2, step=1)
    cuotas = []
    probabilidades = []
    apuestas = []
    
    for i in range(num_apuestas):
        cuota = st.number_input(f"Cuota de la apuesta {i+1}", min_value=0.01)
        probabilidad = st.number_input(f"Probabilidad de la apuesta {i+1} (dejar en blanco para calcular automáticamente)", min_value=0.0, max_value=1.0, value=0.0)
        if probabilidad == 0.0:
            probabilidad = calcular_probabilidad_implicita(cuota)
        apuesta = st.number_input(f"Monto de la apuesta {i+1}", min_value=0.01)
        
        cuotas.append(cuota)
        probabilidades.append(probabilidad)
        apuestas.append(apuesta)
    
    cuota_total = 1
    probabilidad_total = 1
    ganancia_potencial_total = 0
    apuesta_recomendada_total = 0
    
    for i in range(num_apuestas):
        cuota_total *= cuotas[i]
        probabilidad_total *= probabilidades[i]
        ganancia_potencial_total += calcular_ganancia_potencial(apuestas[i], cuotas[i])
        apuesta_recomendada_total += calcular_apuesta_recomendada(apuestas[i], calcular_fraccion_kelly(probabilidades[i], cuotas[i]))
    
    ev_total = calcular_ev(probabilidad_total, cuota_total)
    fraccion_kelly_total = calcular_fraccion_kelly(probabilidad_total, cuota_total)
    
    st.write(f"Cuota Total: {cuota_total:.2f}")
    st.write(f"Probabilidad Total: {probabilidad_total:.2f}")
    st.write(f"Valor Esperado (EV) Total: {ev_total:.2f}")
    st.write(f"Fracción de Kelly Total: {fraccion_kelly_total:.2f}")
    st.write(f"Ganancia Potencial Total: {ganancia_potencial_total:.2f}")
    st.write(f"Apuesta Recomendada Total: {apuesta_recomendada_total:.2f}")
