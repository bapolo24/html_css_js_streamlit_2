# ============================================================
# GUÍA DE LECTURA DEL SCRIPT
# ============================================================
# Python / Streamlit = recibe datos y realiza cálculos.
# HTML = define qué elementos existen en pantalla.
# CSS = define cómo se ven esos elementos.
# JavaScript = define qué sucede cuando el usuario interactúa.
#
# Los comentarios están escritos en términos simples para que
# el archivo pueda utilizarse directamente durante la clase.
# ============================================================

# Streamlit recibe los datos y coordina los cálculos de la aplicación.
import streamlit as st
import streamlit.components.v1 as components
from textwrap import dedent

st.set_page_config(page_title="Oil & Gas | Centro de control", page_icon="🛢️", layout="wide")

# Paleta sobria de operación: azul petróleo, gris acero y verde señal.
NAVY = "#0B1F33"
STEEL = "#173A52"
MINT = "#46D7B0"
ICE = "#EAF3F5"
MUTED = "#A9BFCA"

st.markdown(dedent(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');
:root {{ --navy: {NAVY}; --steel: {STEEL}; --mint: {MINT}; --ice: {ICE}; --muted: {MUTED}; --line: rgba(234,243,245,.14); }}
.stApp {{ background: #071522; color: var(--ice); font-family: 'DM Sans', sans-serif; }}
[data-testid="stHeader"] {{ background: rgba(7,21,34,.82); }}
.block-container {{ max-width: 1260px; padding: 3.5rem 2.5rem 4rem; }}
h1, h2, h3 {{ font-family: 'Barlow Condensed', sans-serif !important; letter-spacing: .02em; }}
h1 {{ font-size: clamp(2.8rem, 6vw, 5.2rem) !important; line-height: .94 !important; }}
h2, h3, p, label, [data-testid="stMetricLabel"] {{ color: var(--ice) !important; }}
.eyebrow {{ color: var(--mint); font-size: .72rem; font-weight: 700; letter-spacing: .18em; text-transform: uppercase; }}
.hero {{ border-left: 4px solid var(--mint); padding: 1.8rem 2rem; margin-bottom: 2.1rem; background: linear-gradient(100deg, rgba(23,58,82,.96), rgba(11,31,51,.64)); box-shadow: 0 18px 48px rgba(0,0,0,.2); }}
.hero p {{ color: var(--muted) !important; max-width: 650px; font-size: 1.02rem; }}
.section-label {{ color: var(--mint); font: 600 1rem 'Barlow Condensed', sans-serif; letter-spacing: .08em; text-transform: uppercase; border-bottom: 1px solid var(--line); padding-bottom: .7rem; margin: 0 0 1.1rem; }}
.panel, .result-card {{ background: rgba(23,58,82,.64); border: 1px solid var(--line); padding: 1.5rem; transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease; }}
.panel:hover, .result-card:hover {{ transform: translateY(-4px); border-color: rgba(70,215,176,.7); box-shadow: 0 16px 35px rgba(0,0,0,.2); }}
.panel {{ min-height: 350px; }}
.result-card {{ margin-top: 1.3rem; border-top: 3px solid var(--mint); }}
.result-card strong {{ color: var(--mint); }}
div[data-testid="stNumberInput"] input {{ background: rgba(7,21,34,.7); color: var(--ice); border-color: var(--line); }}
div.stButton > button {{ width: 100%; border: 1px solid var(--mint); border-radius: 3px; background: var(--mint); color: #071522; font-weight: 700; letter-spacing: .04em; padding: .75rem 1rem; transition: transform .2s ease, box-shadow .2s ease, background .2s ease; }}
div.stButton > button:hover {{ transform: translateY(-3px); background: #80ebcc; box-shadow: 0 10px 24px rgba(70,215,176,.25); color: #071522; }}
div[data-testid="stMetric"] {{ background: rgba(23,58,82,.64); border: 1px solid var(--line); border-left: 3px solid var(--mint); padding: 1rem; transition: transform .2s ease; }}
div[data-testid="stMetric"]:hover {{ transform: translateY(-3px); }}
div[data-testid="stMetricValue"] {{ color: var(--ice); font-family: 'Barlow Condensed', sans-serif; }}
@media (max-width: 700px) {{ .block-container {{ padding: 2rem 1rem 3rem; }} .hero {{ padding: 1.25rem; }} }}
</style>
"""), unsafe_allow_html=True)

st.markdown(dedent("""
<section class="hero">
    <div class="eyebrow">Operations intelligence / Production monitoring</div>
    <h1>Centro de control<br>de producción</h1>
    <p>Lectura ejecutiva de desempeño para un pozo productor. Ajuste los parámetros y obtenga una estimación operacional inmediata.</p>
</section>
"""), unsafe_allow_html=True)

left, right = st.columns([1, 1.08], gap="large")

with left:
    st.markdown('<div class="section-label">01 / Parámetros operacionales</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    oil_bopd = st.slider("Producción de petróleo [BOPD]", 100, 5000, 1200, 50)
    water_bwpd = st.slider("Producción de agua [BWPD]", 0, 5000, 600, 50)
    oil_price = st.number_input("Precio estimado [USD/bbl]", 1.0, 200.0, 75.0, 1.0)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="height: 1rem"></div>', unsafe_allow_html=True)
    calcular = st.button("CALCULAR INDICADORES", type="primary")

with right:
    st.markdown('<div class="section-label">02 / Estado del activo</div>', unsafe_allow_html=True)
    components.html("""
    <style>
    html, body { margin:0; background:transparent; font-family:'DM Sans', sans-serif; }
    .asset { --x:50%; --y:50%; min-height:350px; padding:28px; position:relative; overflow:hidden; border:1px solid rgba(70,215,176,.4); border-top:3px solid #46D7B0; background: radial-gradient(circle at var(--x) var(--y), rgba(70,215,176,.18), transparent 35%), #173A52; color:#EAF3F5; transition: border-color .25s ease, box-shadow .25s ease; }
    .asset:hover { border-color:#46D7B0; box-shadow:0 16px 36px rgba(0,0,0,.28); }
    .asset h2 { margin:0 0 2.4rem; color:#46D7B0; font:700 2rem 'Barlow Condensed', sans-serif; letter-spacing:.04em; }
    .asset p { margin:.7rem 0; color:#A9BFCA; } .asset strong { color:#EAF3F5; }
    .asset .status { position:absolute; bottom:28px; left:28px; right:28px; padding-top:14px; border-top:1px solid rgba(234,243,245,.15); font-size:.8rem; letter-spacing:.06em; text-transform:uppercase; }
    .dot { display:inline-block; width:8px; height:8px; margin-right:8px; background:#46D7B0; border-radius:50%; box-shadow:0 0 12px #46D7B0; }
    </style>
    <div id="asset" class="asset">
        <h2>POZO A-17 / ONLINE</h2>
        <p>Clase de activo: <strong>Productor convencional</strong></p>
        <p>Última lectura: <strong>hace 04 min</strong></p>
        <p>Disponibilidad del sistema: <strong>99.2%</strong></p>
        <div id="status" class="status"><span class="dot"></span>Monitoreo activo</div>
    </div>
    <script>
    const asset = document.getElementById('asset');
    const status = document.getElementById('status');
    asset.addEventListener('mouseenter', () => { status.lastChild.textContent = '  Interacción activa'; });
    asset.addEventListener('mouseleave', () => {
        status.lastChild.textContent = '  Monitoreo activo';
        asset.style.setProperty('--x', '50%'); asset.style.setProperty('--y', '50%');
    });
    asset.addEventListener('mousemove', (event) => {
        const box = asset.getBoundingClientRect();
        asset.style.setProperty('--x', `${((event.clientX - box.left) / box.width) * 100}%`);
        asset.style.setProperty('--y', `${((event.clientY - box.top) / box.height) * 100}%`);
    });
    </script>
    """, height=385)

if calcular:
    total_fluid = oil_bopd + water_bwpd
    water_cut = water_bwpd / total_fluid * 100 if total_fluid else 0
    monthly_oil = oil_bopd * 30
    gross_revenue = monthly_oil * oil_price

    st.markdown('<div class="section-label">03 / Indicadores de desempeño</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Fluido total", f"{total_fluid:,.0f} BFPD")
    c2.metric("Water Cut", f"{water_cut:.1f}%")
    c3.metric("Ingreso mensual", f"${gross_revenue:,.0f}")
    st.markdown(dedent(f"""
    <div class="result-card"><strong>Resumen ejecutivo</strong><p>La operación registra <strong>{oil_bopd:,.0f} BOPD</strong> y un Water Cut de <strong>{water_cut:.1f}%</strong>. El ingreso bruto mensual estimado alcanza <strong>${gross_revenue:,.0f}</strong>.</p></div>
    """), unsafe_allow_html=True)

st.caption("Modelo educativo: no incluye regalías, impuestos, OPEX, transporte ni descuentos comerciales.")



