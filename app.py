import streamlit as st
import sympy as sp

# Configuración de la página
st.set_page_config(
    page_title="Resolutor de Optimización - UIS",
    page_icon="🤖",
    layout="wide"
)

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
    
    st.markdown("#### ℹ️ Acerca de la herramienta")
    st.write("Esta app está diseñada para ayudarte a resolver y comprobar problemas de optimización de una sola variable de forma rápida y analítica.")
    
    st.markdown("---")
    st.caption("Desarrollado como soporte de cálculo aplicado.")

# Definir la variable simbólica principal
x = sp.Symbol('x', real=True)

# --- CUERPO PRINCIPAL ---
st.title("🤖 Asistente Analítico de Optimización")
st.markdown("Ingresa directamente la función matemática de tu problema (o selecciona un modelo base) para obtener el análisis completo de máximos y mínimos.")

# Pestañas para organizar la entrada
tab1, tab2 = st.tabs(["✍️ Ingresar Función Propia", "📚 Cargar Problemas Clásicos"])

with tab1:
    st.markdown("### Introduce tu función objetivo $f(x)$")
    st.write("Escribe la expresión algebraica que modela el problema (ejemplo: área, volumen, costo, distancia). Usa `**` para potencias y `*` para multiplicación.")
    
    col_f1, col_f2 = st.columns([3, 1])
    with col_f1:
        funcion_str = st.text_input("f(x) =", "x*(10 - 2*x)*(6 - 2*x)")
    with col_f2:
        st.markdown("<br>", unsafe_allow_html=True)
        resolver_custom = st.button("Resolver Problema", type="primary")
        
    if resolver_custom and funcion_str:
        try:
            f_expr = sp.sympify(funcion_str)
            st.markdown("---")
            st.markdown("### 🔍 Memoria de Cálculo y Resultados:")
            
            st.write("**1. Función Objetivo planteada:**")
            st.latex(f"f(x) = {sp.latex(f_expr)}")
            
            # Primera derivada
            f_prime = sp.diff(f_expr, x)
            st.write("**2. Primera Derivada $f'(x)$ (para hallar puntos críticos):**")
            st.latex(f"f'(x) = {sp.latex(f_prime)}")
            
            # Puntos críticos
            puntos_criticos = sp.solve(f_prime, x)
            st.write("**3. Puntos Críticos ($f'(x) = 0$):**")
            
            if puntos_criticos:
                for pc in puntos_criticos:
                    st.latex(f"x = {sp.latex(pc)}")
                    
                # Segunda derivada y clasificación
                f_double_prime = sp.diff(f_prime, x)
                st.write("**4. Criterio de la Segunda Derivada ($f''(x)$):**")
                st.latex(f"f''(x) = {sp.latex(f_double_prime)}")
                
                for pc in puntos_criticos:
                    val_segunda = f_double_prime.subs(x, pc)
                    val_y = f_expr.subs(x, pc)
                    try:
                        val_num = float(val_segunda.evalf())
                        y_num = float(val_y.evalf())
                        
                        if val_num < 0:
                            st.success(f"✅ Encontrado un **MÁXIMO LOCAL** en $x \\approx {float(pc.evalf()):.4f}$, con un valor óptimo de $f(x) = {y_num:.4f}$ (la segunda derivada es negativa: {val_num:.2f}).")
                        elif val_num > 0:
                            st.success(f"✅ Encontrado un **MÍNIMO LOCAL** en $x \\approx {float(pc.evalf()):.4f}$, con un valor óptimo de $f(x) = {y_num:.4f}$ (la segunda derivada es positiva: {val_num:.2f}).")
                        else:
                            st.warning(f"⚠️ En $x = {pc}$, la segunda derivada es cero; el criterio no es concluyente.")
                    except:
                        st.info(f"Punto crítico exacto en $x = {pc}$, valor evaluado: $f(x) = {val_y}$.")
            else:
                st.warning("No se encontraron puntos críticos reales para esta función.")
        except Exception as e:
            st.error(f"⚠️ Error al procesar la función. Revisa la sintaxis. Detalle técnico: {e}")

with tab2:
    st.markdown("### Selecciona un problema tipo para cargar su función automática:")
    caso_select = st.selectbox(
        "Problema:",
        (
            "Caja con esquinas recortadas (Hoja 10x6)",
            "Terreno rectangular con un lado libre (Cerca de 100m)"
        )
    )
    
    if st.button("Cargar y Resolver Modelo"):
        st.markdown("---")
        st.markdown("### 🔍 Análisis del Problema Seleccionado:")
        
        if "Caja" in caso_select:
            L, A_hoja = 10.0, 6.0
            st.write(f"Se modela una hoja de {L} x {A_hoja} recortando esquinas de tamaño $x$.")
            f_expr = x * (L - 2*x) * (A_hoja - 2*x)
        else:
            perimetro = 100.0
            st.write(f"Se modela un terreno con {perimetro}m de cerca aprovechando un muro.")
            f_expr = x * (perimetro - 2*x)
            
        st.latex(f"f(x) = {sp.latex(sp.expand(f_expr))}")
        
        f_prime = sp.diff(f_expr, x)
        st.write("**Derivada igualada a cero:**")
        st.latex(f"f'(x) = {sp.latex(f_prime)} = 0")
        
        criticos = sp.solve(f_prime, x)
        f_double_prime = sp.diff(f_prime, x)
        
        for c in criticos:
            c_val = float(c.evalf())
            val_y = float(f_expr.subs(x, c_val))
            seg_val = float(f_double_prime.subs(x, c_val))
            
            st.latex(f"x = {c_val:.4f}")
            if seg_val < 0:
                st.success(f"🎯 **Resultado Óptimo (Máximo):** Para $x = {c_val:.4f}$, se obtiene el valor máximo buscado de **{val_y:.4f}**.")
            else:
                st.info(f"🎯 **Resultado Óptimo (Mínimo):** Para $x = {c_val:.4f}$, se obtiene el valor mínimo de **{val_y:.4f}**.")
