
import tkinter as tk
from tkinter import messagebox

# =========================================
# MATRIXLAB - WITHOUT NUMPY
# =========================================

root = tk.Tk()
root.title("MatrixLab | Without NumPy")
root.geometry("1050x700")
root.minsize(850, 620)
root.configure(bg="#0f172a")

BG = "#0f172a"
PANEL = "#1e293b"
FIELD = "#334155"
ACCENT = "#38bdf8"
WHITE = "#f8fafc"
MUTED = "#94a3b8"

entries_a = []
entries_b = []
last_result = "No calculation performed yet."
last_title = "Result Preview"


# =========================================
# MATRIX FUNCTIONS
# =========================================

def get_matrix(entries):
    matrix = []
    for row in entries:
        values = []
        for entry in row:
            value = entry.get().strip()
            if value == "":
                raise ValueError("Please fill all matrix fields.")
            values.append(float(value))
        matrix.append(values)
    return matrix


def fmt(value):
    if abs(value - round(value)) < 0.0000001:
        return str(int(round(value)))
    return f"{value:.3f}".rstrip("0").rstrip(".")


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(3)] for i in range(3)]


def subtract(a, b):
    return [[a[i][j] - b[i][j] for j in range(3)] for i in range(3)]


def element_multiply(a, b):
    return [[a[i][j] * b[i][j] for j in range(3)] for i in range(3)]


def multiply(a, b):
    result = []
    for i in range(3):
        row = []
        for j in range(3):
            total = 0
            for k in range(3):
                total += a[i][k] * b[k][j]
            row.append(total)
        result.append(row)
    return result


def transpose(m):
    return [[m[j][i] for j in range(3)] for i in range(3)]


def determinant(m):
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def inverse(m):
    det = determinant(m)

    if abs(det) < 1e-10:
        raise ValueError("Inverse does not exist. Determinant is zero.")

    cofactors = []

    for i in range(3):
        row = []
        for j in range(3):
            minor = []
            for r in range(3):
                if r != i:
                    minor_row = []
                    for c in range(3):
                        if c != j:
                            minor_row.append(m[r][c])
                    minor.append(minor_row)

            minor_det = (
                minor[0][0] * minor[1][1]
                - minor[0][1] * minor[1][0]
            )

            row.append(((-1) ** (i + j)) * minor_det)

        cofactors.append(row)

    adj = transpose(cofactors)

    return [[adj[i][j] / det for j in range(3)] for i in range(3)]


# =========================================
# DISPLAY FUNCTIONS
# =========================================

def format_result(result):
    if isinstance(result, list):
        return "\n".join(
            "      ".join(fmt(value) for value in row)
            for row in result
        )
    return fmt(result)


def show_result(title, result):
    global last_result, last_title

    last_title = title
    last_result = format_result(result)

    preview_title.config(text=title)
    preview_text.config(state="normal")
    preview_text.delete("1.0", tk.END)
    preview_text.insert("1.0", last_result)
    preview_text.config(state="disabled")

    status_label.config(text="Calculation completed successfully.")


def view_full_result():
    window = tk.Toplevel(root)
    window.title("Full Matrix Result")
    window.geometry("600x450")
    window.configure(bg=BG)

    tk.Label(
        window,
        text=last_title,
        font=("Arial", 18, "bold"),
        bg=BG,
        fg=ACCENT
    ).pack(pady=15)

    frame = tk.Frame(window, bg=PANEL)
    frame.pack(fill="both", expand=True, padx=20, pady=15)

    output = tk.Text(
        frame,
        font=("Consolas", 16),
        bg=FIELD,
        fg=WHITE,
        wrap="none",
        relief="flat"
    )
    output.pack(fill="both", expand=True, padx=10, pady=10)

    output.insert("1.0", last_result)
    output.config(state="disabled")


# =========================================
# OPERATION HANDLER
# =========================================

def calculate(operation):
    try:
        a = get_matrix(entries_a)
        b = get_matrix(entries_b)

        if operation == "Addition":
            result = add(a, b)

        elif operation == "Subtraction":
            result = subtract(a, b)

        elif operation == "Matrix Multiplication":
            result = multiply(a, b)

        elif operation == "Element-wise Multiplication":
            result = element_multiply(a, b)

        elif operation == "Transpose A":
            result = transpose(a)

        elif operation == "Transpose B":
            result = transpose(b)

        elif operation == "Determinant A":
            result = determinant(a)

        elif operation == "Determinant B":
            result = determinant(b)

        elif operation == "Inverse A":
            result = inverse(a)

        elif operation == "Inverse B":
            result = inverse(b)

        show_result(operation, result)

    except ValueError as error:
        messagebox.showerror("Input Error", str(error))
    except Exception as error:
        messagebox.showerror("Error", str(error))


# =========================================
# BUTTON STYLE
# =========================================

def make_button(parent, text, command, color=ACCENT):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg="#0f172a",
        activebackground="#7dd3fc",
        activeforeground="#0f172a",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=8,
        pady=9
    )


# =========================================
# HEADER
# =========================================

header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=22, pady=(12, 8))

tk.Label(
    header,
    text="MatrixLab",
    font=("Arial", 25, "bold"),
    bg=BG,
    fg=ACCENT
).pack(side="left")

tk.Label(
    header,
    text="3 x 3 MATRIX CALCULATOR  |  WITHOUT NUMPY",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg=MUTED
).pack(side="right", pady=10)


# =========================================
# MATRIX INPUT PANELS
# =========================================

matrix_area = tk.Frame(root, bg=BG)
matrix_area.pack(fill="x", padx=22, pady=7)


def create_matrix_panel(parent, title, matrix_list):
    panel = tk.LabelFrame(
        parent,
        text=title,
        bg=PANEL,
        fg=ACCENT,
        font=("Arial", 12, "bold"),
        padx=10,
        pady=8
    )
    panel.pack(side="left", fill="both", expand=True, padx=7)

    for i in range(3):
        row = []
        for j in range(3):
            entry = tk.Entry(
                panel,
                width=9,
                justify="center",
                font=("Arial", 13, "bold"),
                bg=FIELD,
                fg=WHITE,
                insertbackground=WHITE,
                relief="flat"
            )
            entry.grid(row=i, column=j, padx=6, pady=6, ipady=6)
            row.append(entry)
        matrix_list.append(row)


create_matrix_panel(matrix_area, "MATRIX A", entries_a)
create_matrix_panel(matrix_area, "MATRIX B", entries_b)


# =========================================
# SAMPLE / CLEAR / RESET / SWAP
# =========================================

def clear_all():
    for matrix in [entries_a, entries_b]:
        for row in matrix:
            for entry in row:
                entry.delete(0, tk.END)

    preview_title.config(text="Result Preview")
    preview_text.config(state="normal")
    preview_text.delete("1.0", tk.END)
    preview_text.insert("1.0", "Enter matrices and select an operation.")
    preview_text.config(state="disabled")

    global last_result, last_title
    last_result = "No calculation performed yet."
    last_title = "Result Preview"
    status_label.config(text="All fields cleared.")


def load_sample():
    sample_a = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
    sample_b = [[2, 0, 1], [1, 3, 0], [0, 2, 4]]

    for i in range(3):
        for j in range(3):
            entries_a[i][j].delete(0, tk.END)
            entries_a[i][j].insert(0, str(sample_a[i][j]))

            entries_b[i][j].delete(0, tk.END)
            entries_b[i][j].insert(0, str(sample_b[i][j]))

    status_label.config(text="Sample matrices loaded.")


def reset():
    clear_all()
    load_sample()
    status_label.config(text="Application reset successfully.")


def swap_matrices():
    a = get_matrix(entries_a)
    b = get_matrix(entries_b)

    for i in range(3):
        for j in range(3):
            entries_a[i][j].delete(0, tk.END)
            entries_a[i][j].insert(0, fmt(b[i][j]))

            entries_b[i][j].delete(0, tk.END)
            entries_b[i][j].insert(0, fmt(a[i][j]))

    status_label.config(text="Matrix A and Matrix B swapped.")


toolbar = tk.Frame(root, bg=BG)
toolbar.pack(fill="x", padx=25, pady=9)

make_button(toolbar, "Load Sample", load_sample).pack(side="left", padx=5)
make_button(toolbar, "Clear All", clear_all, "#cbd5e1").pack(side="left", padx=5)
make_button(toolbar, "Reset", reset, "#fbbf24").pack(side="left", padx=5)
make_button(toolbar, "Swap Matrices", swap_matrices, "#a7f3d0").pack(side="left", padx=5)


# =========================================
# OPERATIONS - TWO ROWS
# =========================================

operation_panel = tk.LabelFrame(
    root,
    text="  SELECT MATRIX OPERATION  ",
    bg=PANEL,
    fg=ACCENT,
    font=("Arial", 12, "bold"),
    padx=10,
    pady=10
)
operation_panel.pack(fill="x", padx=22, pady=8)

operations = [
    "Addition",
    "Subtraction",
    "Matrix Multiplication",
    "Element-wise Multiplication",
    "Transpose A",
    "Transpose B",
    "Determinant A",
    "Determinant B",
    "Inverse A",
    "Inverse B"
]

for i, operation in enumerate(operations):
    btn = make_button(
        operation_panel,
        operation,
        lambda op=operation: calculate(op)
    )
    btn.grid(
        row=i // 5,
        column=i % 5,
        padx=5,
        pady=7,
        sticky="ew"
    )

for col in range(5):
    operation_panel.grid_columnconfigure(col, weight=1)


# =========================================
# RESULT PREVIEW
# =========================================

result_panel = tk.LabelFrame(
    root,
    text="  RESULT PREVIEW  ",
    bg=PANEL,
    fg=ACCENT,
    font=("Arial", 12, "bold"),
    padx=12,
    pady=8
)
result_panel.pack(fill="both", expand=True, padx=22, pady=8)

preview_title = tk.Label(
    result_panel,
    text="Result Preview",
    bg=PANEL,
    fg=WHITE,
    font=("Arial", 11, "bold")
)
preview_title.pack(anchor="w", pady=3)

preview_text = tk.Text(
    result_panel,
    height=4,
    font=("Consolas", 13),
    bg=FIELD,
    fg=WHITE,
    relief="flat",
    wrap="none"
)
preview_text.pack(fill="both", expand=True, pady=5)
preview_text.insert("1.0", "Enter matrices and select an operation.")
preview_text.config(state="disabled")


# =========================================
# FOOTER
# =========================================

footer = tk.Frame(root, bg=BG)
footer.pack(fill="x", padx=22, pady=(5, 12))

status_label = tk.Label(
    footer,
    text="Ready to calculate.",
    bg=BG,
    fg=MUTED,
    font=("Arial", 9)
)
status_label.pack(side="left")

make_button(
    footer,
    "View Full Result",
    view_full_result
).pack(side="right")


# =========================================
# START APPLICATION
# =========================================

load_sample()
root.mainloop()
