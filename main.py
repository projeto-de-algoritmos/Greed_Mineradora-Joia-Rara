import tkinter as tk
from tkinter import ttk
from PIL import Image

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


class BobConstrutorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Bob o Construtor")
        self.geometry("400x400")

        self.ferramentas = [
            {"nome": "Martelo", "imagem": "martelo.png"},
            {"nome": "Alicate", "imagem": "alicate.png"},
            {"nome": "Chave de Fenda", "imagem": "chave_fenda.png"},
            {"nome": "Fita Isolante", "imagem": "fita_isolante.png"},
            {"nome": "Trena", "imagem": "trena.png"},
            {"nome": "Furadeira", "imagem": "furadeira.png"},
            {"nome": "Broca", "imagem": "broca.png"},
            {"nome": "Chave Philips", "imagem": "chave_philips.png"},
            {"nome": "Lixa", "imagem": "lixa.png"},
            {"nome": "Chave de Teste", "imagem": "chave_teste.png"},
            {"nome": "Chave de Boca", "imagem": "chave_boca.png"},
            {"nome": "Chave Inglesa", "imagem": "chave_inglesa.png"}
        ]

        self.selected_tool = None
        self.peso_tool = 0
        self.caixa_ferramentas_selecionadas = []

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
        self.lbl_selected_tool_image.pack()

        self.lbl_peso_tool = ttk.Label(self, text="Peso da ferramenta:")
        self.lbl_peso_tool.pack()

        self.entry_peso_tool = ttk.Entry(self)
        self.entry_peso_tool.pack()

        self.btn_add_tool = ttk.Button(self, text="Adicionar ferramenta", command=self.add_tool)
        self.btn_add_tool.pack(pady=10)

        self.lbl_selected_tools = ttk.Label(self, text="Ferramentas selecionadas:")
        self.lbl_selected_tools.pack()

        self.listbox_selected_tools = tk.Listbox(self)
        self.listbox_selected_tools.pack(pady=5)

        self.btn_calculate = ttk.Button(self, text="Calcular", command=self.calculate_knapsack)
        self.btn_calculate.pack(pady=10)

    def select_tool(self, ferramenta):
        self.selected_tool = ferramenta
        img_path = ferramenta["imagem"]
        tool_image = Image.open(img_path)
        self.lbl_selected_tool_image.config(image=tool_image)
        self.lbl_selected_tool_image.image = tool_image

    def add_tool(self):
        if self.selected_tool is not None:
            peso = self.entry_peso_tool.get()
            if peso.isdigit():
                self.selected_tool["peso"] = int(peso)
                self.caixa_ferramentas_selecionadas.append(self.selected_tool)
                self.listbox_selected_tools.insert(tk.END, self.selected_tool["nome"])
                print(f"Ferramenta: {self.selected_tool['nome']}")
                print(f"Peso: {self.selected_tool['peso']}")
                print("Caixa de ferramentas selecionadas:", self.caixa_ferramentas_selecionadas)
            else:
                print("Peso inválido. Insira um valor numérico inteiro.")
        else:
            print("Nenhuma ferramenta selecionada.")

    def calculate_knapsack(self):
        capacidade_caixa = 50  # Capacidade da caixa de ferramentas
        ferramentas_selecionadas = knapsack_problem(self.caixa_ferramentas_selecionadas, capacidade_caixa)
        self.listbox_selected_tools.delete(0, tk.END)
        for ferramenta in ferramentas_selecionadas:
            self.listbox_selected_tools.insert(tk.END, ferramenta["nome"])

if __name__ == "__main__":
    app = BobConstrutorApp()
    app.mainloop()
