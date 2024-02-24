import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx

class AutomataRFC:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Validación de RFC")

        self.entry_label = tk.Label(self.root, text="Ingrese la cadena RFC:")
        self.entry_label.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack()

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

        self.validate_button = tk.Button(self.root, text="Validar", command=self.validar_rfc_and_show)
        self.validate_button.pack()

    def validar_rfc_and_show(self):
        rfc = self.entry.get().upper()
        
        if rfc[0] != 'O':
            self.result_label.config(text="Cadena RFC no válida. El estado inicial debe ser 'O'.")
            return
        
        letters_seen = set()
        for letra in rfc[1:]:
            if letra not in ['O', 'E', 'M']:
                self.result_label.config(text="Cadena RFC no válida. Las letras deben ser 'OOEM'.")
                return
            if letra in letters_seen:
                self.result_label.config(text=f"Cadena RFC no válida. La letra '{letra}' aparece más de una vez o más.")
                return
            letters_seen.add(letra)

        self.result_label.config(text="Cadena RFC válida.")

        self.mostrar_automata()

    def mostrar_automata(self):
        rfc = self.entry.get().upper()

        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()

        G = nx.DiGraph()

        for letra in rfc:
            G.add_node(letra)

        for i in range(len(rfc) - 1):
            G.add_edge(rfc[i], rfc[i+1])

        fig, ax = plt.subplots(figsize=(6, 4))
        pos = nx.spring_layout(G, seed=42)

        nx.draw(G, pos, with_labels=True, node_size=300, node_color='red', font_size=10, arrows=True, ax=ax, edge_color='black')

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    automata = AutomataRFC()
    automata.run()
