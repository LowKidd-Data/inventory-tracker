import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import requests

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Low Kidd AI Manager",
    page_icon="🎹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. FUNCIÓN DE SEGURIDAD (TELEGRAM) ---
def enviar_alerta_telegram(mensaje):
    """Envía alertas usando las claves guardadas en la Caja Fuerte de Streamlit"""
    try:
        # Buscamos las llaves en la configuración segura
        bot_token = st.secrets["TELEGRAM_TOKEN"]
        chat_id = st.secrets["TELEGRAM_CHAT_ID"]

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {"chat_id": chat_id, "text": mensaje}
        requests.post(url, data=data)
        return True
    except Exception as e:
        # Si no hay secretos configurados, no rompe la app, solo avisa en consola
        print(f"No se pudo enviar alerta: {e}")
        return False

# --- 3. CARGAR DATOS (Lectura del Excel) ---
@st.cache_data
def cargar_datos():
    archivo_excel = "LowKidd_Estrategia_Final.xlsx"
    try:
        df = pd.read_excel(archivo_excel)
        return df
    except FileNotFoundError:
        st.error(" Error Crítico: No se encontró el archivo 'LowKidd_Estrategia_Final.xlsx' en el repositorio.")
        return pd.DataFrame() # Retorna vacío para no romper todo

df = cargar_datos()

if df.empty:
    st.stop() # Detiene la app si no hay datos

# --- 4. BARRA LATERAL ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=80)
st.sidebar.title(" Manager AI")

vibra = st.sidebar.select_slider(
    "Vibra del Evento",
    options=["Chill", "Romántico", "Flow", "Fiesta", "Hardcore"]
)

# Botón de Pánico / Alerta
if st.sidebar.button(" Reportar Fallo"):
    exito = enviar_alerta_telegram(f"⚠️ Alerta: Alguien reportó un fallo en el Dashboard desde {vibra}")
    if exito:
        st.sidebar.success("Alerta enviada a tu celular.")
    else:
        st.sidebar.warning("Configura los 'Secrets' para activar esto.")

# --- 5. PANEL PRINCIPAL ---
st.title(" Low Kidd: Centro de Mando")

# Métricas
col1, col2, col3 = st.columns(3)
total_vistas = int(df['Vistas_Totales'].sum())
engagement = df['Engagement_Rate_%'].mean()

col1.metric("Impacto Total", f"{total_vistas:,} Vistas")
col2.metric("Engagement", f"{engagement:.2f}%")
col3.metric("Canciones Activas", len(df))

st.divider()

# Sección IA: Recomendación
st.subheader(f" Setlist Recomendado: Modo {vibra}")
filtro = df.copy()

# Lógica simple de filtro
if vibra in ["Fiesta", "Hardcore"]:
    filtro = df[df['IA_Contexto_Ideal'].str.contains("Fiesta|Energía|Discoteca", case=False, na=False)]
elif vibra in ["Romántico", "Chill"]:
    filtro = df[df['IA_Contexto_Ideal'].str.contains("Romántico|Sad|Viaje", case=False, na=False)]

st.dataframe(
    filtro[['Cancion_Buscada', 'Vistas_Totales', 'Engagement_Rate_%', 'IA_Contexto_Ideal']],
    use_container_width=True,
    hide_index=True
)

st.divider()

# Sección: Predicción Financiera (Corregida)
st.subheader(" Oráculo de Inversión")
presupuesto = st.slider("Presupuesto de Marketing (USD)", 500, 20000, 1000)

# Modelo Lineal Simple
X = np.array([100, 1000, 5000, 10000, 20000, 50000]).reshape(-1, 1)
y = np.array([5000, 60000, 350000, 800000, 1500000, 4000000]) # Datos simulados de entrenamiento

modelo = LinearRegression()
modelo.fit(X, y)
prediccion = modelo.predict([[presupuesto]])[0]

c1, c2 = st.columns(2)
c1.metric("Vistas Proyectadas", f"{int(prediccion):,}")
c2.metric("Retorno Estimado (ROI)", f"${(prediccion * 0.002):,.2f} USD")