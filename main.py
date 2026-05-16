import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

bits_example = "010011"

# unipolar
def nrz(bits):
    signal = []
    for bit in bits:
        if bit == '1':
            signal += [1]
        else:
            signal += [0]
    return signal

# polar
def nrz_level(bits):
    signal = []
    for bit in bits:
        if bit == '1':
            signal += [-1]
        else:
            signal += [1]
    return signal

def nrz_invert(bits):
    signal = []
    level = 1
    for bit in bits:
        if bit == '1':
            signal += [-level]
            level = -level
        else:
            signal += [level]
    return signal

def rz(bits):
    signal = []
    for bit in bits:
        if bit == '0':
            signal += [-1, 0]
        else:
            signal += [1, 0]
    return signal

def manchester(bits):
    signal = []
    for bit in bits:
        if bit == '1':
            signal += [-1, 1]
        else:
            signal += [1, -1]
    return signal

def manchester_diferencial(bits):
    nivel = 1
    signal = []
    for bit in bits:
        if bit == '0':
            nivel = -nivel
        signal += [nivel, -nivel]
        nivel = -nivel
    return signal

# bipolar
def ami(bits):
    index = 0
    signal = []

    for bit in bits:
        if bit == '0':
            signal += [0]
        else:
            if index % 2 == 0:
                signal += [1]
            else:
                signal += [-1]
            index += 1

    return signal

def pseudoternary(bits):
    index = 0
    signal = []

    for bit in bits:
        if bit == '1':
            signal += [0]
        else:
            if index % 2 == 0:
                signal += [1]
            else:
                signal += [-1]
            index += 1

    return signal

# especiais
def mlt3(bits):
    levels = [0, 1, 0, -1]
    index = 0
    signal = []

    for bit in bits:
        if bit == '1':
            index = (index + 1) % 4
        signal.append(levels[index])

    return signal


# expande a amostragem
def expand_signal(signal, half_bit_sample=50):
    expanded = []
    for level in signal:
        expanded += [level] * half_bit_sample
    return expanded

# plota o gráfico da codificação
def plot_signal(signal, bits, cod):
    fig = Figure(figsize=(10, 3))
    ax = fig.add_subplot(111)

    ax.step(
        range(len(signal)),
        signal,
        where='post',
        color='#EC008C',
        linewidth=3,
        linestyle='-'
    )

    bit_length = len(signal) // len(bits)

    for i in range(len(bits) + 1):
        ax.axvline(i * bit_length, linestyle=':', color='black', linewidth=1)

    for i, bit in enumerate(bits):
        x_pos = i * bit_length + bit_length / 2
        ax.text(x_pos, 1.5, str(bit), ha='center', fontsize=10)

    ax.set_ylim(-1.5, 2)
    ax.set_yticks([-1, 0, 1])
    ax.set_yticklabels(['-1', '0', '+1'])

    ax.set_title(f"{cod}")
    ax.axhline(0, color='black', linewidth=0.75)

    xticks = [i * bit_length for i in range(len(bits) + 1)]
    ax.set_xticks(xticks)
    ax.set_xticklabels([])

    return fig


def main():
    window = tk.Tk()
    window.title("Códigos de Linha")
    window.geometry("1600x900")

    # --------- TOPO ---------
    top = tk.Frame(window)
    top.pack(fill=tk.X, padx=10, pady=10)

    entry = tk.Entry(top, font=("Times New Roman", 14))
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    entry.insert(0, "010011")

    btn = tk.Button(top, text="Gerar", width=10)
    btn.pack(side=tk.LEFT, padx=10)

    opcoes = ["Todos gráficos", "NRZ Unipolar", "NRZ Polar", "NRZ-I",
        "RZ", "Manchester","Manchester Diferencial", "AMI","Pseudoternary",
        "MLT-3"
    ]

    selecionado = tk.StringVar(value="Todos gráficos")
    dropdown = tk.OptionMenu(top, selecionado, *opcoes)
    dropdown.config(width=18)
    dropdown.pack(side=tk.LEFT, padx=5)

    # --------- GRID ---------
    grid_frame = tk.Frame(window)
    grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    rows, cols = 3, 4
    cells = []

    for r in range(rows):
        grid_frame.rowconfigure(r, weight=1)
    for c in range(cols):
        grid_frame.columnconfigure(c, weight=1)

    for i in range(rows * cols):
        r, c = divmod(i, cols)
        frame = tk.Frame(grid_frame, bd=1, relief="solid")
        frame.grid(row=r, column=c, sticky="nsew", padx=5, pady=5)
        cells.append(frame)

    # --------- SINGLE VIEW ---------
    single_frame = tk.Frame(window)

    # --------- CODIFICAÇÕES ---------
    codificacoes = [
        ("NRZ Unipolar", nrz),
        ("NRZ Polar", nrz_level),
        ("NRZ-I", nrz_invert),
        ("RZ", rz),
        ("Manchester", manchester),
        ("Manchester Diferencial", manchester_diferencial),
        ("AMI", ami),
        ("Pseudoternary", pseudoternary),
        ("MLT-3", mlt3),
    ]

    canvas_widgets = []

    # --------- GERAR ---------
    def gerar():
        nonlocal canvas_widgets

        # limpar gráficos antigos
        for w in canvas_widgets:
            w.get_tk_widget().destroy()
        canvas_widgets.clear()

        bits = entry.get().strip()
        if not bits or any(c not in "01" for c in bits):
            return

        escolha = selecionado.get()

        # --------- MODO GRID ---------
        if escolha == "Todos gráficos":
            single_frame.pack_forget()
            grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            for i, cell in enumerate(cells):
                if i >= len(codificacoes):
                    break

                nome, func = codificacoes[i]
                sinal = expand_signal(func(bits))

                fig = plot_signal(sinal, bits, nome)
                fig.set_size_inches(3.2, 2.2)

                canvas = FigureCanvasTkAgg(fig, master=cell)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

                canvas_widgets.append(canvas)

        # --------- MODO SINGLE ---------
        else:
            grid_frame.pack_forget()
            single_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            for nome, func in codificacoes:
                if nome == escolha:
                    sinal = expand_signal(func(bits))

                    fig = plot_signal(sinal, bits, nome)
                    fig.set_size_inches(10, 5)

                    canvas = FigureCanvasTkAgg(fig, master=single_frame)
                    canvas.draw()
                    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

                    canvas_widgets.append(canvas)
                    break

    gerar()
    # conectar botão
    btn.config(command=gerar)

    window.mainloop()
if __name__ == "__main__":
    main()