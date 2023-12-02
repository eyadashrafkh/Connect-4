import tkinter as tk
from PIL import Image, ImageTk

class Connect4:

    WIDTH = 65
    HEIGHT = 70

    def __init__(self):

        self.window = tk.Tk()
        self.window.config(bg="black")
        self.load_images()
        self.window.title("Connect 4")
        self.current_player = 'Red'

        self.create_board()

    def load_images(self):
        img = Image.open('AI_college/assigment_two/assets/red.png')
        img = img.resize((self.WIDTH, self.HEIGHT))
        self.RED_IMAGE = ImageTk.PhotoImage(img)

        img = Image.open('AI_college/assigment_two/assets/yellow.png')
        img = img.resize((self.WIDTH, self.HEIGHT))
        self.YELLOW_IMAGE = ImageTk.PhotoImage(img)

    def create_board(self):
        self.buttons = [[None] * 7 for _ in range(6)]
        
        for row in range(6):
            for col in range(7):
                btn = tk.Button(self.window, width=5, height=4,
                                command=lambda r=row, c=col: self.drop_piece(r, c))
                btn["bg"] = "black"
                btn["border"] = "0"
                btn.grid(row=row, column=col)
                self.buttons[row][col] = btn  # places the discs in the selected grid
                
    def drop_piece(self, row, col):
        for r in range(5, row - 1, -1):
            if self.buttons[r][col]["text"] == "":
                img = self.YELLOW_IMAGE if self.current_player == 'Yellow' else self.RED_IMAGE
                self.buttons[r][col].config(image=img, width=self.WIDTH, height=self.HEIGHT)
                self.buttons[r][col]["text"] = self.current_player
                if self.check_winner(r, col):
                    self.display_winner()
                    return
                self.current_player = 'Yellow' if self.current_player == 'Red' else 'Red'
                return

    def place_piece(self, btn, img):
        btn.config(image=img)

    def check_winner(self, row, col):
        # Check for a winning condition (horizontal, vertical, diagonal)
        return (
            self.check_line(row, col, 0, 1) or  # Horizontal
            self.check_line(row, col, 1, 0) or  # Vertical
            self.check_line(row, col, 1, 1) or  # Diagonal \
            self.check_line(row, col, -1, 1)  # Diagonal /
        )

    def check_line(self, row, col, row_change, col_change):
        player = self.current_player
        count = 0

        r = row
        c = col
        # Check in both directions from the dropped piece
        for _ in range(4):
            if 0 <= row < 6 and 0 <= col < 7 and self.buttons[row][col]["text"] == player:
                count += 1
                row += row_change
                col += col_change
            else:
                break

        row = r - row_change
        col = c - col_change
        for _ in range(4):
            if 0 <= row < 6 and 0 <= col < 7 and self.buttons[row][col]["text"] == player:
                count += 1
                row -= row_change
                col -= col_change
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
