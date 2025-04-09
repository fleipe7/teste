import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches
from datetime import datetime

# Tamanho fixo para todas as janelas
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

class DICApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorteio DIC - Experimentos")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg='#dcdcdc')  # Fundo cinza claro

        self.frame = tk.Frame(self.root, bg='#dcdcdc')
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.etapa = 0
        self.dados = {}

        self.avancar_etapa()

    def limpar_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def avancar_etapa(self):
        self.limpar_frame()

        if self.etapa == 0:
            self.etapa_nome_experimento()
        elif self.etapa == 1:
            self.etapa_qtd_tratamentos()
        elif self.etapa == 2:
            self.etapa_nomes_tratamentos()
        elif self.etapa == 3:
            self.etapa_repeticoes()
        elif self.etapa == 4:
            self.exibir_resultado()

    def etapa_nome_experimento(self):
        tk.Label(self.frame, text="Nome do Experimento:", bg='#dcdcdc').pack(pady=10)
        self.nome_entry = tk.Entry(self.frame)
        self.nome_entry.pack(pady=5)
        tk.Button(self.frame, text="Avançar", command=self.salvar_nome_experimento).pack(pady=10)

    def salvar_nome_experimento(self):
        nome = self.nome_entry.get().strip()
        if nome:
            self.dados['experimento'] = nome
            self.etapa += 1
            self.avancar_etapa()
        else:
            messagebox.showerror("Erro", "Digite um nome para o experimento.")

    def etapa_qtd_tratamentos(self):
        tk.Label(self.frame, text="Quantidade de Tratamentos:", bg='#dcdcdc').pack(pady=10)
        self.qtd_entry = tk.Entry(self.frame)
        self.qtd_entry.pack(pady=5)
        tk.Button(self.frame, text="Avançar", command=self.salvar_qtd_tratamentos).pack(pady=10)

    def salvar_qtd_tratamentos(self):
        try:
            qtd = int(self.qtd_entry.get())
            if qtd > 0:
                self.dados['qtd_tratamentos'] = qtd
                self.etapa += 1
                self.avancar_etapa()
        except:
            messagebox.showerror("Erro", "Digite um número válido.")

    def etapa_nomes_tratamentos(self):
        tk.Label(self.frame, text="Nomes dos Tratamentos:", bg='#dcdcdc').pack(pady=10)
        self.entradas_tratamentos = []
        for i in range(self.dados['qtd_tratamentos']):
            frame_linha = tk.Frame(self.frame, bg='#dcdcdc')
            frame_linha.pack()
            tk.Label(frame_linha, text=f"Tratamento {i+1}:", bg='#dcdcdc').pack(side=tk.LEFT)
            entrada = tk.Entry(frame_linha)
            entrada.pack(side=tk.LEFT, padx=5, pady=2)
            self.entradas_tratamentos.append(entrada)
        tk.Button(self.frame, text="Avançar", command=self.salvar_nomes_tratamentos).pack(pady=10)

    def salvar_nomes_tratamentos(self):
        nomes = [e.get().strip() for e in self.entradas_tratamentos]
        if all(nomes):
            self.dados['nomes_tratamentos'] = nomes
            self.etapa += 1
            self.avancar_etapa()
        else:
            messagebox.showerror("Erro", "Preencha todos os nomes de tratamento.")

    def etapa_repeticoes(self):
        tk.Label(self.frame, text="Número de Repetições:", bg='#dcdcdc').pack(pady=10)
        self.reps_entry = tk.Entry(self.frame)
        self.reps_entry.pack(pady=5)
        tk.Button(self.frame, text="Sortear", command=self.sortear).pack(pady=10)

    def sortear_dic(self):
        tratamentos = self.dados['nomes_tratamentos']
        repeticoes = self.dados['repeticoes']
        lista = tratamentos * repeticoes
        random.shuffle(lista)
        return lista

    def gerar_tabela(self, sorteio):
        tratamentos = self.dados['nomes_tratamentos']
        repeticoes = self.dados['repeticoes']
        colunas = [f'Rep {i+1}' for i in range(repeticoes)]
        linhas = [f'Trat {i+1}' for i in range(len(tratamentos))]
        tabela = []
        for i in range(len(tratamentos)):
            linha = []
            for j in range(repeticoes):
                linha.append(sorteio[i * repeticoes + j])
            tabela.append(linha)
        df = pd.DataFrame(tabela, index=linhas, columns=colunas)
        return df.transpose()

    def gerar_paleta(self):
        tratamentos = self.dados['nomes_tratamentos']
        cores = sns.color_palette("Set2", len(tratamentos))
        return {trat: cores[i] for i, trat in enumerate(tratamentos)}

    def sortear(self):
        try:
            repeticoes = int(self.reps_entry.get())
            self.dados['repeticoes'] = repeticoes
            self.dados['sorteio'] = self.sortear_dic()
            self.dados['tabela'] = self.gerar_tabela(self.dados['sorteio'])
            self.dados['cores'] = self.gerar_paleta()
            self.etapa += 1
            self.avancar_etapa()
        except:
            messagebox.showerror("Erro", "Digite um número válido de repetições.")

    def exibir_resultado(self):
        df = self.dados['tabela']
        cores = self.dados['cores']
        fig, ax = plt.subplots(figsize=(len(df.columns)*1.5, len(df)*0.6 + 2))
        ax.set_xlim(0, df.shape[1])
        ax.set_ylim(0, df.shape[0])

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                tratamento = df.iloc[i, j]
                cor = cores[tratamento]
                rect = plt.Rectangle((j + 0.1, df.shape[0] - i - 1 + 0.1), 0.8, 0.8, facecolor=cor, edgecolor='gray')
                ax.add_patch(rect)
                ax.text(j + 0.5, df.shape[0] - i - 0.5, tratamento, ha='center', va='center', fontsize=9)

        ax.set_xticks([x + 0.5 for x in range(df.shape[1])])
        ax.set_xticklabels(df.columns)
        ax.set_yticks([y + 0.5 for y in range(df.shape[0])])
        ax.set_yticklabels(df.index)

        ax.invert_yaxis()
        ax.set_title("Sorteio Experimental - DIC", fontsize=14)
        ax.axis("off")

        patches = [mpatches.Patch(color=cor, label=trat) for trat, cor in cores.items()]
        ax.legend(handles=patches, bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0., title="Tratamentos")

        fig.tight_layout()

        janela = tk.Toplevel(self.root)
        janela.title("Resultado do Sorteio")
        janela.protocol("WM_DELETE_WINDOW", lambda: None)  # Impede fechamento com o X

        canvas = FigureCanvasTkAgg(fig, master=janela)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        frame_btns = tk.Frame(janela, bg='#dcdcdc')
        frame_btns.pack(pady=10)

        tk.Button(frame_btns, text="Salvar PNG", command=self.salvar_png).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btns, text="Salvar PDF", command=self.salvar_pdf).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btns, text="Sortear Outro", command=lambda: [janela.destroy(), self.resetar()]).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btns, text="Fechar", command=janela.destroy).pack(side=tk.LEFT, padx=5)

    def salvar_png(self):
        fig = plt.gcf()
        caminho = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Imagem PNG", "*.png")])
        if caminho:
            fig.savefig(caminho)
            messagebox.showinfo("Salvo", f"Imagem salva em: {caminho}")

    def salvar_pdf(self):
        fig = plt.gcf()
        caminho = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Arquivo PDF", "*.pdf")])
        if caminho:
            fig.savefig(caminho)
            messagebox.showinfo("Salvo", f"PDF salvo em: {caminho}")

    def resetar(self):
        self.etapa = 0
        self.dados = {}
        self.avancar_etapa()

def main():
    root = tk.Tk()
    app = DICApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
