import streamlit as st
import sympy as sp
import re

# Configuración de la página
st.set_page_config(
    page_title="WappGPT - Asistente de Optimización",
    page_icon="🤖",
    layout="centered"
)

# --- ESTILOS CSS PERSONALIZADOS (Estilo WappGPT / Chat Moderno) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #F0F2F5;
        color: #111B21;
    }
    /* Encabezado del Chat tipo App móvil */
    .chat-header {
        background-color: #7B1FA2;
        color: white;
        padding: 16px 20px;
        border-radius: 16px 16px 0 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .chat-container {
        background-color: #FFFFFF;
        border-radius: 0 0 16px 16px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    /* Burbujas de chat */
    .bubble-user {
        background-color: #E7FFDB;
        padding: 12px 16px;
        border-radius: 12px 12px 0 12px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        color: #111B21;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .bubble-assistant {
        background-color: #F3E5F5;
        padding: 14px 18px;
        border-radius: 12px 12px 12px 0;
        margin: 10px 0;
        max-width: 90%;
        color: #111B21;
        border-left: 4px solid #7B1FA2;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .stButton > button {
        background-color: #7B1FA2;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 500;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #4A148C;
        color: white;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #111B21 !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Función para corregir sintaxis matemática de forma segura
def limpiar_sintaxis_matematica(expresion: str) -> str:
    exp = expresion.replace("^", "**")
    exp = re.sub(r'([a-zA-Z])(\d+)', r'\1**\2', exp)
    exp = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', exp)
    return exp

# Inicializar estados de sesión
if "historial_problemas" not in st.session_state:
    st.session_state.historial_problemas = []
if "problema_activo" not in st.session_state:
    st.session_state.problema_activo = None
if "mostrar_solucion" not in st.session_state:
    st.session_state.mostrar_solucion = False

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("### 💬 Conversaciones WappGPT")
    if st.button("➕ Nuevo Problema", use_container_width=True):
        st.session_state.problema_activo = None
        st.session_state.mostrar_solucion = False
        st.rerun()
        
    st.markdown("---")
    st.markdown("<p style='font-size: 12px; color: #64748B; font-weight: 600;'>HISTORIAL</p>", unsafe_allow_html=True)
    
    if st.session_state.historial_problemas:
        for idx, item in enumerate(reversed(st.session_state.historial_problemas)):
            if st.button(f"📌 {item['titulo'][:22]}...", key=f"hist_{idx}", use_container_width=True):
                st.session_state.problema_activo = item
                st.session_state.mostrar_solucion = False
                st.rerun()
    else:
        st.markdown("<p style='font-size: 13px; color: #94A3B8;'>Sin chats recientes.</p>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.caption("UIS | Ing. Inteligencia Artificial")

x = sp.Symbol('x', real=True)

# --- CABECERA ESTILO APP WAPPGPT ---
st.markdown("""
    <div class="chat-header">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 24px;">🤖</span>
            <div>
                <h3 style="margin: 0; color: white; font-size: 18px;">WappGPT - Optimización</h3>
                <span style="font-size: 12px; color: #E1BEE7;">● Online</span>
            </div>
        </div>
        <span style="font-size: 18px; cursor: pointer;">⚙️</span>
    </div>
""", unsafe_allow_html=True)

# --- CUERPO PRINCIPAL DEL CHAT ---
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if st.session_state.problema_activo:
        prob = st.session_state.problema_activo
        
        # Mensaje del usuario (burbuja verde)
        st.markdown(f"""
            <div class="bubble-user">
                <b>Función ingresada:</b> {prob['funcion_original']}<br>
                <span style="font-size: 12px; color: #667781;">Enunciado: {prob['enunciado']}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Respuesta de la IA con los Tips (burbuja morada)
        st.markdown("""
            <div class="bubble-assistant">
                <p style="font-weight: 700; color: #4A148C; margin-bottom: 8px;">🧠 Pistas y Tips de Resolución:</p>
                <p style="margin-bottom: 8px;"><b>💡 Tip 1: ¿Qué representa la función?</b><br>Estamos buscando los puntos más altos (máximos) o más bajos (mínimos) de esta curva analizando su comportamiento.</p>
                <p style="margin-bottom: 8px;"><b>💡 Tip 2: La derivada como pendiente.</b><br>Derivar te da la fórmula de la pendiente ($f'(x)$). Baja los exponentes a multiplicar y réstale uno a cada término.</p>
                <p style="margin-bottom: 8px;"><b>💡 Tip 3: Puntos críticos.</b><br>Iguala la primera derivada a cero ($f'(x) = 0$) para hallar los puntos donde la pendiente es totalmente plana.</p>
                <p style="margin-bottom: 0px;"><b>💡 Tip 4: Criterio de la segunda derivada.</b><br>Evalúa los puntos críticos en $f''(x)$. Si da negativo es una cima (máximo); si da positivo es un valle (mínimo).</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Botón para ver la solución completa paso a paso
        if not st.session_state.mostrar_solucion:
            if st.button("🔍 Ver Solución Paso a Paso Completa"):
                st.session_state.mostrar_solucion = True
                st.rerun()
        else:
            # Despliegue de la solución paso a paso dentro del chat
            st.markdown(f"""
                <div class="bubble-assistant" style="border-left: 4px solid #007A33; background-color: #E8F5E9;">
                    <p style="font-weight: 700; color: #2E7D32; font-size: 16px; margin-bottom: 10px;">📊 Solución Paso a Paso Completa:</p>
                    {prob['html_solucion']}
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Ocultar solución"):
                st.session_state.mostrar_solucion = False
                st.rerun()
                
        if st.button("⬅️ Plantear otro problema"):
            st.session_state.problema_activo = None
            st.session_state.mostrar_solucion = False
            st.rerun()

    else:
        # Pantalla de inicio del chat
        st.markdown("""
            <div class="bubble-assistant">
                <p style="margin: 0; font-size: 15px;">👋 ¡Hola! Soy tu asistente de WappGPT. Ingresa tu función matemática abajo para comenzar el análisis de optimización paso a paso.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        enunciado_user = st.text_area("Descripción del problema (Opcional):", placeholder="Ej: Optimizar las dimensiones de...", height=80)
        funcion_str = st.text_input("Type your message here...", placeholder="Ej: 2x3 - 15x2 + 36*x")
        
        if st.button("🚀 Enviar y Analizar", use_container_width=True):
            if not funcion_str.strip():
                st.warning("⚠️ Por favor ingresa una función matemática válida.")
            else:
                try:
                    funcion_saneada = limpiar_sintaxis_matematica(funcion_str)
                    f_expr = sp.sympify(funcion_saneada)
                    f_prime = sp.diff(f_expr, x)
                    f_double_prime = sp.diff(f_prime, x)
                    puntos_criticos = sp.solve(f_prime, x)
                    
                    # Generar HTML del paso a paso detallado
                    html_paso_a_paso = f"""
                    <div style="margin-bottom: 12px;">
                        <b>Paso 1: Primera derivada y puntos críticos</b><br>
                        Se calcula la derivada de la función:<br>
                        <code style="background: white; padding: 2px 6px; border-radius: 4px;">f'(x) = {sp.latex(f_prime)}</code><br>
                        Igualando a cero se obtienen los puntos críticos.
                    </div>
                    """
                    
                    detalle_evaluacion = ""
                    if puntos_criticos:
                        for pc in puntos_criticos:
                            try:
                                val_seg = float(f_double_prime.subs(x, pc).evalf())
                                val_y = float(f_expr.subs(x, pc).evalf())
                                x_num = float(pc.evalf())
                                tipo_extremo = "máximo local" if val_seg < 0 else "mínimo local"
                                signo_str = "< 0" if val_seg < 0 else "> 0"
                                
                                detalle_evaluacion += f"""
                                <div style="background: white; padding: 10px; border-radius: 8px; margin-top: 8px; border: 1px solid #C8E6C9;">
                                    <b>• Para x = {x_num:.2f}:</b><br>
                                    Evaluamos en $f''({x_num:.2f}) = {val_seg:.2f}$ ({signo_str}).<br>
                                    Resultado: Hay un <b>{tipo_extremo}</b>.<br>
                                    Coordenada del extremo: $({x_num:.2f}, {val_y:.2f})$
                                </div>
                                """
                            except:
                                detalle_evaluacion += f"<div>Punto crítico en x = {pc}</div>"
                    else:
                        detalle_evaluacion = "<div>No se encontraron puntos críticos reales.</div>"
                    
                    html_paso_a_paso += f"""
                    <div style="margin-bottom: 12px;">
                        <b>Paso 2: Segunda derivada</b><br>
                        <code style="background: white; padding: 2px 6px; border-radius: 4px;">f''(x) = {sp.latex(f_double_prime)}</code>
                    </div>
                    <div>
                        <b>Paso 3: Evaluación y clasificación</b>
                        {detalle_evaluacion}
                    </div>
                    """
                    
                    nuevo_item = {
                        "titulo": enunciado_user[:25] if enunciado_user else f"Función: {funcion_str[:15]}",
                        "enunciado": enunciado_user if enunciado_user else "Análisis directo de función.",
                        "funcion_original": funcion_str,
                        "html_solucion": html_paso_a_paso
                    }
                    st.session_state.historial_problemas.append(nuevo_item)
                    st.session_state.problema_activo = nuevo_item
                    st.session_state.mostrar_solucion = False
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"⚠️ Error al interpretar la función. Detalle: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
