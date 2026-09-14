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
    exp = expresion.replace("^", "**")
    exp = re.sub(r'([a-zA-Z])(\d+)', r'\1**\2', exp)
    exp = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', exp)
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
        
        # Paso 1
        with st.container():
            st.markdown("**Paso 1: Cálculo de la primera derivada**")
            st.markdown("Derivamos la función objetivo con respecto a $x$:")
            st.latex(f"f'(x) = {prob['f_prime_latex']}")
            st.markdown("Igualamos a cero ($f'(x) = 0$) para hallar los puntos críticos.")

        # Paso 2
        with st.container():
            st.markdown("---")
            st.markdown("**Paso 2: Cálculo de la segunda derivada**")
            st.markdown("Obtenemos $f''(x)$ para aplicar el criterio de concavidad:")
            st.latex(f"f''(x) = {prob['f_double_prime_latex']}")

        # Paso 3
        with st.container():
            st.markdown("---")
            st.markdown("**Paso 3: Evaluación y clasificación de extremos**")
            for eval_item in prob['evaluaciones']:
                st.info(eval_item)

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
    funcion_str = st.text_input("Función objetivo $f(x)$:", placeholder="Ej: x*(40 - 2*x)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚡ Iniciar Análisis de Optimización", use_container_width=True):
        if not funcion_str.strip():
            st.warning("⚠️ Por favor ingresa una función matemática válida.")
        elif "=" in funcion_str or "y" in funcion_str.lower():
            st.error("⚠️ Ojo aquí: Este asistente resuelve funciones de **una sola variable (en términos de x)**. Si tienes una ecuación con 'y' o un signo '=', debes despejar la variable y escribir únicamente la expresión final en términos de x (por ejemplo, en lugar de 2x + y = 40, ingresa la función ya sustituida como x*(40-2*x)).")
        else:
            try:
                funcion_saneada = limpiar_sintaxis_matematica(funcion_str)
                f_expr = sp.sympify(funcion_saneada)
                f_prime = sp.diff(f_expr, x)
                f_double_prime = sp.diff(f_prime, x)
                puntos_criticos = sp.solve(f_prime, x)
                
                lista_evaluaciones = []
                if puntos_criticos:
                    for pc in puntos_criticos:
                        try:
                            val_seg = float(f_double_prime.subs(x, pc).evalf())
                            val_y = float(f_expr.subs(x, pc).evalf())
                            x_num = float(pc.evalf())
                            tipo_extremo = "máximo local" if val_seg < 0 else "mínimo local"
                            signo_str = "< 0" if val_seg < 0 else "> 0"
                            
                            texto_eval = f"**• Para $x = {x_num:.4f}$:**\n\n" \
                                         f"- Evaluamos en la segunda derivada: $f''({x_num:.4f}) = {val_seg:.4f}$ ({signo_str}).\n" \
                                         f"- Conclusión: Existe un **{tipo_extremo}**.\n" \
                                         f"- Valor óptimo en la función: $f({x_num:.4f}) = {val_y:.4f}$"
                            lista_evaluaciones.append(texto_eval)
                        except Exception as ex:
                            lista_evaluaciones.append(f"Punto crítico encontrado en $x = {pc}$, pero no se pudo evaluar numéricamente ({ex}).")
                else:
                    lista_evaluaciones.append("No se encontraron puntos críticos reales para esta función.")
                
                nuevo_item = {
                    "titulo": enunciado_user[:25] if enunciado_user else f"Función: {funcion_str[:15]}",
                    "enunciado": enunciado_user if enunciado_user else "Análisis de optimización directa.",
                    "funcion_latex": sp.latex(f_expr),
                    "f_prime_latex": sp.latex(f_prime),
                    "f_double_prime_latex": sp.latex(f_double_prime),
                    "evaluaciones": lista_evaluaciones
                }
                st.session_state.historial_problemas.append(nuevo_item)
                st.session_state.problema_activo = nuevo_item
                st.session_state.mostrar_solucion = False
                st.rerun()
                
            except Exception as e:
                st.error(f"⚠️ Error al interpretar la función. Revisa la sintaxis. Detalle: {e}")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
