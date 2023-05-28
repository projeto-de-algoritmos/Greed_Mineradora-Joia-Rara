import tkinter as tk
import os
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk


class WelcomeScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Mineradora Joia Rara - Bem-vindo")
        self.geometry("800x600")

        self.background_image = None
        self.lbl_background = None

        self.create_widgets()

        self.bind("<Configure>", self.on_window_resize)

    def create_widgets(self):
        image_path = os.path.join(os.getcwd(), "assets", "mineradora.png")

        if os.path.exists(image_path):
            self.background_image = Image.open(image_path)
            self.resize_background_image()

        self.lbl_title = ttk.Label(self, text="Bem-vindo à Mineradora Joia Rara", font=("Helvetica", 16))
        self.lbl_title.place(relx=0.5, rely=0.4, anchor="center")

        self.btn_start = ttk.Button(self, text="Iniciar", command=self.open_main_app)
        self.btn_start.place(relx=0.5, rely=0.6, anchor="center")

    def open_main_app(self):
        self.destroy()
        app = MineradoraJoiaRaraApp()
        app.mainloop()

    def on_window_resize(self, event):
        self.resize_background_image()

    def resize_background_image(self):
        if self.background_image is not None:
            window_width = self.winfo_width()
            window_height = self.winfo_height()
            resized_image = self.background_image.resize((window_width, window_height), Image.LANCZOS)
            bg_image = ImageTk.PhotoImage(resized_image)

            if self.lbl_background is not None:
                self.lbl_background.configure(image=bg_image)
                self.lbl_background.image = bg_image
            else:
                self.lbl_background = ttk.Label(self, image=bg_image)
                self.lbl_background.image = bg_image
                self.lbl_background.place(x=0, y=0, relwidth=1, relheight=1)


class MineradoraJoiaRaraApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Mineradora Joia Rara")
        self.geometry("800x800")

        self.minerios = [
            {"nome": "Ouro", "image_path": "assets/ouro.png"},
            {"nome": "Prata", "image_path": "assets/prata.png"},
            {"nome": "Cobre", "image_path": "assets/cobre.png"},
            {"nome": "Ferro", "image_path": "assets/ferro.png"},
            {"nome": "Chumbo", "image_path": "assets/chumbo.png"},
        ]

        self.selected_tool = None
        self.peso_tool = 0
        self.minerios_selecionados = []

        self.create_widgets()

    def create_widgets(self):
        self.frame_content = ttk.Frame(self)
        self.frame_content.pack(fill="both", expand=True)

        text = "Precisamos transportar a maior quantidade possível de minerais para outra cidade, mas nosso caminhão só suporta 500 quilos. Você pode nos ajudar?"

        self.lbl_title = ttk.Label(self.frame_content, text=text, font=("Helvetica", 10), wraplength=300)
        self.lbl_title.pack(pady=10)

        self.frame_tools = ttk.Frame(self.frame_content)
        self.frame_tools.pack()

        num_items_per_row = 3

        for i, minerio in enumerate(self.minerios):
            btn_tool = ttk.Button(
                self.frame_tools,
                text=minerio["nome"],
                command=lambda f=minerio: self.select_tool(f),
                width=15
            )

            # Configure o posicionamento dos botões usando a geometria Grid
            row = i // num_items_per_row  # Determina a linha
            column = i % num_items_per_row  # Determina a coluna
            btn_tool.grid(row=row, column=column, padx=5, pady=5)

            if "image_path" in minerio:
                image = Image.open(minerio["image_path"])
                image = image.resize((100, 100))
                photo = ImageTk.PhotoImage(image)
                btn_tool.config(image=photo, compound=tk.TOP)
                btn_tool.image = photo

        self.frame_tools.grid_columnconfigure(0, weight=1)
        self.frame_tools.grid_columnconfigure(2, weight=1)

        self.frame_selected_tool = ttk.Frame(self.frame_content)
        self.frame_selected_tool.pack(pady=10)

        self.lbl_peso_tool = ttk.Label(self.frame_content, text="Peso do minério (1-100):")
        self.lbl_peso_tool.pack()

        self.entry_peso_tool = ttk.Entry(self.frame_content)
        self.entry_peso_tool.pack()

        self.lbl_valor_tool = ttk.Label(self.frame_content, text="Valor do minério (10-100):")
        self.lbl_valor_tool.pack()

        self.entry_valor_tool = ttk.Entry(self.frame_content)
        self.entry_valor_tool.pack()

        self.btn_add_tool = ttk.Button(self.frame_content, text="Adicionar minério", command=self.add_tool)
        self.btn_add_tool.pack(pady=10)

        self.lbl_selected_tools = ttk.Label(self.frame_content, text="Minérios selecionados:")
        self.lbl_selected_tools.pack()

        self.listbox_selected_tools = tk.Listbox(self.frame_content)
        self.listbox_selected_tools.pack(pady=5)

        self.listbox_selected_tools.bind("<<ListboxSelect>>", self.show_selected_tool_image)

        self.btn_calculate = ttk.Button(self.frame_content, text="Calcular", command=self.calculate_knapsack)
        self.btn_calculate.pack(pady=10)

    def select_tool(self, minerio):
        if self.selected_tool:
            self.selected_tool.configure(relief=tk.RAISED, bd=1, borderwidth=1)
        self.selected_tool = minerio
        self.selected_tool.configure(relief=tk.SUNKEN, bd=2, borderwidth=1)

    def add_tool(self):
        if self.selected_tool is not None:
            peso = self.entry_peso_tool.get()
            valor = self.entry_valor_tool.get()
            if peso.isdigit() and valor.isdigit():
                peso = int(peso)
                valor = int(valor)
                if 10 <= peso <= 100 and 10 <= valor <= 100:
                    self.selected_tool["peso"] = peso
                    self.selected_tool["valor"] = valor
                    self.minerios_selecionados.append(self.selected_tool)
                    self.listbox_selected_tools.insert(tk.END, self.selected_tool["nome"])
                    print(f"Minério: {self.selected_tool['nome']}")
                    print(f"Peso: {self.selected_tool['peso']}")
                    print(f"Valor: {self.selected_tool['valor']}")
                    print("Minérios selecionados:", self.minerios_selecionados)

    def show_selected_tool_image(self, event):
        selected_index = self.listbox_selected_tools.curselection()
        if selected_index:
            selected_minerio = self.minerios_selecionados[selected_index[0]]
            image_path = selected_minerio.get("image_path")
            if image_path and os.path.exists(image_path):
                image = Image.open(image_path)
                image = image.resize((200, 200))
                self.selected_tool_image = ImageTk.PhotoImage(image)
                self.lbl_selected_tool_image.configure(image=self.selected_tool_image)

    def calculate_knapsack(self):
        def knapsack(capacity, items):
            num_items = len(items)
            dp = [[0] * (capacity + 1) for _ in range(num_items + 1)]

            for i in range(1, num_items + 1):
                for j in range(1, capacity + 1):
                    if items[i - 1]["peso"] <= j:
                        dp[i][j] = max(dp[i - 1][j], items[i - 1]["valor"] + dp[i - 1][j - items[i - 1]["peso"]])
                    else:
                        dp[i][j] = dp[i - 1][j]

            return dp[num_items][capacity]

        capacity = 500
        total_value = knapsack(capacity, self.minerios_selecionados)

        messagebox.showinfo("Resultado", f"Valor máximo obtido: {total_value}")

if __name__ == "__main__":
    welcome_screen = WelcomeScreen()
    welcome_screen.mainloop()
