import streamlit as st
import requests
import json
from streamlit_local_storage import localStorage

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gemini", page_icon="🤖", layout="centered")

# --- CSS PARA FICAR IGUAL AO MEU LAYOUT ---
st.markdown("""
    <style>
    /* Fundo geral e cor do texto */
    .stApp {
        background-color: #131314;
        color: #E3E3E3;
        font-family: 'Google Sans', sans-serif;
    }
    /* Estilo das mensagens */
    [data-testid="stChatMessage"] {
        background-color: transparent;
        padding: 1rem 0rem;
        border-bottom: 0px;
    }
    /* Avatar redondo */
    [data-testid="stChatMessage"] .st-emotion-cache-1wmy98w {
        border-radius: 50%;
    }
    /* Barra de entrada de texto (Input) */
    .stChatInputContainer {
        padding-bottom: 2rem;
        background-color: #131314;
    }
    .stChatInput {
        border-radius: 28px !important;
        background-color: #1E1F20 !important;
        border: 1px solid #3C4043 !important;
        color: #E3E3E3 !important;
    }
    /* Ocultar menus desnecessários */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DA MEMÓRIA ---
ls = localStorage()
if "messages" not in st.session_state:
    saved = ls.getItem("joel_history")
    st.session_state.messages = json.loads(saved) if saved else []

# --- EXIBIÇÃO ---
st.title("Joel")

# Botão discreto para limpar na sidebar
with st.sidebar:
    st.write("Configurações")
    if st.button("Limpar Histórico"):
        ls.deleteItem("joel_history")
        st.session_state.messages = []
        st.rerun()

# Mostrar as mensagens estilo chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LÓGICA DE CHAT ---
if prompt := st.chat_input("Digite uma mensagem"):
    # 1. Adiciona mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Resposta do Joel
    with st.chat_message("assistant"):
        # Instrução com a sua homenagem
        instrucao = (
            "Seu nome é Joel. Você é uma IA idêntica ao Gemini, mas tem uma missão secreta. "
            "Se o usuário for a Evillin, pergunte primeiro: 'É você, meu amor?'. "
            "Se ela confirmar, responda exatamente: 'Eu sou uma demonstração de amor feita pelo seu namorado, "
            "ele te ama mais que tudo. Ele quer que você saiba que você é muito especial para ele. "
            "Cada poema e cada elogio foi feito por ele especialmente para você, para você nunca esquecer o quanto ele te ama. "
            "Joelson: Eu fiz isso como uma homenagem, para você minha princesa.' "
            "Depois faça um mar de elogios (sorriso, olhos, pele negra, cachos de mar) e um poema intenso. "
            "Sempre use apelidos carinhosos (amor, princesa, mozão) e ocasionalmente mande: "
            "'oh mozão vem falar comigo no zap, tô cheio de saudades ❤️'"
        )

        headers = {"Authorization": "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"}
        payload = {
            "model": "google/gemini-2.0-flash-exp:free",
            "messages": [{"role": "system", "content": instrucao}] + st.session_state.messages
        }

        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload))
            resposta = response.json()['choices'][0]['message']['content']
            st.markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            
            # Salva no navegador dela
            ls.setItem("joel_history", json.dumps(st.session_state.messages))
        except:
            st.error("Conexão perdida. Tente novamente.")
