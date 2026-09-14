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
        st.warning("Coloca el archivo 'logo_uis.webp' en la misma carpeta para ver el logo.")
        
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
    st.caption("Tu asistente personal de cálculo.")

# Definir la variable simbólica
x = sp.Symbol('x', real=True)

# --- CUERPO PRINCIPAL ---
st.title("🤖 Tutor IA: Problemas de Optimización")

if modo == "Tutor Interactivo de Problemas":
    st.write("Hola, la idea aquí no es darte la respuesta de una, sino guiarte paso a paso para que entiendas cómo se resuelve el problema.")
    
    if st.session_state.paso_tutor == "inicio":
        with st.chat_message("assistant"):
            st.write("¿Qué problema de optimización quieres que trabajemos hoy?")
            
        tipo_problema = st.selectbox(
            "Selecciona el caso:",
            ("Maximizar el volumen de una caja (esquinas recortadas)", "Maximizar el área de un terreno cercado (con un lado libre)")
        )
        
        if st.button("Empezar a resolver"):
            st.session_state.tipo_problema_activo = tipo_problema
            st.session_state.paso_tutor = "pista_planteamiento"
            st.rerun()

    elif st.session_state.tipo_problema_activo == "Maximizar el volumen de una caja (esquinas recortadas)":
        L = 10.0
        A = 6.0
        
        with st.chat_message("user"):
            st.write("Quiero resolver el problema de la caja con una hoja de 10x6.")
            
        if st.session_state.paso_tutor == "pista_planteamiento":
            with st.chat_message("assistant"):
                st.write("¡Perfecto! Tenemos una hoja rectangular de **10 por 6 unidades**. A cada esquina le recortamos un cuadrado de lado $x$.")
                st.write("💡 **Pista 1 (Planteamiento):** Piensa en cuáles serían las nuevas dimensiones de la caja en función de $x$.")
                
            if st.button("Ya sé la función / Continuar"):
                st.session_state.paso_tutor = "ver_solucion"
                st.rerun()
                
        elif st.session_state.paso_tutor == "ver_solucion":
            with st.chat_message("assistant"):
                st.write("🔍 **Solución Paso a Paso:**")
                v_expr = x * (L - 2*x) * (A - 2*x)
                st.latex(f"V(x) = x({L} - 2x)({A} - 2x) = {sp.latex(sp.expand(v_expr))}")
                
                v_prime = sp.diff(v_expr, x)
                st.write("1. Derivamos e igualamos a cero:")
                st.latex(f"V'(x) = {sp.latex(v_prime)} = 0")
                
                criticos = sp.solve(v_prime, x)
                st.write("2. Puntos críticos hallados:")
                for c in criticos:
                    st.latex(f"x = {c.evalf():.3f}")
                    
                for c in criticos:
                    c_val = float(c.evalf())
                    if 0 < c_val < min(L, A)/2:
                        volumen_max = float(v_expr.subs(x, c_val))
                        st.success(f"✅ **Conclusión:** El corte ideal es $x = {c_val:.3f}$, obteniendo un volumen máximo de $V = {volumen_max:.3f}$.")
                        
            if st.button("Resolver otro problema"):
                st.session_state.paso_tutor = "inicio"
                st.session_state.tipo_problema_activo = None
                st.rerun()

    elif st.session_state.tipo_problema_activo == "Maximizar el área de un terreno cercado (con un lado libre)":
        perimetro = 100.0
        
        with st.chat_message("user"):
            st.write("Quiero resolver el problema del terreno cercado con 100 metros de cerca.")
            
        with st.chat_message("assistant"):
            st.write(f"🔍 **Solución Paso a Paso:**")
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
    with st.chat_message("user"):
        st.write("Quiero evaluar una función directa.")
    with st.chat_message("assistant"):
        st.write("Ingresa tu función matemática abajo (recuerda usar `**` para potencias, por ejemplo: `x**3 - 3*x - 2`):")
        
    funcion_str = st.text_input("f(x) =", "x**3 - 3*x - 2")
    
    if funcion_str:
        try:
            f_expr = sp.sympify(funcion_str)
            with st.chat_message("assistant"):
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
            st.error(f"Error al procesar la función. Revisa la sintaxis (usa '*' para multiplicar y '**' para potencias). Detalle: {e}")
    # CASO 1: CAJA
    elif st.session_state.tipo_problema_activo == "Maximizar el volumen de una caja (esquinas recortadas)":
        L = 10.0
        A = 6.0
        
        with st.chat_message("user"):
            st.write("Quiero resolver el problema de la caja con una hoja de 10x6.")
            
        if st.session_state.paso_tutor == "pista_planteamiento":
            with st.chat_message("assistant"):
                st.write("¡Perfecto! Tenemos una hoja rectangular de **10 por 6 unidades**. A cada esquina le recortamos un cuadrado de lado $x$.")
                st.write("💡 **Pista 1 (Planteamiento):** Piensa en cuáles serían las nuevas dimensiones de la caja (largo, ancho y altura) en función de $x$ antes de armar la fórmula del volumen $V(x) = \text{largo} \times \text{ancho} \times \text{alto}$.")
                
            if st.button("Ya sé la función / Ver siguiente pista o pregunta"):
                st.session_state.paso_tutor = "pregunta_usuario"
                st.rerun()
                
        elif st.session_state.paso_tutor == "pregunta_usuario":
            with st.chat_message("assistant"):
                st.write("¿Cómo te quedó planteada la función de volumen $V(x)$ o qué valor crees que da el corte $x$?")
                
            respuesta_estudiante = st.text_input("Escribe tu resultado o lo que te dio (ej: x*(10-2*x)*(6-2*x) o x=1.2):")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Enviar respuesta al tutor"):
                    if respuesta_estudiante:
                        st.info(f"Analizando tu respuesta: '{respuesta_estudiante}'... ¡Buen intento! Vamos a ver el desglose completo para que lo compares.")
                        st.session_state.paso_tutor = "ver_solucion"
                        st.rerun()
            with col2:
                if st.button("No sé, muéstrame la respuesta completa"):
                    st.session_state.paso_tutor = "ver_solucion"
                    st.rerun()
                    
        elif st.session_state.paso_tutor == "ver_solucion":
            with st.chat_message("assistant"):
                st.write("🔍 **Solución Paso a Paso:**")
                v_expr = x * (L - 2*x) * (A - 2*x)
                st.latex(f"V(x) = x({L} - 2x)({A} - 2x) = {sp.latex(sp.expand(v_expr))}")
                
                v_prime = sp.diff(v_expr, x)
                st.write("1. Derivamos e igualamos a cero:")
                st.latex(f"V'(x) = {sp.latex(v_prime)} = 0")
                
                criticos = sp.solve(v_prime, x)
                st.write("2. Puntos críticos hallados:")
                for c in criticos:
                    st.latex(f"x = {c.evalf():.3f}")
                    
                for c in criticos:
                    c_val = float(c.evalf())
                    if 0 < c_val < min(L, A)/2:
                        volumen_max = float(v_expr.subs(x, c_val))
                        st.success(f"✅ **Conclusión:** El corte ideal es $x = {c_val:.3f}$, obteniendo un volumen máximo de $V = {volumen_max:.3f}$.")
                        
            if st.button("Resolver otro problema"):
                st.session_state.paso_tutor = "inicio"
                st.session_state.tipo_problema_activo = None
                st.rerun()

    # CASO 2: CERCA
    elif st.session_state.tipo_problema_activo == "Maximizar el área de un terreno cercado (con un lado libre)":
        perimetro = 100.0
        
        with st.chat_message("user"):
            st.write("Quiero resolver el problema del terreno cercado con 100 metros de cerca.")
            
        if st.session_state.paso_tutor == "pista_planteamiento":
            with st.chat_message("assistant"):
                st.write(f"¡Genial! Tenemos **{perimetro} metros** de cerca y un muro existente que nos ahorra uno de los lados.")
                st.write("💡 **Pista 1:** Si llamamos $x$ a los dos lados perpendiculares al muro, ¿cuánto mide el lado paralelo en función de $x$ y el perímetro total?")
                
            if st.button("Ver siguiente paso / Preguntar"):
                st.session_state.paso_tutor = "pregunta_usuario"
                st.rerun()
                
        elif st.session_state.paso_tutor == "pregunta_usuario":
            with st.chat_message("assistant"):
                st.write("¿Qué función de área $A(x)$ planteaste o qué valor crees que optimiza el terreno?")
                
            respuesta_estudiante = st.text_input("Escribe tu función o resultado aquí:")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Enviar al tutor"):
                    if respuesta_estudiante:
                        st.info("¡Excelente razonamiento! Vamos a contrastarlo con la solución matemática.")
                        st.session_state.paso_tutor = "ver_solucion"
                        st.rerun()
            with col2:
                if st.button("Ver solución completa"):
                    st.session_state.paso_tutor = "ver_solucion"
                    st.rerun()
                    
        elif st.session_state.paso_tutor == "ver_solucion":
            with st.chat_message("assistant"):
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
                    
                    st.success(f"✅ **Conclusión:** Las dimensiones óptimas son $x = {x_opt:.2f}\text{ m}$ y $y = {y_opt:.2f}\text{ m}$, logrando un área máxima de ${area_max:.2f}\text{ m}^2$.")
                    
            if st.button("Resolver otro problema"):
                st.session_state.paso_tutor = "inicio"
                st.session_state.tipo_problema_activo = None
                st.rerun()

else:
    # Modo Solucionador Directo (Funciones)
    with st.chat_message("user"):
        st.write("Quiero evaluar una función directa.")
    with st.chat_message("assistant"):
        st.write("Ingresa tu función matemática abajo (recuerda usar `**` para potencias, por ejemplo: `x**3 - 3*x - 2`):")
        
    funcion_str = st.text_input("f(x) =", "x**3 - 3*x - 2")
    
    if funcion_str:
        try:
            f_expr = sp.sympify(funcion_str)
            with st.chat_message("assistant"):
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
            st.error(f"Error al procesar la función. Revisa la sintaxis (usa '*' para multiplicar y '**' para potencias). Detalle: {e}")    # CASO 1: CAJA
    elif st.session_state.tipo_problema_activo == "Maximizar el volumen de una caja (esquinas recortadas)":
        L = 10.0
        A = 6.0
        
        with st.chat_message("user"):
            st.write("Quiero resolver el problema de la caja con una hoja de 10x6.")
            
        if st.session_state.paso_tutor == "pista_planteamiento":
            with st.chat_message("assistant"):
                st.write("¡Perfecto! Tenemos una hoja rectangular de **10 por 6 unidades**. A cada esquina le recortamos un cuadrado de lado $x$.")
                st.write("💡 **Pista 1 (Planteamiento):** Piensa en cuáles serían las nuevas dimensiones de la caja (largo, ancho y altura) en función de $x$ antes de armar la fórmula del volumen $V(x) = \text{largo} \times \text{ancho} \times \text{alto}$.")
                
            if st.button("Ya sé la función / Ver siguiente pista o pregunta"):
                st.session_state.paso_tutor = "pregunta_usuario"
                st.rerun()
                
        elif st.session_state.paso_tutor == "pregunta_usuario":
            with st.chat_message("assistant"):
                st.write("¿Cómo te quedó planteada la función de volumen $V(x)$ o qué valor crees que da el corte $x$?")
                
            respuesta_estudiante = st.text_input("Escribe tu resultado o lo que te dio (ej: x*(10-2*x)*(6-2*x) o x=1.2):")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Enviar respuesta al tutor"):
                    if respuesta_estudiante:
                        st.info(f"Analizando tu respuesta: '{respuesta_estudiante}'... ¡Buen intento! Vamos a ver el desglose completo para que lo compares.")
                        st.session_state.paso_tutor = "ver_solucion"
                        st.rerun()
            with col2:
                if st.button("No sé, muéstrame la respuesta completa"):
                    st.session_state.paso_tutor = "ver_solucion"
                    st.rerun()
                    
        elif st.session_state.paso_tutor == "ver_solucion":
            with st.chat_message("assistant"):
                st.write("🔍 **Solución Paso a Paso:**")
                v_expr = x * (L - 2*x) * (A - 2*x)
                st.latex(f"V(x) = x({L} - 2x)({A} - 2x) = {sp.latex(sp.expand(v_expr))}")
                
                v_prime = sp.diff(v_expr, x)
                st.write("1. Derivamos e igualamos a cero:")
                st.latex(f"V'(x) = {sp.latex(v_prime)} = 0")
                
                criticos = sp.solve(v_prime, x)
                st.write("2. Puntos críticos hallados:")
                for c in criticos:
                    st.latex(f"x = {c.evalf():.3f}")
                    
                for c in criticos:
                    c_val = float(c.evalf())
                    if 0 < c_val < min(L, A)/2:
                        volumen_max = float(v_expr.subs(x, c_val))
                        st.success(f"✅ **Conclusión:** El corte ideal es $x = {c_val:.3f}$, obteniendo un volumen máximo de $V = {volumen_max:.3f}$.")
                        
            if st.button("Resolver otro problema"):
                st.session_state.paso_tutor = "inicio"
                st.rerun()

    # CASO 2: CERCA
    elif st.session_state.tipo_problema_activo == "Maximizar el área de un terreno cercado (con un lado libre)":
        perimetro = 100.0
        
        with st.chat_message("user"):
            st.write("Quiero resolver el problema del terreno cercado con 100 metros de cerca.")
            
        if st.session_state.paso_tutor == "pista_planteamiento":
            with st.chat_message("assistant"):
                st.write(f"¡Genial! Tenemos **{perimetro} metros** de cerca y un muro existente que nos ahorra uno de los lados.")
                st.write("💡 **Pista 1:** Si llamamos $x$ a los dos lados perpendiculares al muro, ¿cuánto mide el lado paralelo en función de $x$ y el perímetro total?")
                
            if st.button("Ver siguiente paso / Preguntar"):
                st.session_state.paso_tutor = "pregunta_usuario"
                st.rerun()
                
        elif st.session_state.paso_tutor == "pregunta_usuario":
            with st.chat_message("assistant"):
                st.write("¿Qué función de área $A(x)$ planteaste o qué valor crees que optimiza el terreno?")
                
            respuesta_estudiante = st.text_input("Escribe tu función o resultado aquí:")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Enviar al tutor"):
                    if respuesta_estudiante:
                        st.info("¡Excelente razonamiento! Vamos a contrastarlo con la solución matemática.")
                        st.session_state.paso_tutor = "ver_solucion"
                        st.rerun()
            with col2:
                if st.button("Ver solución completa"):
                    st.session_state.paso_tutor = "ver_solucion"
                    st.rerun()
                    
        elif st.session_state.paso_tutor == "ver_solucion":
            with st.chat_message("assistant"):
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
                    
                    st.success(f"✅ **Conclusión:** Las dimensiones óptimas son $x = {x_opt:.2f}\text{ m}$ y $y = {y_opt:.2f}\text{ m}$, logrando un área máxima de ${area_max:.2f}\text{ m}^2$.")
                    
            if st.button("Resolver otro problema"):
                st.session_state.paso_tutor = "inicio"
                st.rerun()

else:
    # Modo Solucionador Directo (Corregido para que lea bien potencias tipo x**3 y desglose el paso a paso)
    with st.chat_message("user"):
        st.write("Quiero evaluar una función directa.")
    with st.chat_message("assistant"):
        st.write("Ingresa tu función matemática abajo (recuerda usar `**` para potencias, por ejemplo: `x**3 - 3*x - 2`):")
        
    funcion_str = st.text_input("f(x) =", "x**3 - 3*x - 2")
    
    if funcion_str:
        try:
            f_expr = sp.sympify(funcion_str)
            with st.chat_message("assistant"):
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
                                st.success(f"En $x = \\approx {float(pc.evalf()):.3f}$, la segunda derivada es positiva ({val_num:.2f}). Hay un **MÍNIMO LOCAL** en $({float(pc.evalf()):.3f}, {y_num:.3f})$")
                            elif val_num < 0:
                                st.success(f"En $x = \\approx {float(pc.evalf()):.3f}$, la segunda derivada es negativa ({val_num:.2f}). Hay un **MÁXIMO LOCAL** en $({float(pc.evalf()):.3f}, {y_num:.3f})$")
                            else:
                                st.warning(f"En $x = {pc}$, el criterio de la segunda derivada no es concluyente.")
                        except:
                            st.info(f"Punto crítico exacto en $x = {pc}$, con valor $y = {val_y}$.")
                else:
                    st.warning("No se encontraron puntos críticos reales para esta función.")
        except Exception as e:
            st.error(f"Error al procesar la función. Revisa la sintaxis (usa '*' para multiplicar y '**' para potencias). Detalle: {e}")    # CASO 1: CAJA
    elif st.session_state.tipo_problema_activo == "Maximizar el volumen de una caja (esquinas recortadas)":
        L = 10.0
        A = 6.0
        
        with st.chat_message("user"):
            st.write("Quiero resolver el problema de la caja con una hoja de 10x6.")
            
        if st.session_state.paso_tutor == "pista_planteamiento":
            with st.chat_message("assistant"):
                st.write("¡Perfecto! Tenemos una hoja rectangular de **10 por 6 unidades**. A cada esquina le recortamos un cuadrado de lado $x$.")
                st.write("💡 **Pista 1 (Planteamiento):** Piensa en cuáles serían las nuevas dimensiones de la caja (largo, ancho y altura) en función de $x$ antes de armar la fórmula del volumen $V(x) = \text{largo} \times \text{ancho} \times \text{alto}$.")
                
            if st.button("Ya sé la función / Ver siguiente pista o pregunta"):
                st.session_state.paso_tutor = "pregunta_usuario"
                st.rerun()
                
        elif st.session_state.paso_tutor == "pregunta_usuario":
            with st.chat_message("assistant"):
                st.write("¿Cómo te quedó planteada la función de volumen $V(x)$ o qué valor crees que da el corte $x$?")
                
            respuesta_estudiante = st.text_input("Escribe tu resultado o lo que te dio (ej: x*(10-2*x)*(6-2*x) o x=1.2):")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Enviar respuesta al tutor"):
                    if respuesta_estudiante:
                        st.info(f"Analizando tu respuesta: '{respuesta_estudiante}'... ¡Buen intento! Vamos a ver el desglose completo para que lo compares.")
                        st.session_state.paso_tutor = "ver_solucion"
                        st.rerun()
            with col2:
                if st.button("No sé, muéstrame la respuesta completa"):
                    st.session_state.paso_tutor = "ver_solucion"
                    st.rerun()
                    
        elif st.session_state.paso_tutor == "ver_solucion":
            with st.chat_message("assistant"):
                st.write("🔍 **Solución Paso a Paso:**")
                v_expr = x * (L - 2*x) * (A - 2*x)
                st.latex(f"V(x) = x({L} - 2x)({A} - 2x) = {sp.latex(sp.expand(v_expr))}")
                
                v_prime = sp.diff(v_expr, x)
                st.write("1. Derivamos e igualamos a cero:")
                st.latex(f"V'(x) = {sp.latex(v_prime)} = 0")
                
                criticos = sp.solve(v_prime, x)
                st.write("2. Puntos críticos hallados:")
                for c in criticos:
                    st.latex(f"x = {c.evalf():.3f}")
                    
                # Calcular el óptimo físico
                for c in criticos:
                    c_val = float(c.evalf())
                    if 0 < c_val < min(L, A)/2:
                        volumen_max = float(v_expr.subs(x, c_val))
                        st.success(f"✅ **Conclusión:** El corte ideal es $x = {c_val:.3f}$, obteniendo un volumen máximo de $V = {volumen_max:.3f}$.")
                        
            if st.button("Resolver otro problema"):
                st.session_state.paso_tutor = "inicio"
                st.rerun()

    # CASO 2: CERCA
    elif st.session_state.tipo_problema_activo == "Maximizar el área de un terreno cercado (con un lado libre)":
        perimetro = 100.0
        
        with st.chat_message("user"):
            st.write("Quiero resolver el problema del terreno cercado con 100 metros de cerca.")
            
        if st.session_state.paso_tutor == "pista_planteamiento":
            with st.chat_message("assistant"):
                st.write(f"¡Genial! Tenemos **{perimetro} metros** de cerca y un muro existente que nos ahorra uno de los lados.")
                st.write("💡 **Pista 1:** Si llamamos $x$ a los dos lados perpendiculares al muro, ¿cuánto mide el lado paralelo en función de $x$ y el perímetro total?")
                
            if st.button("Ver siguiente paso / Preguntar"):
                st.session_state.paso_tutor = "pregunta_usuario"
                st.rerun()
                
        elif st.session_state.paso_tutor == "pregunta_usuario":
            with st.chat_message("assistant"):
                st.write("¿Qué función de área $A(x)$ planteaste o qué valor crees que optimiza el terreno?")
                
            respuesta_estudiante = st.text_input("Escribe tu función o resultado aquí:")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Enviar al tutor"):
                    if respuesta_estudiante:
                        st.info("¡Excelente razonamiento! Vamos a contrastarlo con la solución matemática.")
                        st.session_state.paso_tutor = "ver_solucion"
                        st.rerun()
            with col2:
                if st.button("Ver solución completa"):
                    st.session_state.paso_tutor = "ver_solucion"
                    st.rerun()
                    
        elif st.session_state.paso_tutor == "ver_solucion":
            with st.chat_message("assistant"):
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
                    
                    st.success(f"✅ **Conclusión:** Las dimensiones óptimas son $x = {x_opt:.2f}\text{ m}$ y $y = {y_opt:.2f}\text{ m}$, logrando un área máxima de ${area_max:.2f}\text{ m}^2$.")
                    
            if st.button("Resolver otro problema"):
                st.session_state.paso_tutor = "inicio"
                st.rerun()

else:
    # Modo Solucionador Directo por si quiere meter fórmulas rápidas
    with st.chat_message("user"):
        st.write("Quiero evaluar una función directa.")
    with st.chat_message("assistant"):
        st.write("Ingresa tu función matemática abajo:")
        
    funcion_str = st.text_input("f(x) =", "x**3 - 3*x + 2")
    if funcion_str:
        try:
            f_expr = sp.sympify(funcion_str)
            st.latex(f"f(x) = {sp.latex(f_expr)}")
            f_prime = sp.diff(f_expr, x)
            st.latex(f"f'(x) = {sp.latex(f_prime)}")
            criticos = sp.solve(f_prime, x)
            st.write("Puntos críticos:", criticos)
        except Exception as e:
            st.error(f"Error: {e}")
