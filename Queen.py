import tkinter as tk
from tkinter import ttk
import random

CELL_SIZE = 60  # اندازه هر خانه در جدول شطرنج

# بررسی امنیت قرارگیری وزیر (الگوریتم بک‌ترکینگ)
def is_safe_bt(board, row, col):
    for i in range(row):
        if board[i] == col or abs(board[i] - col) == row - i:
            return False
    return True

# الگوریتم بک‌ترکینگ برای حل n-Queens
def solve_backtracking(n):
    board = [-1] * n
    result = []

    def backtrack(row):
        if row == n:
            result.append(board[:])
            return True
        for col in range(n):
            if is_safe_bt(board, row, col):
                board[row] = col
                if backtrack(row + 1):
                    return True
                board[row] = -1
        return False

    backtrack(0)
    return result[0] if result else None

# بررسی امنیت در حل با روش CSP
def is_safe_csp(partial, row, col):
    for r, c in enumerate(partial):
        if c == col or abs(r - row) == abs(c - col):
            return False
    return True

# الگوریتم CSP برای حل n-Queens
def solve_csp(n):
    result = []

    def csp(row, partial):
        if row == n:
            result.append(partial[:])
            return True
        for col in range(n):
            if is_safe_csp(partial, row, col):
                partial.append(col)
                if csp(row + 1, partial):
                    return True
                partial.pop()
        return False

    csp(0, [])
    return result[0] if result else None

# محاسبه تعداد برخورد وزیرها (برای ژنتیک)
def fitness(board):
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                conflicts += 1
    return conflicts

# ترکیب دو والد برای تولید فرزند
def crossover(parent1, parent2):
    n = len(parent1)
    point = random.randint(0, n - 1)
    return parent1[:point] + parent2[point:]

# اعمال جهش روی برد
def mutate(board):
    n = len(board)
    new_board = board[:]
    i = random.randint(0, n - 1)
    new_board[i] = random.randint(0, n - 1)
    return new_board

# الگوریتم ژنتیک برای حل n-Queens
def solve_genetic(n, max_generations=1000, population_size=100):
    population = [random.sample(range(n), n) for _ in range(population_size)]
    for _ in range(max_generations):
        population.sort(key=fitness)
        if fitness(population[0]) == 0:
            return population[0]
        new_population = population[:10]
        while len(new_population) < population_size:
            parents = random.sample(population[:50], 2)
            child = crossover(parents[0], parents[1])
            if random.random() < 0.1:
                child = mutate(child)
            new_population.append(child)
        population = new_population
    return None

# کلاس اصلی برنامه گرافیکی
class NQueensApp:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens Solver")
        self.root.configure(bg="#f0f4f8")
        self.create_widgets()

    # ایجاد عناصر گرافیکی
    def create_widgets(self):
        control_frame = tk.Frame(self.root, bg="#f0f4f8")
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Enter N:", bg="#f0f4f8", font=("Segoe UI", 10)).grid(row=0, column=0)
        self.n_entry = tk.Entry(control_frame, width=5, font=("Segoe UI", 10))
        self.n_entry.grid(row=0, column=1, padx=5)

        tk.Label(control_frame, text="Algorithm:", bg="#f0f4f8", font=("Segoe UI", 10)).grid(row=0, column=2)
        self.algorithm_var = tk.StringVar()
        self.algorithm_box = ttk.Combobox(control_frame, textvariable=self.algorithm_var, state="readonly", width=12)
        self.algorithm_box['values'] = ("backtracking", "csp", "genetic")
        self.algorithm_box.current(0)
        self.algorithm_box.grid(row=0, column=3, padx=5)

        tk.Button(control_frame, text="Solve", command=self.solve, bg="#4CAF50", fg="white", font=("Segoe UI", 10)).grid(row=0, column=4, padx=10)
        tk.Button(control_frame, text="Reset", command=self.reset, bg="#f44336", fg="white", font=("Segoe UI", 10)).grid(row=0, column=5)

        self.result_label = tk.Label(self.root, text="", bg="#f0f4f8", font=("Segoe UI", 11, "bold"))
        self.result_label.pack()

        self.canvas = tk.Canvas(self.root, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(pady=10)

    # حل و نمایش نتیجه
    def solve(self):
        self.canvas.delete("all")
        try:
            n = int(self.n_entry.get())
            if n < 1 or n > 30:
                raise ValueError
        except ValueError:
            self.result_label.config(text="Please enter a valid N (1-30).")
            return

        algorithm = self.algorithm_var.get()
        if algorithm == "backtracking":
            solution = solve_backtracking(n)
        elif algorithm == "csp":
            solution = solve_csp(n)
        elif algorithm == "genetic":
            solution = solve_genetic(n)
        else:
            self.result_label.config(text="Invalid algorithm selected.")
            return

        if solution:
            self.result_label.config(text="Solution found.")
            self.draw_board(solution)
        else:
            self.result_label.config(text="No solution found.")

    # رسم صفحه شطرنج
    def draw_board(self, board):
        n = len(board)
        self.canvas.config(width=n * CELL_SIZE, height=n * CELL_SIZE)
        for row in range(n):
            for col in range(n):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                if board[row] == col:
                    self.canvas.create_text(x1 + CELL_SIZE//2, y1 + CELL_SIZE//2,
                                            text="♛", font=("Segoe UI", CELL_SIZE//2), fill="#ff3366")

    # ریست کردن فرم
    def reset(self):
        self.canvas.delete("all")
        self.n_entry.delete(0, tk.END)
        self.result_label.config(text="")

# اجرای برنامه
if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensApp(root)
    root.mainloop()
