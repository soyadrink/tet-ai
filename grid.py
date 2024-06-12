import pygame
from colours import Colours

class Grid:
    def __init__(self):
        self.rows = 20
        self.cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.cols)] for i in range(self.rows)]
        self.colours = Colours.get_cell_colours()
    
    def display_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                print(self.grid[row][col], end = " ")
            print()
    
    def is_inside(self, row, col):
        if row < self.rows and col >= 0 and col < self.cols:
            return True
        return False

    def is_empty(self, row, col):
        if row+1 > self.rows:
            return False
        if self.grid[row][col] == 0 or row < 0:
            return True
        return False
    
    def row_full(self, row):
        for col in range(self.cols):
            if self.grid[row][col] == 0:
                return False
        return True
    
    def shift_row_down(self, row, rows):
        for col in range(self.cols):
            self.grid[row + rows][col] = self.grid[row][col]
            self.grid[row][col] = 0

    def clear_row(self, row):
        for col in range(self.cols):
            self.grid[row][col] = 0

    def clear_rows(self):
        cleared = 0
        for row in range(self.rows - 1, -1, -1):
            if self.row_full(row):
                self.clear_row(row)
                cleared += 1
            elif cleared > 0:
                self.shift_row_down(row, cleared)
        return cleared

    def draw(self, window):
        spawn_rect = pygame.Rect(250, 0, self.cols*self.cell_size, 4*self.cell_size)
        pygame.draw.rect(window, pygame.Color("Black"), spawn_rect)
        bg_rect = pygame.Rect(250, 4*self.cell_size, self.cols*self.cell_size+1, self.rows*self.cell_size)
        pygame.draw.rect(window, pygame.Color("White"), bg_rect)
        for row in range(self.rows):
            for col in range(self.cols):
                cell_value = self.grid[row][col]
                cell_rect = pygame.Rect(col*self.cell_size+251, row*self.cell_size+120, self.cell_size-1, self.cell_size-1)
                pygame.draw.rect(window, self.colours[cell_value], cell_rect)