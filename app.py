import streamlit as st
import sympy as sp

st.title("🧮 Solucionador de Optimización de una Variable")
st.write("Ingresa una función y esta herramienta te ayudará a resolver el problema de optimización paso a paso: derivada, puntos críticos y clasificación.")

# Definir la variable simbólica
x = sp.Symbol('x', real=True)

# Campo para que el usuario ingrese la función
funcion_str = st.text_input("Ingresa la función f(x) (ejemplo: x**3 - 3*x + 2):", "x**3 - 3*x + 2")

if funcion_str:
    try:
        # Convertir el texto del usuario en una expresión matemática de SymPy
        f_expr = sp.sympify(funcion_str)
        
        st.markdown("---")
        st.subheader("1. Función analizada")
        st.latex(f"f(x) = {sp.latex(f_expr)}")
        
        # Paso 2: Calcular la primera derivada
        f_prime = sp.diff(f_expr, x)
        st.subheader("2. Primera Derivada f'(x)")
        st.write("Calculamos la derivada para encontrar las posibles pendientes cero:")
        st.latex(f"f'(x) = {sp.latex(f_prime)}")
        
        # Paso 3: Encontrar puntos críticos (igualar a 0)
        st.subheader("3. Puntos Críticos")
        st.write("Igualamos la primera derivada a cero ($f'(x) = 0$) para hallar los valores críticos:")
        
        puntos_criticos = sp.solve(f_prime, x)
        
        if puntos_criticos:
            st.write("Se encontraron los siguientes valores críticos de $x$:")
            for pc in puntos_criticos:
                st.latex(f"x = {sp.latex(pc)}")
                
            # Paso 4: Criterio de la segunda derivada para clasificar
            st.subheader("4. Clasificación (Criterio de la Segunda Derivada)")
            f_double_prime = sp.diff(f_prime, x)
            st.write("Evaluamos la segunda derivada $f''(x)$ en los puntos críticos:")
            st.latex(f"f''(x) = {sp.latex(f_double_prime)}")
            
            for pc in puntos_criticos:
                # Evaluar la segunda derivada en el punto crítico
                val_segunda = f_double_prime.subs(x, pc)
                val_y = f_expr.subs(x, pc)
                
                try:
                    val_num = float(val_segunda)
                    y_num = float(val_y)
                    
                    if val_num > 0:
                        st.success(لf"En $x = {pc}$, $f''(x) = {val_num} > 0$. Por lo tanto, hay un **MÍNIMO LOCAL** en el punto $({pc}, {y_num})$")
                    elif val_num < 0:
                        st.success(f"En $x = {pc}$, $f''(x) = {val_num} < 0$. Por lo tanto, hay un **MÁXIMO LOCAL** en el punto $({pc}, {y_num})$")
                    else:
                        st.warning(f"En $x = {pc}$, $f''(x) = 0$. El criterio no es concluyente.")
                except:
                    st.info(f"Encontrado punto crítico en $x = {pc}$, con valor $y = {val_y}$.")
        else:
            st.warning("No se encontraron puntos críticos reales para esta función.")
            
    except Exception as e:
        st.error(f"Hubo un error al interpretar la función. Revisa la sintaxis (usa '*' para multiplicar y '**' para potencias). Detalle: {e}")
