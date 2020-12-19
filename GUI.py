import tkinter as tk
from tkinter import *

class Cell():
    BACKGROUND_COLOR = "grey"
    CELL_OCCUPIED = "yellow"
    BORDER = "black"

    def __init__(self, master, x, y, size):
        #Constructor
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.fill = False

    def _switch(self):
        #Switch if the cell is filled in or not
        self.fill = not self.fill
    
    def draw(self):
    #Draw the cell on the canvas as derived from CellGrid
        if self.master != None:
            fill = Cell.CELL_OCCUPIED
            outline = Cell.BORDER

            if not self.fill:
                fill = Cell.BACKGROUND_COLOR
                outline = Cell.BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)

class CellGrid(Canvas):
    def __init__(self, master, row_number, column_number, cell_size, *args, **kwargs):
        Canvas.__init__(self, master, width = cell_size * column_number, height = cell_size * row_number, *args, **kwargs)

        self.cell_size = cell_size

        self.grid = []
        for row in range(row_number):
            line = []
            for column in range(column_number):
                line.append(Cell(self, column, row, cell_size))
            self.grid.append(line)

        self.switched = []

        #bind click
        self.bind("<Button-1>", self.handle_mouse_click)
        #bind moving while clicking
        #TODO Add switch to turn on/off
        self.bind("<B1-Motion>", self.handle_mouse_motion)
        #bind release button - clear the memory of the modified cells
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())

        self.draw()

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _EventCoords(self, event):
        row = int(event.y / self.cell_size)
        column = int(event.x / self.cell_size)
        return row, column

    def handle_mouse_click(self, event):
        row, column = self._EventCoords(event)
        cell = self.grid[row][column]
        cell._switch()
        cell.draw()
        #add cell to the list of cells switched during the click
        self.switched.append(cell)

    def handle_mouse_motion(self, event):
        row, column = self._EventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.switched:
            cell._switch()
            cell.draw()
            self.switched.append(cell)

if __name__ == "__main__":
    app = tk.Tk()

    grid = CellGrid(app, 75, 75, 20)
    grid.pack()

    app.mainloop()

