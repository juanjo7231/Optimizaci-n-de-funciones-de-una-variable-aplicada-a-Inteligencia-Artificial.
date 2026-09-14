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
    try:
        st.image("logo_uis.webp", use_container_width=True)
    except:
        st.info("💡 Consejo: Sube un archivo llamado 'logo_uis.webp' a tu repositorio para ver el escudo de la UIS aquí.")
        
    st.markdown("### Universidad Industrial de Santander")
    st.markdown("**Sede Barrancabermeja**")
    st.markdown("Ingeniería en Inteligencia Artificial")
    st.markdown("---")
    
    modo = st.radio(
        "Modo de operación:",
        ("🎓 Tutor Interactivo de Problemas", "⚡ Solucionador Directo (Funciones)")
    )
    
    st.markdown("---")
    if st.button("🔄 Reiniciar Aplicación"):
        st.session_state.paso_tutor = "inicio"
        st.session_state.tipo_problema_activo = None
        st.rerun()
        
    st.markdown("---")
    st.caption("Desarrollado como asistente de cálculo aplicado.")

# Definir la variable simbólica
x = sp.Symbol('x', real=True)

# --- CUERPO PRINCIPAL ---
st.title("🤖 Tutor IA: Problemas de Optimización")

if modo == "🎓 Tutor Interactivo de Problemas":
    st.markdown("Hola, la idea de este espacio no es darte la respuesta de golpe, sino ayudarte a razonar, plantear y resolver paso a paso problemas clásicos de optimización.")
    
    if st.session_state.paso_tutor == "inicio":
        st.markdown("### Selecciona el problema que deseas resolver hoy:")
        tipo_problema = st.selectbox(
            "Caso de estudio:",
            (
                "Maximizar el volumen de una caja (esquinas recortadas)", 
                "Maximizar el área de un terreno cercado (con un lado libre)"
            )
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🚀 Empezar"):
                st.session_state.tipo_problema_activo = tipo_problema
                st.session_state.paso_tutor = "planteamiento"
                st.rerun()
                
    elif st.session_state.tipo_problema_activo == "Maximizar el volumen de una caja (esquinas recortadas)":
        L, A = 10.0, 6.0
        
        st.info("📦 **Problema Activo:** Se tiene una hoja de cartón rectangular de **10 x 6 unidades**. Se recortan cuadrados de lado $x$ en cada esquina para doblar los lados y construir una caja sin tapa.")
        
        if st.session_state.paso_tutor == "planteamiento":
            st.markdown("#### Paso 1: Planteamiento de la función")
            st.write("Piensa en cuáles serían las expresiones algebraicas para el **largo**, el **ancho** y la **altura** de la caja en función de $x$.")
            
            with st.expander("💡 Ver pista de apoyo"):
                st.write(f"Si a una longitud de {L} le quitas dos esquinas de tamaño $x$, el lado resultante es $L - 2x$. Haz lo mismo con el ancho $A = {A}$.")
                
            usuario_funcion = st.text_input("Escribe tu propuesta de función V(x) (ej: x*(10-2*x)*(6-2*x)):")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Ver solución paso a paso"):
                    st.session_state.paso_tutor = "solucion"
                    st.rerun()
            with col_b:
                if usuario_funcion:
                    st.success("¡Excelente iniciativa al escribir tu modelo! Vamos a contrastarlo con el desarrollo analítico a continuación.")
                    
        if st.session_state.paso_tutor == "solucion" or st.session_state.paso_tutor == "planteamiento":
            if st.session_state.paso_tutor == "solucion":
                st.markdown("---")
                st.markdown("#### 🔍 Desarrollo Analítico Completo:")
                v_expr = x * (L - 2*x) * (A - 2*x)
                st.latex(f"V(x) = x({L} - 2x)({A} - 2x) = {sp.latex(sp.expand(v_expr))}")
                
                v_prime = sp.diff(v_expr, x)
                st.markdown("**1. Derivada de la función de volumen:**")
                st.latex(f"V'(x) = {sp.latex(v_prime)} = 0")
                
                criticos = sp.solve(v_prime, x)
                st.markdown("**2. Puntos críticos encontrados:**")
                for c in criticos:
                    st.latex(f"x = {c.evalf():.3f}")
                    
                for c in criticos:
                    c_val = float(c.evalf())
                    if 0 < c_val < min(L, A)/2:
                        volumen_max = float(v_expr.subs(x, c_val))
                        st.balloons()
                        st.success(f"✅ **Conclusión:** El corte ideal es $x = {c_val:.3f}$ unidades, lo que nos otorga un volumen máximo de $V = {volumen_max:.3f}$ unidades cúbicas.")
                
                if st.button("🔄 Resolver otro problema"):
                    st.session_state.paso_tutor = "inicio"
                    st.session_state.tipo_problema_activo = None
                    st.rerun()

    else:
        # Caso Terreno Cercado
        perimetro = 100.0
        st.info(f" fenced 🏞️ **Problema Activo:** Se dispone de **{perimetro} metros** de cerca para cercar un terreno rectangular aprovechando un muro largo ya existente como uno de sus lados (no requiere cerca en ese lado).")
        
        st.markdown("#### 🔍 Desarrollo Analítico Completo:")
        a_expr = x * (perimetro - 2*x)
        st.latex(f"A(x) = x({perimetro} - 2x) = {sp.latex(sp.expand(a_expr))}")
        
        a_prime = sp.diff(a_expr, x)
        st.markdown("**1. Primera derivada:**")
        st.latex(f"A'(x) = {sp.latex(a_prime)}")
        
        criticos = sp.solve(a_prime, x)
        if criticos:
            x_opt = float(criticos[0].evalf())
            y_opt = float(perimetro - 2*x_opt)
            area_max = float(a_expr.subs(x, x_opt))
            st.balloons()
            st.success(f"✅ **Conclusión:** Las dimensiones óptimas del terreno son $x = {x_opt:.2f}\text{{ m}}$ (lados perpendiculares) y $y = {y_opt:.2f}\text{{ m}}$ (lado paralelo al muro), logrando un área máxima de ${area_max:.2f}\text{{ m}}^2$.")
            
        if st.button("🔄 Resolver otro problema"):
            st.session_state.paso_tutor = "inicio"
            st.session_state.tipo_problema_activo = None
            st.rerun()

else:
    # Modo Solucionador Directo (Funciones)
    st.markdown("### ⚡ Analizador y Solucionador de Funciones Arbitrarias")
    st.write("Introduce cualquier función de una variable $f(x)$ para calcular automáticamente sus puntos críticos y clasificarlos mediante el criterio de la segunda derivada.")
    
    col_input1, col_input2 = st.columns([3, 1])
    with col_input1:
        funcion_str = st.text_input("Función f(x) (Usa `**` para potencias y `*` para multiplicar):", "x**3 - 3*x - 2")
    with col_input2:
        st.markdown("<br>", unsafe_allow_html=True)
        analizar_btn = st.button("Analizar Función")
    
    if funcion_str:
        try:
            f_expr = sp.sympify(funcion_str)
            st.markdown("---")
            st.markdown("#### 📊 Resultados del Análisis:")
            
            st.write("Función analizada:")
            st.latex(f"f(x) = {sp.latex(f_expr)}")
            
            # Primera derivada
            f_prime = sp.diff(f_expr, x)
            st.markdown("**1. Primera derivada ($f'(x)$):**")
            st.latex(f"f'(x) = {sp.latex(f_prime)}")
            
            # Puntos críticos
            puntos_criticos = sp.solve(f_prime, x)
            st.markdown("**2. Puntos críticos ($f'(x) = 0$):**")
            
            if puntos_criticos:
                for pc in puntos_criticos:
                    st.latex(f"x = {sp.latex(pc)}")
                    
                # Segunda derivada y clasificación
                f_double_prime = sp.diff(f_prime, x)
                st.markdown("**3. Criterio de la segunda derivada ($f''(x)$):**")
                st.latex(f"f''(x) = {sp.latex(f_double_prime)}")
                
                for pc in puntos_criticos:
                    val_segunda = f_double_prime.subs(x, pc)
                    val_y = f_expr.subs(x, pc)
                    try:
                        val_num = float(val_segunda.evalf())
                        y_num = float(val_y.evalf())
                        
                        if val_num > 0:
                            st.success(f"En $x \\approx {float(pc.evalf()):.3f}$, la segunda derivada es positiva ($val = {val_num:.2f}$). Se trata de un **MÍNIMO LOCAL** en el punto $({float(pc.evalf()):.3f}, {y_num:.3f})$")
                        elif val_num < 0:
                            st.error(f"En $x \\approx {float(pc.evalf()):.3f}$, la segunda derivada es negativa ($val = {val_num:.2f}$). Se trata de un **MÁXIMO LOCAL** en el punto $({float(pc.evalf()):.3f}, {y_num:.3f})$")
                        else:
                            st.warning(f"En $x = {pc}$, la segunda derivada es cero; el criterio no es concluyente.")
                    except:
                        st.info(f"Punto crítico exacto hallado en $x = {pc}$, con imagen $y = {val_y}$.")
            else:
                st.warning("No se encontraron puntos críticos reales para esta función dentro del campo de los números reales.")
        except Exception as e:
            st.error(f"⚠️ Error al interpretar la función. Revisa que la sintaxis sea correcta (ejemplo: `2*x**2 + 5*x - 3`). Detalle técnico: {e}")import streamlit as st
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
    try:
        st.image("logo_uis.webp", use_container_width=True)
    except:
        st.info("💡 Consejo: Sube un archivo llamado 'logo_uis.webp' a tu repositorio para ver el escudo de la UIS aquí.")
        
    st.markdown("### Universidad Industrial de Santander")
    st.markdown("**Sede Barrancabermeja**")
    st.markdown("Ingeniería en Inteligencia Artificial")
    st.markdown("---")
    
    modo = st.radio(
        "Modo de operación:",
        ("🎓 Tutor Interactivo de Problemas", "⚡ Solucionador Directo (Funciones)")
    )
    
    st.markdown("---")
    if st.button("🔄 Reiniciar Aplicación"):
        st.session_state.paso_tutor = "inicio"
        st.session_state.tipo_problema_activo = None
        st.rerun()
        
    st.markdown("---")
    st.caption("Desarrollado como asistente de cálculo aplicado.")

# Definir la variable simbólica
x = sp.Symbol('x', real=True)

# --- CUERPO PRINCIPAL ---
st.title("🤖 Tutor IA: Problemas de Optimización")

if modo == "🎓 Tutor Interactivo de Problemas":
    st.markdown("Hola, la idea de este espacio no es darte la respuesta de golpe, sino ayudarte a razonar, plantear y resolver paso a paso problemas clásicos de optimización.")
    
    if st.session_state.paso_tutor == "inicio":
        st.markdown("### Selecciona el problema que deseas resolver hoy:")
        tipo_problema = st.selectbox(
            "Caso de estudio:",
            (
                "Maximizar el volumen de una caja (esquinas recortadas)", 
                "Maximizar el área de un terreno cercado (con un lado libre)"
            )
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🚀 Empezar"):
                st.session_state.tipo_problema_activo = tipo_problema
                st.session_state.paso_tutor = "planteamiento"
                st.rerun()
                
    elif st.session_state.tipo_problema_activo == "Maximizar el volumen de una caja (esquinas recortadas)":
        L, A = 10.0, 6.0
        
        st.info("📦 **Problema Activo:** Se tiene una hoja de cartón rectangular de **10 x 6 unidades**. Se recortan cuadrados de lado $x$ en cada esquina para doblar los lados y construir una caja sin tapa.")
        
        if st.session_state.paso_tutor == "planteamiento":
            st.markdown("#### Paso 1: Planteamiento de la función")
            st.write("Piensa en cuáles serían las expresiones algebraicas para el **largo**, el **ancho** y la **altura** de la caja en función de $x$.")
            
            with st.expander("💡 Ver pista de apoyo"):
                st.write(f"Si a una longitud de {L} le quitas dos esquinas de tamaño $x$, el lado resultante es $L - 2x$. Haz lo mismo con el ancho $A = {A}$.")
                
            usuario_funcion = st.text_input("Escribe tu propuesta de función V(x) (ej: x*(10-2*x)*(6-2*x)):")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Ver solución paso a paso"):
                    st.session_state.paso_tutor = "solucion"
                    st.rerun()
            with col_b:
                if usuario_funcion:
                    st.success("¡Excelente iniciativa al escribir tu modelo! Vamos a contrastarlo con el desarrollo analítico a continuación.")
                    
        if st.session_state.paso_tutor == "solucion" or st.session_state.paso_tutor == "planteamiento":
            if st.session_state.paso_tutor == "solucion":
                st.markdown("---")
                st.markdown("#### 🔍 Desarrollo Analítico Completo:")
                v_expr = x * (L - 2*x) * (A - 2*x)
                st.latex(f"V(x) = x({L} - 2x)({A} - 2x) = {sp.latex(sp.expand(v_expr))}")
                
                v_prime = sp.diff(v_expr, x)
                st.markdown("**1. Derivada de la función de volumen:**")
                st.latex(f"V'(x) = {sp.latex(v_prime)} = 0")
                
                criticos = sp.solve(v_prime, x)
                st.markdown("**2. Puntos críticos encontrados:**")
                for c in criticos:
                    st.latex(f"x = {c.evalf():.3f}")
                    
                for c in criticos:
                    c_val = float(c.evalf())
                    if 0 < c_val < min(L, A)/2:
                        volumen_max = float(v_expr.subs(x, c_val))
                        st.balloons()
                        st.success(f"✅ **Conclusión:** El corte ideal es $x = {c_val:.3f}$ unidades, lo que nos otorga un volumen máximo de $V = {volumen_max:.3f}$ unidades cúbicas.")
                
                if st.button("🔄 Resolver otro problema"):
                    st.session_state.paso_tutor = "inicio"
                    st.session_state.tipo_problema_activo = None
                    st.rerun()

    else:
        # Caso Terreno Cercado
        perimetro = 100.0
        st.info(f" fenced 🏞️ **Problema Activo:** Se dispone de **{perimetro} metros** de cerca para cercar un terreno rectangular aprovechando un muro largo ya existente como uno de sus lados (no requiere cerca en ese lado).")
        
        st.markdown("#### 🔍 Desarrollo Analítico Completo:")
        a_expr = x * (perimetro - 2*x)
        st.latex(f"A(x) = x({perimetro} - 2x) = {sp.latex(sp.expand(a_expr))}")
        
        a_prime = sp.diff(a_expr, x)
        st.markdown("**1. Primera derivada:**")
        st.latex(f"A'(x) = {sp.latex(a_prime)}")
        
        criticos = sp.solve(a_prime, x)
        if criticos:
            x_opt = float(criticos[0].evalf())
            y_opt = float(perimetro - 2*x_opt)
            area_max = float(a_expr.subs(x, x_opt))
            st.balloons()
            st.success(f"✅ **Conclusión:** Las dimensiones óptimas del terreno son $x = {x_opt:.2f}\text{{ m}}$ (lados perpendiculares) y $y = {y_opt:.2f}\text{{ m}}$ (lado paralelo al muro), logrando un área máxima de ${area_max:.2f}\text{{ m}}^2$.")
            
        if st.button("🔄 Resolver otro problema"):
            st.session_state.paso_tutor = "inicio"
            st.session_state.tipo_problema_activo = None
            st.rerun()

else:
    # Modo Solucionador Directo (Funciones)
    st.markdown("### ⚡ Analizador y Solucionador de Funciones Arbitrarias")
    st.write("Introduce cualquier función de una variable $f(x)$ para calcular automáticamente sus puntos críticos y clasificarlos mediante el criterio de la segunda derivada.")
    
    col_input1, col_input2 = st.columns([3, 1])
    with col_input1:
        funcion_str = st.text_input("Función f(x) (Usa `**` para potencias y `*` para multiplicar):", "x**3 - 3*x - 2")
    with col_input2:
        st.markdown("<br>", unsafe_allow_html=True)
        analizar_btn = st.button("Analizar Función")
    
    if funcion_str:
        try:
            f_expr = sp.sympify(funcion_str)
            st.markdown("---")
            st.markdown("#### 📊 Resultados del Análisis:")
            
            st.write("Función analizada:")
            st.latex(f"f(x) = {sp.latex(f_expr)}")
            
            # Primera derivada
            f_prime = sp.diff(f_expr, x)
            st.markdown("**1. Primera derivada ($f'(x)$):**")
            st.latex(f"f'(x) = {sp.latex(f_prime)}")
            
            # Puntos críticos
            puntos_criticos = sp.solve(f_prime, x)
            st.markdown("**2. Puntos críticos ($f'(x) = 0$):**")
            
            if puntos_criticos:
                for pc in puntos_criticos:
                    st.latex(f"x = {sp.latex(pc)}")
                    
                # Segunda derivada y clasificación
                f_double_prime = sp.diff(f_prime, x)
                st.markdown("**3. Criterio de la segunda derivada ($f''(x)$):**")
                st.latex(f"f''(x) = {sp.latex(f_double_prime)}")
                
                for pc in puntos_criticos:
                    val_segunda = f_double_prime.subs(x, pc)
                    val_y = f_expr.subs(x, pc)
                    try:
                        val_num = float(val_segunda.evalf())
                        y_num = float(val_y.evalf())
                        
                        if val_num > 0:
                            st.success(f"En $x \\approx {float(pc.evalf()):.3f}$, la segunda derivada es positiva ($val = {val_num:.2f}$). Se trata de un **MÍNIMO LOCAL** en el punto $({float(pc.evalf()):.3f}, {y_num:.3f})$")
                        elif val_num < 0:
                            st.error(f"En $x \\approx {float(pc.evalf()):.3f}$, la segunda derivada es negativa ($val = {val_num:.2f}$). Se trata de un **MÁXIMO LOCAL** en el punto $({float(pc.evalf()):.3f}, {y_num:.3f})$")
                        else:
                            st.warning(f"En $x = {pc}$, la segunda derivada es cero; el criterio no es concluyente.")
                    except:
                        st.info(f"Punto crítico exacto hallado en $x = {pc}$, con imagen $y = {val_y}$.")
            else:
                st.warning("No se encontraron puntos críticos reales para esta función dentro del campo de los números reales.")
        except Exception as e:
            st.error(f"⚠️ Error al interpretar la función. Revisa que la sintaxis sea correcta (ejemplo: `2*x**2 + 5*x - 3`). Detalle técnico: {e}")
