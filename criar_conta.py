import streamlit as st
from models import session, Usuario
import streamlit_authenticator as stauth
import pandas as pd

def buscar_usuarios():
    usuarios = session.query(Usuario).all()
    df = pd.DataFrame([
    {"id": u.id, "nome": u.nome, "email": u.email, "Admin": u.admin, "Excluir": False} 
        for u in usuarios
    ])
    return df #df.drop(index=0,axis=1)

def monta_grid():
    larguras = [0.5, 2, 3, 1, 1]

    # 2. Cabeçalho
    cols_header = st.columns(larguras)
    cols_header[0].write("**ID**")
    cols_header[1].write("**Nome**")
    cols_header[2].write("**Email**")
    cols_header[3].write("**Admin**")
    cols_header[4].write("**Excluir?**")
    st.divider()

    # 3. Buscar e listar usuários
    usuarios = session.query(Usuario).all()

    for u in usuarios:
        cols = st.columns(larguras)
        
        cols[0].write(u.id)
        cols[1].write(u.nome)
        cols[2].write(u.email)
        
        # Exibe um ícone ou texto para o status de Admin
        status_admin = "✅ Sim" if u.admin else "❌ Não"
        cols[3].write(status_admin)
        if u.nome == "Admin":
        # Exibe um ícone de cadeado ou nada na coluna de ação
            cols[4].write("🔒") 
        else:
            # Botão de exclusão
            if cols[4].button("🗑️", key=f"btn_del_{u.id}"):
                try:
                    usuario_para_deletar = session.query(Usuario).get(u.id)
                    if usuario_para_deletar:
                        session.delete(usuario_para_deletar)
                        session.commit()
                        st.toast(f"Usuário {u.nome} removido.")
                        st.rerun()
                except Exception as e:
                    st.error(f"Erro ao excluir: {e}")

st.title("Criar Conta")

form = st.form("form_criar_conta")
nome_usuario = form.text_input("Nome do usuário")
email_usuario = form.text_input("Email do usuário")
senha_usuario = form.text_input("Senha do usuário", type="password")
admin_usuario = form.checkbox("É um admin?")
botao_submit = form.form_submit_button("Enviar")

# st.table(buscar_usuarios())

# 
monta_grid()
if botao_submit:
    lista_usuarios_existentes = session.query(Usuario).filter_by(email=email_usuario).all()
    if len(lista_usuarios_existentes) > 0:
        st.write("Já existe um usuário com esse email cadastrado")
    elif len(email_usuario) < 5 or len(senha_usuario) < 3:
        st.write("Preencha o campo de email e senha corretamente")
    else:
        senha_criptografada = senha_criptografada = stauth.Hasher.hash(senha_usuario) # stauth.Hasher([senha_usuario]).generate()[0]
        usuario = Usuario(nome=nome_usuario, senha=senha_criptografada, email=email_usuario, admin=admin_usuario)
        session.add(usuario)
        session.commit()
        st.rerun()
