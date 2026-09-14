import streamlit as st
import sympy as sp
import re
import os

# Configuración de la página
st.set_page_config(
    page_title="Asistente UIS - IA de Optimización",
    page_icon="🧠",
    layout="centered"
)

# --- ESTILOS CSS CORREGIDOS (INPUT GRIS Y TEXTO BLANCO) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAFC;
        color: #1E293B !important;
    }
    .stChatMessage {
        color: #1E293B !important;
    }
    .stChatMessage p, .stChatMessage span, .stChatMessage div {
        color: #1E293B !important;
    }
    
    /* Configuración para que el cuadro de texto sea gris y lo que escribas sea blanco */
    .stChatInput textarea, .stChatInput input {
        color: #FFFFFF !important;
        background-color: #1E293B !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    div[data-baseweb="input"], div[data-baseweb="base-input"], div[data-baseweb="textarea"] {
        background-color: #1E293B !important;
        border-radius: 8px !important;
    }
    /* Color del texto de placeholder (guía) dentro del input */
    .stChatInput textarea::placeholder {
        color: #94A3B8 !important;
        opacity: 1 !important;
    }

    .uis-header {
        background-color: #007A33;
        color: white;
        padding: 16px 20px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }
    .tip-box-chat {
        background-color: #E2F6EC;
        border-left: 4px solid #007A33;
        padding: 14px 16px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
        color: #1E293B !important;
        font-size: 14px;
        line-height: 1.5;
    }
    .stButton > button {
        background-color: #007A33;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 500;
        padding: 0.4rem 0.8rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #005E27;
        color: white;
    }
    /* Estilo para redondear la imagen nativa del logo circular */
    .logo-circular img {
        border-radius: 50%;
        border: 2px solid #007A33;
        object-fit: cover;
        width: 48px;
        height: 48px;
    }
    </style>
""", unsafe_allow_html=True)

def limpiar_sintaxis_matematica(expresion: str) -> str:
    exp = expresion.strip()
    if "=" in exp:
        parts = exp.split("=")
        exp = parts[-1]
    
    exp = re.sub(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*\([xX]\)\s*=', '', exp)
    
    exp = exp.replace("^", "**")
    exp = re.sub(r'([a-zA-Z0-9\)])\(', r'\1*(', exp)
    exp = re.sub(r'\)([a-zA-Z0-9])', r')*\1', exp)
    exp = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', exp)
    exp = re.sub(r'([a-zA-Z])(\d+)', r'\1**\2', exp)
    return exp.strip()

if "historial_problemas" not in st.session_state:
    st.session_state.historial_problemas = []
if "problema_activo" not in st.session_state:
    st.session_state.problema_activo = None
if "mostrar_solucion" not in st.session_state:
    st.session_state.mostrar_solucion = False

# --- BARRA LATERAL (Usa logo_uis.webp) ---
with st.sidebar:
    if os.path.exists("logo_uis.webp"):
        st.image("logo_uis.webp", use_container_width=True)
    else:
        st.info("💡 Sube tu 'logo_uis.webp' al directorio.")
        
    st.markdown("### 🤖 Sesiones de Chat")
    if st.button("➕ Nueva Conversación", use_container_width=True):
        st.session_state.problema_activo = None
        st.session_state.mostrar_solucion = False
        st.rerun()
        
    st.markdown("---")
    st.markdown("<p style='font-size: 12px; color: #64748B; font-weight: 600;'>HISTORIAL</p>", unsafe_allow_html=True)
    
    if st.session_state.historial_problemas:
        for idx, item in enumerate(reversed(st.session_state.historial_problemas)):
            if st.button(f"💬 {item['titulo'][:22]}...", key=f"hist_{idx}", use_container_width=True):
                st.session_state.problema_activo = item
                st.session_state.mostrar_solucion = False
                st.rerun()
    else:
        st.markdown("<p style='font-size: 13px; color: #94A3B8;'>Sin chats previos.</p>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.caption("Universidad Industrial de Santander\nSede Barrancabermeja")

x = sp.Symbol('x', real=True)

# --- ENCABEZADO CON LOGO CIRCULAR (logo-universidad-industrial-de-santander.webp) ---
col_head1, col_head2 = st.columns([0.12, 0.88])
with col_head1:
    logo_circular = "logo-universidad-industrial-de-santander.webp"
    if os.path.exists(logo_circular):
        st.markdown('<div class="logo-circular">', unsafe_allow_html=True)
        st.image(logo_circular)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Falta 'logo-universidad-industrial-de-santander.webp'")

with col_head2:
    st.markdown("""
        <div class="uis-header" style="margin-bottom: 0px;">
            <div>
                <h3 style="margin: 0; color: white; font-size: 18px;">🧠 Asistente IA de Optimización</h3>
                <span style="font-size: 12px; color: #E2F6EC;">Ingeniería en Inteligencia Artificial • UIS</span>
            </div>
            <span style="background-color: #005E27; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; color: white;">En línea</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- INTERFAZ PRINCIPAL DE CONVERSACIÓN ---
if st.session_state.problema_activo:
    prob = st.session_state.problema_activo
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(f"**Enunciado / Contexto:** {prob['enunciado']}")
        st.markdown(f"**Función a optimizar:**")
        st.latex(f"f(x) = {prob['funcion_latex']}")
        
    with st.chat_message("assistant", avatar="🧠"):
        st.markdown("¡Hola de nuevo! Analicemos este ejercicio paso a paso. Aquí tienes algunas pistas conceptuales para guiar tu razonamiento:")
        
        st.markdown(f"""
            <div class="tip-box-chat">
                <p style="margin-bottom: 8px;"><b>💡 Pista 1: Visualiza la forma geométrica.</b><br>Piensa en qué tipo de curva representa tu función y hacia dónde abre. Eso te orienta sobre el tipo de extremo que buscas.</p>
                <p style="margin-bottom: 8px;"><b>💡 Pista 2: El papel de la pendiente.</b><br>Recuerda qué representa gráficamente la primera derivada en la cumbre o el valle de una función.</p>
                <p style="margin-bottom: 8px;"><b>💡 Pista 3: Planteamiento del punto crítico.</b><br>Deriva la función e iguala a cero para despejar los valores candidatos de <i>x</i>.</p>
                <p style="margin-bottom: 0px;"><b>💡 Pista 4: La prueba de la curvatura.</b><br>Usa la segunda derivada para confirmar si el punto hallado es un máximo o un mínimo.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.mostrar_solucion:
            if st.button("🔍 Revelar Solución Paso a Paso"):
                st.session_state.mostrar_solucion = True
                st.rerun()
        else:
            st.markdown("---")
            st.markdown("### 📊 Desglose de la Solución:")
            for paso in prob['pasos_narrativos']:
                st.markdown(paso['texto'])
                if paso.get('latex'):
                    st.latex(paso['latex'])
                if paso.get('subtext'):
                    st.markdown(paso['subtext'])
                st.markdown("")

            if st.button("Ocultar solución"):
                st.session_state.mostrar_solucion = False
                st.rerun()
                
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Iniciar otro análisis"):
            st.session_state.problema_activo = None
            st.session_state.mostrar_solucion = False
            st.rerun()

else:
    with st.chat_message("assistant", avatar="🧠"):
        st.markdown("¡Hola! Soy tu asistente de cálculo y optimización de la UIS. ¿Qué función matemática o problema de optimización de una sola variable quieres que analicemos hoy?")
    
    user_input = st.chat_input("Escribe tu función f(x) o el contexto del problema...")
    
    if user_input:
        if "x" not in user_input.lower():
            st.warning("⚠️ Recuerda ingresar la expresión en términos de la variable **x**.")
        else:
            funcion_str = user_input
            enunciado_user = "Análisis directo desde el chat."
            
            try:
                funcion_saneada = limpiar_sintaxis_matematica(funcion_str)
                f_expr = sp.sympify(funcion_saneada, locals={'x': x})
                
                if not any(s.name == 'x' for s in f_expr.free_symbols):
                    st.error("⚠️ La expresión no contiene la variable 'x'. Inténtalo de nuevo.")
                else:
                    f_prime = sp.diff(f_expr, x)
                    f_double_prime = sp.diff(f_prime, x)
                    puntos_criticos = sp.solve(f_prime, x)
                    
                    pasos_narrativos = []
                    pasos_narrativos.append({
                        "texto": "**Planteamiento y Derivada**\n\nLa función está expresada en términos de una única variable ($x$). Calculamos su primera derivada:",
                        "latex": f"f'(x) = {sp.latex(f_prime)}"
                    })
                    
                    pasos_narrativos.append({
                        "texto": "**Punto Crítico**\n\nIgualamos la derivada a cero:",
                        "latex": f"{sp.latex(f_prime)} = 0"
                    })
                    
                    if puntos_criticos:
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
                            "texto": f"El punto crítico se localiza en $x = {x_num:g}$."
                        })
                        
                        pasos_narrativos.append({
                            "texto": "**Verificación del Extremo**\n\nAplicamos el criterio de la segunda derivada:",
                            "latex": f"f''(x) = {sp.latex(f_double_prime)}",
                            "subtext": f"Como $f''(x) {signo_str}$, confirmamos que se trata de un **{tipo_extremo}**."
                        })
                        
                        pasos_narrativos.append({
                            "texto": f"**Valor Óptimo**\n\nEvaluamos en la función original:",
                            "latex": f"f({x_num:g}) = {sp.latex(f_expr.subs(x, pc))}",
                            "subtext": f"Resultado óptimo: **{val_y:g}**"
                        })
                    else:
                        pasos_narrativos.append({
                            "texto": "No se hallaron puntos críticos reales con los parámetros ingresados."
                        })
                    
                    nuevo_item = {
                        "titulo": f"Función: {funcion_str[:15]}",
                        "enunciado": enunciado_user,
                        "funcion_latex": sp.latex(f_expr),
                        "pasos_narrativos": pasos_narrativos
                    }
                    st.session_state.historial_problemas.append(nuevo_item)
                    st.session_state.problema_activo = nuevo_item
                    st.session_state.mostrar_solucion = False
                    st.rerun()
                    
            except Exception as e:
                st.error(f"⚠️ No pude interpretar la sintaxis matemática. Asegúrate de ingresar una expresión válida en términos de x (ej: x*(12 - 2*x)^2). Detalle: {e}")
