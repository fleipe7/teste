import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches

st.set_page_config(page_title="Sorteio DIC", layout="centered")

st.title("🔢 Sorteio DIC - Experimentos")

# Etapa 1 - Nome do Experimento
experimento = st.text_input("Nome do Experimento")

# Etapa 2 - Número de Tratamentos
qtd_trat = st.number_input("Quantidade de Tratamentos", min_value=2, step=1)

# Etapa 3 - Nomes dos Tratamentos
nomes_tratamentos = []
for i in range(qtd_trat):
    nome = st.text_input(f"Nome do Tratamento {i+1}", key=f"trat{i}")
    nomes_tratamentos.append(nome)

# Etapa 4 - Número de Repetições
reps = st.number_input("Número de Repetições", min_value=1, step=1)

# Sorteio
if st.button("🎲 Sortear"):
    if not experimento or "" in nomes_tratamentos:
        st.error("Preencha todos os campos corretamente!")
    else:
        lista = nomes_tratamentos * reps
        random.shuffle(lista)

        # Monta a tabela transposta (tratamentos em colunas)
        df = pd.DataFrame({
            f"Repetição {i+1}": lista[i::reps] for i in range(reps)
        }).transpose()

        st.subheader(f"📋 Tabela de Sorteio - {experimento}")
        st.dataframe(df)

        # Gera cores únicas para os tratamentos
        cores = sns.color_palette("Set2", len(nomes_tratamentos))
        mapa_cores = {trat: cores[i] for i, trat in enumerate(nomes_tratamentos)}

        # Gráfico visual do sorteio
        st.subheader("🎨 Visualização do Sorteio")
        fig, ax = plt.subplots(figsize=(len(df.columns), len(df)*0.6 + 1))

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                trat = df.iloc[i, j]
                rect = plt.Rectangle((j, df.shape[0] - i - 1), 1, 1, facecolor=mapa_cores[trat], edgecolor='gray')
                ax.add_patch(rect)
                ax.text(j + 0.5, df.shape[0] - i - 0.5, trat, ha='center', va='center', fontsize=9)

        ax.set_xticks([x + 0.5 for x in range(df.shape[1])])
        ax.set_xticklabels(df.columns)
        ax.set_yticks([y + 0.5 for y in range(df.shape[0])])
        ax.set_yticklabels(df.index)
        ax.invert_yaxis()
        ax.axis("off")

        # Legenda
        patches = [mpatches.Patch(color=cor, label=trat) for trat, cor in mapa_cores.items()]
        ax.legend(handles=patches, bbox_to_anchor=(1.01, 1), loc='upper left', title="Tratamentos")

        st.pyplot(fig)
