import streamlit as st
import random

# --- Configuração da Página ---
st.set_page_config(page_title="RPG - Apocalipse Zumbi no SESI", layout="wide")

# --- Páginas na Sidebar ---
pagina = st.sidebar.radio("Menu", ["Instruções", "Jogar", "Créditos"])

# --- Estado da Sessão ---
if "secao_atual" not in st.session_state:
    st.session_state["secao_atual"] = "inicio"

# --- Dicionário da História (versão expandida com derrotas e vitórias) ---
historia = {
    "inicio": {
        "titulo": "Acordando para o Caos",
        "texto": "Você chega na escola SESI e algo está errado. Os corredores estão vazios e há um cheiro estranho no ar. Do fundo do corredor, um grunhido arrepiante.\n\nO que você faz?",
        "opcoes": {
            "Investigar o som na sala de ciências": "sala_ciencias",
            "Correr para o pátio": "pátio",
            "Subir para a sala dos professores": "sala_professores"
        }
    },
    "sala_ciencias": {
        "titulo": "Professor zumbi",
        "texto": "Você entra na sala e vê o professor transformado em um zumbi! Ele se vira e vem em sua direção.",
        "opcoes": {
            "Usar tubo de ensaio para se defender": "luta",
            "Gritar por ajuda": "fim_derrota",
            "Fechar a porta e fugir": "corredor"
        }
    },
    "pátio": {
        "titulo": "Pátio Assombrado",
        "texto": "Você corre até o pátio e vê vários alunos zumbificados. Há uma árvore, um portão e a entrada da cantina.",
        "opcoes": {
            "Subir na árvore": "arvore",
            "Entrar na cantina": "cantina",
            "Tentar sair pelo portão": "portao"
        }
    },
    "sala_professores": {
        "titulo": "Sala dos Professores",
        "texto": "A sala está vazia. Mas há uma chave e um rádio velho sobre a mesa.",
        "opcoes": {
            "Pegar a chave": "chave",
            "Pegar o rádio": "radio",
            "Fugir dali": "corredor"
        }
    },
    "luta": {
        "titulo": "Confronto",
        "texto": "Você tenta enfrentar o professor zumbi. Jogue o dado para saber o resultado:",
        "opcoes": {}
    },
    "corredor": {
        "titulo": "Nos Corredores",
        "texto": "Você corre pelos corredores escuros. Há duas portas: uma leva ao laboratório e outra à biblioteca.",
        "opcoes": {
            "Entrar no laboratório": "laboratorio",
            "Entrar na biblioteca": "biblioteca",
            "Descer para o ginásio": "ginasio"
        }
    },
    "laboratorio": {
        "titulo": "Equipamento Improvisado",
        "texto": "Você encontra materiais de robótica. Pode tentar montar algo útil.",
        "opcoes": {}
    },
    "armario": {
        "titulo": "Armário Trancado",
        "texto": "Você está preso. Teste sua sorte para escapar.",
        "opcoes": {}
    },
    "biblioteca": {
        "titulo": "Refúgio Silencioso",
        "texto": "Você encontra alguns alunos escondidos. Eles bolam um plano de fuga pelo telhado.",
        "opcoes": {
            "Subir para o telhado": "telhado",
            "Procurar suprimentos": "suprimentos",
            "Voltar para o corredor": "corredor"
        }
    },
    "telhado": {
        "titulo": "No Alto",
        "texto": "Do telhado, você vê o caos na cidade. Um helicóptero se aproxima...",
        "opcoes": {
            "Acenar com pano branco": "resgate_final",
            "Descer para o estacionamento": "estacionamento",
            "Ficar observando": "fim_derrota"
        }
    },
    "resgate_final": {
        "titulo": "Você Sobreviveu!",
        "texto": "O helicóptero pousa e você escapa da escola. O mundo está em ruínas, mas você tem esperança.\n\n**FIM DE JOGO - VITÓRIA!**",
        "opcoes": {
            "Jogar novamente": "inicio"
        }
    },
    "fim_derrota": {
        "titulo": "Fim da Linha",
        "texto": "Você foi alcançado pelos zumbis. Sua jornada termina aqui.\n\n**FIM DE JOGO - DERROTA**",
        "opcoes": {
            "Tentar novamente": "inicio"
        }
    }
}

# --- Instruções ---
if pagina == "Instruções":
    st.title("🧟‍♂️ Apocalipse Zumbi no SESI - RPG Interativo")
    st.markdown("""
    **Bem-vindo ao RPG interativo do Apocalipse Zumbi na Escola SESI!**

    Neste jogo estilo *livro-jogo*, você será um estudante tentando sobreviver a um surto zumbi dentro da escola.

    - Leia cada situação com atenção.
    - Escolha entre 3 caminhos possíveis.
    - Em alguns momentos, sua sorte será testada!
    - Algumas decisões podem levar ao **fim da sua jornada**.

    🧠 Pense bem antes de agir. Boa sorte!
    """)

# --- Créditos ---
elif pagina == "Créditos":
    st.title("Créditos")
    st.markdown("""
    - História e programação: Sergio Campos & ChatGPT
    - Plataforma: Streamlit
    - Ilustrações: (adicionar imagens futuramente)
    - Licença: Livre para uso educacional
    """)

# --- Jogo ---
elif pagina == "Jogar":

    def mostrar_secao(secao_id):
        secao = historia[secao_id]
        st.header(secao["titulo"])
        st.write(secao["texto"])

        if secao_id == "laboratorio":
            if "sorte_lab" not in st.session_state:
                if st.button("Sortear equipamento útil"):
                    item = random.choice(["Drone espião", "Armadura de LEDs", "Nada funcional..."])
                    st.session_state["sorte_lab"] = item
                    if item == "Nada funcional...":
                        st.session_state["secao_atual"] = "fim_derrota"
                    else:
                        st.session_state["secao_atual"] = "biblioteca"
                    st.rerun()
            else:
                st.success(f"Você encontrou: {st.session_state['sorte_lab']}")

        elif secao_id == "luta":
            if st.button("Lançar dado (1 a 6)"):
                resultado = random.randint(1, 6)
                st.write(f"Você tirou: {resultado}")
                if resultado >= 4:
                    st.success("Você escapou da sala e corre pelos corredores!")
                    st.session_state["secao_atual"] = "corredor"
                else:
                    st.error("O professor zumbi te pegou!")
                    st.session_state["secao_atual"] = "fim_derrota"
                st.rerun()

        elif secao_id == "armario":
            if st.button("Testar sorte (1 a 6)"):
                resultado = random.randint(1, 6)
                st.write(f"Você tirou: {resultado}")
                if resultado >= 4:
                    st.success("Você forçou a porta e escapou com sucesso!")
                    st.session_state["secao_atual"] = "corredor"
                else:
                    st.error("A porta não abre! Você precisa tentar outro caminho.")
                    st.session_state["secao_atual"] = "fim_derrota"
                st.rerun()

        else:
            for opcao, destino in secao.get("opcoes", {}).items():
                if st.button(opcao):
                    st.session_state["secao_atual"] = destino
                    st.rerun()

    mostrar_secao(st.session_state["secao_atual"])
