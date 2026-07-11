import streamlit as st
import requests

BOT_TOKEN = st.secrets["8986604181:AAGz9DFyJPMu8HIdcGQFtos_wLSK_2PENs0"]
CHAT_ID = st.secrets["1699473564"]

def send_telegram(message):

    url = (
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    )

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )