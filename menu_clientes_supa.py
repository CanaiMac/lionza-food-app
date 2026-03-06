import streamlit as st
import json
from datetime import datetime
from supabase import create_client

# ============================================================
# SUPABASE
# ============================================================
SUPA_URL = "https://omluvyfminfkgdrasbll.supabase.co"
SUPA_KEY = "sb_publishable_Y6ZsdRYXg0OZZMagdAmB2w_1r345bzI"

@st.cache_resource
def get_supabase():
    return create_client(SUPA_URL, SUPA_KEY)

sb = get_supabase()

# ============================================================
# CONFIGURACIÓN
# ============================================================
st.set_page_config(
    page_title="Lionza Food — Haz tu pedido",
    page_icon="🦁",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: #0f0f0f; color: #e8e2d9; }
.stApp { background: #0f0f0f; }
section[data-testid="stSidebar"] { display: none !important; }
#MainMenu { visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #d4a017, #f0c040) !important;
    color: #0f0f0f !important; font-family: 'DM Sans', sans-serif; font-weight: 700;
    font-size: 15px; border: none !important; border-radius: 12px !important;
    padding: 14px 28px !important; transition: all 0.2s ease; width: 100%;
}
.stButton > button[kind="primary"]:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(212,160,23,0.4); }
.stButton > button { background: #1e1e1e !important; color: #e8e2d9 !important; border: 1px solid #333 !important; border-radius: 10px !important; font-family: 'DM Sans', sans-serif; transition: all 0.15s ease; }
.stButton > button:hover { border-color: #d4a017 !important; color: #d4a017 !important; }
.stTextInput input { background: #1e1e1e !important; border: 1px solid #333 !important; border-radius: 10px !important; color: #e8e2d9 !important; font-family: 'DM Sans', sans-serif; font-size: 15px; padding: 12px !important; }
.stTextInput input:focus { border-color: #d4a017 !important; box-shadow: 0 0 0 3px rgba(212,160,23,0.15) !important; }
.stRadio label { color: #e8e2d9 !important; font-size: 14px; }
.stNumberInput input { background: #1e1e1e !important; border: 1px solid #333 !important; border-radius: 8px !important; color: #e8e2d9 !important; }

.menu-card { background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 16px; padding: 0; overflow: hidden; transition: all 0.2s ease; text-align: center; }
.menu-card:hover { border-color: #d4a017; transform: translateY(-2px); box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
.menu-card-emoji { height: 80px; display: flex; align-items: center; justify-content: center; background: #111; font-size: 38px; border-radius: 16px 16px 0 0; }
.menu-card-body { padding: 10px 8px 14px; }
.menu-card-name { font-weight: 600; font-size: 12px; color: #e8e2d9; line-height: 1.3; margin-bottom: 4px; }
.menu-card-price { font-family: 'Bebas Neue', sans-serif; font-size: 20px; color: #d4a017; }
.menu-card-bs { font-size: 10px; color: #666; }

.ticket { background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 16px; overflow: hidden; margin-top: 8px; }
.ticket-head { background: #222; padding: 14px 18px; border-bottom: 1px dashed #333; font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: #888; }
.ticket-item { display: flex; justify-content: space-between; padding: 9px 18px; border-bottom: 1px solid #1e1e1e; font-size: 13px; }
.ticket-total { background: #222; padding: 14px 18px; border-top: 2px dashed #d4a017; display: flex; justify-content: space-between; align-items: center; }
.cat-label { font-size: 10px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #555; margin: 20px 0 10px; }
hr { border-color: #2a2a2a; }
::-webkit-scrollbar { width: 4px; } ::-webkit-scrollbar-thumb { background: #333; border-radius: 999px; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# LEER TASA DESDE SUPABASE
# ============================================================
def leer_tasa():
    try:
        res = sb.table('configuracion').select('valor').eq('clave', 'tasa_dia').execute()
        if res.data:
            return float(res.data[0]['valor'])
    except:
        pass
    return 419.05

TASA = leer_tasa()


# ============================================================
# GUARDAR PEDIDO EN SUPABASE
# ============================================================
def guardar_pedido(pedido):
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
            'origen':       'cliente',
            'estado':       'pendiente',
        }).execute()
        return True
    except Exception as e:
        st.error(f"Error al enviar pedido: {e}")
        return False


# ============================================================
# CATÁLOGO
# ============================================================
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
DESCRIPCIONES = {
    'Perro Caliente Simple':'Pan + salchicha','Perro Jumbo':'Pan jumbo + salchicha',
    'Combo 6 Perros + 1.5L':'6 perros + refresco 1.5L','Combo Jumbos + 1.5L':'4 jumbos + refresco 1.5L',
    'Hamburguesa Especial':'Carne, huevo, jamón, queso','Hamburguesa Sencilla':'Carne, jamón, queso',
    'Medio Pollo Solo':'Pollo + arepitas + ensalada','Alitas x6':'6 alitas + papas + arepitas',
    'Combo Pollo + 1.5L':'Pollo + refresco + acompañantes','Combo Pollo+2Perros+1.5L':'Pollo + 2 perros + refresco',
    'Refresco 1.5L':'Bebida 1.5 litros',
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


# ============================================================
# ESTADO
# ============================================================
if 'carrito'        not in st.session_state: st.session_state.carrito        = []
if 'pedido_enviado' not in st.session_state: st.session_state.pedido_enviado = False
if 'key_reset'      not in st.session_state: st.session_state.key_reset      = 0


# ============================================================
# PANTALLA DE CONFIRMACIÓN
# ============================================================
if st.session_state.pedido_enviado:
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;">
        <div style="font-size:72px;">🎉</div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:40px;color:#d4a017;letter-spacing:3px;margin-top:16px;">¡PEDIDO RECIBIDO!</div>
        <div style="font-size:15px;color:#888;margin-top:10px;line-height:1.6;">
            Tu pedido ya está en cocina.<br>Te avisamos cuando esté listo. 🍽️
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🛒 Hacer otro pedido", type="primary"):
        st.session_state.pedido_enviado = False
        st.session_state.carrito        = []
        st.session_state.key_reset     += 1
        st.rerun()
    st.stop()


# ============================================================
# HERO
# ============================================================
st.markdown("""
<div style="text-align:center;padding:32px 0 20px;">
    <div style="font-family:'Bebas Neue',sans-serif;font-size:52px;letter-spacing:4px;color:#e8e2d9;line-height:1;">
        🦁 LIONZA <span style="color:#d4a017;">FOOD</span>
    </div>
    <div style="font-size:14px;color:#666;margin-top:6px;letter-spacing:1px;">Haz tu pedido · Lo preparamos al momento</div>
</div>
""", unsafe_allow_html=True)
st.divider()


# ============================================================
# DATOS DEL CLIENTE
# ============================================================
st.markdown('<div class="cat-label">Tus datos</div>', unsafe_allow_html=True)
col_n, col_h = st.columns(2)
with col_n:
    nombre = st.text_input("👤 Tu nombre", placeholder="Ej: María González", key=f"nombre_{st.session_state.key_reset}")
with col_h:
    hora_str = st.text_input("⏰ ¿Para qué hora?", placeholder="Ej: 07:30 PM",
                              value=datetime.now().strftime("%I:%M %p"),
                              key=f"hora_{st.session_state.key_reset}")

st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# MENÚ
# ============================================================
st.markdown('<div class="cat-label">Elige tus productos</div>', unsafe_allow_html=True)

for cat_name, productos in CATEGORIAS.items():
    st.markdown(f'<div class="cat-label" style="margin-top:18px;color:#555;">{cat_name}</div>', unsafe_allow_html=True)
    cols = st.columns(len(productos))
    for col, prod in zip(cols, productos):
        precio_usd = PRECIOS_BASE[prod]
        precio_bs  = precio_usd * TASA
        emoji      = EMOJIS[prod]
        desc       = DESCRIPCIONES[prod]
        with col:
            st.markdown(
                f'<div class="menu-card">'
                f'<div class="menu-card-emoji">{emoji}</div>'
                f'<div class="menu-card-body">'
                f'<div class="menu-card-name">{prod}</div>'
                f'<div style="font-size:10px;color:#666;margin-bottom:4px;">{desc}</div>'
                f'<div class="menu-card-price">${precio_usd:.2f}</div>'
                f'<div class="menu-card-bs">{precio_bs:.0f} Bs.</div>'
                f'</div></div>', unsafe_allow_html=True)
            if st.button("＋", key=f"add_{prod}_{st.session_state.key_reset}", use_container_width=True):
                p_usd  = calcular_precio(prod, 1)
                existe = False
                for item in st.session_state.carrito:
                    if item['Producto'] == prod:
                        nc = item['Cant']+1; item['Cant']=nc; item['USD']=calcular_precio(prod,nc); item['BS']=item['USD']*TASA; existe=True; break
                if not existe:
                    st.session_state.carrito.append({'Producto':prod,'Cant':1,'USD':p_usd,'BS':round(p_usd*TASA,2)})
                st.toast(f"✅ {prod} añadido", icon="🛒"); st.rerun()


# ============================================================
# CARRITO
# ============================================================
st.divider()
st.markdown('<div class="cat-label">Tu pedido</div>', unsafe_allow_html=True)

if not st.session_state.carrito:
    st.markdown('<div style="background:#141414;border:1px dashed #2a2a2a;border-radius:14px;padding:32px 20px;text-align:center;color:#444;"><div style="font-size:32px;">🛒</div><div style="font-size:13px;margin-top:8px;">Aún no has añadido nada</div></div>', unsafe_allow_html=True)
else:
    total_usd = sum(i['USD'] for i in st.session_state.carrito)
    total_bs  = total_usd * TASA

    items_html = "".join([
        f'<div class="ticket-item"><span>{i["Cant"]}× {i["Producto"]}</span>'
        f'<span style="color:#d4a017;font-family:Bebas Neue;font-size:15px;">${i["USD"]:.2f}</span></div>'
        for i in st.session_state.carrito
    ])
    st.markdown(
        f'<div class="ticket"><div class="ticket-head">Resumen de tu pedido</div>'
        + items_html +
        f'<div class="ticket-total"><span style="font-size:12px;color:#888;letter-spacing:1px;text-transform:uppercase;">Total</span>'
        f'<div><span style="font-family:Bebas Neue;font-size:28px;color:#d4a017;">${total_usd:.2f}</span>'
        f'<span style="font-size:11px;color:#666;margin-left:8px;">{total_bs:.0f} Bs.</span></div></div></div>',
        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    for idx, item in enumerate(st.session_state.carrito):
        c1, c2, c3 = st.columns([4,1,1])
        c1.markdown(f"**{item['Producto']}**")
        nueva_cant = c2.number_input("", min_value=1, max_value=20, value=item['Cant'],
                                      key=f"cant_{idx}_{st.session_state.key_reset}", label_visibility="collapsed")
        if nueva_cant != item['Cant']:
            item['Cant']=nueva_cant; item['USD']=calcular_precio(item['Producto'],nueva_cant); item['BS']=round(item['USD']*TASA,2); st.rerun()
        if c3.button("🗑", key=f"del_{idx}_{st.session_state.key_reset}"):
            st.session_state.carrito.pop(idx); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="cat-label">Método de pago</div>', unsafe_allow_html=True)
    metodo = st.radio("Pago:", ["💵 Efectivo $","📱 Pago Móvil","💸 Zelle","🏧 Efectivo Bs.","🔀 Mixto"],
                      horizontal=True, label_visibility="collapsed", key=f"metodo_{st.session_state.key_reset}")

    nota = st.text_input("📝 ¿Alguna indicación especial? (opcional)",
                          placeholder="Sin cebolla, extra queso...", key=f"nota_{st.session_state.key_reset}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔥 ENVIAR PEDIDO", type="primary", use_container_width=True):
        if not nombre.strip():
            st.warning("⚠️ Por favor escribe tu nombre antes de enviar.")
        else:
            pedido = {
                'Cliente':      nombre.strip(),
                'Detalle':      st.session_state.carrito.copy(),
                'Total_U':      round(total_usd, 2),
                'Total_B':      round(total_bs, 2),
                'Metodo':       metodo,
                'Hora_Reg':     datetime.now().strftime("%I:%M %p"),
                'Hora_Entrega': hora_str.strip().upper(),
                'Nota':         nota.strip(),
            }
            if guardar_pedido(pedido):
                st.session_state.pedido_enviado = True
                st.rerun()

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div style="text-align:center;font-size:11px;color:#333;">🦁 Lionza Food · Hecho con amor</div>', unsafe_allow_html=True)
