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
    .tip-box {
        background-color: #E2F6EC;
        border-left: 5px solid #007A33;
        padding: 1.5rem;
        border-radius: 0 12px 12px 0;
        margin-bottom: 1.5rem;
        color: #1E293B;
    }
    .step-box {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
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
        st.markdown("<p style='font-size: 13px; color: #94A3B8;'>No hay problemas analizados aún.</p>", unsafe_allow_html=True)
        
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
    
    # Tips claros y con lenguaje humano, sin etiquetas rotas
    st.markdown("""
        <div class="tip-box">
            <p><b>💡 Tip 1: ¿Qué representa la función?</b><br>
            La verdad, cuando nos dan la función ya lista, lo primero es pensar que estamos buscando los puntos más altos (cima) o más bajos (valle) de esa curva. No te afanes, piensa en el comportamiento general de la gráfica.</p>
            
            <p><b>💡 Tip 2: La derivada como la pendiente.</b><br>
            Recuerda que derivar significa hallar cómo cambia la función en cada instante. Si bajas los exponentes a multiplicar y le restas uno, vas a encontrar la fórmula de la pendiente ($f'(x)$).</p>
            
            <p><b>💡 Tip 3: ¿De dónde salen los puntos críticos?</b><br>
            Imagínate la cumbre de una colina o el fondo de un valle: justo ahí, la pendiente es plana, es decir, vale cero. Por eso igualamos la primera derivada a cero para despejar nuestra $x$.</p>
            
            <p><b>💡 Tip 4: El toque final con la segunda derivada.</b><br>
            Para estar seguros de si es un máximo o un mínimo sin dibujar toda la gráfica, tomamos la segunda derivada ($f''(x)$) y evaluamos nuestros puntos. Si da negativo, es una cima; si da positivo, es un valle.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Botón para revelar el paso a paso completo estilo la 3ra foto
    if not st.session_state.mostrar_solucion:
        if st.button("🔍 Ver Solución Paso a Paso Completa"):
            st.session_state.mostrar_solucion = True
            st.rerun()
    else:
        st.markdown("---")
        st.markdown("### 📊 Solución Paso a Paso Completa:")
        
        # HTML renderizado con bloques limpios idénticos al formato solicitado
        st.markdown(prob['html_solucion'], unsafe_allow_html=True)
        
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
            <p style="color: #64748B; font-size: 15px;">Ingresa tu función (ej: <code>2x3 - 15x2 + 36*x</code>). Primero te daremos las pistas para que lo pienses con calma, y luego podrás desplegar el desglose analítico completo paso a paso.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("#### ✍️ Planta tu caso de estudio:")
    enunciado_user = st.text_area("Enunciado o descripción del problema:", placeholder="Ej: Analizar los puntos extremos de la función...", height=100)
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
                
                # Construir el HTML detallado paso a paso exactamente como en la foto 3
                html_paso_a_paso = f"""
                <div class="step-box">
                    <p style="font-weight: 700; color: #004D20; font-size: 16px;">Paso 1: Primera derivada y puntos críticos</p>
                    <p>Se calcula la primera derivada de la función para encontrar las pendientes iguales a cero:</p>
                    <div style="text-align: center; margin: 15px 0;">
                        <code>f'(x) = {sp.latex(f_prime)}</code>
                    </div>
                    <p>Igualando la primera derivada a cero para hallar los puntos críticos:</p>
                </div>
                """
                
                # Añadir puntos críticos y evaluación detallada
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
                            <div class="step-box">
                                <p style="font-weight: 700; color: #1E293B;">Para $x = {x_num:.2f}$:</p>
                                <p>Evaluamos en la segunda derivada: $f''({x_num:.2f}) = {val_seg:.2f}$ ({signo_str}).</p>
                                <p>Como el resultado es {'negativo' if val_seg < 0 else 'positivo'}, existe un <b>{tipo_extremo}</b> en este punto.</p>
                                <p>Evaluando en la función original: $f({x_num:.2f}) = {val_y:.2f}$.</p>
                                <p><b>Coordenada del extremo:</b> $({x_num:.2f}, {val_y:.2f})$</p>
                            </div>
                            """
                        except:
                            detalle_evaluacion += f"<p>Punto crítico en $x = {pc}$</p>"
                else:
                    detalle_evaluacion = "<p>No se encontraron puntos críticos reales.</p>"
                
                html_paso_a_paso += f"""
                <div class="step-box">
                    <p style="font-weight: 700; color: #004D20; font-size: 16px;">Paso 2: Segunda derivada</p>
                    <p>Se obtiene la segunda derivada para aplicar el criterio correspondiente:</p>
                    <div style="text-align: center; margin: 15px 0;">
                        <code>f''(x) = {sp.latex(f_double_prime)}</code>
                    </div>
                </div>
                
                <div class="step-box">
                    <p style="font-weight: 700; color: #004D20; font-size: 16px;">Paso 3: Evaluación y clasificación de extremos</p>
                    {detalle_evaluacion}
                </div>
                """
                
                # Guardar en sesión
                nuevo_item = {
                    "titulo": enunciado_user[:30] if enunciado_user else f"Función: {funcion_str[:20]}",
                    "enunciado": enunciado_user if enunciado_user else "Sin enunciado redactado.",
                    "f_latex": sp.latex(f_expr),
                    "html_solucion": html_paso_a_paso
                }
                st.session_state.problema_activo = nuevo_item
                st.session_state.mostrar_solucion = False
                st.rerun()
                
            except Exception as e:
                st.error(f"⚠️ Error al interpretar la función. Revisa la sintaxis. Detalle: {e}")
