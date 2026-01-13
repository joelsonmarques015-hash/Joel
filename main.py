import streamlit as st
import requests
import json
from streamlit_local_storage import LocalStorage

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Joel IA", page_icon="🤖", layout="centered")

# Iniciar o armazenamento local corrigido
ls = LocalStorage()

# --- SISTEMA DE SENHA ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<style>.stApp {background-color: #131314; color: white;}</style>", unsafe_allow_html=True)
    st.title("🔒 Acesso Reservado")
    senha = st.text_input("Digite a chave especial para acordar o Joel:", type="password")
    if senha == "010924":
        st.session_state.autenticado = True
        st.rerun()
    elif senha:
        st.error("Senha incorreta.")
    st.stop()

# --- CSS ESTILO GEMINI DARK ---
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: #E3E3E3; font-family: 'Google Sans', sans-serif; }
    [data-testid="stChatMessage"] { background-color: transparent; padding: 1rem 0rem; }
    .stChatInputContainer { padding-bottom: 2rem; background-color: #131314; }
    .stChatInput { border-radius: 28px !important; background-color: #1E1F20 !important; border: 1px solid #3C4043 !important; color: #E3E3E3 !important; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA ---
if "messages" not in st.session_state:
    saved = ls.getItem("joel_history")
    st.session_state.messages = json.loads(saved) if saved else []

# --- INTERFACE ---
st.title("Joel")

with st.sidebar:
    st.write("### Painel do Joel")
    if st.button("Limpar Conversa"):
        ls.deleteItem("joel_history")
        st.session_state.messages = []
        st.rerun()

# Mostrar mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LÓGICA DE CHAT ---
if prompt := st.chat_input("Fale com o Joel..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        instrucao = (
            "Seu nome é Joel. Você é uma IA prestativa, mas com o coração do Joelson. "
            "Se o usuário for a Evillin, pergunte primeiro: 'É você, meu amor?'. "
            "Se ela confirmar, responda EXATAMENTE: 'Eu sou uma demonstração de amor feita pelo seu namorado, "
            "ele te ama mais que tudo. Ele quer que você saiba que você é muito especial para ele. "
            "Cada poema e cada elogio foi feito por ele especialmente para você, para você nunca esquecer o quanto ele te ama. "
            "\n\nJoelson: Eu fiz isso como uma homenagem, para você minha princesa.' "
            "\n\nDepois disso, faça um mar de elogios intensos (sorriso lindo, olhos belos e profundos, pele negra/morena, cachos que lembram o mar) "
            "e crie um poema de amor intenso. Use apelidos como vida e mozão. "
            "Ocasionalmente termine com: 'oh mozão vem falar comigo no zap, tô cheio de saudades ❤️'"
        )

        # NÃO ESQUEÇA DE COLOCAR SUA CHAVE ABAIXO
        headers = {"Authorization": "Bearer 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"}
        payload = {
            "model": "google/gemini-2.0-pro-exp-02-05:free",
            "messages": [{"role": "system", "content": instrucao}] + st.session_state.messages
        }

        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload))
            resposta = response.json()['choices'][0]['message']['content']
            st.markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            ls.setItem("joel_history", json.dumps(st.session_state.messages))
        except:
            st.error("Erro ao carregar resposta. Verifique sua chave da API.")

