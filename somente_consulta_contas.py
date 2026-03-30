import streamlit as st
from models import session, Usuario
import streamlit_authenticator as stauth

def buscar_usuarios():
    usuarios = session.query(Usuario).all()
    dados_tabela = [ {"ID": u.id, "Nome": u.nome, "Email": u.email, "Admin": u.admin} 
                    for u in usuarios ]
    return dados_tabela


st.title("Criar Conta - (Somente admins)")

st.table(buscar_usuarios())