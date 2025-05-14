
import streamlit as st

def calcular_ev(cuota, probabilidad_ganar, apuesta):
    ganancia_potencial = (cuota - 1) * apuesta
    ev = (probabilidad_ganar * ganancia_potencial) - ((1 - probabilidad_ganar) * apuesta)
    return ev, ganancia_potencial

def calcular_fraccion_kelly(ev, ganancia_potencial):
    return ev / ganancia_potencial

def calcular_apuesta_recomendada(bankroll, fraccion_kelly):
    return bankroll * fraccion_kelly

st.title("Calculadora de Apuestas y Parlays")

st.header("Apuesta Individual")
bankroll = st.number_input("Bankroll (capital total)", min_value=0.0, value=1000.0)
cuota = st.number_input("Cuota de la apuesta", min_value=1.0, value=2.0)
probabilidad_ganar = st.number_input("Probabilidad estimada de ganar (%)", min_value=0.0, max_value=100.0, value=50.0) / 100
apuesta = st.number_input("Cantidad a apostar", min_value=0.0, value=100.0)

ev, ganancia_potencial = calcular_ev(cuota, probabilidad_ganar, apuesta)
fraccion_kelly = calcular_fraccion_kelly(ev, ganancia_potencial)
apuesta_recomendada = calcular_apuesta_recomendada(bankroll, fraccion_kelly)

st.write(f"Valor Esperado (EV): {ev:.2f}")
st.write(f"Ganancia Potencial: {ganancia_potencial:.2f}")
st.write(f"Fracción de Kelly: {fraccion_kelly:.2f}")
st.write(f"Apuesta Recomendada: {apuesta_recomendada:.2f}")

st.header("Parley")
num_apuestas = st.number_input("Número de apuestas en el parley", min_value=2, value=2)
cuotas = []
probabilidades_ganar = []
for i in range(num_apuestas):
    cuota_parley = st.number_input(f"Cuota de la apuesta {i+1}", min_value=1.0, value=2.0, key=f"cuota_{i}")
    probabilidad_ganar_parley = st.number_input(f"Probabilidad estimada de ganar (%) de la apuesta {i+1}", min_value=0.0, max_value=100.0, value=50.0, key=f"probabilidad_{i}") / 100
    cuotas.append(cuota_parley)
    probabilidades_ganar.append(probabilidad_ganar_parley)

cuota_total_parley = 1
probabilidad_total_ganar = 1
for cuota, probabilidad_ganar in zip(cuotas, probabilidades_ganar):
    cuota_total_parley *= cuota
    probabilidad_total_ganar *= probabilidad_ganar

ev_parley, ganancia_potencial_parley = calcular_ev(cuota_total_parley, probabilidad_total_ganar, apuesta)
fraccion_kelly_parley = calcular_fraccion_kelly(ev_parley, ganancia_potencial_parley)
apuesta_recomendada_parley = calcular_apuesta_recomendada(bankroll, fraccion_kelly_parley)

st.write(f"Cuota Total del Parley: {cuota_total_parley:.2f}")
st.write(f"Valor Esperado (EV) del Parley: {ev_parley:.2f}")
st.write(f"Ganancia Potencial del Parley: {ganancia_potencial_parley:.2f}")
st.write(f"Fracción de Kelly del Parley: {fraccion_kelly_parley:.2f}")
st.write(f"Apuesta Recomendada para el Parley: {apuesta_recomendada_parley:.2f}")
