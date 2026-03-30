import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from models import session, Usuario

import streamlit as st

# Configuração da página (opcional para mudar o título na aba do navegador)
# st.set_page_config(page_title="Meu App Limpo", layout="wide")




##########################
# codigo para buscar os usuarios de um arquivo yaml e montando a Credentials
# comentado pois vai passar a pegar do banco de dados que foi criado
###########################
# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)
# stauth.Hasher.hash_passwords(config['credentials'])
# credenciais = config['credentials']

###########################
# Pegando agora os usurios do banco de dados
# montaremos a Credential pelo cadastro de usuarios do bd
###########################
lista_usuarios_db = session.query(Usuario).all()
credenciais = {'usernames': {}}
for usuario in lista_usuarios_db:
    credenciais['usernames'][usuario.email] = {  # ou u.username, se tiver esse campo
        'name': usuario.nome,
        'password': usuario.senha,  # Aqui deve estar o hash que você salvou
        'email': usuario.email
    }


authenticator = stauth.Authenticate(credenciais, "cookie_app_empresarial_python","abc123!@#zxc", cookie_expiry_days=10)





def logout():
    authenticator.logout()

def autenticar_usuario():
    # autenticar o usuario
    authenticator.login()

    # 2. Verifique o status usando o session_state
    if st.session_state["authentication_status"]:
        # authenticator.logout('Logout', 'main')

        return {"nome":st.session_state["name"],
                "status":st.session_state["authentication_status"],
                "email":st.session_state["username"]}
    elif st.session_state["authentication_status"] is False:
        st.error('Usuário/Senha incorretos')
        
    elif st.session_state["authentication_status"] is None:
        st.warning('Por favor, insira seu usuário e senha')

st.set_page_config(
    page_title="Consultoria & Soluções",  # Título da aba do navegador
    page_icon="📊",  # Pode ser um emoji ou o caminho para um arquivo .png/.ico
    layout="wide"    # Opcional: define se o app ocupa a tela toda
)


import streamlit as st

# Configuração para garantir que o menu comece aberto e o layout seja limpo
st.set_page_config(
    page_title="Consultoria & Soluções", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

style = """
    <style>
    /* 1. Esconde APENAS o botão de 'Deploy' e a barra colorida, mas mantém o botão do menu */
    .stAppDeployButton {display:none;}
    
    /* 2. Esconde o rodapé 'Made with Streamlit' */
    footer {visibility: hidden;}

    /* 3. Remove a margem superior excessiva para o app subir e ocupar o topo */
    .block-container {padding-top: 2rem;}

    /* 4. Opcional: Se quiser esconder o menu de 3 pontinhos (configurações) 
       mas manter o botão de abrir/fechar a barra lateral: */
    #MainMenu {visibility: hidden;}
    </style>
    """
st.markdown(style, unsafe_allow_html=True)

# Teste de conteúdo
#st.title("Agora o botão de voltar deve aparecer!")

# dados_usuario = autenticar_usuario()

dados_usuario = {"nome":"Admin","status":"","email":"admin@gmail.com"}
if dados_usuario:

    
    usuario = session.query(Usuario).filter_by(email=dados_usuario["email"]).first()
    #print(usuario.email,usuario.admin)
    if usuario.admin:
        pg = st.navigation(
            {
            "Home": [
                st.Page("homepage.py", title="Consultoria & Soluções")
                ],
            "Dashboards": [
                st.Page("dashboard.py", title="Dashboard"), 
                st.Page("indicadores.py", title="Indicadores")
                ],
            "Conta": [
                st.Page("criar_conta.py", title="Criar Conta"),
                #st.Page(logout, title="Sair")
                
                ]
            }
        )
    else:
        pg = st.navigation(
            {
            "Home": [
                st.Page("homepage.py", title="IA & Solucoes")
                ],
            "Dashboards": [
                st.Page("dashboard.py", title="Dashboard"), 
                st.Page("indicadores.py", title="Indicadores")
                ],
            "Conta": [ 
                st.Page("somente_consulta_contas.py", title="Criar Conta"),
                st.Page(logout, title="Sair")
                ]
            }
        )
    pg.run()
