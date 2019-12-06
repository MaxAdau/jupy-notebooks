#!/usr/bin/env python
# coding: utf-8

# ## My game of life
# 
# Ok, it's been a while since I wanted to implement a game fo life, but lack of time and motivation were against me.
# I have both right now so ... let's do this a pythonic way !
# 
# ### What is the game of life ?
# 
# It is a cellular automation, designed by Conway in 1970
# More info here : https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
# 
# ### Rules of the game :
# - A cell can be either dead or alive
# - Any live cell with two or three neighbors survives
# - Any dead cell with three live neighbors becomes a live cell
# - All other live cells die in the next generation. Similarly, all other dead cells stay dead

import tkinter as tk


class Grid:
    """
    This class implement the grid that contains all the cells in the game
    """
    def __init__(self, canvas, width, height, cell_size):
        self.cell_size = cell_size
        self.canvas = canvas    

        # Variable calculated from default ones
        self.nbr_cell_width = int(width / cell_size)
        self.nbr_cell_height = int(height / cell_size)
        
        # List of all cells in the grid
        self.cells = []
        
    def generate_grid(self):
        """
        Generate aa grid with empty rectangle
        Also instantiate cells that will be used in the game
        """
        # Loop in Y then X and draw rectangles
        for grid_y in range(0, self.nbr_cell_height):
            y1 = grid_y * self.cell_size
            y2 = grid_y * self.cell_size + self.cell_size
            self.cells.append([])
            for grid_x in range(0, self.nbr_cell_width):
                x1 = grid_x * self.cell_size
                x2 = grid_x * self.cell_size + self.cell_size
                # Append the cell in the double list array
                self.cells[grid_y].append(Cell(grid_x, grid_y,
                                               x1, y1, x2, y2,
                                               self.canvas))
    
    def compute_next_grid(self):
        """
        Iterate over all cells and set their next_gen attribute
        """
        # Iterate over cells
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                # Get the neighbors of a cell, then define the next status
                nbr_neighbors = self._get_alive_neighbors(cell)
                # print('Cell {} has {} neighbors'. format(cell.get_xy(), nbr_neighbors))
                self.cells[y][x].next_gen = self._apply_rules(cell, nbr_neighbors)
    
    def swap_status(self, tkevent):
        """
        Change the status of a cell
        Called from a click
        """
        # Get the position on the grid from the tkinter coordinates
        x, y = self._xy_to_grid_idx(tkevent.x, tkevent.y)

        # Change the current status of the cell and draw it
        self.cells[y][x].is_alive = not self.cells[y][x].is_alive
        self.cells[y][x].draw_cell()
    
    def draw_next_gen(self):
        """
        Update the cell.isActivate attribute
        and display the grid using the updated value
        """
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                self.cells[y][x].is_alive = self.cells[y][x].next_gen
                self.cells[y][x].draw_cell()
                
    def _apply_rules(self, cell, nbr_neighbors):
        """
        Calculate the next value of a specific cell, either
        return True if the cell will be alive
        return False if not
        """
        
        # Rules of the game
        # Any live cell with two or three neighbors survives
        if cell.is_alive and nbr_neighbors in [2, 3]:
            return True
        # Any dead cell with three live neighbors becomes a live cell
        elif not cell.is_alive and nbr_neighbors == 3:
            return True
        # All other live cells die in the next generation
        else:
            return False

    def _get_alive_neighbors(self, cell):
        """
        Return the number of cells alives in the vicinity of the given cell
        """
        # Coordinates to apply to current cell to get all 8 neighbors
        neighbors = [(-1, -1), (0, -1), (1, -1),
                     (-1,  0),          (1,  0),
                     (-1,  1), (0,  1), (1,  1)]
        
        # Iterate over neighbors and get the is_alive status
        nbr_neighbors = 0
        for coordinates in neighbors:
            adjusted_x = cell.grid_x + coordinates[0]
            adjusted_y = cell.grid_y + coordinates[1]
            # print('Cell {} : looking for cell {}'.format(cell.get_xy(),(adjusted_x, adjusted_y)))
            
            # Try to get the neighbors
            if adjusted_x >= 0 and adjusted_y >= 0:
                try:
                    neighbor = self.cells[adjusted_y][adjusted_x].is_alive
                    if neighbor:
                        # print('Cell {} : found an alive nbg in {}'.format((cell.grid_x, cell.grid_y),
                        #                                                   (adjusted_x, adjusted_y)))
                        nbr_neighbors += 1
                # We get an error while searching for out of range cells, not a problem
                except IndexError:
                    pass

        return nbr_neighbors

    def _xy_to_grid_idx(self, x, y):
        """
        Translate a x and y tkinter coordinates in a grid xy position
        Trick : I use int() to round down my coordinates
        """
        return(int(x / self.cell_size),
               int(y / self.cell_size))
    
    def _debug(self):
        """
        Print all cells and their status
        """
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                print('cell {} in {}'.format(cell.get_xy(), (x, y)))


class Cell:
    """
    This class represent a cell as intended in the game of life
    """
    def __init__(self, grid_x, grid_y, x1, y1, x2, y2, canvas):
        
        # Position of the cell in the grid
        self.grid_x = grid_x
        self.grid_y = grid_y
        
        # Position of the cell in the canvas
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        
        # The canvas used to perform graphical magic
        self.canvas = canvas
        
        # Used for the game logic
        self.is_alive = False
        self.next_gen = False
        
        # Automatically display the cell when instantiate
        self.draw_cell()
        
    def draw_cell(self):
        """
        Draw the cell
        """
        color = ''

        # Cell is alive
        if not self.is_alive:
            color = 'white'
        # Cell is dead
        elif self.is_alive:
            color = 'black'
        # Draw the rectangle
        self.canvas.create_rectangle(self.x1, self.y1,
                                     self.x2, self.y2,
                                     fill=color)

    def get_xy(self):
        """
        Return x and y in a tuple
        """
        return self.grid_x, self.grid_y

    def __str__(self):
        return '{} : {} --> {}'.format((self.grid_x, self.grid_y),
                                       self.is_alive, self.next_gen)
         

class Game:
    """
    This class contains the game logic
    """
    def __init__(self):
        # Game default values
        width = 600
        height = 600
        cell_size = 20
        
        # Instantiation of the main windows
        self.root = tk.Tk()
        self.root.title("My game of life ! \0/")
        
        # Instantiation of the frame on which the canvas will be added
        # pack() organizes widgets in blocks before placing them in the parent widget
        # Without it, the main windows will remain at default size
        # https://www.tutorialspoint.com/python/tk_pack.htm
        self.frame = tk.Frame(self.root, width=width, height=height)
        self.frame.pack()

        # Instantiation of the Canvas
        # The Canvas widget provides structured graphics facilities for Tkinter
        self.canvas = tk.Canvas(self.frame, width=width, height=height)
        self.canvas.pack()
    
        # Place buttons and link functions to them
        start_button = tk.Button(self.root, text="Start game", command=self.start)
        start_button.pack(side=tk.LEFT)
        stop_button = tk.Button(self.root, text="Stop it", command=self.stop)
        stop_button.pack(side=tk.RIGHT)

        # For debug purpose only
        # debug_button = tk.Button(self.root, text="Next loop", command=self.game_loop)
        # debug_button.pack(side = tk.BOTTOM)

        # Create the grid and generate the visible rectangles
        self.grid = Grid(self.canvas, width, height, cell_size)
        self.grid.generate_grid()
        
        # link the left click action to the swap status function
        self.canvas.bind("<Button-1>", self.grid.swap_status)

        # Launch the main loop
        self.root.mainloop()
        
    def start(self):
        """
        Start the game
        """
        # I don't want a petit rigolo to change the status of cells
        self.canvas.unbind("<Button-1>")
        self.game_loop()
    
    def game_loop(self):
        """
        Contains the main loop of the game
        """
        self.grid.compute_next_grid()
        self.grid.draw_next_gen()
        self.root.after(200, self.game_loop)

    def stop(self):
        self.root.destroy()


if __name__ == '__main__':
    game = Game()
