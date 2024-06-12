import pygame
from colours import Colours
from position import Position

class Tetromino:
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.row = 0
        self.col = 0
        self.rotation = 0
        self.colours = Colours.get_cell_colours()
    
    def move(self, rows, cols):
        self.row += rows
        self.col += cols
    
    def get_cell_positions(self):
        tiles = self.cells[self.rotation]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row, position.col + self.col)
            moved_tiles.append(position)
        return moved_tiles

    def get_lowest_row(self, grid):
        tiles = self.get_cell_positions()
        for i in range(30):
            for tile in tiles:
                if grid.is_inside(tile.row+i, tile.col) == False or grid.is_empty(tile.row+i, tile.col) == False:
                    return i-1

    def rotate_cw(self):
        self.rotation += 1
        if self.rotation == len(self.cells):
            self.rotation = 0
    
    def rotate_ccw(self):
        self.rotation -= 1
        if self.rotation == -1:
            self.rotation = 3

    def draw_ghost(self, window, grid):
        tiles = self.get_cell_positions()
        low = self.get_lowest_row(grid)
        for tile in tiles:
            tile_rect = pygame.Rect(tile.col*self.cell_size+251, (tile.row+low)*self.cell_size+120, self.cell_size-1, self.cell_size-1)
            pygame.draw.rect(window, self.colours[self.id], tile_rect, 4)

    def draw_hold(self, window):
        hold_bg = pygame.Rect(60, 150, 150, 100)
        pygame.draw.rect(window, pygame.Color("Black"), hold_bg)
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(tile.col*self.cell_size-20, tile.row*self.cell_size+250, self.cell_size-1, self.cell_size-1)
            pygame.draw.rect(window, self.colours[self.id], tile_rect)

    def draw(self, window, x, y):
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(tile.col*self.cell_size+x, tile.row*self.cell_size+y, self.cell_size-1, self.cell_size-1)
            pygame.draw.rect(window, self.colours[self.id], tile_rect)