import streamlit as st
import math

def main():
    st.set_page_config(page_title="Calculadora de Apuestas", page_icon="💰")
    st.title("💰 Calculadora de Apuestas Deportivas")
    st.markdown("""
    Esta herramienta te ayuda a calcular:
    - Probabilidades implícitas
    - Valor esperado (EV)
    - Ganancia potencial
    - Fracción de Kelly
    - Apuesta recomendada
    """)

    # Selección de tipo de apuesta
    tipo_apuesta = st.radio("Tipo de apuesta:", ("Individual", "Parlay"))

    if tipo_apuesta == "Individual":
        calcular_apuesta_individual()
    else:
        calcular_parlay()

def calcular_apuesta_individual():
    st.subheader("Apuesta Individual")
    
    col1, col2 = st.columns(2)
    with col1:
        cuota = st.number_input("Cuota (ej. 2.5):", min_value=1.01, step=0.01, format="%.2f")
    with col2:
        probabilidad_estimada = st.number_input("Tu probabilidad estimada (0-100%):", min_value=0.0, max_value=100.0, step=1.0, format="%.1f") / 100
    
    col3, col4 = st.columns(2)
    with col3:
        banca = st.number_input("Banca total ($):", min_value=1, step=1)
    with col4:
        apuesta = st.number_input("Monto a apostar ($):", min_value=1, step=1)

    if st.button("Calcular"):
        try:
            # Calcular probabilidad implícita
            prob_implicita = 1 / cuota
            
            # Calcular valor esperado (EV)
            ev = (probabilidad_estimada * (cuota - 1) - (1 - probabilidad_estimada)) * 100
            
            # Calcular ganancia potencial
            ganancia_potencial = apuesta * (cuota - 1)
            
            # Calcular fracción de Kelly
            if cuota > 1:
                kelly = ((cuota - 1) * probabilidad_estimada - (1 - probabilidad_estimada)) / (cuota - 1)
                kelly = max(0, kelly)  # No apostar si Kelly es negativo
                apuesta_recomendada = banca * kelly
            else:
                kelly = 0
                apuesta_recomendada = 0
            
            # Mostrar resultados
            st.success("### Resultados")
            
            cols = st.columns(2)
            cols[0].metric("Probabilidad implícita", f"{prob_implicita*100:.2f}%")
            cols[1].metric("Valor esperado (EV)", f"{ev:.2f}%", delta_color="inverse")
            
            cols = st.columns(2)
            cols[0].metric("Ganancia potencial", f"${ganancia_potencial:.2f}")
            cols[1].metric("Fracción de Kelly", f"{kelly*100:.2f}%")
            
            st.metric("Apuesta recomendada (Kelly)", f"${apuesta_recomendada:.2f}")
            
        except ZeroDivisionError:
            st.error("Error: División por cero. Verifica los valores ingresados.")

def calcular_parlay():
    st.subheader("Parlay")
    
    num_apuestas = st.slider("Número de apuestas en el Parlay:", 2, 10, 2)
    
    cuotas = []
    probabilidades = []
    
    for i in range(num_apuestas):
        st.markdown(f"### Apuesta {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            cuota = st.number_input(f"Cuota {i+1}:", min_value=1.01, step=0.01, format="%.2f", key=f"cuota_{i}")
            cuotas.append(cuota)
        with col2:
            prob = st.number_input(f"Probabilidad estimada {i+1} (0-100%):", min_value=0.0, max_value=100.0, step=1.0, format="%.1f", key=f"prob_{i}") / 100
            probabilidades.append(prob)
    
    col3, col4 = st.columns(2)
    with col3:
        banca = st.number_input("Banca total ($):", min_value=1, step=1, key="banca_parlay")
    with col4:
        apuesta = st.number_input("Monto a apostar ($):", min_value=1, step=1, key="apuesta_parlay")

    if st.button("Calcular Parlay"):
        try:
            # Calcular cuota total del parlay
            cuota_parlay = math.prod(cuotas)
            
            # Calcular probabilidad implícita total
            prob_implicita_parlay = 1 / cuota_parlay
            
            # Calcular probabilidad estimada total
            prob_estimada_parlay = math.prod(probabilidades)
            
            # Calcular EV del parlay
            ev_parlay = (prob_estimada_parlay * (cuota_parlay - 1) - (1 - prob_estimada_parlay)) * 100
            
            # Calcular ganancia potencial
            ganancia_potencial_parlay = apuesta * (cuota_parlay - 1)
            
            # Calcular fracción de Kelly para parlay
            if cuota_parlay > 1:
                kelly_parlay = ((cuota_parlay - 1) * prob_estimada_parlay - (1 - prob_estimada_parlay)) / (cuota_parlay - 1)
                kelly_parlay = max(0, kelly_parlay)  # No apostar si Kelly es negativo
                apuesta_recomendada_parlay = banca * kelly_parlay
            else:
                kelly_parlay = 0
                apuesta_recomendada_parlay = 0
            
            # Mostrar resultados
            st.success("### Resultados del Parlay")
            
            cols = st.columns(2)
            cols[0].metric("Cuota total", f"{cuota_parlay:.2f}")
            cols[1].metric("Probabilidad implícita", f"{prob_implicita_parlay*100:.4f}%")
            
            cols = st.columns(2)
            cols[0].metric("Probabilidad estimada", f"{prob_estimada_parlay*100:.4f}%")
            cols[1].metric("Valor esperado (EV)", f"{ev_parlay:.2f}%", delta_color="inverse")
            
            cols = st.columns(2)
            cols[0].metric("Ganancia potencial", f"${ganancia_potencial_parlay:.2f}")
            cols[1].metric("Fracción de Kelly", f"{kelly_parlay*100:.4f}%")
            
            st.metric("Apuesta recomendada (Kelly)", f"${apuesta_recomendada_parlay:.2f}")
            
        except ZeroDivisionError:
            st.error("Error: División por cero. Verifica los valores ingresados.")
        except Exception as e:
            st.error(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()