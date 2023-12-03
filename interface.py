import tkinter as tk
from PIL import Image, ImageTk

class Connect4:

    WIDTH = 65
    HEIGHT = 70

    def __init__(self):

        self.red_score = 0
        self.red_potential_score = 0
        self.yellow_score = 0
        self.yellow_potential_score = 0

        self.window = tk.Tk()
        self.window.config(bg="black")
        self.load_images()
        self.window.title("Connect 4")
        self.current_player = 'Red'

        self.score_label = tk.Label(self.window, text=f"yellow: {self.yellow_score}\tred: {self.red_score}",
                                    font=("Helvetica", 16, "bold"))
        self.score_label.grid(row=6, columnspan=7)
        self.create_board()

    def load_images(self):
        img = Image.open('AI_college/assigment_two/assets/red.png')
        img = img.resize((self.WIDTH, self.HEIGHT))
        self.RED_IMAGE = ImageTk.PhotoImage(img)

        img = Image.open('AI_college/assigment_two/assets/yellow.png')
        img = img.resize((self.WIDTH, self.HEIGHT))
        self.YELLOW_IMAGE = ImageTk.PhotoImage(img)

    def drop_piece(self, row, col):
        for r in range(5, row - 1, -1):
            if self.buttons[r][col]["text"] == "":
                img = self.YELLOW_IMAGE if self.current_player == 'Yellow' else self.RED_IMAGE
                self.buttons[r][col].config(image=img, width=self.WIDTH, height=self.HEIGHT)
                self.buttons[r][col]["text"] = self.current_player

                # check for score and potential score
                result = self.check_score(r, col)

                # update score and potential score
                if self.current_player == 'Yellow':
                    self.yellow_score += result[0]
                    self.yellow_potential_score -= result[0]
                    self.yellow_potential_score += result[1]
                else:
                    self.red_score += result[0]
                    self.red_potential_score -= result[0]
                    self.red_potential_score += result[1]

                self.current_player = 'Yellow' if self.current_player == 'Red' else 'Red'

                # check for score and potential score for opposite color
                result = self.check_score(r, col)

                # update score and potential score
                if self.current_player == 'Yellow':
                    self.yellow_potential_score -= result[0]
                else:
                    self.red_potential_score -= result[0]

                self.update_score()
                return

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

    def update_score(self):
        self.score_label.config(text=f"yellow: {self.yellow_score}\tred: {self.red_score}")
        print(f"red pot: {self.red_potential_score}\tyellow pot: {self.yellow_potential_score}")

    def place_piece(self, btn, img):
        btn.config(image=img)

    def check_score(self, row, col):
        # Check for a winning condition (horizontal, vertical, diagonal)
        return [sum(x) for x in zip(
                self.check_line(row, col, 0, 1),  # Horizontal
                self.check_line(row, col, 1, 0),  # Vertical
                self.check_line(row, col, 1, 1),  # Diagonal
                self.check_line(row, col, -1, 1)  # Diagonal
        )]

    def check_line(self, row, col, row_change, col_change):
        player = self.current_player
        count = 0
        potential_count = 0

        # keep track of original play
        r = row
        c = col

        # Check in both directions from the dropped piece
        while 0 <= row < 6 and 0 <= col < 7:
            # count consecutive pieces of the same color
            if self.buttons[row][col]["text"] == player:
                count += 1
                row += row_change
                col += col_change

            # if there is an empty space, count it as a potential score
            elif self.buttons[row][col]["text"] == "" and count >= 3:
                potential_count += 1
                row += row_change
                col += col_change

                # if there are similar pieces after gap, count it as aditional potential score
                while 0 <= row < 6 and 0 <= col < 7 and self.buttons[row][col]["text"] == player:
                    row += row_change
                    col += col_change
                    potential_count += 1
                break
            else:
                break

        if count > 4:
            count = 4

        right_count = count

        # reset to starting position
        row = r - row_change
        col = c - col_change

        # check in the opposite direction
        while 0 <= row < 6 and 0 <= col < 7:
            # count consecutive pieces of the same color
            if self.buttons[row][col]["text"] == player:
                count += 1
                row -= row_change
                col -= col_change

            # if there is an empty space, count it as a potential score
            elif self.buttons[row][col]["text"] == "" and count >= 3:
                potential_count += 1
                row -= row_change
                col -= col_change

                # if there are similar pieces after gap, count it as aditional potential score
                while 0 <= row < 6 and 0 <= col < 7 and self.buttons[row][col]["text"] == player:
                    row -= row_change
                    col -= col_change
                    potential_count += 1
                break
            else:
                break

        if count - right_count > 3:
            count = right_count + 3

        score = max(0, count - 3)
        return score, potential_count

    def display_winner(self):
        winner_label = tk.Label(self.window, text=f"{self.current_player} wins!", font=("Helvetica", 16, "bold"))
        winner_label.grid(row=6, columnspan=7)
        # You can add more logic to end the game or reset the board after displaying the winner.

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = Connect4()
    game.run()
