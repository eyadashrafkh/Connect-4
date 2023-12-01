import tkinter as tk

class Connect4:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Connect 4")
        self.current_player = 'Red'
        self.create_board()
        
    def create_board(self):
        self.buttons = [[None] * 7 for _ in range(6)]
        
        for row in range(6):
            for col in range(7):
                btn = tk.Button(self.window, width=5, height=2, command=lambda r=row, c=col: self.drop_piece(r, c))
                btn.grid(row=row, column=col)
                self.buttons[row][col] = btn # places the discs in the selected grid
                
    def drop_piece(self, row, col):
        for r in range(5, row - 1, -1):
            if self.buttons[r][col]["text"] == "":
                self.buttons[r][col]["text"] = self.current_player
                if self.check_winner(row, col):
                    self.display_winner()
                    return
                self.current_player = 'Yellow' if self.current_player == 'Red' else 'Red'
                return
    
    def check_winner(self, row, col):
        # Check for a winning condition (horizontal, vertical, diagonal)
        return (
            self.check_line(row, col, 0, 1) or  # Horizontal
            self.check_line(row, col, 0, -1) or  # Horizontal
            self.check_line(row, col, 1, 0) or  # Vertical
            self.check_line(row, col, -1, 0) or  # Vertical
            self.check_line(row, col, 1, 1) or  # Diagonal \
            self.check_line(row, col, -1, -1) or  # Diagonal \
            self.check_line(row, col, -1, 1) or  # Diagonal /
            self.check_line(row, col, 1, -1)     # Diagonal /
        )

    def check_line(self, row, col, row_change, col_change):
        player = self.current_player
        count = 0
        # Check in both directions from the dropped piece
        for _ in range(4):
            if 0 <= row < 6 and 0 <= col < 7 and self.buttons[row][col]["text"] == player:
                count += 1
                row += row_change
                col += col_change
            else:
                break

        return count >= 4

    def display_winner(self):
        winner_label = tk.Label(self.window, text=f"{self.current_player} wins!", font=("Helvetica", 16, "bold"))
        winner_label.grid(row=6, columnspan=7)
        # You can add more logic to end the game or reset the board after displaying the winner.

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = Connect4()
    game.run()
