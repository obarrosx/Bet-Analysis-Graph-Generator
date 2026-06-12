import random
import math
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
 
 
def simular_apostador(num_apostas, chance_acerto, valor_aposta=10, ganho_se_acertar=10):
    saldo = 100
    historico = [saldo]
    for _ in range(num_apostas):
        if saldo > 0:
            if random.random() < chance_acerto:
                saldo += ganho_se_acertar
            else:
                saldo -= valor_aposta
        historico.append(saldo)
    return historico
 
 
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Apostas")
 
        self.historicos = []
 
        frame = ttk.Frame(root, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")
 
        ttk.Label(frame, text="Quantidade de apostadores:").grid(row=0, column=0, sticky="w")
        self.entry_apostadores = ttk.Entry(frame, width=10)
        self.entry_apostadores.insert(0, "5")
        self.entry_apostadores.grid(row=0, column=1, pady=2)
 
        ttk.Label(frame, text="Quantidade de apostas:").grid(row=1, column=0, sticky="w")
        self.entry_apostas = ttk.Entry(frame, width=10)
        self.entry_apostas.insert(0, "100")
        self.entry_apostas.grid(row=1, column=1, pady=2)
 
        ttk.Label(frame, text="Chance de acerto (0 a 1):").grid(row=2, column=0, sticky="w")
        self.entry_chance = ttk.Entry(frame, width=10)
        self.entry_chance.insert(0, "0.5")
        self.entry_chance.grid(row=2, column=1, pady=2)
 
        # Botoes
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
 
        ttk.Button(btn_frame, text="Refresh (gerar dados)", command=self.refresh).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Grafico Unico", command=self.grafico_unico).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Graficos Individuais", command=self.grafico_individual).grid(row=0, column=2, padx=5)
 
        self.status_label = ttk.Label(frame, text="", foreground="black")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=5)
 
    def refresh(self):
        try:
            num_apostadores = int(self.entry_apostadores.get())
            num_apostas = int(self.entry_apostas.get())
            chance = float(self.entry_chance.get())
 
            if num_apostadores <= 0 or num_apostas <= 0:
                raise ValueError
            if not (0 <= chance <= 1):
                raise ValueError
        except ValueError:
            self.status_label.config(text="Erro: verifique os valores digitados.", foreground="red")
            return
 
        self.historicos = [
            simular_apostador(num_apostas, chance)
            for _ in range(num_apostadores)
        ]
        self.status_label.config(text="Grafico gerado!", foreground="green")
 
    def grafico_unico(self):
        if not self.historicos:
            self.status_label.config(text="Erro: clique em Refresh primeiro.", foreground="red")
            return
 
        plt.figure(figsize=(10, 6))
        for i, historico in enumerate(self.historicos):
            plt.plot(historico, label=f"Apostador {i+1}")
 
        plt.title("Evolucao do saldo das apostas - Todos")
        plt.xlabel("Numero de apostas")
        plt.ylabel("Saldo acumulado")
        plt.axhline(100, color="gray", linestyle="--")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
 
    def grafico_individual(self):
        if not self.historicos:
            self.status_label.config(text="Erro: clique em Refresh primeiro.", foreground="red")
            return
 
        num_apostadores = len(self.historicos)
        cols = 2
        rows = math.ceil(num_apostadores / cols)
 
        fig, axs = plt.subplots(rows, cols, figsize=(5 * cols, 3 * rows))
        axs = axs.flatten() if num_apostadores > 1 else [axs]
 
        for i, historico in enumerate(self.historicos):
            saldo_final = historico[-1]
            if saldo_final > 100:
                cor = "green"
            elif saldo_final == 100:
                cor = "gold"
            else:
                cor = "red"
 
            axs[i].plot(historico, color=cor)
            axs[i].set_title(f"Apostador {i+1} (saldo final: {saldo_final})")
            axs[i].axhline(100, color="gray", linestyle="--")
            axs[i].grid(True)
 
        for j in range(num_apostadores, len(axs)):
            axs[j].axis("off")
 
        plt.tight_layout()
        plt.show()
 
 
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()