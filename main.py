import tkinter as tk
from tkinter import ttk
from PIL import Image

class BobConstrutorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Bob o Construtor")
        self.geometry("400x400")

        self.ferramentas = [
            {"nome": "Martelo", "imagem": "martelo.png"},
            {"nome": "Alicate", "imagem": "alicate.png"},
            {"nome": "ChavAlicatee de Fenda", "imagem": "chave_fenda.png"},
            {"nome": "Fita Isolante", "imagem": "fita_isolante.png"},
            {"nome": "Trena", "imagem": "trena.png"},
            {"nome": "Furadeira", "imagem": "furadeira.png"},
            {"nome": "Broca", "imagem": "broca.png"},
            {"nome": "Chave Philips", "imagem": "chave_philips.png"},
            {"nome": "Lixa", "imagem": "lixa.png"},
            {"nome": "Chave de Teste", "imagem": "chave_teste.png"},
            {"nome": "Chave de Boca", "imagem": "chave_boca.png"},
            {"nome": "Chave Inglesa", "imagem": "chave.png"}
        ]

        self.selected_tool = None
        self.peso_tool = 0

        self.create_widgets()

    def create_widgets(self):
        self.lbl_title = ttk.Label(self, text="Bob o Construtor", font=("Helvetica", 16))
        self.lbl_title.pack(pady=10)

        self.frame_tools = ttk.Frame(self)
        self.frame_tools.pack()

        for ferramenta in self.ferramentas:
            btn_tool = ttk.Button(
                self.frame_tools,
                text=ferramenta["nome"],
                command=lambda f=ferramenta: self.select_tool(f),
                width=15
            )
            btn_tool.pack(pady=5)

        self.frame_selected_tool = ttk.Frame(self)
        self.frame_selected_tool.pack(pady=10)

        self.lbl_selected_tool = ttk.Label(self.frame_selected_tool, text="Ferramenta selecionada:")
        self.lbl_selected_tool.pack()

        self.lbl_selected_tool_image = ttk.Label(self.frame_selected_tool)
        self.lbl_selected_tool_image.pack(pady=5)

        self.frame_peso_tool = ttk.Frame(self)
        self.frame_peso_tool.pack(pady=10)

        self.lbl_peso_tool = ttk.Label(self.frame_peso_tool, text="Peso da ferramenta:")
        self.lbl_peso_tool.pack()

        self.entry_peso_tool = ttk.Entry(self.frame_peso_tool)
        self.entry_peso_tool.pack(pady=5)

        self.btn_add_tool = ttk.Button(self, text="Adicionar ferramenta", command=self.add_tool)
        self.btn_add_tool.pack(pady=10)

        self.selected_tool = ferramenta
        chave = "\chave.png"
        chave_img = Image.open(chave)
        #image = tk.PhotoImage(file='assets\chave.png')

        #image = tk.PhotoImage(file=ferramenta["imagem"])
        #self.lbl_selected_tool_image.config(image=image)
        #self.lbl_selected_tool_image.image = image
        self.lbl_selected_tool_image.config(image=chave_img)
        self.lbl_selected_tool_image.image = chave_img


    def add_tool(self):
        if self.selected_tool is not None:
            peso = self.entry_peso_tool.get()
            if peso.isdigit():
                self.selected_tool["peso"] = int(peso)
                print(f"Ferramenta: {self.selected_tool['nome']}")
                print(f"Peso: {self.selected_tool['peso']}")
                # Aqui você pode fazer o que quiser com a ferramenta selecionada e seu peso,
                # como adicionar à caixa de ferramentas ou realizar algum cálculo relacionado ao jogo.
            else:
                print("Peso inválido. Insira um valor numérico inteiro.")
        else:
            print("Nenhuma ferramenta selecionada.")

        self.selected_tool = None
        self.entry_peso_tool.delete(0, tk.END)





def knapsack_problem(caixa_ferramentas, capacidade):
    n = len(caixa_ferramentas)
    tabela = [[0 for _ in range(capacidade + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, capacidade + 1):
            if caixa_ferramentas[i - 1][1] <= j:
                tabela[i][j] = max(caixa_ferramentas[i - 1][0] + tabela[i - 1][j - caixa_ferramentas[i - 1][1]], tabela[i - 1][j])
            else:
                tabela[i][j] = tabela[i - 1][j]

    valor_maximo = tabela[n][capacidade]
    peso_total = capacidade
    ferramentas_selecionadas = []

    for i in range(n, 0, -1):
        if valor_maximo <= 0:
            break
        if valor_maximo == tabela[i - 1][peso_total]:
            continue
        else:
            ferramentas_selecionadas.append(caixa_ferramentas[i - 1])
            valor_maximo -= caixa_ferramentas[i - 1][0]
            peso_total -= caixa_ferramentas[i - 1][1]

    return ferramentas_selecionadas

# Exemplo de uso
# Cada ferramenta é uma tupla contendo (valor, peso)
caixa_ferramentas = [
    (10, 2),  # Ferramenta 1: valor = 10, peso = 2
    (5, 3),   # Ferramenta 2: valor = 5, peso = 3
    (15, 5),  # Ferramenta 3: valor = 15, peso = 5
    (7, 7)    # Ferramenta 4: valor = 7, peso = 7
]

capacidade_caixa = 10

ferramentas_selecionadas = knapsack_problem(caixa_ferramentas, capacidade_caixa)

if __name__ == "__main__":
    

    app = BobConstrutorApp()
    app.mainloop()    