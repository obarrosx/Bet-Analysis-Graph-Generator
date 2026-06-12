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

        num_apostas = len(self.historicos[0]) - 1

        plt.figure(figsize=(10, 6))

        # Pontos: saldo de cada apostador em cada aposta
        for historico in self.historicos:
            plt.scatter(range(len(historico)), historico, color="gray", alpha=0.4, s=15)

        # Linha da media entre todos os apostadores
        media = [
            sum(h[i] for h in self.historicos) / len(self.historicos)
            for i in range(num_apostas + 1)
        ]
        plt.plot(media, color="blue", linewidth=2, label="Media")

        plt.title("Evolucao do saldo das apostas - Todos")
        plt.xlabel("Numero de apostas")
        plt.ylabel("Saldo acumulado")
        plt.axhline(100, color="gray", linestyle="--")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def grafico_individual(self):
        if not self.historicos:
            self.status_label.config(text="Erro: clique em Refresh primeiro.", foreground="red")
            return

        from matplotlib.backends.backend_agg import FigureCanvasAgg
        from PIL import Image, ImageTk
        import io

        num_apostadores = len(self.historicos)
        cols = 3
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

        # Renderiza a figura como imagem (PNG) em memoria
        buf = io.BytesIO()
        FigureCanvasAgg(fig).print_png(buf)
        plt.close(fig)
        buf.seek(0)
        img = Image.open(buf)

        # Janela com scroll
        win = tk.Toplevel(self.root)
        win.title("Graficos Individuais")
        win.geometry("800x600")

        canvas_frame = tk.Frame(win)
        canvas_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        scroll_canvas = tk.Canvas(canvas_frame, yscrollcommand=scrollbar.set)
        scroll_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=scroll_canvas.yview)

        photo = ImageTk.PhotoImage(img)
        self._img_ref = photo  # evita garbage collection

        scroll_canvas.create_image(0, 0, image=photo, anchor="nw")
        scroll_canvas.config(scrollregion=(0, 0, img.width, img.height))

        def on_scroll(event):
            scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        scroll_canvas.bind_all("<MouseWheel>", on_scroll)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()