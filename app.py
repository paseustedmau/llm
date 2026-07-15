"""Interfaz Streamlit para el sistema de atención al cliente Lumen Casa."""

from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, AuthenticationError, RateLimitError

from support import SupportAssistant


load_dotenv()

st.set_page_config(page_title="Lumen Casa · Soporte", page_icon="☀️", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Fraunces:opsz,wght@9..144,600;9..144,750&display=swap');
    :root { --ink:#25231f; --paper:#f4efe5; --orange:#e85d2a; --sage:#6f8064; }
    .stApp { background: var(--paper); color: var(--ink); }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] { background:#25231f; color:#f4efe5; border-right:0; }
    [data-testid="stSidebar"] * { color:#f4efe5; }
    h1,h2,h3 { font-family:'Fraunces',Georgia,serif !important; letter-spacing:-.025em; }
    p,button,input,textarea { font-family:'DM Mono',monospace !important; }
    .hero { border-top:4px solid var(--ink); border-bottom:1px solid var(--ink); padding:1.2rem 0 1.6rem; margin-bottom:1.5rem; }
    .eyebrow { color:var(--orange); font:500 .78rem 'DM Mono'; letter-spacing:.14em; text-transform:uppercase; }
    .hero h1 { font-size:clamp(2.8rem,7vw,6.7rem); line-height:.84; margin:.35rem 0 1rem; max-width:900px; }
    .hero-copy { max-width:650px; font-size:.92rem; line-height:1.7; }
    .status { display:inline-block; border:1px solid var(--sage); color:#40513a; padding:.35rem .65rem; font:500 .72rem 'DM Mono'; text-transform:uppercase; }
    [data-testid="stChatMessage"] {
      width:min(78%, 760px);
      padding:1rem 1.2rem;
      margin:0 0 1.15rem 0;
      border-radius:18px 18px 18px 4px;
      border:1px solid #cfc5b5;
      background:#fffaf0;
      box-shadow:4px 4px 0 #25231f;
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] strong,
    [data-testid="stChatMessage"] em,
    [data-testid="stChatMessage"] code {
      color:#25231f !important;
      -webkit-text-fill-color:#25231f !important;
      opacity:1 !important;
    }
    [data-testid="stChatMessage"] p { line-height:1.65; }
    [data-testid="stChatMessage"] a { color:#a33c18 !important; }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
      margin-left:auto;
      margin-right:0;
      border-color:#b4411d;
      border-radius:18px 18px 4px 18px;
      background:#d95224;
      box-shadow:4px 4px 0 #7c2a10;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p,
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) li,
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) span,
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) strong,
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) em,
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) code {
      color:#fffaf0 !important;
      -webkit-text-fill-color:#fffaf0 !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
      margin-left:0;
      margin-right:auto;
    }
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"] {
      background:#25231f !important;
      border:1px solid #25231f;
    }
    .tool-note { border-left:3px solid var(--orange); padding:.5rem .8rem; margin:.5rem 0; color:#665d50; font:400 .75rem 'DM Mono'; }
    .demo-card { border:1px solid #d8d0c1; padding:1rem; margin:.8rem 0; background:#faf7f0; }
    .stButton button { border-radius:0; border:1px solid #f4efe5; background:transparent; }
    .stButton button:hover { color:#25231f !important; background:#f4efe5; border-color:#f4efe5; }
    [data-testid="stChatInput"] {
      border-radius:0;
      border:1px solid #e85d2a;
      background:#25231f;
      box-shadow:4px 4px 0 #e85d2a;
    }
    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] textarea:focus {
      color:#fffaf0 !important;
      -webkit-text-fill-color:#fffaf0 !important;
      caret-color:#ffbd73 !important;
      background:#25231f !important;
      font-weight:500 !important;
      opacity:1 !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
      color:#c9bda9 !important;
      -webkit-text-fill-color:#c9bda9 !important;
      opacity:1 !important;
    }
    [data-testid="stChatInput"] button {
      background:#e85d2a !important;
      color:#fffaf0 !important;
      border-radius:0 !important;
    }
    [data-testid="stChatInput"] button:hover { background:#ff7a45 !important; }
    @media (max-width:700px) {
      [data-testid="stChatMessage"] { width:92%; padding:.85rem 1rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def reset_chat() -> None:
    st.session_state.messages = []
    st.session_state.previous_response_id = None


if "messages" not in st.session_state:
    reset_chat()

with st.sidebar:
    st.markdown("## LUMEN / SOPORTE")
    st.caption("Demostración académica · datos ficticios")
    st.divider()
    api_key = os.getenv("OPENAI_API_KEY") or st.text_input(
        "OpenAI API key", type="password", help="No se guarda ni se muestra en pantalla."
    )
    model = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
    st.caption(f"Modelo: {model}")
    st.divider()
    st.markdown("**Pedidos de prueba**")
    st.code("LUM-1042\nLUM-2088\nLUM-3301", language=None)
    st.markdown("**También puedes preguntar por**")
    st.caption("Envíos · devoluciones · garantía · pagos · atención humana")
    st.divider()
    if st.button("Nueva conversación", use_container_width=True):
        reset_chat()
        st.rerun()

st.markdown(
    """
    <section class="hero">
      <div class="eyebrow">Atención clara, sin vueltas</div>
      <h1>Hola, soy Sol.</h1>
      <p class="hero-copy">Te ayudo a rastrear un pedido, entender una política o pasar tu caso a una persona. Sin formularios eternos.</p>
      <span class="status">● disponible ahora</span>
    </section>
    """,
    unsafe_allow_html=True,
)

if not st.session_state.messages:
    st.info("Prueba: “¿Dónde está mi pedido LUM-1042?” o “Quiero devolver un producto”.")

for item in st.session_state.messages:
    with st.chat_message(item["role"], avatar="☀️" if item["role"] == "assistant" else "👤"):
        st.markdown(item["content"])
        for event in item.get("events", []):
            st.markdown(f'<div class="tool-note">↳ {event}</div>', unsafe_allow_html=True)

prompt = st.chat_input("Escribe tu consulta…", disabled=not bool(api_key))
if not api_key:
    st.warning("Agrega tu OPENAI_API_KEY en el archivo .env o en la barra lateral para comenzar.")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="☀️"):
        try:
            with st.spinner("Sol está revisando tu caso…"):
                assistant = SupportAssistant(api_key=api_key, model=model)
                reply = assistant.reply(prompt, st.session_state.previous_response_id)
            st.markdown(reply.text)
            labels = {
                "lookup_order": "Consultando base de datos de pedidos",
                "search_policy": "Consultando base de conocimiento",
                "create_support_ticket": "Creando ticket para atención humana",
            }
            event_texts = [labels.get(event.name, event.name) for event in reply.events]
            for text in event_texts:
                st.markdown(f'<div class="tool-note">↳ {text}</div>', unsafe_allow_html=True)
            st.session_state.messages.append(
                {"role": "assistant", "content": reply.text, "events": event_texts}
            )
            st.session_state.previous_response_id = reply.response_id
        except AuthenticationError:
            st.error("La API key no es válida. Revísala e intenta de nuevo.")
        except RateLimitError:
            st.error("Se alcanzó el límite temporal de la API. Espera un momento e intenta de nuevo.")
        except APIConnectionError:
            st.error("No fue posible conectar con OpenAI. Revisa tu conexión a internet.")
        except APIStatusError as exc:
            st.error(f"OpenAI devolvió un error ({exc.status_code}). Intenta nuevamente.")
        except Exception:
            st.error("Ocurrió un error inesperado. Inicia una nueva conversación e intenta de nuevo.")
