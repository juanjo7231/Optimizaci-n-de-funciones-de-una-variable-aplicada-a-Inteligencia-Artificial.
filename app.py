import streamlit as st
import sympy as sp

# Configuración de la página
st.set_page_config(
    page_title="Solucionador de Optimización - UIS",
    page_icon="🧮",
    layout="wide"
)

# --- BARRA LATERAL (IDENTIDAD Y OPCIONES) ---
with st.sidebar:
    # Cargamos tu imagen local en formato webp
    try:
        st.image("logo_uis.webp", use_container_width=True)
    except:
        st.warning("Coloca el archivo 'logo_uis.webp' en la misma carpeta para ver el logo.")
        
    st.markdown("### Universidad Industrial de Santander")
    st.markdown("**Sede Barrancabermeja**")
    st.markdown("Ingeniería en Inteligencia Artificial")
    st.markdown("---")
    
    modo = st.radio(
        "Modo de operación:",
        ("Problemas de Texto (Clásicos)", "Función Matemática Directa")
    )
    
    st.markdown("---")
    st.caption("Asistente interactivo para cálculo y optimización de una variable.")

# --- CUERPO PRINCIPAL (ESTILO CHAT) ---
st.title("🤖 Asistente IA: Solucionador de Optimización")
st.write("Hola, soy tu compañero para resolver problemas de optimización paso a paso. Plantéame el problema y te ayudo con todo el desglose matemático.")

# Definir la variable simbólica
x = sp.Symbol('x', real=True)

# Contenedor del chat
if modo == "Problemas de Texto (Clásicos)":
    with st.chat_message("user"):
        st.write("Necesito resolver un problema verbal de optimización (cajas o cercas).")
        
    with st.chat_message("assistant"):
        st.write("¡Claro que sí! Selecciona abajo cuál de los casos típicos vamos a resolver hoy y ajustamos los datos.")
        
    tipo_problema = st.selectbox(
        "Elige el tipo de problema:",
        ("Maximizar el volumen de una caja (esquinas recortadas)", "Maximizar el área de un terreno cercado (con un lado libre)")
    )
    
    if tipo_problema == "Maximizar el volumen de una caja (esquinas recortadas)":
        st.write("---")
        st.markdown("### 📦 Problema de la Caja")
        L = st.number_input("Largo de la hoja de cartón:", min_value=1.0, value=10.0)
        A = st.number_input("Ancho de la hoja de cartón:", min_value=1.0, value=6.0)
        
        if st.button("Resolver con IA"):
            try:
                v_expr = x * (L - 2*x) * (A - 2*x)
                with st.chat_message("assistant"):
                    st.write("Analizando el planteamiento geométrico...")
                    st.latex(f"V(x) = x({L} - 2x)({A} - 2x)")
                    st.latex(f"V(x) = {sp.latex(sp.expand(v_expr))}")
                    
                    v_prime = sp.diff(v_expr, x)
                    st.write("Calculando la derivada para hallar los puntos críticos:")
                    st.latex(f"V'(x) = {sp.latex(v_prime)}")
                    
                    criticos = sp.solve(v_prime, x)
                    encontrado = False
                    for c in criticos:
                        try:
                            c_val = float(c.evalf())
                            if 0 < c_val < min(L, A)/2:
                                volumen_max = float(v_expr.subs(x, c_val))
                                st.success(f"✅ **Solución encontrada:** Cortando esquinas de **$x = {c_val:.3f}$** unidades, se obtiene un volumen máximo de **$V = {volumen_max:.3f}$**.")
                                encontrado = True
                        except:
                            pass
                    if not encontrado:
                        st.warning("Los puntos críticos obtenidos no aplican físicamente para las dimensiones dadas.")
            except Exception as e:
                st.error(f"Ocurrió un error en el cálculo: {e}")
                
    elif tipo_problema == "Maximizar el área de un terreno cercado (con un lado libre)":
        st.write("---")
        st.markdown("### 🏡 Problema del Terreno / Cerca")
        perimetro = st.number_input("Cantidad total de cerca disponible (metros):", min_value=1.0, value=100.0)
        
        if st.button("Resolver con IA"):
            try:
                a_expr = x * (perimetro - 2*x)
                with st.chat_message("assistant"):
                    st.write("Planteando la función de área:")
                    st.latex(f"A(x) = x({perimetro} - 2x)")
                    
                    a_prime = sp.diff(a_expr, x)
                    st.write("Derivando e igualando a cero:")
                    st.latex(f"A'(x) = {sp.latex(a_prime)}")
                    
                    criticos = sp.solve(a_prime, x)
                    if criticos:
                        x_opt = float(criticos[0].evalf())
                        y_opt = float(perimetro - 2*x_opt)
                        area_max = float(a_expr.subs(x, x_opt))
                        
                        st.success(f"✅ **Dimensiones óptimas calculadas:**")
                        st.markdown(f"- Lados perpendiculares ($x$): **{x_opt:.2f} m**")
                        st.markdown(f"- Lado paralelo al muro ($y$): **{y_opt:.2f} m**")
                        st.markdown(f"- Área máxima: **{area_max:.2f} m²**")
            except Exception as e:
                st.error(f"Ocurrió un error en el cálculo: {e}")

else:
    with st.chat_message("user"):
        st.write("Tengo una función matemática directa para analizar.")
        
    with st.chat_message("assistant"):
        st.write("Perfecto, ingresa la expresión y te muestro el desglose completo de derivadas y puntos críticos.")
        
    funcion_str = st.text_input("Ingresa la función f(x) (ejemplo: x**3 - 3*x + 2):", "x**3 - 3*x + 2")
    
    if funcion_str:
        try:
            f_expr = sp.sympify(funcion_str)
            with st.chat_message("assistant"):
                st.write("Función evaluada:")
                st.latex(f"f(x) = {sp.latex(f_expr)}")
                
                f_prime = sp.diff(f_expr, x)
                st.write("1. Primera derivada:")
                st.latex(f"f'(x) = {sp.latex(f_prime)}")
                
                puntos_criticos = sp.solve(f_prime, x)
                st.write("2. Puntos críticos ($f'(x) = 0$):")
                
                if puntos_criticos:
                    for pc in puntos_criticos:
                        st.latex(f"x = {sp.latex(pc)}")
                        
                    f_double_prime = sp.diff(f_prime, x)
                    st.write("3. Criterio de la segunda derivada:")
                    st.latex(f"f''(x) = {sp.latex(f_double_prime)}")
                    
                    for pc in puntos_criticos:
                        val_segunda = f_double_prime.subs(x, pc)
                        val_y = f_expr.subs(x, pc)
                        try:
                            val_num = float(val_segunda)
                            y_num = float(val_y)
                            if val_num > 0:
                                st.success(f"En $x = {pc}$: MÍNIMO LOCAL en el punto $({pc}, {y_num})$")
                            elif val_num < 0:
                                st.success(f"En $x = {pc}$: MÁXIMO LOCAL en el punto $({pc}, {y_num})$")
                            else:
                                st.warning(f"En $x = {pc}$: Criterio no concluyente.")
                        except:
                            pass
                else:
                    st.warning("No se encontraron puntos críticos reales para esta función.")
        except Exception as e:
            st.error(f"Error al procesar la función. Verifica la sintaxis: {e}")
