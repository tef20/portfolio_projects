import tkinter as tk

DEBUG_MODE = False


class Door:
    """
    Door object:
     -
    """
    # Class defaults
    # TODO: relativize geometry for better flexibility
    #   - eg. midpoints

    patch_width = 120
    patch_height = 200
    patch_col = 'blue' if DEBUG_MODE else '#9933FF'

    door_col = 'red'
    doorway_col = 'black'
    doorway_col_winner = 'pink'
    door_mark_col = 'black'
    shuffle_door_col = 'green'
    highlight_col = 'yellow'
    highlight_thickness = 6
    door_width = 60
    door_height = 150

    def __init__(self, frame, column, row, door_num, prize):
        self.door_num = door_num
        self.prize = prize
        self.column = column
        self.row = row

        # populate canvas
        self.patch = tk.Canvas(
            master=frame,
            bg=self.patch_col,
            height=self.patch_height,
            width=self.patch_width,
            highlightthickness=0
        )

        self.door_closed = self.patch.create_rectangle(
            # x0, y0
            30, 25,
            # x1, y1
            30 + self.door_width, 25 + self.door_height,
            width=6,
            outline='',
            fill=self.door_col
        )

        self.door_mark = self.patch.create_text(
            # x, y coordinates
            self.patch_width / 2, self.patch_height / 8 * 3,
            text=self.door_num,
            font='bold 40',
            fill='black'
        )

        self.doorway_open = self.patch.create_rectangle(
            # x0, y0
            30, 25,
            # x1, y1
            30 + self.door_width, 25 + self.door_height,
            outline='',
            fill=''
        )

        self.door_open = self.patch.create_polygon(
            # x0, y0
            50, 10,
            # x1, y1
            50, (self.patch_height - 10),
            # x2, y2
            (self.patch_width - 30), (self.patch_height - 25),
            # x3, y3
            (self.patch_width - 30), 25,
            fill=''
        )

        # TODO: prize

        self.patch.grid(row=self.row, column=self.column)

    # actions
    # door operation
    def toggle_open(self, prize_reveal=True):
        if self.patch.itemcget(self.door_closed, "fill") == self.door_col:
            self.open_door(prize_reveal)
        else:
            self.close_door()

    def open_door(self, prize_reveal):
        self.patch.itemconfig(self.door_closed, fill='')
        self.patch.itemconfig(self.door_mark, fill='')
        self.patch.itemconfig(self.door_open, fill=self.door_col)
        self.patch.itemconfig(
            self.doorway_open,
            fill=(
                self.doorway_col_winner if self.prize else
                self.doorway_col
            )
        )
        # TODO: show prize

    def close_door(self):
        self.patch.itemconfig(self.door_closed, fill=self.door_col)
        self.patch.itemconfig(self.door_mark, fill=self.door_mark_col)
        self.patch.itemconfig(self.door_open, fill='')
        self.patch.itemconfig(self.doorway_open, fill='')
        # TODO: hide prize

    # highlighting
    def highlight_select(self):
        self.patch.itemconfig(self.door_closed, outline=self.highlight_col)

    def highlight_deselect(self):
        self.patch.itemconfig(self.door_closed, outline='')

    # shuffle
    def toggle_shuffle_colour(self):
        if self.patch.itemcget(self.door_closed, "fill") == self.door_col:
            self.patch.itemconfig(self.door_closed, fill=self.shuffle_door_col)
        else:
            self.patch.itemconfig(self.door_closed, fill=self.door_col)

    # door marking
    def update_door_mark(self, new_text=None):
        self.patch.itemconfig(self.door_mark, text=new_text)
        self.patch.itemconfig(self.door_mark, font="20")