from models import session, Usuario
import streamlit_authenticator as stauth

# Na versão atual, usa-se Hasher.hash() para uma única string
senha_criptografada = stauth.Hasher.hash("123456")

# Criando o objeto do banco de dados
usuario = Usuario(
    nome="Admin", 
    senha=senha_criptografada, 
    email="admin@gmail.com", 
    admin=True
)

session.add(usuario)
session.commit() # Lembre-se do commit para persistir no banco

print("Usuário Admin inserido com sucesso!")