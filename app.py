import streamlit as st

st.title("Tutor de Optimización con IA")
st.write("¡Bienvenido! Este espacio te guiará paso a paso para resolver problemas de optimización de una variable sin darte la respuesta directa.")

funcion_usuario = st.text_input("Ingresa tu función en términos de x (por ejemplo: x**2 - 4*x):", "")

if funcion_usuario:
    st.write(f"Has ingresado la función: **$f(x) = {funcion_usuario}$**")
    st.write("Ahora, intenta calcular la primera derivada $f'(x)$ en tu cuaderno o calculadora. ¿Cuál crees que es el primer paso?")
  
    intento_derivada = st.text_input("Escribe tu propuesta para la derivada:", "")
    
    if intento_derivada:
        st.info("¡Buen intento! Vamos a revisar la lógica paso a paso para ver si nos acercamos al punto crítico.")
