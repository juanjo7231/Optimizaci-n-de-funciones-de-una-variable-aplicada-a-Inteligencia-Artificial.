import streamlit as st
import sympy as sp
import re

# Configuración de la página
st.set_page_config(
    page_title="Asistente IA - Optimización UIS",
    page_icon="🤖",
    layout="wide"
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAF9;
        color: #1E293B;
    }
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
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
    h1, h2, h3 {
        color: #004D20 !important;
    }
    .chat-welcome-card {
        background-color: #FFFFFF;
        padding: 2.5rem;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
        text-align: center;
        margin-bottom: 2rem;
    }
    .tip-card {
        background-color: #E2F6EC;
        border-left: 5px solid #007A33;
        padding: 1.2rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Función segura para limpiar la sintaxis matemática sin dañar operadores
def limpiar_sintaxis_matematica(expresion: str) -> str:
    exp = expresion.replace("^", "**")
    # Convertir x3 a x**3 de forma segura
    exp = re.sub(r'([a-zA-Z])(\d+)', r'\1**\2', exp)
    # Convertir 2x a 2*x
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
    try:
        st.image("logo_uis.webp", use_container_width=True)
    except:
        st.info("💡 Sube tu 'logo_uis.webp' al directorio para ver el escudo.")
        
    st.markdown("### 💬 Conversaciones")
    
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
        st.markdown("<p style='font-size: 13px; color: #94A38B;'>No hay problemas analizados aún.</p>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("##### 🏛️ Universidad Industrial de Santander")
    st.caption("Sede Barrancabermeja | Ing. Inteligencia Artificial")

x = sp.Symbol('x', real=True)

# --- CUERPO PRINCIPAL ---
col_head1, col_head2 = st.columns([6, 1])
with col_head1:
    st.markdown("### 🤖 Asistente IA - Optimización de Una Variable")
with col_head2:
    st.markdown("<div style='text-align: right; padding-top: 5px;'><span style='background-color: #E2F6EC; color: #007A33; padding: 6px 12px; border-radius: 20px; font-weight: 600; font-size: 13px;'>🟢 Online UIS</span></div>", unsafe_allow_html=True)

st.markdown("---")

if st.session_state.problema_activo:
    prob = st.session_state.problema_activo
    st.markdown(f"#### 📄 Análisis: {prob['titulo']}")
    st.info(f"**Enunciado:** {prob['enunciado']}")
    
    st.markdown("---")
    st.markdown("### 🧠 Pistas y Tips de Resolución (Paso 1):")
    st.markdown("""
        <div class="tip-card">
            <p><b>💡 Tip 1: Entiende qué buscas optimizar.</b><br>
            La función objetivo ya está dada. Recuerda que para hallar máximos o mínimos locales, el primer paso fundamental es encontrar dónde la pendiente de la curva se vuelve cero.</p>
            
            <p><b>💡 Tip 2: Aplica la regla de la potencia para derivar.</b><br>
            Piensa en cómo derivar cada término por separado: baja el exponente a multiplicar y réstale 1. Por ejemplo, la derivada de un término cúbico te quedará con grado 2.</p>
            
            <p><b>💡 Tip 3: Iguala la primera derivada a cero.</b><br>
            Los puntos críticos salen de resolver $f'(x) = 0$. Intenta factorizar o simplificar la ecuación cuadrática resultante antes de buscar las raíces.</p>
            
            <p><b>💡 Tip 4: Usa el criterio de la segunda derivada.</b><br>
            Una vez hallados los puntos $x$, evalúalos en $f''(x)$. Si el resultado es negativo, es una cima (máximo); si es positivo, es un valle (mínimo).</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Botón para revelar el paso a paso completo
    if not st.session_state.mostrar_solucion:
        if st.button("🔍 Ver Solución Paso a Paso Completa"):
            st.session_state.mostrar_solucion = True
            st.rerun()
    else:
        st.markdown("---")
        st.markdown("### 📊 Solución Paso a Paso Completa:")
        
        st.write("**1. Función Objetivo:**")
        st.latex(f"f(x) = {prob['f_latex']}")
        
        st.write("**2. Primera Derivada ($f'(x)$):**")
        st.latex(f"f'(x) = {prob['f_prime_latex']}")
        
        st.write("**3. Segunda Derivada ($f''(x)$):**")
        st.latex(f"f''(x) = {prob['f_double_latex']}")
        
        st.write("**4. Puntos Críticos y Criterio de la Segunda Derivada:**")
        st.markdown(prob['resultado_texto'], unsafe_allow_html=True)
        
        if st.button("Ocultar solución"):
            st.session_state.mostrar_solucion = False
            st.rerun()
            
    if st.button("⬅️ Volver al inicio"):
        st.session_state.problema_activo = None
        st.session_state.mostrar_solucion = False
        st.rerun()

else:
    st.markdown("""
        <div class="chat-welcome-card">
            <h2>¿Qué problema vamos a resolver hoy?</h2>
            <p style="color: #64748B; font-size: 15px;">Ingresa tu función (ej: <code>2x3 - 15x2 + 36x</code>). Primero te daremos tips de razonamiento y pistas para que pienses el ejercicio, y luego podrás revelar la solución paso a paso.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("#### ✍️ Planta tu caso de estudio:")
    enunciado_user = st.text_area("Enunciado o descripción del problema:", placeholder="Ej: Maximizar una caja sin tapa...", height=100)
    funcion_str = st.text_input("Función objetivo $f(x)$:", placeholder="Ej: 2x3 - 15x2 + 36*x")
    
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        analizar = st.button("⚡ Analizar", use_container_width=True)
        
    if analizar:
        if not funcion_str.strip():
            st.warning("⚠️ Por favor ingresa una función matemática válida.")
        else:
            try:
                funcion_saneada = limpiar_sintaxis_matematica(funcion_str)
                f_expr = sp.sympify(funcion_saneada)
                f_prime = sp.diff(f_expr, x)
                f_double_prime = sp.diff(f_prime, x)
                puntos_criticos = sp.solve(f_prime, x)
                
                res_texto_guardado = ""
                if puntos_criticos:
                    for pc in puntos_criticos:
                        try:
                            val_seg = float(f_double_prime.subs(x, pc).evalf())
                            val_y = float(f_expr.subs(x, pc).evalf())
                            x_num = float(pc.evalf())
                            
                            if val_seg < 0:
                                msg = f"• Para $x = {x_num:.4f}$: evaluamos en $f''(x)$ y obtenemos ${val_seg:.2f} < 0$. Por lo tanto, hay un **MÁXIMO LOCAL**, con un valor óptimo de $f(x) = {val_y:.4f}$.<br>"
                                res_texto_guardado += msg
                            elif val_seg > 0:
                                msg = f"• Para $x = {x_num:.4f}$: evaluamos en $f''(x)$ y obtenemos ${val_seg:.2f} > 0$. Por lo tanto, hay un **MÍNIMO LOCAL**, con un valor óptimo de $f(x) = {val_y:.4f}$.<br>"
                                res_texto_guardado += msg
                            else:
                                msg = f"• En $x = {pc}$, la segunda derivada es cero; no es concluyente.<br>"
                                res_texto_guardado += msg
                        except:
                            msg = f"• Punto crítico en $x = {pc}$.<br>"
                            res_texto_guardado += msg
                else:
                    res_texto_guardado = "No se encontraron puntos críticos reales."
                    
                # Guardar en sesión
                nuevo_item = {
                    "titulo": enunciado_user[:30] if enunciado_user else f"Función: {funcion_str[:20]}",
                    "enunciado": enunciado_user if enunciado_user else "Sin enunciado redactado.",
                    "f_latex": sp.latex(f_expr),
                    "f_prime_latex": sp.latex(f_prime),
                    "f_double_latex": sp.latex(f_double_prime),
                    "resultado_texto": res_texto_guardado
                }
                st.session_state.problema_activo = nuevo_item
                st.session_state.mostrar_solucion = False
                st.rerun()
                
            except Exception as e:
                st.error(f"⚠️ Error al interpretar la función. Revisa la sintaxis. Detalle: {e}")
