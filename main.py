from tkinter import *
import random


class Minesweeper:
    images = {}
    tiles = []

    # standard size and mines:
    mines = 99
    rows = 16
    columns = 30
    total_tiles = rows * columns

    flagged_tiles = 0
    revealed_tiles = 0

    # set states for tiles
    STATE_UNREVEALED = 0  # when a tile has not been clicked or flagged
    STATE_REVEALED = 1  # when a tile has been clicked
    STATE_FLAG = 2  # when a tile is flagged

    game_running = False

    def __init__(self, tk):
        # load all needed images
        self.images = {"blank": PhotoImage(file="images/unclicked.png"),
                       "0": PhotoImage(file="images/clicked_0.png"),
                       "1": PhotoImage(file="images/clicked_1.png"),
                       "2": PhotoImage(file="images/clicked_2.png"),
                       "3": PhotoImage(file="images/clicked_3.png"),
                       "4": PhotoImage(file="images/clicked_4.png"),
                       "5": PhotoImage(file="images/clicked_5.png"),
                       "6": PhotoImage(file="images/clicked_6.png"),
                       "7": PhotoImage(file="images/clicked_7.png"),
                       "8": PhotoImage(file="images/clicked_8.png"),
                       "flag": PhotoImage(file="images/flag.png"),
                       "flag_wrong": PhotoImage(file="images/flag_wrong.png"),
                       "bomb": PhotoImage(file="images/bomb.png"),
                       "bomb_clicked": PhotoImage(file="images/bomb_clicked.png"),
                       "reset_happy": PhotoImage(file="images/reset_happy.png"),
                       "reset_dead": PhotoImage(file="images/reset_dead.png"),
                       "reset_cool": PhotoImage(file="images/reset_cool.png")
                       }

        # set tkinter instance
        self.tk = tk
        self.frame = Frame(self.tk)
        self.frame.pack()

        # button to reset the game
        self.reset_button = Button(self.frame, image=self.images.get("reset_happy"), command=self.reset)
        # label that shows how many mines are left
        self.mines_label = Label(self.frame, font=("Courier", 40), text=str(self.mines), fg="#d40000")

        # build a label and Textfield to set a custom width/amount of columns
        self.columns_label = Label(self.frame, font=("Courier", 18), text="width:")
        self.columns_label.grid(row=0, column=0, columnspan=2, sticky=E)
        self.input_columns = Text(self.frame, width=3, height=1, font=("Courier", 18))
        self.input_columns.grid(row=0, column=2, sticky=W)
        self.input_columns.insert(1.0, str(self.columns))

        # build a label and Textfield to set a custom height/amount of rows
        self.rows_label = Label(self.frame, font=("Courier", 18), text="height:")
        self.rows_label.grid(row=0, column=3, columnspan=2, sticky=E)
        self.input_rows = Text(self.frame, width=3, height=1, font=("Courier", 18))
        self.input_rows.grid(row=0, column=5, sticky=W)
        self.input_rows.insert(1.0, str(self.rows))

        # build a label and Textfield to set a custom amount of mines
        self.mines_input_Label = Label(self.frame, font=("Courier", 18), text="mines:")
        self.mines_input_Label.grid(row=0, column=6, columnspan=2, sticky=E)
        self.input_mines = Text(self.frame, width=3, height=1, font=("Courier", 18))
        self.input_mines.grid(row=0, column=8, sticky=W)
        self.input_mines.insert(1.0, str(self.mines))

        # setup a game
        self.setup()

    def setup(self):

        # read custom values for rows, columns and mines for the game

        try:
            # read the absolute value of the column input (only if grater than zero)
            if abs(int(self.input_columns.get(1.0, "end"))) > 0:
                columns = abs(int(self.input_columns.get(1.0, "end")))
            else:
                columns = self.columns
        except ValueError:  # if an invalid value is given, the value doesn't change
            columns = self.columns

        self.columns = columns
        # set the text in the input field to the correct value(in case of an invalid input)
        self.input_columns.delete(1.0, "end")
        self.input_columns.insert(1.0, str(self.columns))

        try:
            # read the absolute value of the row input (only if grater than zero)
            if abs(int(self.input_rows.get(1.0, "end"))) > 0:
                rows = abs(int(self.input_rows.get(1.0, "end")))
            else:
                rows = self.rows
        except ValueError:  # if an invalid value is given, the value doesn't change
            rows = self.rows

        self.rows = rows
        # set the text in the input field to the correct value(in case of an invalid input)
        self.input_rows.delete(1.0, "end")
        self.input_rows.insert(1.0, str(self.rows))

        self.total_tiles = rows * columns

        try:
            # read the absolute value of the mines input
            mines = abs(int(self.input_mines.get(1.0, "end")))
        except ValueError:  # if an invalid value is given, the value doesn't change
            mines = self.mines

        # check if the amount of mines is possible for the current size of the game
        if mines < self.total_tiles:  # a game must have less mines that tiles
            self.mines = mines
        else:
            # if the game is not possible set mines to 0,
            # so that it is always possible no matter what size
            self.mines = 0

        # set the text in the input field to the correct value(in case of an invalid input)
        self.input_mines.delete(1.0, "end")
        self.input_mines.insert(1.0, str(self.mines))

        # reset flagged and revealed tiles
        self.flagged_tiles = 0
        self.revealed_tiles = 0

        # place reset button in the middle and mines label on a quarter of the board
        self.reset_button.grid(row=1, column=round((columns / 2)))
        self.mines_label.grid(row=1, column=0, columnspan=int((columns / 2) + 0.5))
        # reset amount of mines
        self.mines_label.config(text=str(self.mines))

        # create a 2 dimensional list of tiles
        self.tiles = []
        for i in range(rows):
            row = []
            for j in range(columns):
                button = Button(self.frame, image=self.images.get("blank"))
                button.grid(row=i + 2, column=j, sticky=W)
                tile = Tile(x=i, y=j, button=button)  # each tile has coordinates and a button

                # set functions for right and left click events
                button.bind("<Button-1>", self.on_left_click_wrapper(tile))
                button.bind("<Button-3>", self.on_right_click_wrapper(tile))
                row.append(tile)

            self.tiles.append(row)

        self.game_running = True

    # function is called when the reset button is clicked
    def reset(self):

        # delete all buttons
        for row in self.tiles:
            for tile in row:
                tile.button.destroy()

        # reset the image
        self.reset_button.config(image=self.images.get("reset_happy"))
        # setup a new game
        self.setup()

    def on_right_click_wrapper(self, tile):
        # returns the 'flag' function, which is called when a button gets right-clicked
        return lambda button: self.flag(tile)

    def on_left_click_wrapper(self, tile):
        # returns the 'click' function, which is called when a button gets left-clicked
        return lambda button: self.click(tile)

    # function used to add and remove flags from tiles
    def flag(self, tile):
        # can only add/remove flags when the game has started and at least one tile has been revealed
        if self.game_running and self.revealed_tiles > 0:
            # if the tile has not been clicked and is not flagged either
            if tile.state == self.STATE_UNREVEALED:
                tile.state = self.STATE_FLAG  # change the state of the tile
                self.flagged_tiles += 1
                tile.button.config(image=self.images.get("flag"))  # change the image of the button
            # if the tile has been flagged
            elif tile.state == self.STATE_FLAG:
                tile.state = self.STATE_UNREVEALED  # change the state of the tile
                self.flagged_tiles -= 1
                tile.button.config(image=self.images.get("blank"))  # change the image of the button

            # set the amount of mines that have not been found
            self.mines_label.config(text=str(self.mines - self.flagged_tiles))

    # function that gets called when a tile gets left-clicked
    def click(self, tile):
        if self.game_running:  # can only click when the game is running
            if self.revealed_tiles == 0:
                # generate the mines on the field if no tile was clicked before
                self.generate_mines(self.mines, tile)

                # set the amount of surrounding mines for each tile
                for row in self.tiles:
                    for current_tile in row:
                        current_tile.mines = self.get_mines(current_tile)

                # self.print_tiles()  # used for debug purposes (shows solution)

            # if the clicked tile was not clicked before and is not flagged
            if tile.state == self.STATE_UNREVEALED:
                if tile.is_mine:
                    tile.button.config(image=self.images.get("bomb_clicked"))  # change image of the button
                    self.end_game(tile)  # end the game because the clicked tile was a mine
                else:
                    tile.state = self.STATE_REVEALED  # change state of the tile
                    self.revealed_tiles += 1
                    # change the image of the button to the fitting number
                    tile.button.config(image=self.images.get(str(tile.mines)))
                    # if the tile has 0 mines around itself, all unrevealed neighbours get automatically clicked
                    if tile.mines == 0:
                        for n in self.get_neighbours(tile):
                            if n.state == self.STATE_UNREVEALED:
                                self.click(n)
            # chording:
            # if the tile has been revealed and the same amount of mines of that tile have been flagged in the
            # surrounding tiles, all unrevealed neighbours get automatically clicked
            elif tile.state == self.STATE_REVEALED and tile.mines == self.get_flags(tile):
                for n in self.get_neighbours(tile):
                    if n.state == self.STATE_UNREVEALED:
                        self.click(n)

            # check if all tiles except the mines have been revealed and the player won
            if self.revealed_tiles == self.total_tiles - self.mines:
                self.end_game(tile)

    # function used for debug purposes to print the whole minefield with solution
    def print_tiles(self):
        print("-" * (self.columns * 3 + 4))
        for row in self.tiles:
            r = "| "
            for tile in row:
                if tile.is_mine:
                    r += " X "
                elif tile.mines == 0:
                    r += "   "
                else:
                    r += " " + str(tile.mines) + " "
            print(r + " |")
        print("-" * (self.columns * 3 + 4))

    # function used to generate a random pattern of mines(probably not very efficient but it works :) )
    def generate_mines(self, mines, tile):
        i = 0
        while i < mines:
            # choose a random tile
            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.columns - 1)
            # if it is not already a mine or the first clicked tile, the random tile will become a mine
            if not self.tiles[x][y].is_mine and self.tiles[x][y] != tile:
                self.tiles[x][y].is_mine = True
                i += 1

    # function to get the amount of surrounding mines of a tile
    def get_mines(self, tile):
        if tile.is_mine:
            return -1
        mines = 0
        neighbours = self.get_neighbours(tile)  # get all neighbour tiles
        for n in neighbours:
            if n.is_mine:
                mines += 1

        return mines

    # function to get the amount of surrounding flags of a tile
    def get_flags(self, tile):
        flags = 0
        neighbours = self.get_neighbours(tile)  # get all neighbour tiles
        for n in neighbours:
            if n.state == self.STATE_FLAG:
                flags += 1

        return flags

    # function to get all neighbours of a tile
    def get_neighbours(self, tile):
        x = tile.x
        y = tile.y
        result = []
        # all possible 8 surrounding coordinates
        cords = (
            (x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y),
            (x + 1, y + 1))
        for cord in cords:
            # only add tiles with valid coordinates(positive and in index) to the result
            try:
                if cord[0] >= 0 and cord[1] >= 0:
                    result.append(self.tiles[cord[0]][cord[1]])
            except IndexError:
                pass
        return result

    # function to end the game depending on the outcome
    def end_game(self, t):
        self.game_running = False

        # if the last clicked tile was a mine and the game is lost
        if t.is_mine:
            for row in self.tiles:
                for tile in row:
                    # change the image for all mines that are not flagged
                    if tile.is_mine and tile != t and tile.state != self.STATE_FLAG:
                        tile.button.config(image=self.images.get("bomb"))

                    # change the image for all faulty flagged tiles
                    if tile.state == self.STATE_FLAG and not tile.is_mine:
                        tile.button.config(image=self.images.get("flag_wrong"))

            # change image of the reset button, to show that the player lost
            self.reset_button.config(image=self.images.get("reset_dead"))
        else:  # if the last clicked tile was not a mine and the game is won
            for row in self.tiles:
                for tile in row:
                    # automatically flag all non-flagged mines
                    if tile.is_mine:
                        tile.button.config(image=self.images.get("flag"))

            # change image of the reset button, to show that the player won
            self.reset_button.config(image=self.images.get("reset_cool"))

            self.mines_label.config(text="0")  # set the label of mines to find to 0


class Tile:
    is_mine = False
    state = 0
    mines = -1

    def __init__(self, x, y, button):
        self.x = x
        self.y = y
        self.button = button


### END OF CLASSES ###

def main():
    # create Tk instance
    window = Tk()
    # set program title
    window.title("Minesweeper")
    # create game instance
    minesweeper = Minesweeper(window)

    # run event loop
    window.mainloop()


if __name__ == "__main__":
    main()
