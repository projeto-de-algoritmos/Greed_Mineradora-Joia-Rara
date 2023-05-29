import os
import tkinter as tk
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
        app.run()

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
        self.previous_tool = None
        self.peso_tool = 0
        self.minerios_selecionados = []

        self.create_widgets()

    def create_widgets(self):
        self.frame_content = ttk.Frame(self)
        self.frame_content.pack(fill="both", expand=True)

        text = "Precisamos transportar a maior quantidade possível de minerais para outra cidade, " \
               "mas nosso caminhão tem um peso máximo suportado de 100 unidades de peso. " \
               "Escolha os minérios que deseja transportar e clique em 'Calcular' para determinar " \
               "a melhor combinação de minérios que se encaixa no peso disponível."

        self.lbl_description = ttk.Label(self.frame_content, text=text, wraplength=600, anchor="center")
        self.lbl_description.pack(pady=10)

        self.frame_tools = ttk.Frame(self.frame_content)
        self.frame_tools.pack()

        self.tools = []

        for i, minerio in enumerate(self.minerios):
            image = Image.open(minerio["image_path"])
            resized_image = image.resize((100, 100), Image.ANTIALIAS)
            icon = ImageTk.PhotoImage(resized_image)

            tool = ttk.Button(self.frame_tools, text=minerio["nome"], image=icon, compound="top",
                              command=lambda m=minerio: self.select_tool(m))
            tool.grid(row=0, column=i, padx=5, pady=5)
            self.tools.append(tool)
            tool.image = icon

        self.frame_selected_tool = ttk.Frame(self.frame_content)
        self.frame_selected_tool.pack(pady=10)

        self.lbl_peso_tool = ttk.Label(self.frame_selected_tool, text="Peso do minério (1-100):")
        self.lbl_peso_tool.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.entry_peso_tool = ttk.Entry(self.frame_selected_tool)
        self.entry_peso_tool.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_valor_tool = ttk.Label(self.frame_selected_tool, text="Valor do minério (1-100):")
        self.lbl_valor_tool.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.entry_valor_tool = ttk.Entry(self.frame_selected_tool)
        self.entry_valor_tool.grid(row=1, column=1, padx=5, pady=5)

        self.btn_add_tool = ttk.Button(self.frame_selected_tool, text="Adicionar minério", command=self.add_tool)
        self.btn_add_tool.grid(row=2, columnspan=2, padx=5, pady=10)

        self.lbl_selected_tools = ttk.Label(self.frame_content, text="Minérios selecionados:")
        self.lbl_selected_tools.pack()

        self.listbox_selected_tools = tk.Listbox(self.frame_content)
        self.listbox_selected_tools.pack(pady=5)

        self.frame_buttons = ttk.Frame(self.frame_content)
        self.frame_buttons.pack()

        self.btn_calculate = ttk.Button(self.frame_buttons, text="Calcular", command=self.calculate_knapsack)
        self.btn_calculate.pack(pady=10)

    def select_tool(self, minerio):
        self.previous_tool = self.selected_tool
        self.selected_tool = minerio
        self.update_tool_buttons()

    def update_tool_buttons(self):
        for tool in self.tools:
            if self.selected_tool and tool.cget("text") == self.selected_tool["nome"]:
                tool.configure(state="disabled")
            elif self.previous_tool and tool.cget("text") == self.previous_tool["nome"]:
                tool.configure(state="enabled")

    def add_tool(self):
        peso = int(self.entry_peso_tool.get())
        valor = int(self.entry_valor_tool.get())

        if peso < 1 or peso > 100:
            messagebox.showerror("Erro", "O peso do minério deve estar entre 1 e 100.")
            return

        if valor < 1 or valor > 100:
            messagebox.showerror("Erro", "O valor do minério deve estar entre 1 e 100.")
            return

        tool_info = {
            "nome": self.selected_tool["nome"],
            "image_path": self.selected_tool["image_path"],
            "peso": peso,
            "valor": valor
        }

        self.minerios_selecionados.append(tool_info)
        self.listbox_selected_tools.insert(tk.END, f"{tool_info['nome']} - Peso: {peso} - Valor: {valor}")

        self.clear_tool_selection()

    def clear_tool_selection(self):
        self.selected_tool = None
        self.previous_tool = None
        self.entry_peso_tool.delete(0, tk.END)
        self.entry_valor_tool.delete(0, tk.END)
        self.update_tool_buttons()

    def calculate_knapsack(self):
        if len(self.minerios_selecionados) == 0:
            messagebox.showerror("Erro", "Selecione pelo menos um minério.")
            return

        peso_max = 500

        items = []
        for minerio in self.minerios_selecionados:
            peso_minerio = minerio["peso"]
            valor_minerio = minerio["valor"]
            taxa = peso_minerio / valor_minerio
            items.append((minerio, taxa))

        items.sort(key=lambda x: x[1], reverse=True)

        peso_total = 0
        valor_total = 0
        minerais_selecionados = []

        for item in items:
            minerio = item[0]
            peso_minerio = minerio["peso"]
            valor_minerio = minerio["valor"]

            if peso_total + peso_minerio <= peso_max:
                peso_total += peso_minerio
                valor_total += valor_minerio
                minerais_selecionados.append(minerio)

        messagebox.showinfo("Resultado", f"Valor máximo possível: {valor_total}")

        for minerio in minerais_selecionados:
            print(minerio["nome"])

        self.clear_tool_selection()


if __name__ == "__main__":
    app = WelcomeScreen()
    app.mainloop()
