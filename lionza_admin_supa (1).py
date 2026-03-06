import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
import time
from datetime import datetime
from supabase import create_client

# ============================================================
# SUPABASE — conexión central
# ============================================================
SUPA_URL = "https://omluvyfminfkgdrasbll.supabase.co"
SUPA_KEY = "sb_publishable_Y6ZsdRYXg0OZZMagdAmB2w_1r345bzI"

@st.cache_resource
def get_supabase():
    return create_client(SUPA_URL, SUPA_KEY)

sb = get_supabase()

# ============================================================
# CONFIGURACIÓN GLOBAL
# ============================================================
st.set_page_config(
    page_title="Lionza Food Pro",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS PREMIUM + ALARMA
# ============================================================
# Generar beep WAV en base64
import struct, math, base64 as b64mod

def _gen_beep():
    sr = 44100
    samples = []
    for freq in [880, 1100, 880, 1320]:
        for i in range(int(sr * 0.12)):
            t = i / sr
            env = math.sin(math.pi * t / 0.12)
            samples.append(int(env * 0.6 * math.sin(2 * math.pi * freq * t) * 32767))
        samples.extend([0] * int(sr * 0.06))
    n = len(samples)
    wav = b'RIFF' + struct.pack('<I', 36 + n*2) + b'WAVEfmt '
    wav += struct.pack('<IHHIIHH', 16, 1, 1, sr, sr*2, 2, 16) + b'data' + struct.pack('<I', n*2)
    for s in samples:
        wav += struct.pack('<h', s)
    return b64mod.b64encode(wav).decode()

BEEP_B64 = _gen_beep()

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');
html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; background-color: #0f0f0f; color: #e8e2d9; }}
.stApp {{ background: #0f0f0f; }}
section[data-testid="stSidebar"] {{ background: #141414; border-right: 1px solid #2a2a2a; }}
.stTabs [data-baseweb="tab-list"] {{ background: #141414; border-radius: 12px; padding: 4px; gap: 4px; border: 1px solid #2a2a2a; }}
.stTabs [data-baseweb="tab"] {{ background: transparent; color: #888; font-family: 'DM Sans', sans-serif; font-weight: 600; font-size: 13px; letter-spacing: 0.5px; border-radius: 8px; padding: 8px 18px; border: none; }}
.stTabs [aria-selected="true"] {{ background: #d4a017 !important; color: #0f0f0f !important; }}
div[data-testid="stContainer"] > div {{ background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 16px; }}
[data-testid="stMetric"] {{ background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 12px; padding: 16px 20px; }}
[data-testid="stMetricValue"] {{ font-family: 'Bebas Neue', sans-serif; font-size: 2.2rem !important; color: #d4a017; }}
[data-testid="stMetricLabel"] {{ color: #888; font-size: 11px; letter-spacing: 1px; text-transform: uppercase; }}
.stButton > button[kind="primary"] {{ background: linear-gradient(135deg, #d4a017, #f0c040) !important; color: #0f0f0f !important; font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 14px; border: none !important; border-radius: 10px !important; padding: 12px 24px !important; transition: all 0.2s ease; }}
.stButton > button[kind="primary"]:hover {{ transform: translateY(-1px); box-shadow: 0 8px 25px rgba(212,160,23,0.35); }}
.stButton > button {{ background: #222 !important; color: #e8e2d9 !important; border: 1px solid #333 !important; border-radius: 10px !important; font-family: 'DM Sans', sans-serif; font-weight: 500; transition: all 0.15s ease; }}
.stButton > button:hover {{ border-color: #d4a017 !important; color: #d4a017 !important; }}
.stTextInput input, .stNumberInput input {{ background: #1e1e1e !important; border: 1px solid #333 !important; border-radius: 8px !important; color: #e8e2d9 !important; font-family: 'DM Sans', sans-serif; }}
.stTextInput input:focus, .stNumberInput input:focus {{ border-color: #d4a017 !important; box-shadow: 0 0 0 3px rgba(212,160,23,0.15) !important; }}
.stSelectbox [data-baseweb="select"] > div {{ background: #1e1e1e !important; border: 1px solid #333 !important; border-radius: 8px !important; color: #e8e2d9 !important; }}
.stProgress > div > div {{ background: #1a1a1a; border-radius: 999px; }}
.stProgress > div > div > div {{ background: linear-gradient(90deg, #d4a017, #f0c040); border-radius: 999px; }}
.stTable table {{ background: #1a1a1a; border-collapse: collapse; width: 100%; border-radius: 12px; overflow: hidden; }}
.stTable table th {{ background: #222; color: #d4a017; font-family: 'DM Sans', sans-serif; font-weight: 600; font-size: 11px; letter-spacing: 1px; text-transform: uppercase; padding: 12px 16px; border-bottom: 1px solid #2a2a2a; }}
.stTable table td {{ color: #e8e2d9; padding: 10px 16px; border-bottom: 1px solid #1e1e1e; font-size: 13px; }}
.stTable table tr:last-child td {{ border-bottom: none; }}
.stTable table tr:hover td {{ background: #222; }}
.prod-card {{ background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 14px; padding: 0; overflow: hidden; transition: all 0.2s ease; text-align: center; }}
.prod-card:hover {{ border-color: #d4a017; transform: translateY(-3px); box-shadow: 0 12px 30px rgba(0,0,0,0.5); }}
.prod-card-body {{ padding: 10px 8px 12px; }}
.prod-card-name {{ font-family: 'DM Sans', sans-serif; font-weight: 600; font-size: 12px; color: #e8e2d9; line-height: 1.3; margin-bottom: 4px; }}
.prod-card-price {{ font-family: 'Bebas Neue', sans-serif; font-size: 18px; color: #d4a017; }}
.ticket-header {{ background: linear-gradient(135deg,#1a1a1a,#222); border: 1px solid #2a2a2a; border-radius: 12px 12px 0 0; padding: 16px 20px; border-bottom: 1px dashed #333; }}
.ticket-total {{ background: #222; padding: 14px 20px; border-radius: 0 0 12px 12px; border: 1px solid #2a2a2a; border-top: 2px dashed #d4a017; }}
.cocina-badge {{ display: inline-block; background: #d4a017; color: #0f0f0f; font-family: 'Bebas Neue', sans-serif; font-size: 13px; letter-spacing: 1px; padding: 3px 12px; border-radius: 999px; margin-bottom: 6px; }}
.item-line {{ background: #1e1e1e; border-left: 3px solid #d4a017; border-radius: 0 8px 8px 0; padding: 7px 14px; margin: 4px 0; font-size: 14px; font-weight: 500; }}
@keyframes alarm-pulse {{ 0%{{background:#3a0000;border-color:#ff3333}} 50%{{background:#1a0000;border-color:#ff6666}} 100%{{background:#3a0000;border-color:#ff3333}} }}
.alarm-banner {{ animation: alarm-pulse 1s infinite; border: 2px solid #ff3333; border-radius: 14px; padding: 16px 22px; margin-bottom: 12px; }}
.alarm-title {{ font-family: 'Bebas Neue', sans-serif; font-size: 20px; color: #ff4444; letter-spacing: 2px; }}
.alarm-detail {{ font-size: 12px; color: #ffaaaa; margin-top: 3px; }}
.tasa-box {{ background: linear-gradient(135deg,#1a1500,#201900); border: 1px solid #d4a017; border-radius: 12px; padding: 14px 16px; margin: 12px 0; }}
.tasa-box .label {{ font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: #888; }}
.tasa-box .value {{ font-family: 'Bebas Neue', sans-serif; font-size: 32px; color: #d4a017; line-height: 1.1; }}
.tasa-box .sub {{ font-size: 11px; color: #666; }}
.stock-ok {{ color: #4ade80; font-weight: 600; }}
.stock-warn {{ color: #fbbf24; font-weight: 600; }}
.stock-crit {{ color: #f87171; font-weight: 600; }}
.section-label {{ font-family: 'DM Sans', sans-serif; font-size: 10px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: #555; margin-bottom: 8px; }}
hr {{ border-color: #2a2a2a; }}
::-webkit-scrollbar {{ width: 4px; }} ::-webkit-scrollbar-thumb {{ background: #333; border-radius: 999px; }}
</style>
<audio id="lionza_beep" src="data:audio/wav;base64,{BEEP_B64}" preload="auto"></audio>
<script>
(function(){{
    var _loop=null;
    function play(){{var a=document.getElementById('lionza_beep');if(a){{a.currentTime=0;a.play().catch(function(){{}});}}}}
    function startAlarm(){{if(_loop)return;play();_loop=setInterval(play,2800);}}
    function stopAlarm(){{if(_loop){{clearInterval(_loop);_loop=null;}}var a=document.getElementById('lionza_beep');if(a){{a.pause();a.currentTime=0;}}}}
    window._lionzaStartAlarm=startAlarm;
    window._lionzaStopAlarm=stopAlarm;
}})();
</script>
""", unsafe_allow_html=True)


# ============================================================
# SUPABASE — FUNCIONES DE DATOS
# ============================================================
def sb_cargar_inventario():
    try:
        res = sb.table('inventario').select('*').execute()
        return {r['insumo']: int(r['cantidad']) for r in res.data}
    except:
        return {
            'Pan Perro': 100, 'Salchichas': 100, 'Pan Jumbo': 50,
            'Pan Burger': 50, 'Carne Burger': 50, 'Medio Pollo': 20,
            'Alitas (unidades)': 120, 'Huevo': 60, 'Jamon': 100,
            'Queso': 100, 'Refresco 1.5L': 20, 'Arepitas': 200,
            'Ensalada': 50, 'Papas Fritas': 50
        }

def sb_guardar_inventario(inventario):
    try:
        for insumo, cantidad in inventario.items():
            sb.table('inventario').upsert({'insumo': insumo, 'cantidad': int(cantidad)}).execute()
    except Exception as e:
        st.error(f"Error guardando inventario: {e}")

def sb_guardar_tasa(tasa):
    try:
        sb.table('configuracion').upsert({'clave': 'tasa_dia', 'valor': str(tasa)}).execute()
    except:
        pass

def sb_leer_pedidos_clientes():
    """Lee pedidos con estado 'pendiente' enviados por clientes online."""
    try:
        res = sb.table('pedidos').select('*').eq('estado', 'pendiente').eq('origen', 'cliente').execute()
        pedidos = []
        for r in res.data:
            detalle = r['detalle'] if isinstance(r['detalle'], list) else json.loads(r['detalle'])
            pedidos.append({
                'id_supa':      r['id'],
                'Cliente':      r['cliente'],
                'Detalle':      detalle,
                'Total_U':      float(r['total_u'] or 0),
                'Total_B':      float(r['total_b'] or 0),
                'Metodo':       r['metodo'] or '',
                'Hora_Reg':     r['hora_reg'] or '',
                'Hora_Entrega': r['hora_entrega'] or '',
                'Nota':         r['nota'] or '',
                'Origen':       'cliente',
            })
        return pedidos
    except:
        return []

def sb_marcar_pedido_procesado(id_supa):
    try:
        sb.table('pedidos').update({'estado': 'en_cocina'}).eq('id', id_supa).execute()
    except:
        pass

def sb_marcar_despachado(id_supa):
    try:
        sb.table('pedidos').update({'estado': 'despachado'}).eq('id', id_supa).execute()
    except:
        pass

def sb_guardar_historial(pedido):
    try:
        sb.table('pedidos').insert({
            'cliente':      pedido['Cliente'],
            'detalle':      json.dumps(pedido['Detalle'], ensure_ascii=False),
            'total_u':      pedido['Total_U'],
            'total_b':      pedido['Total_B'],
            'metodo':       pedido['Metodo'],
            'hora_reg':     pedido['Hora_Reg'],
            'hora_entrega': pedido['Hora_Entrega'],
            'nota':         pedido.get('Nota', ''),
            'origen':       'admin',
            'estado':       'despachado',
        }).execute()
    except:
        pass


# ============================================================
# HELPERS DE ALARMA
# ============================================================
def hora_a_minutos(hora_str):
    try:
        s = hora_str.strip().upper()
        t = datetime.strptime(s, "%I:%M %p") if ('AM' in s or 'PM' in s) else datetime.strptime(s, "%H:%M")
        return t.hour * 60 + t.minute
    except:
        return None

def pedidos_vencidos():
    ahora_min   = datetime.now().hour * 60 + datetime.now().minute
    silenciados = st.session_state.get('alarmas_silenciadas', set())
    resultado   = []
    for idx, p in enumerate(st.session_state.pedidos):
        clave = f"{p['Cliente']}_{p['Hora_Reg']}"
        mins  = hora_a_minutos(p.get('Hora_Entrega', ''))
        if mins is not None and ahora_min >= mins and clave not in silenciados:
            resultado.append({'idx': idx, 'pedido': p, 'clave': clave})
    return resultado


# ============================================================
# ESTADO
# ============================================================
defaults = {
    'inventario':          None,   # se carga de Supabase abajo
    'pedidos':             [],
    'historial_ventas':    [],
    'carrito':             [],
    'key_reset':           0,
    'tasa_dia':            419.05,
    'alarmas_silenciadas': set(),
    'inv_cargado':         False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Cargar inventario desde Supabase la primera vez
if not st.session_state.inv_cargado:
    st.session_state.inventario  = sb_cargar_inventario()
    st.session_state.inv_cargado = True


# ============================================================
# CATÁLOGO
# ============================================================
RECETAS = {
    'Perro Caliente Simple':    {'Pan Perro': 1, 'Salchichas': 1},
    'Perro Jumbo':              {'Pan Jumbo': 1, 'Salchichas': 1},
    'Combo 6 Perros + 1.5L':   {'Pan Perro': 6, 'Salchichas': 6, 'Refresco 1.5L': 1},
    'Combo Jumbos + 1.5L':     {'Pan Jumbo': 4, 'Salchichas': 4, 'Refresco 1.5L': 1},
    'Hamburguesa Especial':     {'Pan Burger': 1, 'Carne Burger': 1, 'Huevo': 1, 'Jamon': 1, 'Queso': 1},
    'Hamburguesa Sencilla':     {'Pan Burger': 1, 'Carne Burger': 1, 'Jamon': 1, 'Queso': 1},
    'Medio Pollo Solo':         {'Medio Pollo': 1, 'Arepitas': 3, 'Ensalada': 1},
    'Alitas x6':                {'Alitas (unidades)': 6, 'Papas Fritas': 1, 'Arepitas': 2},
    'Combo Pollo + 1.5L':       {'Medio Pollo': 1, 'Refresco 1.5L': 1, 'Arepitas': 3, 'Ensalada': 1},
    'Combo Pollo+2Perros+1.5L': {'Medio Pollo': 1, 'Pan Perro': 2, 'Salchichas': 2, 'Refresco 1.5L': 1, 'Arepitas': 3, 'Ensalada': 1},
    'Refresco 1.5L':            {'Refresco 1.5L': 1},
}
PRECIOS_BASE = {
    'Perro Caliente Simple':    1.0,  'Perro Jumbo': 1.5,
    'Combo 6 Perros + 1.5L':   5.0,  'Combo Jumbos + 1.5L': 5.0,
    'Hamburguesa Especial':     3.0,  'Hamburguesa Sencilla': 2.0,
    'Medio Pollo Solo':         7.0,  'Alitas x6': 3.5,
    'Combo Pollo + 1.5L':       8.0,  'Combo Pollo+2Perros+1.5L': 9.0,
    'Refresco 1.5L':            1.5,
}
EMOJIS = {
    'Perro Caliente Simple':'🌭','Perro Jumbo':'🌭',
    'Combo 6 Perros + 1.5L':'🌭🥤','Combo Jumbos + 1.5L':'🌭🥤',
    'Hamburguesa Especial':'🍔','Hamburguesa Sencilla':'🍔',
    'Medio Pollo Solo':'🍗','Alitas x6':'🍗',
    'Combo Pollo + 1.5L':'🍗🥤','Combo Pollo+2Perros+1.5L':'🍗🌭🥤',
    'Refresco 1.5L':'🥤',
}
CATEGORIAS = {
    '🌭 Perros':           ['Perro Caliente Simple', 'Perro Jumbo'],
    '🌭🥤 Combos Perros':  ['Combo 6 Perros + 1.5L', 'Combo Jumbos + 1.5L'],
    '🍔 Hamburguesas':     ['Hamburguesa Especial', 'Hamburguesa Sencilla'],
    '🍗 Pollo':            ['Medio Pollo Solo', 'Alitas x6', 'Combo Pollo + 1.5L', 'Combo Pollo+2Perros+1.5L'],
    '🥤 Bebidas':          ['Refresco 1.5L'],
}

def calcular_precio(prod, cant):
    if prod == 'Perro Caliente Simple':
        return (cant // 2) * 1.5 + (cant % 2) * 1.0
    return PRECIOS_BASE[prod] * cant

def stock_disponible(prod, cant):
    return [ing for ing, cnt in RECETAS[prod].items()
            if st.session_state.inventario.get(ing, 0) < cnt * cant]


# ============================================================
# ABSORBER PEDIDOS DE CLIENTES ONLINE
# ============================================================
pedidos_online = sb_leer_pedidos_clientes()
if pedidos_online:
    ids_ya_en_cocina = {p.get('id_supa') for p in st.session_state.pedidos}
    nuevos = [p for p in pedidos_online if p.get('id_supa') not in ids_ya_en_cocina]
    if nuevos:
        for p in nuevos:
            puede = True
            for item in p.get('Detalle', []):
                for ing, cnt in RECETAS.get(item['Producto'], {}).items():
                    if st.session_state.inventario.get(ing, 0) < cnt * item['Cant']:
                        puede = False; break
            if puede:
                for item in p.get('Detalle', []):
                    for ing, cnt in RECETAS.get(item['Producto'], {}).items():
                        st.session_state.inventario[ing] = max(0, st.session_state.inventario[ing] - cnt * item['Cant'])
                sb_guardar_inventario(st.session_state.inventario)
                sb_marcar_pedido_procesado(p['id_supa'])
                st.session_state.pedidos.append(p)
        st.toast(f"🛎️ {len(nuevos)} pedido(s) nuevo(s) de clientes online", icon="🔔")
        st.rerun()


# ============================================================
# BANNERS DE ALARMA
# ============================================================
vencidos = pedidos_vencidos()
if vencidos:
    components.html("<script>var p=window.parent;var a=p.document.getElementById('lionza_beep');if(a){a.currentTime=0;a.play().catch(function(){});if(!p._lionzaLoop){p._lionzaLoop=setInterval(function(){a.currentTime=0;a.play().catch(function(){});},2800);}}</script>", height=0)
    for a in vencidos:
        p = a['pedido']
        prod_txt = ", ".join([f"{i['Cant']}× {i['Producto']}" for i in p['Detalle']])
        col_info, col_btn = st.columns([5, 1])
        with col_info:
            st.markdown(
                f'<div class="alarm-banner"><div class="alarm-title">🔔 ¡HORA DE ENTREGA! — {p["Cliente"]}</div>'
                f'<div class="alarm-detail">⏰ Para las {p["Hora_Entrega"]} · {prod_txt}</div></div>',
                unsafe_allow_html=True)
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔕 Silenciar", key=f"sil_top_{a['clave']}", use_container_width=True):
                st.session_state.alarmas_silenciadas.add(a['clave'])
                components.html("<script>if(window.parent._lionzaLoop){clearInterval(window.parent._lionzaLoop);window.parent._lionzaLoop=null;}var a=window.parent.document.getElementById('lionza_beep');if(a){a.pause();a.currentTime=0;}</script>", height=0)
                st.rerun()
else:
    components.html("<script>if(window.parent._lionzaLoop){clearInterval(window.parent._lionzaLoop);window.parent._lionzaLoop=null;}var a=window.parent.document.getElementById('lionza_beep');if(a){a.pause();a.currentTime=0;}</script>", height=0)


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:20px 0 10px;'><div style='font-family:Bebas Neue,sans-serif;font-size:36px;letter-spacing:3px;color:#d4a017;'>LIONZA</div><div style='font-size:10px;letter-spacing:3px;color:#555;text-transform:uppercase;'>Food Pro · Terminal</div></div>", unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="section-label">Tasa BCV del día</div>', unsafe_allow_html=True)
    tasa_bcv = st.number_input("BCV:", value=414.05, format="%.2f", label_visibility="collapsed")
    st.session_state.tasa_dia = tasa_bcv + 5.0
    sb_guardar_tasa(st.session_state.tasa_dia)

    st.markdown(f"""<div class="tasa-box"><div class="label">Tasa de venta</div>
    <div class="value">{st.session_state.tasa_dia:.2f}</div>
    <div class="sub">Bs. por dólar · margen +5 incluido</div></div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="section-label">Resumen del día</div>', unsafe_allow_html=True)
    monto_dia = sum(v['Total_U'] for v in st.session_state.historial_ventas)
    col_a, col_b = st.columns(2)
    col_a.metric("En cocina",   len(st.session_state.pedidos))
    col_b.metric("Despachados", len(st.session_state.historial_ventas))
    st.metric("Recaudado hoy",  f"${monto_dia:.2f}")
    st.divider()
    st.markdown('<div class="section-label">Acciones</div>', unsafe_allow_html=True)
    if st.button("🔄 Revisar pedidos online", use_container_width=True):
        st.rerun()
    if st.button("🔃 Recargar inventario", use_container_width=True):
        st.session_state.inventario  = sb_cargar_inventario()
        st.toast("Inventario recargado desde Supabase")
    st.divider()
    st.markdown(f'<div style="font-size:10px;color:#444;text-align:center;">{datetime.now().strftime("%A %d %b %Y — %I:%M %p")}</div>', unsafe_allow_html=True)

# ── AUTO-REFRESH cada 10 segundos para detectar pedidos online ──
# Usa st_autorefresh si está disponible, si no usa un componente JS
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=10000, key="autorefresh")
except ImportError:
    # Fallback: meta-refresh via components.html
    components.html(
        """<script>
        if (!window._lionzaRefreshSet) {
            window._lionzaRefreshSet = true;
            setTimeout(function() {
                // Simula clic en el botón "Revisar pedidos online" del sidebar
                var btns = window.parent.document.querySelectorAll('button');
                btns.forEach(function(b) {
                    if (b.innerText.includes('Revisar pedidos')) b.click();
                });
            }, 10000);
        }
        </script>""",
        height=0
    )


# ============================================================
# CABECERA
# ============================================================
st.markdown("""<div style="padding:20px 0 10px;border-bottom:1px solid #2a2a2a;margin-bottom:24px;">
<div style="font-family:'Bebas Neue',sans-serif;font-size:42px;letter-spacing:3px;color:#e8e2d9;margin:0;line-height:1;">
🦁 LIONZA <span style="color:#d4a017;">FOOD</span></div>
<div style="font-size:13px;color:#555;margin-top:4px;letter-spacing:1px;">SISTEMA DE PUNTO DE VENTA · VERSIÓN PRO</div></div>""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🛒  Caja & Pedidos","👨‍🍳  Cocina","📦  Almacén","📊  Cierre de Caja"])


# ────────────────────────────────────────────────────────────
# TAB 1 · CAJA
# ────────────────────────────────────────────────────────────
with tab1:
    col_menu, col_orden = st.columns([1.6, 1], gap="large")

    with col_menu:
        st.markdown('<div class="section-label">Datos del pedido</div>', unsafe_allow_html=True)
        c_cli, c_hora = st.columns(2)
        with c_cli:
            cliente = st.text_input("👤 Cliente / Mesa", placeholder="Ej: Mesa 3 o Juan", key=f"cli_{st.session_state.key_reset}")
        with c_hora:
            hora_str     = st.text_input("⏰ Hora de entrega", value=datetime.now().strftime("%I:%M %p"), placeholder="Ej: 07:30 PM", key=f"hora_{st.session_state.key_reset}")
            hora_entrega = hora_str.strip().upper() if hora_str.strip() else datetime.now().strftime("%I:%M %p")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Menú</div>', unsafe_allow_html=True)

        for cat_name, productos in CATEGORIAS.items():
            st.markdown(f'<div class="section-label" style="margin-top:14px;color:#666;">{cat_name}</div>', unsafe_allow_html=True)
            cols = st.columns(len(productos))
            for col, prod in zip(cols, productos):
                precio_usd = PRECIOS_BASE[prod]
                precio_bs  = precio_usd * st.session_state.tasa_dia
                emoji      = EMOJIS.get(prod, '🍽️')
                sin_stock  = len(stock_disponible(prod, 1)) > 0
                with col:
                    cs = "opacity:0.35;filter:grayscale(1);" if sin_stock else ""
                    sb_badge = '<div style="font-size:9px;color:#f87171;margin-top:2px;">SIN STOCK</div>' if sin_stock else ""
                    st.markdown(
                        f'<div class="prod-card" style="{cs}">'
                        f'<div style="height:90px;display:flex;align-items:center;justify-content:center;background:#111;font-size:44px;border-radius:12px 12px 0 0;">{emoji}</div>'
                        f'<div class="prod-card-body"><div class="prod-card-name">{prod}</div>'
                        f'<div class="prod-card-price">${precio_usd:.2f}</div>'
                        f'<div style="font-size:10px;color:#666;">{precio_bs:.0f} Bs.</div>'
                        + sb_badge + '</div></div>', unsafe_allow_html=True)
                    if not sin_stock:
                        if st.button("＋ Añadir", key=f"btn_{prod}_{st.session_state.key_reset}", use_container_width=True):
                            en_carrito = sum(i['Cant'] for i in st.session_state.carrito if i['Producto'] == prod)
                            faltantes  = [ing for ing, cnt in RECETAS[prod].items() if st.session_state.inventario.get(ing,0) < cnt*(en_carrito+1)]
                            if faltantes:
                                st.toast(f"⛔ Sin stock: {', '.join(faltantes)}", icon="🚫")
                            else:
                                p_usd = calcular_precio(prod, 1)
                                existe = False
                                for item in st.session_state.carrito:
                                    if item['Producto'] == prod:
                                        nc = item['Cant']+1; item['Cant']=nc; item['USD']=calcular_precio(prod,nc); item['BS']=item['USD']*st.session_state.tasa_dia; existe=True; break
                                if not existe:
                                    st.session_state.carrito.append({'Producto':prod,'Cant':1,'USD':p_usd,'BS':round(p_usd*st.session_state.tasa_dia,2)})
                                st.toast(f"✅ {prod} añadido", icon="🛒"); st.rerun()

    with col_orden:
        st.markdown('<div class="section-label">Orden actual</div>', unsafe_allow_html=True)
        if not st.session_state.carrito:
            st.markdown('<div style="background:#141414;border:1px dashed #2a2a2a;border-radius:14px;padding:50px 20px;text-align:center;color:#444;"><div style="font-size:40px;">🛒</div><div style="font-size:13px;margin-top:10px;">La orden está vacía</div></div>', unsafe_allow_html=True)
        else:
            total_usd = sum(i['USD'] for i in st.session_state.carrito)
            total_bs  = total_usd * st.session_state.tasa_dia
            st.markdown(f'<div class="ticket-header"><div style="font-size:11px;color:#888;letter-spacing:1px;text-transform:uppercase;">Pedido para</div><div style="font-family:DM Sans;font-size:18px;font-weight:700;color:#e8e2d9;">{cliente if cliente else "—"}</div><div style="font-size:11px;color:#666;margin-top:4px;">⏰ {hora_entrega}</div></div>', unsafe_allow_html=True)

            for idx, item in enumerate(st.session_state.carrito):
                c_i, c_cant, c_p, c_d = st.columns([3,1,2,1])
                c_i.markdown(f"**{item['Producto']}**")
                nueva_cant = c_cant.number_input("", min_value=1, max_value=50, value=item['Cant'], key=f"cant_{idx}_{st.session_state.key_reset}", label_visibility="collapsed")
                if nueva_cant != item['Cant']:
                    item['Cant']=nueva_cant; item['USD']=calcular_precio(item['Producto'],nueva_cant); item['BS']=item['USD']*st.session_state.tasa_dia; st.rerun()
                c_p.markdown(f"<span style='color:#d4a017;font-family:Bebas Neue;font-size:16px;'>${item['USD']:.2f}</span>", unsafe_allow_html=True)
                c_p.caption(f"{item['BS']:.0f} Bs.")
                if c_d.button("🗑", key=f"del_{idx}_{st.session_state.key_reset}"):
                    st.session_state.carrito.pop(idx); st.rerun()

            st.markdown(f'<div class="ticket-total"><div style="display:flex;justify-content:space-between;align-items:center;"><div style="font-size:11px;letter-spacing:1px;text-transform:uppercase;color:#888;">Total</div><div><span style="font-family:Bebas Neue;font-size:26px;color:#d4a017;">${total_usd:.2f}</span><span style="font-size:12px;color:#666;margin-left:6px;">{total_bs:.2f} Bs.</span></div></div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-label">Método de pago</div>', unsafe_allow_html=True)
            metodo_pago = st.radio("Pago:", ["💵 Efectivo $","📱 Pago Móvil","💸 Zelle","🏧 Efectivo Bs.","🔀 Mixto"], horizontal=False, label_visibility="collapsed", key=f"metodo_{st.session_state.key_reset}")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔥 ENVIAR A COCINA", use_container_width=True, type="primary"):
                if not cliente:
                    st.warning("⚠️ Ingresa el nombre del cliente o número de mesa.")
                else:
                    errores = []
                    for item in st.session_state.carrito:
                        for ing, cnt in RECETAS[item['Producto']].items():
                            if st.session_state.inventario.get(ing,0) < cnt*item['Cant']:
                                errores.append(f"**{ing}**: necesitas {cnt*item['Cant']}, hay {st.session_state.inventario.get(ing,0)}")
                    if errores:
                        st.error("⛔ Stock insuficiente:\n\n" + "\n".join(errores))
                    else:
                        for item in st.session_state.carrito:
                            for ing, cnt in RECETAS[item['Producto']].items():
                                st.session_state.inventario[ing] = max(0, st.session_state.inventario[ing]-cnt*item['Cant'])
                        sb_guardar_inventario(st.session_state.inventario)
                        pedido = {'Cliente':cliente,'Detalle':st.session_state.carrito.copy(),'Total_U':total_usd,'Total_B':total_bs,'Metodo':metodo_pago,'Hora_Reg':datetime.now().strftime("%I:%M %p"),'Hora_Entrega':hora_entrega,'Nota':'','Origen':'admin'}
                        st.session_state.pedidos.append(pedido)
                        st.session_state.carrito = []
                        st.success("✅ Pedido enviado a cocina", icon="🚀")
                        st.balloons(); time.sleep(1.5)
                        st.session_state.key_reset += 1; st.rerun()


# ────────────────────────────────────────────────────────────
# TAB 2 · COCINA
# ────────────────────────────────────────────────────────────
with tab2:
    if not st.session_state.pedidos:
        st.markdown('<div style="text-align:center;padding:80px 0;color:#333;"><div style="font-size:64px;">✨</div><div style="font-family:Bebas Neue;font-size:28px;letter-spacing:2px;margin-top:12px;color:#444;">COCINA DESPEJADA</div><div style="font-size:13px;color:#555;margin-top:6px;">No hay pedidos pendientes</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="section-label">{len(st.session_state.pedidos)} pedido(s) activo(s)</div>', unsafe_allow_html=True)
        ahora_min   = datetime.now().hour*60+datetime.now().minute
        silenciados = st.session_state.get('alarmas_silenciadas', set())
        num_cols    = min(len(st.session_state.pedidos), 3)
        cols        = st.columns(num_cols)

        # Usamos una copia de la lista para iterar — evita el bug de pop(idx)
        # que borraba el pedido equivocado cuando había múltiples pedidos
        pedido_a_despachar = None
        pedido_a_silenciar = None

        for idx, p in enumerate(st.session_state.pedidos):
            clave      = f"{p['Cliente']}_{p['Hora_Reg']}"
            mins       = hora_a_minutos(p.get('Hora_Entrega',''))
            es_urgente = (mins is not None and ahora_min >= mins and clave not in silenciados)
            es_online  = p.get('Origen') == 'cliente'

            with cols[idx % num_cols]:
                with st.container(border=True):
                    urgente_tag = ' &nbsp;<span style="background:#ff3333;color:#fff;font-size:10px;padding:2px 8px;border-radius:999px;">¡AHORA!</span>' if es_urgente else ''
                    online_tag  = ' &nbsp;<span style="background:#1a3a1a;color:#4ade80;font-size:10px;padding:2px 8px;border-radius:999px;">ONLINE</span>' if es_online else ''
                    st.markdown(
                        f'<div class="cocina-badge">PEDIDO #{idx+1}{urgente_tag}{online_tag}</div>'
                        f'<div style="font-family:DM Sans;font-size:22px;font-weight:700;color:#e8e2d9;margin-bottom:2px;">{p["Cliente"]}</div>'
                        f'<div style="font-family:JetBrains Mono;font-size:11px;color:#666;margin-bottom:10px;">🕒 {p["Hora_Reg"]} &nbsp;|&nbsp; ⏰ <strong style="color:#d4a017;">{p["Hora_Entrega"]}</strong></div>',
                        unsafe_allow_html=True)
                    for i in p['Detalle']:
                        st.markdown(f'<div class="item-line"><span style="color:#d4a017;font-family:Bebas Neue;font-size:18px;">{i["Cant"]}×</span>&nbsp;{i["Producto"]}</div>', unsafe_allow_html=True)

                    nota_txt  = p.get('Nota','')
                    nota_html = f'<div style="margin-top:4px;font-size:11px;color:#aaa;">📝 {nota_txt}</div>' if nota_txt else ''
                    st.markdown(f'<div style="margin-top:10px;font-size:12px;color:#666;">{p["Metodo"]} · <span style="color:#d4a017;font-weight:600;">${p["Total_U"]:.2f}</span> / {p["Total_B"]:.0f} Bs.</div>' + nota_html, unsafe_allow_html=True)

                    b1, b2 = st.columns(2)
                    if b1.button("✅ DESPACHADO", key=f"des_{idx}", use_container_width=True, type="primary"):
                        pedido_a_despachar = (idx, p, clave)
                    if es_urgente:
                        if b2.button("🔕 Silenciar", key=f"sil_cocina_{clave}", use_container_width=True):
                            pedido_a_silenciar = clave

        # Ejecutar despacho FUERA del loop — evita el bug de índices corruptos
        if pedido_a_despachar:
            idx_d, listo, clave_d = pedido_a_despachar
            st.session_state.pedidos.pop(idx_d)
            st.session_state.historial_ventas.append(listo)
            st.session_state.alarmas_silenciadas.discard(clave_d)
            if listo.get('id_supa'):
                sb_marcar_despachado(listo['id_supa'])
            else:
                sb_guardar_historial(listo)
            st.rerun()

        if pedido_a_silenciar:
            st.session_state.alarmas_silenciadas.add(pedido_a_silenciar)
            components.html("<script>if(window.parent._lionzaLoop){clearInterval(window.parent._lionzaLoop);window.parent._lionzaLoop=null;}var a=window.parent.document.getElementById('lionza_beep');if(a){a.pause();a.currentTime=0;}</script>", height=0)
            st.rerun()


# ────────────────────────────────────────────────────────────
# TAB 3 · ALMACÉN
# ────────────────────────────────────────────────────────────
with tab3:
    col_inv, col_reab = st.columns([2,1], gap="large")
    with col_inv:
        st.markdown('<div class="section-label">Niveles de stock</div>', unsafe_allow_html=True)
        criticos = {k:v for k,v in st.session_state.inventario.items() if v<=10}
        alertas  = {k:v for k,v in st.session_state.inventario.items() if 10<v<=20}
        normales = {k:v for k,v in st.session_state.inventario.items() if v>20}
        if criticos:
            st.markdown('<div style="background:#1a0505;border:1px solid #5a1a1a;border-radius:10px;padding:10px 16px;margin-bottom:16px;font-size:12px;color:#f87171;">⛔ STOCK CRÍTICO: ' + ", ".join(criticos.keys()) + '</div>', unsafe_allow_html=True)
        for grupo, clase, max_v in [(criticos,'stock-crit',15),(alertas,'stock-warn',25),(normales,'stock-ok',200)]:
            for ing, stock in grupo.items():
                c1,c2,c3 = st.columns([3,1,4])
                c1.markdown(f"**{ing}**")
                c2.markdown(f'<span class="{clase}">{stock}</span>', unsafe_allow_html=True)
                c3.progress(max(0.0, min(stock/max_v, 1.0)))

    with col_reab:
        st.markdown('<div class="section-label">Reabastecer</div>', unsafe_allow_html=True)
        with st.container(border=True):
            ing_surtir   = st.selectbox("Insumo:", list(st.session_state.inventario.keys()))
            stock_actual = st.session_state.inventario[ing_surtir]
            st.caption(f"Stock actual: **{stock_actual}** ud.")
            cant_nueva = st.number_input("Nuevo total físico:", min_value=0, value=int(stock_actual))
            dif = cant_nueva - stock_actual
            if dif>0: st.success(f"➕ +{dif} unidades")
            elif dif<0: st.warning(f"➖ -{abs(dif)} unidades")
            if st.button("💾 Guardar en Supabase", use_container_width=True, type="primary"):
                st.session_state.inventario[ing_surtir] = cant_nueva
                sb_guardar_inventario(st.session_state.inventario)
                st.success(f"✅ Guardado en la nube"); time.sleep(1); st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        cA,cB = st.columns(2)
        cA.metric("🔴 Críticos", len(criticos))
        cB.metric("🟡 Alertas",  len(alertas))
        st.metric("Total insumos", len(st.session_state.inventario))


# ────────────────────────────────────────────────────────────
# TAB 4 · CIERRE DE CAJA
# ────────────────────────────────────────────────────────────
with tab4:
    if not st.session_state.historial_ventas:
        st.markdown('<div style="text-align:center;padding:80px 0;color:#333;"><div style="font-size:64px;">📊</div><div style="font-family:Bebas Neue;font-size:28px;letter-spacing:2px;margin-top:12px;color:#444;">SIN VENTAS AÚN</div></div>', unsafe_allow_html=True)
    else:
        df_h = pd.DataFrame(st.session_state.historial_ventas)
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("💵 Total USD",       f"${df_h['Total_U'].sum():.2f}")
        c2.metric("🇻🇪 Total Bs.",      f"{df_h['Total_B'].sum():.0f}")
        c3.metric("🍔 Pedidos",         len(df_h))
        c4.metric("🎯 Ticket promedio", f"${df_h['Total_U'].mean():.2f}")
        st.divider()

        col_rep, col_pago = st.columns([2,1], gap="large")
        with col_rep:
            st.markdown('<div class="section-label">Detalle de facturación</div>', unsafe_allow_html=True)
            rep_lista = []
            for v in st.session_state.historial_ventas:
                prod_txt = ", ".join([f"{i['Cant']}× {i['Producto']}" for i in v['Detalle']])
                rep_lista.append({"Hora":v['Hora_Reg'],"Para":v['Hora_Entrega'],"Cliente":v['Cliente'],"Pedido":prod_txt,"Método":v['Metodo'],"Monto ($)":f"${v['Total_U']:.2f}","Monto (Bs)":f"{v['Total_B']:.2f} Bs."})
            st.table(pd.DataFrame(rep_lista))

        with col_pago:
            st.markdown('<div class="section-label">Por método de pago</div>', unsafe_allow_html=True)
            resumen = df_h.groupby('Metodo')['Total_U'].sum().reset_index()
            resumen.columns = ['Método','Total USD']
            resumen['Total Bs'] = resumen['Total USD'] * st.session_state.tasa_dia
            resumen['Total USD'] = resumen['Total USD'].apply(lambda x: f"${x:.2f}")
            resumen['Total Bs']  = resumen['Total Bs'].apply(lambda x: f"{x:.0f} Bs.")
            st.table(resumen)
            conteo = {}
            for v in st.session_state.historial_ventas:
                for i in v['Detalle']:
                    conteo[i['Producto']] = conteo.get(i['Producto'],0)+i['Cant']
            if conteo:
                top = max(conteo, key=conteo.get)
                st.markdown(f'<div style="background:#1a1500;border:1px solid #d4a017;border-radius:12px;padding:16px;text-align:center;margin-top:12px;"><div style="font-size:10px;letter-spacing:2px;color:#888;text-transform:uppercase;">⭐ Más vendido</div><div style="font-family:Bebas Neue;font-size:22px;color:#d4a017;margin:6px 0;">{top}</div><div style="font-size:12px;color:#666;">{conteo[top]} unidades</div></div>', unsafe_allow_html=True)

        st.divider()
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔒 CERRAR TURNO Y GUARDAR", use_container_width=True, type="primary"):
                st.session_state.historial_ventas = []
                st.success("✅ Turno cerrado.")
                time.sleep(2); st.rerun()
        with col_btn2:
            csv_data = pd.DataFrame(rep_lista).to_csv(index=False).encode('utf-8')
            st.download_button(label="⬇️ EXPORTAR CSV", data=csv_data,
                               file_name="reporte_lionza_{}.csv".format(datetime.now().strftime("%Y%m%d")),
                               mime="text/csv", use_container_width=True)
