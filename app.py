from openai import OpenAI
from msal import ConfidentialClientApplication
import streamlit as st
# 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

# Azure B2C Configuration
client_id = "f0b2ec2a-c5e3-4e2b-8317-4952ae23223e"
authority = "https://authcentauri.b2clogin.com/authcentauri.onmicrosoft.com/B2C_1_LOGIN"
redirect_uri = "http://localhost:8501"
client_secret = "QII8Q~WV5CbQcdYxUJE2f1OF7G22ID40~LvgNcXM"

app = ConfidentialClientApplication(client_id, client_secret, authority=authority)


# initialize session state
if not 'authenticated' in st.session_state:
    st.session_state['authenticated'] = False

if not 'messages' in st.session_state:
    st.session_state['messages'] = []

if not 'token' in st.session_state:
    st.session_state['token'] = None


# Frontend: Login Page
def login_page():
    st.title("Inicia sesión en 💬 Centauri Chat")
    if st.button("Login"):
        initiate_login_flow()

        # Function to start the login process
def initiate_login_flow():
    auth_url = app.get_authorization_request_url(scopes=[], redirect_uri=redirect_uri, response_type="code")
    st.session_state['auth_url'] = auth_url
    st.title("Inicia sesión en 💬 Centauri Chat")
    st.markdown(f"Por favor, [Haz clic aquí para iniciar sesión]({auth_url})")

# Function to handle the redirect callback
def handle_redirect():
    code = st.experimental_get_query_params().get('code')
    if code:
        code = code[0]  # Extract the authorization code
        result = app.acquire_token_by_authorization_code(code, scopes=[], redirect_uri=redirect_uri)
        print(result)

        if "id_token" in result:
            print("Authentication successful.", result['id_token'])
            st.session_state['authenticated'] = True
            st.session_state['token'] = result['id_token']
            st.title("💬 Centauri Chat")
            st.button("Empezar a chatear")
        else:
            print("Authentication failed.", result['id_token'])
            st.error("Authentication failed.")
            st.session_state['authenticated'] = False


if not 'authenticated' in st.session_state or not st.session_state['authenticated']:
    print("Not authenticated", st.session_state)
    code = st.experimental_get_query_params().get('code')
    if not code:
        initiate_login_flow()
    else:
        handle_redirect()
else:
    print("Authenticated", st.session_state)
    st.title("💬 Centauri Chat") 

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "¿Cómo te puedo ayudar?"}]

    for msg in st.session_state.messages:
        # pring msg
        print(msg)
        # if msg is dictionary 
        if isinstance(msg, dict):
            st.chat_message(msg["role"]).write(msg["content"])
        else:
            st.chat_message(msg.role).write(msg.content)

    prompt = st.chat_input("Escribe tu mensaje aquí...")
 

    if prompt:
        openai_api_key = "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"
        client = OpenAI(api_key=openai_api_key) 
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner('Espera un momento, estoy pensando 😅...'):
            response = client.chat.completions.create(model="gpt-4-1106-preview", messages=st.session_state.messages)
            msg = response.choices[0].message
            st.session_state.messages.append(msg)

        st.chat_message("assistant").write(msg.content)