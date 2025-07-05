import tkinter as tk
from tkinter import messagebox

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🧩 Sudoku Solver")
        self.entries = []

        self.create_grid()
        self.create_buttons()
        self.load_sample_puzzle()  # Load a sample puzzle at startup

    def create_grid(self):
        for i in range(9):
            row = []
            for j in range(9):
                entry = tk.Entry(self.root, width=3, font=('Arial', 18), justify='center', borderwidth=2, relief='ridge')
                entry.grid(row=i, column=j, padx=1, pady=1)

                # Light background for alternating blocks
                if (i // 3 + j // 3) % 2 == 0:
                    entry.config(bg="#f0f0f0")
                row.append(entry)
            self.entries.append(row)

    def create_buttons(self):
        solve_btn = tk.Button(self.root, text="Solve", command=self.solve_gui, width=10, bg="lightgreen")
        solve_btn.grid(row=9, column=2, columnspan=2, pady=10)

        clear_btn = tk.Button(self.root, text="Clear", command=self.clear_grid, width=10, bg="lightcoral")
        clear_btn.grid(row=9, column=5, columnspan=2)

    def load_sample_puzzle(self):
        sample_board = [
            [5, 1, 7, 6, 0, 0, 0, 3, 4],
            [2, 8, 9, 0, 0, 4, 0, 0, 0],
            [3, 4, 6, 2, 0, 5, 0, 9, 0],
            [6, 0, 2, 0, 0, 0, 0, 1, 0],
            [0, 3, 8, 0, 0, 6, 0, 4, 7],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 9, 0, 0, 0, 0, 0, 7, 8],
            [7, 0, 3, 4, 0, 0, 5, 6, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        for i in range(9):
            for j in range(9):
                if sample_board[i][j] != 0:
                    self.entries[i][j].insert(0, str(sample_board[i][j]))

    def read_grid(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                if val == "":
                    row.append(0)
                else:
                    try:
                        num = int(val)
                        if 1 <= num <= 9:
                            row.append(num)
                        else:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Invalid Input", f"Invalid number at ({i+1},{j+1})")
                        return None
            board.append(row)
        return board

    def update_grid(self, board):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(board[i][j]))

    def clear_grid(self):
        for row in self.entries:
            for cell in row:
                cell.delete(0, tk.END)

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve_board(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, i, j, num):
                            board[i][j] = num
                            if self.solve_board(board):
                                return True
                            board[i][j] = 0
                    return False
        return True

    def solve_gui(self):
        board = self.read_grid()
        if board is None:
            return
        if self.solve_board(board):
            self.update_grid(board)
            messagebox.showinfo("Solved", "✅ Sudoku Solved Successfully!")
        else:
            messagebox.showerror("Unsolvable", "❌ This Sudoku puzzle cannot be solved.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
