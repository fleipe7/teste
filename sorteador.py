import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import io
from datetime import datetime

st.set_page_config(page_title="Sorteio DIC", layout="centered")
st.title("🎲 Sorteio Experimental - DIC")

st.markdown("Preencha os dados abaixo para realizar o sorteio.")

with st.form("formulario"):
    nome_exp = st.text_input("Nome do experimento")
    num_trat = st.number_input("Quantidade de tratamentos", min_value=2, max_value=20, step=1)
    nomes = []
    for i in range(num_trat):
        nomes.append(st.text_input(f"Nome do Tratamento {i+1}", key=f"trat_{i}"))
    repeticoes = st.number_input("Número de repetições", min_value=2, max_value=20, step=1)
    submitted = st.form_submit_button("Sortear")

if submitted:
    if not nome_exp.strip():
        st.error("Digite um nome para o experimento.")
    elif any(not nome.strip() for nome in nomes):
        st.error("Preencha todos os nomes de tratamentos.")
    else:
        tratamentos = nomes
        lista = tratamentos * int(repeticoes)
        random.shuffle(lista)

        # Criar tabela
        colunas = [f"Rep {i+1}" for i in range(int(repeticoes))]
        linhas = [f"Trat {i+1}" for i in range(len(tratamentos))]
        tabela = []
        for i in range(len(tratamentos)):
            linha = []
            for j in range(int(repeticoes)):
                linha.append(lista[i * int(repeticoes) + j])
            tabela.append(linha)
        df = pd.DataFrame(tabela, index=linhas, columns=colunas).transpose()

        st.subheader("🔢 Tabela do Sorteio")
        st.dataframe(df)

        st.subheader("🎨 Visualização do Sorteio")
        cores = sns.color_palette("Set2", len(tratamentos))
        cor_dict = {trat: cores[i] for i, trat in enumerate(tratamentos)}

        fig, ax = plt.subplots(figsize=(len(df.columns)*1.5, len(df)*0.6 + 2))
        ax.set_xlim(0, df.shape[1])
        ax.set_ylim(0, df.shape[0])

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                trat = df.iloc[i, j]
                cor = cor_dict[trat]
                ax.add_patch(plt.Rectangle((j + 0.1, df.shape[0] - i - 1 + 0.1), 0.8, 0.8,
                                           facecolor=cor, edgecolor='gray'))
                ax.text(j + 0.5, df.shape[0] - i - 0.5, trat, ha='center', va='center', fontsize=8)

        ax.set_xticks([x + 0.5 for x in range(df.shape[1])])
        ax.set_xticklabels(df.columns)
        ax.set_yticks([y + 0.5 for y in range(df.shape[0])])
        ax.set_yticklabels(df.index)

        ax.invert_yaxis()
        ax.set_title(f"Sorteio - {nome_exp}", fontsize=14)
        ax.axis("off")

        legendas = [plt.Line2D([0], [0], marker='s', color='w', label=trat,
                               markerfacecolor=cor_dict[trat], markersize=10) for trat in tratamentos]
        ax.legend(handles=legendas, bbox_to_anchor=(1.01, 1), loc='upper left', title="Tratamentos")

        st.pyplot(fig)

        # Exportar imagem
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight')
        st.download_button("📥 Baixar PNG", data=buffer.getvalue(), file_name=f"{nome_exp}_sorteio.png", mime="image/png")

        # Exportar PDF
        pdf_buffer = io.BytesIO()
        fig.savefig(pdf_buffer, format='pdf', bbox_inches='tight')
        st.download_button("📥 Baixar PDF", data=pdf_buffer.getvalue(), file_name=f"{nome_exp}_sorteio.pdf", mime="application/pdf")
