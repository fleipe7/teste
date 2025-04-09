import streamlit as st
import pandas as pd
import random
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Sorteio DIC", layout="wide")
st.title("🔀 Sorteio de Delineamento Inteiramente Casualizado (DIC)")

# Etapas do formulário
with st.form("dic_form"):
    nome_experimento = st.text_input("Nome do experimento")
    qtd_tratamentos = st.number_input("Número de tratamentos", min_value=2, step=1)
    nomes_tratamentos = []
    for i in range(qtd_tratamentos):
        nome = st.text_input(f"Nome do tratamento {i+1}", key=f"trat_{i}")
        nomes_tratamentos.append(nome)
    repeticoes = st.number_input("Número de repetições", min_value=2, step=1)
    sortear = st.form_submit_button("Sortear")

if sortear:
    if not nome_experimento or any([not n for n in nomes_tratamentos]):
        st.error("Preencha todos os campos antes de sortear.")
    else:
        lista = nomes_tratamentos * repeticoes
        random.shuffle(lista)

        # Montar tabela
        colunas = [f"Repetição {i+1}" for i in range(repeticoes)]
        linhas = [f"Parcela {i+1}" for i in range(len(nomes_tratamentos))]
        tabela = []
        for i in range(len(nomes_tratamentos)):
            linha = []
            for j in range(repeticoes):
                linha.append(lista[i * repeticoes + j])
            tabela.append(linha)

        df = pd.DataFrame(tabela, index=linhas, columns=colunas).transpose()

        st.subheader("📋 Tabela do Sorteio")
        st.dataframe(df, use_container_width=True)

        # Paleta de cores e gráfico
        paleta = sns.color_palette("Set2", len(nomes_tratamentos))
        cores = {trat: paleta[i] for i, trat in enumerate(nomes_tratamentos)}

        fig, ax = plt.subplots(figsize=(df.shape[1] * 1.5, df.shape[0]))
        ax.set_xlim(0, df.shape[1])
        ax.set_ylim(0, df.shape[0])

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                trat = df.iloc[i, j]
                cor = cores[trat]
                ax.add_patch(plt.Rectangle((j + 0.1, df.shape[0] - i - 1 + 0.1), 0.8, 0.8,
                                           facecolor=cor, edgecolor='gray'))
                ax.text(j + 0.5, df.shape[0] - i - 0.5, trat,
                        ha='center', va='center', fontsize=9)

        ax.set_xticks([x + 0.5 for x in range(df.shape[1])])
        ax.set_xticklabels(df.columns)
        ax.set_yticks([y + 0.5 for y in range(df.shape[0])])
        ax.set_yticklabels(df.index)
        ax.invert_yaxis()
        ax.axis("off")
        ax.set_title(f"{nome_experimento} - DIC", fontsize=14)
        fig.tight_layout()

        st.subheader("📊 Visualização Gráfica")
        st.pyplot(fig)

        # Exportar CSV
        st.subheader("💾 Exportar Resultados")
        csv = df.to_csv().encode('utf-8')
        st.download_button("⬇️ Baixar CSV", csv, f"{nome_experimento}_sorteio.csv", "text/csv")
