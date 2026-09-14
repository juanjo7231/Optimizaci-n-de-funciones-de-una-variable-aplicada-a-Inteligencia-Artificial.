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
    .stTextInput label, .stTextArea label, .stSelectbox label {
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
    </style>
""", unsafe_allow_html=True)

# Función para corregir automáticamente sintaxis común (ej: 2x3 -> 2*x**3, 15x2 -> 15*x**2)
def limpiar_sintaxis_matematica(expresion: str) -> str:
    # Reemplazar potencias implícitas tipo x3 por x**3 o 2x3 por 2*x**3
    exp = expresion.replace("^", "**")
    # Insertar ** antes de los exponentes numéricos si están pegados a letras (ej: x3 -> x**3)
    exp = re.sub(r'([a-zA-Z])(\d+)', r'\1**\2', exp)
    # Insertar * entre números y letras pegadas (ej: 2x -> 2*x, 15x**2 -> 15*x**2)
    exp = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', exp)
    return exp

# Inicializar estados de la sesión
if "historial_problemas" not in st.session_state:
    st.session_state.historial_problemas = []
if "problema_activo" not in st.session_state:
    st.session_state.problema_activo = None

# --- BARRA LATERAL ---
with st.sidebar:
    try:
        st.image("logo_uis.webp", use_container_width=True)
    except:
        st.info("💡 Sube un archivo 'logo_uis.webp' al directorio para ver el escudo oficial.")
        
    st.markdown("### 💬 Conversaciones")
    
    if st.button("➕ Nuevo Problema", use_container_width=True):
        st.session_state.problema_activo = None
        st.rerun()
        
    st.markdown("---")
    st.markdown("<p style='font-size: 12px; color: #64748B; font-weight: 600;'>HISTORIAL RECIENTE</p>", unsafe_allow_html=True)
    
    if st.session_state.historial_problemas:
        for idx, item in enumerate(reversed(st.session_state.historial_problemas)):
            if st.button(f"📌 {item['titulo'][:22]}...", key=f"hist_{idx}", use_container_width=True):
                st.session_state.problema_activo = item
                st.rerun()
    else:
        st.markdown("<p style='font-size: 13px; color: #94A3B8;'>No hay problemas analizados aún.</p>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("##### 🏛️ Universidad Industrial de Santander")
    st.caption("Sede Barrancabermeja | Ing. Inteligencia Artificial")

# Definir la variable simbólica principal
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
    st.markdown("### 🔍 Memoria de Cálculo y Resultados:")
    st.latex(f"f(x) = {prob['f_latex']}")
    st.latex(f"f'(x) = {prob['f_prime_latex']}")
    st.latex(f"f''(x) = {prob['f_double_latex']}")
    
    st.markdown(prob['resultado_texto'], unsafe_allow_html=True)
    
    if st.button("⬅️ Volver al chat principal"):
        st.session_state.problema_activo = None
        st.rerun()

else:
    st.markdown("""
        <div class="chat-welcome-card">
            <h2>¿Qué problema vamos a resolver hoy?</h2>
            <p style="color: #64748B; font-size: 15px;">Ingresa tu función (ej: <code>2x3 - 15x2 + 36x</code>). La IA se encarga de adaptarla, derivar, hallar puntos críticos y darte el resultado paso a paso.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("#### ✍️ Planta tu caso de estudio:")
    enunciado_user = st.text_area("Enunciado o descripción del problema:", placeholder="Ej: Maximizar la función de costos...", height=100)
    funcion_str = st.text_input("Función objetivo $f(x)$:", placeholder="Ej: 2x3 - 15x2 + 36*x")
    
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        ejecutar = st.button("⚡ Analizar", use_container_width=True)
        
    if ejecutar:
        if not funcion_str.strip():
            st.warning("⚠️ Por favor ingresa una función matemática válida.")
        else:
            try:
                # Limpiar y parsear automáticamente la sintaxis natural del usuario
                funcion_saneada = limpiar_sintaxis_matematica(funcion_str)
                f_expr = sp.sympify(funcion_saneada)
                f_prime = sp.diff(f_expr, x)
                f_double_prime = sp.diff(f_prime, x)
                puntos_criticos = sp.solve(f_prime, x)
                
                st.markdown("---")
                st.markdown("### 📊 Resultados del Análisis:")
                
                st.write("**1. Función Objetivo:**")
                st.latex(f"f(x) = {sp.latex(f_expr)}")
                
                st.write("**2. Primera Derivada ($f'(x)$):**")
                st.latex(f"f'(x) = {sp.latex(f_prime)}")
                
                st.write("**3. Segunda Derivada ($f''(x)$):**")
                st.latex(f"f''(x) = {sp.latex(f_double_prime)}")
                
                res_texto_guardado = ""
                if puntos_criticos:
                    st.write("**4. Puntos Críticos y Criterio de la Segunda Derivada:**")
                    for pc in puntos_criticos:
                        st.latex(f"x = {sp.latex(pc)}")
                        try:
                            val_seg = float(f_double_prime.subs(x, pc).evalf())
                            val_y = float(f_expr.subs(x, pc).evalf())
                            x_num = float(pc.evalf())
                            
                            if val_seg < 0:
                                msg = f"✅ **MÁXIMO LOCAL** hallado en $x \\approx {x_num:.4f}$, con un valor de $f(x) = {val_y:.4f}$ (Segunda derivada negativa: {val_seg:.2f} < 0)."
                                st.success(msg)
                                res_texto_guardado += f"<br>{msg}"
                            elif val_seg > 0:
                                msg = f"✅ **MÍNIMO LOCAL** hallado en $x \\approx {x_num:.4f}$, con un valor de $f(x) = {val_y:.4f}$ (Segunda derivada positiva: {val_seg:.2f} > 0)."
                                st.success(msg)
                                res_texto_guardado += f"<br>{msg}"
                            else:
                                msg = f"⚠️ En $x = {pc}$, la segunda derivada es cero; el criterio no es concluyente."
                                st.warning(msg)
                                res_texto_guardado += f"<br>{msg}"
                        except:
                            msg = f"Punto crítico exacto en $x = {pc}$."
                            st.info(msg)
                            res_texto_guardado += f"<br>{msg}"
                else:
                    st.warning("No se encontraron puntos críticos reales.")
                    res_texto_guardado = "No se encontraron puntos críticos reales."
                    
                # Guardar en el historial de sesión
                nuevo_item = {
                    "titulo": enunciado_user[:30] if enunciado_user else f"Función: {funcion_str[:20]}",
                    "enunciado": enunciado_user if enunciado_user else "Sin enunciado redactado.",
                    "f_latex": sp.latex(f_expr),
                    "f_prime_laser": sp.latex(f_prime),
                    "f_prime_latex": sp.latex(f_prime),
                    "f_double_latex": sp.latex(f_double_prime),
                    "resultado_texto": res_texto_guardado
                }
                st.session_state.historial_problemas.append(nuevo_item)
                
            except Exception as e:
                st.error(f"⚠️ Error al interpretar la función. Revisa la sintaxis. Detalle: {e}")
