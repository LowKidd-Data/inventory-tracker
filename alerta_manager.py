import streamlit as st
import requests

# -------------------------------------------
#  CONFIGURACIÓN SEGURA (LEER DESDE SECRETOS)
# -------------------------------------------
try:
    # Busca las claves en la nube de Streamlit
    BOT_TOKEN = st.secrets["TELEGRAM_TOKEN"]
    CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]
except FileNotFoundError:
    # Si estás en tu PC y no configuraste secretos locales, avisa
    print(" Error: No se encontraron las claves secretas.")
    BOT_TOKEN = "CLAVE_FALTANTE"
    CHAT_ID = "ID_FALTANTE"

def enviar_alerta(mensaje):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    datos = {"chat_id": CHAT_ID, "text": mensaje}
    try:
        requests.post(url, data=datos)
        print(" Alerta enviada a Telegram")
    except Exception as e:
        print(f" Error enviando alerta: {e}")

# Ejemplo de uso (solo para probar si se ejecuta directo)
if __name__ == "__main__":
    enviar_alerta(" El sistema de Low Kidd está activo en la nube.")