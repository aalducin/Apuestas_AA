import streamlit as st
import math

def main():
    st.set_page_config(page_title="Calculadora de Apuestas", page_icon="💰")
    st.title("💰 Calculadora de Apuestas Deportivas")
    
    tipo_apuesta = st.radio("Tipo de apuesta:", ("Individual", "Parlay"))
    
    if tipo_apuesta == "Individual":
        calcular_apuesta_individual()
    else:
        calcular_parlay()

def calcular_apuesta_individual():
    st.subheader("Apuesta Individual")
    
    col1, col2 = st.columns(2)
    with col1:
        cuota = st.number_input("Cuota (ej. 2.5):", min_value=1.01, step=0.01, format="%.2f", value=1.5)
    with col2:
        usar_prob_implicita = st.checkbox("Usar probabilidad implícita", value=False)
        if usar_prob_implicita:
            probabilidad_estimada = 1 / cuota
            st.info(f"Probabilidad implícita usada: {probabilidad_estimada*100:.2f}%")
        else:
            probabilidad_estimada = st.number_input("Tu probabilidad estimada (0-100%):", 
                                                  min_value=0.0, max_value=100.0, step=1.0, 
                                                  format="%.1f", value=70.0) / 100
    
    col3, col4 = st.columns(2)
    with col3:
        banca = st.number_input("Banca total ($):", min_value=1, step=1, value=2000)
    with col4:
        apuesta = st.number_input("Monto a apostar ($):", min_value=1, step=1, value=100)

    if st.button("Calcular"):
        try:
            # Cálculos básicos
            prob_implicita = 1 / cuota
            ganancia_potencial = apuesta * (cuota - 1)
            
            # Cálculo de EV corregido
            ev = (probabilidad_estimada * (cuota - 1) - (1 - probabilidad_estimada)) * 100
            
            # Cálculo de Kelly corregido (fórmula exacta)
            if cuota > 1:
                kelly = (probabilidad_estimada * cuota - 1) / (cuota - 1)
                kelly = max(0, min(kelly, 1))  # Asegurar entre 0% y 100%
                apuesta_recomendada = banca * kelly
            else:
                kelly = 0
                apuesta_recomendada = 0
            
            # Mostrar resultados
            st.success("### Resultados Exactos")
            
            cols = st.columns(2)
            cols[0].metric("Probabilidad implícita", f"{prob_implicita*100:.2f}%")
            cols[1].metric("Valor esperado (EV)", f"{ev:.2f}%", 
                          delta_color="inverse" if ev < 0 else "normal")
            
            cols = st.columns(2)
            cols[0].metric("Ganancia potencial", f"${ganancia_potencial:.2f}")
            cols[1].metric("Fracción de Kelly", f"{kelly*100:.2f}%")
            
            st.metric("Apuesta recomendada (Kelly)", f"${apuesta_recomendada:.2f}")
            
        except Exception as e:
            st.error(f"Error en los cálculos: {str(e)}")

def calcular_parlay():
    st.subheader("Parlay")
    
    num_apuestas = st.slider("Número de apuestas:", 2, 10, 2)
    
    cuotas = []
    probabilidades = []
    
    for i in range(num_apuestas):
        st.markdown(f"### Apuesta {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            cuota = st.number_input(f"Cuota {i+1}:", min_value=1.01, step=0.01, format="%.2f", key=f"cuota_{i}")
            cuotas.append(cuota)
        with col2:
            usar_prob_implicita = st.checkbox(f"Usar prob. implícita {i+1}", value=False, key=f"usar_prob_{i}")
            if usar_prob_implicita:
                prob = 1 / cuota
                st.info(f"Prob. implícita usada: {prob*100:.2f}%")
            else:
                prob = st.number_input(f"Probabilidad estimada {i+1} (0-100%):", 
                                     min_value=0.0, max_value=100.0, step=1.0, 
                                     format="%.1f", key=f"prob_{i}") / 100
            probabilidades.append(prob)
    
    col3, col4 = st.columns(2)
    with col3:
        banca = st.number_input("Banca total ($):", min_value=1, step=1, key="banca_parlay")
    with col4:
        apuesta = st.number_input("Monto a apostar ($):", min_value=1, step=1, key="apuesta_parlay")

    if st.button("Calcular Parlay"):
        try:
            # Cálculos básicos
            cuota_parlay = math.prod(cuotas)
            prob_implicita_parlay = 1 / cuota_parlay
            prob_estimada_parlay = math.prod(probabilidades)
            
            # Cálculos corregidos
            ev_parlay = (prob_estimada_parlay * (cuota_parlay - 1) - (1 - prob_estimada_parlay)) * 100
            ganancia_potencial_parlay = apuesta * (cuota_parlay - 1)
            
            # Kelly para parlay corregido
            if cuota_parlay > 1:
                kelly_parlay = (prob_estimada_parlay * cuota_parlay - 1) / (cuota_parlay - 1)
                kelly_parlay = max(0, min(kelly_parlay, 1))  # Limitar entre 0% y 100%
                apuesta_recomendada_parlay = banca * kelly_parlay
            else:
                kelly_parlay = 0
                apuesta_recomendada_parlay = 0
            
            # Resultados
            st.success("### Resultados del Parlay")
            
            cols = st.columns(2)
            cols[0].metric("Cuota total", f"{cuota_parlay:.2f}")
            cols[1].metric("Probabilidad implícita", f"{prob_implicita_parlay*100:.4f}%")
            
            cols = st.columns(2)
            cols[0].metric("Probabilidad estimada", f"{prob_estimada_parlay*100:.4f}%")
            cols[1].metric("EV", f"{ev_parlay:.2f}%", 
                          delta_color="inverse" if ev_parlay < 0 else "normal")
            
            cols = st.columns(2)
            cols[0].metric("Ganancia potencial", f"${ganancia_potencial_parlay:.2f}")
            cols[1].metric("Fracción de Kelly", f"{kelly_parlay*100:.4f}%")
            
            st.metric("Apuesta recomendada", f"${apuesta_recomendada_parlay:.2f}")
            
        except Exception as e:
            st.error(f"Error en los cálculos: {str(e)}")

if __name__ == "__main__":
    main()