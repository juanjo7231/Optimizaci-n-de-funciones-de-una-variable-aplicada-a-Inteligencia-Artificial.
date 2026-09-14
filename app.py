import streamlit as st
import sympy as sp

st.title("🧮 Solucionador Integral de Optimización")
st.write("La verdad, esto de la optimización casi siempre empieza con un texto largo de un problema. Aquí puedes resolver tanto si ya tienes la fórmula lista como si quieres revisar un problema clásico.")

# Definir la variable simbólica
x = sp.Symbol('x', real=True)

# Pestañas para elegir cómo quieres trabajar
opcion = st.radio(
    "¿Cómo quieres resolver el problema hoy?",
    ("Tengo la función matemática directa", "Problemas clásicos de texto (Caja, Cerca, etc.)")
)

if opcion == "Tengo la función matemática directa":
    st.markdown("---")
    st.write("Escribe tu función $f(x)$ y dejamos que el cálculo hable por sí solo.")
    
    funcion_str = st.text_input("Ingresa la función f(x) (ejemplo: x**3 - 3*x + 2):", "x**3 - 3*x + 2")
    
    if funcion_str:
        try:
            f_expr = sp.sympify(funcion_str)
            
            st.subheader("1. Función analizada")
            st.latex(f"f(x) = {sp.latex(f_expr)}")
            
            # Primera derivada
            f_prime = sp.diff(f_expr, x)
            st.subheader("2. Primera Derivada f'(x)")
            st.latex(f"f'(x) = {sp.latex(f_prime)}")
            
            # Puntos críticos
            st.subheader("3. Puntos Críticos")
            puntos_criticos = sp.solve(f_prime, x)
            
            if puntos_criticos:
                for pc in puntos_criticos:
                    st.latex(f"x = {sp.latex(pc)}")
                    
                # Segunda derivada
                st.subheader("4. Clasificación")
                f_double_prime = sp.diff(f_prime, x)
                st.latex(f"f''(x) = {sp.latex(f_double_prime)}")
                
                for pc in puntos_criticos:
                    val_segunda = f_double_prime.subs(x, pc)
                    val_y = f_expr.subs(x, pc)
                    
                    try:
                        val_num = float(val_segunda)
                        y_num = float(val_y)
                        
                        if val_num > 0:
                            st.success(f"En x = {pc}, la segunda derivada es positiva ({val_num}). Hay un MÍNIMO LOCAL en ({pc}, {y_num})")
                        elif val_num < 0:
                            st.success(f"En x = {pc}, la segunda derivada es negativa ({val_num}). Hay un MÁXIMO LOCAL en ({pc}, {y_num})")
                        else:
                            st.warning(f"En x = {pc}, la segunda derivada es cero. El criterio no es concluyente.")
                    except:
                        st.info(f"Punto crítico en x = {pc}, y = {val_y}")
            else:
                st.warning("No se encontraron puntos críticos reales.")
        except Exception as e:
            st.error(f"Revisa la sintaxis. Detalle del error: {e}")

else:
    st.markdown("---")
    st.write("Aquí puedes calcular los problemas verbales más comunes de los parciales y talleres.")
    
    tipo_problema = st.selectbox(
        "Selecciona el tipo de problema:",
        ("Maximizar el volumen de una caja (esquinas recortadas)", "Maximizar el área de un terreno cercado (con un lado libre)")
    )
    
    if tipo_problema == "Maximizar el volumen de una caja (esquinas recortadas)":
        st.write("Imagina que tienes una hoja de cartón de dimensiones dadas y le recortas cuadrados de lado $x$ en las esquinas para doblar las pestañas.")
        
        L = st.number_input("Largo de la hoja (unidades):", min_value=1.0, value=10.0)
        A = st.number_input("Ancho de la hoja (unidades):", min_value=1.0, value=6.0)
        
        # Volumen V(x) = x * (L - 2x) * (A - 2x)
        # V(x) = x * (L*A - 2Lx - 2Ax + 4x^2)
        if st.button("Resolver problema de la caja"):
            try:
                # Construimos la función de volumen con sympy
                v_expr = x * (L - 2*x) * (A - 2*x)
                st.write("La función de volumen planteada es:")
                st.latex(f"V(x) = x({L} - 2x)({A} - 2x)")
                st.latex(f"V(x) = {sp.latex(sp.expand(v_expr))}")
                
                # Derivada del volumen
                v_prime = sp.diff(v_expr, x)
                st.subheader("Derivada V'(x)")
                st.latex(f"V'(x) = {sp.latex(v_prime)}")
                
                # Puntos críticos
                criticos = sp.solve(v_prime, x)
                st.subheader("Valores de x posibles:")
                
                # Filtrar valores lógicos (0 < x < min(L,A)/2)
                for c in criticos:
                    try:
                        c_val = float(c.evalf())
                        if 0 < c_val < min(L, A)/2:
                            volumen_max = float(v_expr.subs(x, c_val))
                            st.success(f"El corte ideal es $x = {c_val:.3f}$. Con esto se obtiene un volumen máximo de $V = {volumen_max:.3f}$ unidades cúbicas.")
                        else:
                            st.info(f"El valor $x = {c_val:.3f}$ matemático no aplica físicamente para las medidas de la hoja.")
                    except:
                        pass
            except Exception as e:
                st.error(f"Hubo un fallo al calcular: {e}")
                
    elif tipo_problema == "Maximizar el área de un terreno cercado (con un lado libre)":
        st.write("Tienes una cantidad fija de cerca $P$ y quieres armar un corral rectangular usando un muro existente como uno de los lados.")
        
        perimetro = st.number_input("Cantidad total de cerca disponible (metros):", min_value=1.0, value=100.0)
        
        # Si el lado contra el muro es y, y los otros dos son x, entonces P = 2x + y => y = P - 2x
        # Área A(x) = x * y = x * (P - 2x)
        if st.button("Resolver problema de la cerca"):
            try:
                a_expr = x * (perimetro - 2*x)
                st.write("La función de área planteada es:")
                st.latex(f"A(x) = x({perimetro} - 2x)")
                
                a_prime = sp.diff(a_expr, x)
                st.subheader("Derivada A'(x)")
                st.latex(f"A'(x) = {sp.latex(a_prime)}")
                
                criticos = sp.solve(a_prime, x)
                if criticos:
                    x_opt = float(criticos[0].evalf())
                    y_opt = float(perimetro - 2*x_opt)
                    area_max = float(a_expr.subs(x, x_opt))
                    
                    st.success(f"Para maximizar el área, las dimensiones ideales son:")
                    st.write(f"- Lados perpendiculares al muro ($x$): **{x_opt:.2f} metros**")
                    st.write(f"- Lado paralelo al muro ($y$): **{y_opt:.2f} metros**")
                    st.write(f"- Área máxima resultante: **{area_max:.2f} metros cuadrados**")
            except Exception as e:
                st.error(f"Hubo un fallo al calcular: {e}")
