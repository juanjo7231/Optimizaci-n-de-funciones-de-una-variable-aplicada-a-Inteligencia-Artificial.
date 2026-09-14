import streamlit as st
import sympy as sp
import re

# Configuración de la página
st.set_page_config(
    page_title="Asistente UIS - Optimización de Una Variable",
    page_icon="📐",
    layout="centered"
)

# --- ESTILOS CSS LIMPIOS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #F4F7F5;
        color: #1E293B;
    }
    .main-container {
        background-color: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        overflow: hidden;
        margin-bottom: 20px;
    }
    .uis-header {
        background-color: #007A33;
        color: white;
        padding: 22px 25px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .uis-body {
        padding: 25px;
    }
    .tip-box {
        background-color: #E2F6EC;
        border-left: 5px solid #007A33;
        padding: 16px;
        border-radius: 0 8px 8px 0;
        margin: 15px 0;
        color: #1E293B;
    }
    .stButton > button {
        background-color: #007A33;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 500;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #005E27;
        color: white;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    .stTextInput label, .stTextArea label {
        color: #1E293B !important;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

def limpiar_sintaxis_matematica(expresion: str) -> str:
    # Cambiar ^ por potenciación de python
    exp = expresion.replace("^", "**")
    # Manejar multiplicación implícita antes de un paréntesis: x( o 2( o )( -> x*( o 2*( o )*(
    exp = re.sub(r'([a-zA-Z0-9\)])\(', r'\1*(', exp)
    # Manejar multiplicación implícita después de un paréntesis: )x o )2 -> )*x or )*2
    exp = re.sub(r'\)([a-zA-Z0-9])', r')*\1', exp)
    # Número seguido de letra: 2x -> 2*x
    exp = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', exp)
    # Letra seguida de número (si aplica): x2 -> x**2
    exp = re.sub(r'([a-zA-Z])(\d+)', r'\1**\2', exp)
    return exp

if "historial_problemas" not in st.session_state:
    st.session_state.historial_problemas = []
if "problema_activo" not in st.session_state:
    st.session_state.problema_activo = None
if "mostrar_solucion" not in st.session_state:
    st.session_state.mostrar_solucion = False

# --- BARRA LATERAL ---
with st.sidebar:
    try:
        st.image("logo_uis.webp", use_container_width=True)
    except:
        st.info("💡 Sube tu 'logo_uis.webp' al directorio para ver el escudo.")
        
    st.markdown("### 📐 Casos de Optimización")
    if st.button("➕ Nuevo Problema", use_container_width=True):
        st.session_state.problema_activo = None
        st.session_state.mostrar_solucion = False
        st.rerun()
        
    st.markdown("---")
    st.markdown("<p style='font-size: 12px; color: #64748B; font-weight: 600;'>HISTORIAL RECIENTE</p>", unsafe_allow_html=True)
    
    if st.session_state.historial_problemas:
        for idx, item in enumerate(reversed(st.session_state.historial_problemas)):
            if st.button(f"📌 {item['titulo'][:22]}...", key=f"hist_{idx}", use_container_width=True):
                st.session_state.problema_activo = item
                st.session_state.mostrar_solucion = False
                st.rerun()
    else:
        st.markdown("<p style='font-size: 13px; color: #94A3B8;'>Sin registros previos.</p>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.caption("Universidad Industrial de Santander\nSede Barrancabermeja")

x = sp.Symbol('x', real=True)

# --- ESTRUCTURA MAESTRA UNIFICADA ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown("""
    <div class="uis-header">
        <div>
            <h3 style="margin: 0; color: white; font-size: 20px;">Asistente de Optimización - UIS</h3>
            <span style="font-size: 13px; color: #E2F6EC;">Ingeniería en Inteligencia Artificial</span>
        </div>
        <span style="background-color: #005E27; padding: 5px 12px; border-radius: 15px; font-size: 12px; font-weight: 600; color: white;">Académico</span>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="uis-body">', unsafe_allow_html=True)

if st.session_state.problema_activo:
    prob = st.session_state.problema_activo
    
    st.markdown("#### 📄 Análisis del Problema")
    st.markdown(f"**Enunciado:** {prob['enunciado']}")
    st.markdown("**Función Objetivo:**")
    st.latex(f"f(x) = {prob['funcion_latex']}")
    
    st.markdown("### 🧠 Pistas y Tips de Resolución:")
    st.markdown("""
        <div class="tip-box">
            <p style="margin-bottom: 8px;"><b>💡 Tip 1: Comprende el objetivo.</b><br>Buscamos los valores óptimos (máximos o mínimos) analizando el comportamiento de la función.</p>
            <p style="margin-bottom: 8px;"><b>💡 Tip 2: Deriva con cuidado.</b><br>Calcula la primera derivada f'(x) para conocer la tasa de cambio.</p>
            <p style="margin-bottom: 8px;"><b>💡 Tip 3: Halla los puntos críticos.</b><br>Iguala f'(x) = 0 y despeja x para encontrar los posibles extremos.</p>
            <p style="margin-bottom: 0px;"><b>💡 Tip 4: Criterio de la segunda derivada.</b><br>Sustituye los puntos críticos en f''(x) para clasificarlos.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.mostrar_solucion:
        if st.button("🔍 Ver Solución Paso a Paso Completa"):
            st.session_state.mostrar_solucion = True
            st.rerun()
    else:
        st.markdown("---")
        st.markdown("### 📊 Solución Detallada Paso a Paso:")
        
        for paso in prob['pasos_narrativos']:
            st.markdown(paso['texto'])
            if paso.get('latex'):
                st.latex(paso['latex'])
            if paso.get('subtext'):
                st.markdown(paso['subtext'])
            st.markdown("")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Ocultar solución"):
            st.session_state.mostrar_solucion = False
            st.rerun()
            
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Analizar otro problema"):
        st.session_state.problema_activo = None
        st.session_state.mostrar_solucion = False
        st.rerun()

else:
    st.markdown("""
        <p style="color: #475569; font-size: 15px; margin-bottom: 20px;">Bienvenido al módulo de cálculo y optimización. Ingresa la función objetivo de tu problema expresada en función de <b>x</b> para recibir guía analítica, pistas y el desglose paso a paso.</p>
    """, unsafe_allow_html=True)
    
    enunciado_user = st.text_area("Enunciado o contexto del problema (Opcional):", placeholder="Ej: Determinar las dimensiones para maximizar el área...", height=90)
    funcion_str = st.text_input("Función objetivo $f(x)$:", placeholder="Ej: x*(12 - 2*x)^2")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚡ Iniciar Análisis de Optimización", use_container_width=True):
        if not funcion_str.strip():
            st.warning("⚠️ Por favor ingresa una función matemática válida.")
        elif "=" in funcion_str or "y" in funcion_str.lower():
            st.error("⚠️ Ojo aquí: Este asistente resuelve funciones de **una sola variable (en términos de x)**. Si tienes una ecuación con 'y' o un signo '=', debes despejar la variable y escribir únicamente la expresión final en términos de x.")
        else:
            try:
                funcion_saneada = limpiar_sintaxis_matematica(funcion_str)
                f_expr = sp.sympify(funcion_saneada, locals={'x': x})
                
                if not any(s.name == 'x' for s in f_expr.free_symbols):
                    st.error("⚠️ La expresión ingresada no contiene la variable 'x'. Asegúrate de escribirla correctamente.")
                else:
                    f_prime = sp.diff(f_expr, x)
                    f_double_prime = sp.diff(f_prime, x)
                    puntos_criticos = sp.solve(f_prime, x)
                    
                    pasos_narrativos = []
                    
                    # 1. Planteamiento y Derivada
                    pasos_narrativos.append({
                        "texto": "**Planteamiento y Derivada**\n\nLa función ya se encuentra expresada en términos de una única variable ($x$). Para encontrar el punto crítico, calculamos la primera derivada de $f(x)$ respecto a $x$:",
                        "latex": f"f'(x) = {sp.latex(f_prime)}"
                    })
                    
                    # 2. Punto Crítico
                    pasos_narrativos.append({
                        "texto": "**Punto Crítico**\n\nIgualamos la derivada a cero para hallar el valor de $x$:",
                        "latex": f"{sp.latex(f_prime)} = 0"
                    })
                    
                    if puntos_criticos:
                        # Filtramos solo raíces reales si es posible, o tomamos la primera real
                        pc_real = None
                        for pc in puntos_criticos:
                            if pc.is_real:
                                pc_real = pc
                                break
                        if not pc_real and puntos_criticos:
                            pc_real = puntos_criticos[0]
                            
                        pc = pc_real
                        x_num = float(pc.evalf())
                        val_seg = float(f_double_prime.subs(x, pc).evalf())
                        val_y = float(f_expr.subs(x, pc).evalf())
                        
                        tipo_extremo = "máximo absoluto" if val_seg < 0 else ("mínimo absoluto" if val_seg > 0 else "extremo")
                        signo_str = "< 0" if val_seg < 0 else ("> 0" if val_seg > 0 else "= 0")
                        
                        pasos_narrativos.append({
                            "texto": "",
                            "latex": f"{sp.latex(f_prime)} = 0 \\implies x = {x_num:g}" if pc.is_Integer else f"{sp.latex(f_prime)} = 0 \\implies x = {x_num:.4f}"
                        })
                        
                        pasos_narrativos.append({
                            "texto": f"Esto significa que el punto crítico se encuentra en $x = {x_num:g}$."
                        })
                        
                        # 3. Verificación del Extremo
                        pasos_narrativos.append({
                            "texto": "**Verificación del Máximo / Mínimo**\n\nAplicamos el criterio de la segunda derivada para comprobar de qué tipo de extremo se trata:",
                            "latex": f"f''(x) = {sp.latex(f_double_prime)}",
                            "subtext": f"Dado que la segunda derivada evaluada es $f''(x) {signo_str}$, el criterio confirma que $x = {x_num:g}$ corresponde a un **{tipo_extremo}**."
                        })
                        
                        # 4. Cálculo del Valor Óptimo
                        pasos_narrativos.append({
                            "texto": f"**Cálculo del Valor Óptimo**\n\nSustituimos $x = {x_num:g}$ en la función original:",
                            "latex": f"f({x_num:g}) = {sp.latex(f_expr.subs(x, pc))}",
                            "subtext": f"Resultado final de la evaluación óptima: **{val_y:g}**"
                        })
                    else:
                        pasos_narrativos.append({
                            "texto": "No se encontraron puntos críticos reales para esta función con los parámetros dados."
                        })
                    
                    nuevo_item = {
                        "titulo": enunciado_user[:25] if enunciado_user else f"Función: {funcion_str[:15]}",
                        "enunciado": enunciado_user if enunciado_user else "Análisis de optimización directa.",
                        "funcion_latex": sp.latex(f_expr),
                        "pasos_narrativos": pasos_narrativos
                    }
                    st.session_state.historial_problemas.append(nuevo_item)
                    st.session_state.problema_activo = nuevo_item
                    st.session_state.mostrar_solucion = False
                    st.rerun()
                    
            except Exception as e:
                st.error(f"⚠️ Error al interpretar la función. Revisa la sintaxis. Detalle: {e}")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_app_html=True)
