import streamlit as st
import sympy as sp

# Configuración de la página
st.set_page_config(
    page_title="Tutor de Optimización - UIS",
    page_icon="🤖",
    layout="wide"
)

# Inicializar variables de estado
if "paso_tutor" not in st.session_state:
    st.session_state.paso_tutor = "inicio"
if "tipo_problema_activo" not in st.session_state:
    st.session_state.tipo_problema_activo = None

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("### Universidad Industrial de Santander")
    st.markdown("**Sede Barrancabermeja**")
    st.markdown("Ingeniería en Inteligencia Artificial")
    st.markdown("---")
    
    modo = st.radio(
        "Modo de operación:",
        ("Tutor Interactivo de Problemas", "Solucionador Directo (Funciones)")
    )
    
    if st.button("Reiniciar Tutor / App"):
        st.session_state.paso_tutor = "inicio"
        st.session_state.tipo_problema_activo = None
        st.rerun()
        
    st.markdown("---")
    st.caption("Asistente personal de cálculo.")

# Definir la variable simbólica
x = sp.Symbol('x', real=True)

# --- CUERPO PRINCIPAL ---
st.title("🤖 Tutor IA: Problemas de Optimización")

if modo == "Tutor Interactivo de Problemas":
    st.write("Hola, aquí te ayudo a plantear y resolver paso a paso los problemas clásicos de optimización.")
    
    if st.session_state.paso_tutor == "inicio":
        tipo_problema = st.selectbox(
            "Selecciona el caso:",
            (
                "Maximizar el volumen de una caja (esquinas recortadas)", 
                "Maximizar el área de un terreno cercado (con un lado libre)"
            )
        )
        
        if st.button("Empezar a resolver"):
            st.session_state.tipo_problema_activo = tipo_problema
            st.session_state.paso_tutor = "ver_solucion"
            st.rerun()
            
    else:
        if st.session_state.tipo_problema_activo == "Maximizar el volumen de una caja (esquinas recortadas)":
            L = 10.0
            A = 6.0
            st.write("🔍 **Solución Paso a Paso:**")
            v_expr = x * (L - 2*x) * (A - 2*x)
            st.latex(f"V(x) = x({L} - 2x)({A} - 2x) = {sp.latex(sp.expand(v_expr))}")
            
            v_prime = sp.diff(v_expr, x)
            st.write("1. Derivamos e igualamos a cero:")
            st.latex(f"V'(x) = {sp.latex(v_prime)} = 0")
            
            criticos = sp.solve(v_prime, x)
            st.write("2. Puntos críticos hallados:")
            for c in criticos:
                c_val = float(c.evalf())
                if 0 < c_val < min(L, A)/2:
                    volumen_max = float(v_expr.subs(x, c_val))
                    st.success(f"✅ **Conclusión:** El corte ideal es $x = {c_val:.3f}$, obteniendo un volumen máximo de $V = {volumen_max:.3f}$.")
        else:
            perimetro = 100.0
            st.write("🔍 **Solución Paso a Paso:**")
            a_expr = x * (perimetro - 2*x)
            st.latex(f"A(x) = x({perimetro} - 2x) = {sp.latex(sp.expand(a_expr))}")
            
            a_prime = sp.diff(a_expr, x)
            st.write("1. Derivamos la función de área:")
            st.latex(f"A'(x) = {sp.latex(a_prime)}")
            
            criticos = sp.solve(a_prime, x)
            if criticos:
                x_opt = float(criticos[0].evalf())
                y_opt = float(perimetro - 2*x_opt)
                area_max = float(a_expr.subs(x, x_opt))
                st.success(f"✅ **Conclusión:** Las dimensiones óptimas son $x = {x_opt:.2f}\text{{ m}}$ y $y = {y_opt:.2f}\text{{ m}}$, logrando un área máxima de ${area_max:.2f}\text{{ m}}^2$.")
                
        if st.button("Resolver otro problema"):
            st.session_state.paso_tutor = "inicio"
            st.session_state.tipo_problema_activo = None
            st.rerun()

else:
    # Modo Solucionador Directo (Funciones)
    st.write("Ingresa tu función matemática abajo (usa `**` para potencias, por ejemplo: `x**3 - 3*x - 2`):")
    funcion_str = st.text_input("f(x) =", "x**3 - 3*x - 2")
    
    if funcion_str:
        try:
            f_expr = sp.sympify(funcion_str)
            st.write("Función analizada:")
            st.latex(f"f(x) = {sp.latex(f_expr)}")
            
            # Primera derivada
            f_prime = sp.diff(f_expr, x)
            st.write("1. Primera derivada $f'(x)$:")
            st.latex(f"f'(x) = {sp.latex(f_prime)}")
            
            # Puntos críticos
            puntos_criticos = sp.solve(f_prime, x)
            st.write("2. Puntos críticos ($f'(x) = 0$):")
            
            if puntos_criticos:
                for pc in puntos_criticos:
                    st.latex(f"x = {sp.latex(pc)}")
                    
                # Segunda derivada y clasificación
                f_double_prime = sp.diff(f_prime, x)
                st.write("3. Criterio de la segunda derivada $f''(x)$:")
                st.latex(f"f''(x) = {sp.latex(f_double_prime)}")
                
                for pc in puntos_criticos:
                    val_segunda = f_double_prime.subs(x, pc)
                    val_y = f_expr.subs(x, pc)
                    try:
                        val_num = float(val_segunda.evalf())
                        y_num = float(val_y.evalf())
                        if val_num > 0:
                            st.success(f"En $x \\approx {float(pc.evalf()):.3f}$, la segunda derivada es positiva ({val_num:.2f}). Hay un **MÍNIMO LOCAL** en $({float(pc.evalf()):.3f}, {y_num:.3f})$")
                        elif val_num < 0:
                            st.success(f"En $x \\approx {float(pc.evalf()):.3f}$, la segunda derivada es negativa ({val_num:.2f}). Hay un **MÁXIMO LOCAL** en $({float(pc.evalf()):.3f}, {y_num:.3f})$")
                        else:
                            st.warning(f"En $x = {pc}$, el criterio de la segunda derivada no es concluyente.")
                    except:
                        st.info(f"Punto crítico exacto en $x = {pc}$, con valor $y = {val_y}$.")
            else:
                st.warning("No se encontraron puntos críticos reales para esta función.")
        except Exception as e:
            st.error(f"Error al procesar la función. Revisa la sintaxis. Detalle: {e}")
