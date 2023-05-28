import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def knapsack_problem(caminhao, capacidade):
    n = len(caminhao)
    tabela = [[0 for _ in range(capacidade + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, capacidade + 1):
            if caminhao[i - 1][1] <= j:
                tabela[i][j] = max(caminhao[i - 1][0] + tabela[i - 1][j - caminhao[i - 1][1]], tabela[i - 1][j])
            else:
                tabela[i][j] = tabela[i - 1][j]

    valor_maximo = tabela[n][capacidade]
    peso_total = capacidade
    minerios_selecionados = []

    for i in range(n, 0, -1):
        if valor_maximo <= 0:
            break
        if valor_maximo == tabela[i - 1][peso_total]:
            continue
        else:
            minerios_selecionados.append(caminhao[i - 1])
            valor_maximo -= caminhao[i - 1][0]
            peso_total -= caminhao[i - 1][1]

    return minerios_selecionados

class MineradoraJoiaRaraApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Mineradora Joia Rara")
        self.geometry("800x800")

        self.minerios = [
            {"nome": "Ouro"},
            {"nome": "Prata"},
            {"nome": "Cobre"},
            {"nome": "Ferro"},
            {"nome": "Chumbo"   },
        ]

        self.selected_tool = None
        self.peso_tool = 0
        self.minerios_selecionados = []

        self.create_widgets()

    def create_widgets(self):
        self.lbl_title = ttk.Label(self, text="Mineradora Joia Rara", font=("Helvetica", 16))
        self.lbl_title.pack(pady=10)

        self.frame_tools = ttk.Frame(self)
        self.frame_tools.pack()

        for minerio in self.minerios:
            btn_tool = ttk.Button(
                self.frame_tools,
                text=minerio["nome"],
                command=lambda f=minerio: self.select_tool(f),
                width=15
            )
            btn_tool.pack(pady=5)

        self.frame_selected_tool = ttk.Frame(self)
        self.frame_selected_tool.pack(pady=10)

        self.lbl_selected_tool = ttk.Label(self.frame_selected_tool, text="Minerio selecionado:")
        self.lbl_selected_tool.pack()

        self.lbl_selected_tool_image = ttk.Label(self.frame_selected_tool)
        self.lbl_selected_tool_image.pack()

        self.lbl_peso_tool = ttk.Label(self, text="Peso do minerio:")
        self.lbl_peso_tool.pack()

        self.entry_peso_tool = ttk.Entry(self)
        self.entry_peso_tool.pack()

        self.btn_add_tool = ttk.Button(self, text="Adicionar minerio", command=self.add_tool)
        self.btn_add_tool.pack(pady=10)

        self.lbl_selected_tools = ttk.Label(self, text="Minerios selecionados:")
        self.lbl_selected_tools.pack()

        self.listbox_selected_tools = tk.Listbox(self)
        self.listbox_selected_tools.pack(pady=5)

        self.btn_calculate = ttk.Button(self, text="Calcular", command=self.calculate_knapsack)
        self.btn_calculate.pack(pady=10)

    def select_tool(self, minerio):
        self.selected_tool = minerio
        #img_path = minerio["imagem"]
        #tool_image = Image.open(img_path)
        #self.lbl_selected_tool_image.config(image=tool_image)
        #self.lbl_selected_tool_image.image = tool_image

    def add_tool(self):
        if self.selected_tool is not None:
            peso = self.entry_peso_tool.get()
            if peso.isdigit():
                self.selected_tool["peso"] = int(peso)
                self.minerios_selecionados.append(self.selected_tool)
                self.listbox_selected_tools.insert(tk.END, self.selected_tool["nome"])
                print(f"Minerio: {self.selected_tool['nome']}")
                print(f"Peso: {self.selected_tool['peso']}")
                print("Minerios selecionados:", self.minerios_selecionados)
            else:
                print("Peso inválido. Insira um valor numérico inteiro.")
        else:
             messagebox.showinfo(" ", "Nenhum minerio cadastratado!")

    def calculate_knapsack(self):
        capacidade_caminhao = 500  # Capacidade do caminhao
        minerios_selecionados = knapsack_problem(self.minerios_selecionados, capacidade_caminhao)
        self.listbox_selected_tools.delete(0, tk.END)
        for minerio in minerios_selecionados:
            self.listbox_selected_tools.insert(tk.END, minerio["nome"])

if __name__ == "__main__":
    app = MineradoraJoiaRaraApp()
    app.mainloop()
