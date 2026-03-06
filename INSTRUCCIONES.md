# 🦁 Lionza Food — Guía de despliegue

## Archivos del sistema

| Archivo                  | Para quién         | Descripción                              |
|--------------------------|--------------------|------------------------------------------|
| `lionza_food_pro_v4.py`  | Solo tú (admin)    | Panel completo: caja, cocina, almacén    |
| `menu_clientes.py`       | Tus clientes       | Menú público para hacer pedidos          |
| `pedidos_clientes.json`  | Automático         | Se crea solo, conecta ambas apps         |
| `inventario_lionza.csv`  | Automático         | Se crea solo, guarda el stock            |
| `tasa_dia.json`          | Automático         | Comparte la tasa BCV con el menú cliente |

---

## Paso a paso para publicarlo GRATIS en Streamlit Cloud

### 1. Crea una cuenta en GitHub (si no tienes)
→ https://github.com

### 2. Crea un repositorio nuevo
- Nombre: `lionza-food`
- Que sea **Public**
- Sube estos archivos:
  - `lionza_food_pro_v4.py`
  - `menu_clientes.py`
  - `requirements.txt` (ver abajo)

### 3. Crea el archivo requirements.txt
Crea un archivo llamado `requirements.txt` con este contenido:

```
streamlit
pandas
```

### 4. Ve a Streamlit Cloud
→ https://streamlit.io/cloud
- Inicia sesión con tu cuenta de GitHub
- Clic en **"New app"**

### 5. Despliega el menú de clientes primero
- Repository: `tu-usuario/lionza-food`
- Branch: `main`
- Main file path: `menu_clientes.py`
- Clic en **Deploy**
- Cuando termine, copia la URL — esa es la que le das a tus clientes
  Ejemplo: `https://lionza-menu.streamlit.app`

### 6. Despliega el panel admin
- Repite el proceso con `lionza_food_pro_v4.py`
- Esta URL es solo para ti, no la compartas
  Ejemplo: `https://lionza-admin.streamlit.app`

---

## ¿Cómo se conectan?

Ambas apps corren en el mismo servidor de Streamlit Cloud y comparten
el mismo directorio de archivos. Cuando un cliente envía un pedido:

1. `menu_clientes.py` escribe en `pedidos_clientes.json`
2. Tu panel admin lee ese archivo automáticamente cada vez que se recarga
3. El pedido aparece en tu pantalla de Cocina con el badge **ONLINE**
4. El inventario se descuenta igual que si lo hicieras tú

---

## ¿Cómo reciben los pedidos los clientes?

Cuando un cliente envía su pedido, ve una pantalla de confirmación.
No hay notificación por WhatsApp ni correo (eso requeriría un plan de pago).
La comunicación es: el cliente llega y pregunta, o lo llamas tú.

---

## Consejos

- **Tasa BCV**: la actualizas en tu panel admin y se refleja automáticamente
  en los precios que ven los clientes (se guarda en `tasa_dia.json`)
- **Comparte la URL del menú** por WhatsApp, Instagram o donde quieras
- **No compartas la URL del admin** — no tiene contraseña fuerte todavía
- Si quieres agregar contraseña al admin, dile a Claude que lo haga

---

## ¿Problemas?

Si las apps no se "ven" entre sí (pedidos no aparecen), es porque
Streamlit Cloud puede aislar las apps en servidores distintos.
En ese caso la solución es usar una base de datos compartida como
**Supabase** (gratis) — pídele a Claude que integre eso.
