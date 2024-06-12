import pygame
import random
import math
from grid import Grid
from tetrominos import *
from kicks import Kicks
from autolock import Autolock

class Game:
    def __init__(self, lock_delay):
        self.grid = Grid()
        self.autolock = Autolock(lock_delay)
        self.tetrominos = [I(), J(), L(), O(), S(), T(), Z()]
        self.current_tetromino = self.get_random_block()
        self.next_tetromino1 = self.get_random_block()
        self.next_tetromino2 = self.get_random_block()
        self.next_tetromino3 = self.get_random_block()
        self.next_tetromino4 = self.get_random_block()
        self.next_tetromino5 = self.get_random_block()
        self.held_tetromino = X()
        self.pre_held = False
        self.I_kicks = Kicks.get_I()
        self.A_kicks = Kicks.get_A()
        self.successful = True
        self.kicked_up = True
        self.game_over = False
        self.score = 0
    
    def get_bumpiness(self):
        bumps = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        bumpiness = 0
        for i in range(self.grid.cols):
            for j in range(self.grid.rows):
                if not self.grid.is_empty(j, i):
                    bumps[i] = (self.grid.rows - j)
                    break
        for i in range(len(bumps) - 1):
            bumpiness += abs(bumps[i] - bumps[i+1])
        return bumpiness
    
    def get_height(self):
        for index, row in enumerate(self.grid.grid):
            if row != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                return self.grid.rows - index
        return 20

    def update_score(self, level, lines, dropped):
        if lines == 1:
            self.score += 100*level
        elif lines == 2:
            self.score += 300*level
        elif lines == 3:
            self.score += 500*level
        elif lines == 4:
            self.score += 800*level
        self.score += dropped

    def get_random_block(self):
        if len(self.tetrominos) == 0:
            self.tetrominos = [I(), J(), L(), O(), S(), T(), Z()]
        tetromino = random.choice(self.tetrominos)
        self.tetrominos.remove(tetromino)
        return tetromino
    
    def reset_autolock(self):
        self.autolock.reset_timer()
    
    def check_autolock(self):
        if self.autolock.check_timer():
            return True
        return False
    
    def increment_autolock(self, inc, touching):
        return self.autolock.increment(inc, touching)
    
    def reset_autolock_counter(self):
        self.autolock.reset_counter()

    def move_left(self):
        self.successful = True
        self.current_tetromino.move(0, -1)
        if self.tetromino_inside() == False or self.tetromino_fits() == False:
            self.current_tetromino.move(0, 1)
            self.successful = False
    
    def move_right(self):
        self.successful = True
        self.current_tetromino.move(0, 1)
        if self.tetromino_inside() == False or self.tetromino_fits() == False:
            self.current_tetromino.move(0, -1)
            self.successful = False
    
    def move_down(self):
        self.successful = True
        self.current_tetromino.move(1, 0)
        if self.tetromino_inside() == False or self.tetromino_fits() == False:
            self.current_tetromino.move(-1, 0)
            self.successful = False
    
    def hard_drop(self):
        lines = 0
        self.move_down()
        if self.successful:
            self.hard_drop()
        else:
            lines = self.lock_tetromino()
            self.pre_held = False
        return lines
    
    def lock_tetromino(self):
        tiles = self.current_tetromino.get_cell_positions()
        for position in tiles:
            if position.row < 0:
                self.game_over = True
            self.grid.grid[position.row][position.col] = self.current_tetromino.id
        self.current_tetromino = self.next_tetromino1
        self.next_tetromino1 = self.next_tetromino2
        self.next_tetromino2 = self.next_tetromino3
        self.next_tetromino3 = self.next_tetromino4
        self.next_tetromino4 = self.next_tetromino5
        self.next_tetromino5 = self.get_random_block()
        lines = self.grid.clear_rows()
        self.update_score(1, lines, 0)
        self.update_score(1, 0, 1)
        self.pre_held = False
        return math.pow(2, lines)
    
    def hold_tetromino(self):
        self.successful = True
        if self.held_tetromino.id == 8:
            self.held_tetromino = self.current_tetromino
            self.held_tetromino.row = -3
            self.held_tetromino.col = 3
            while self.held_tetromino.rotation != 0:
                self.held_tetromino.rotate_cw()
            self.current_tetromino = self.next_tetromino1
            self.next_tetromino1 = self.next_tetromino2
            self.next_tetromino2 = self.next_tetromino3
            self.next_tetromino3 = self.next_tetromino4
            self.next_tetromino4 = self.next_tetromino5
            self.next_tetromino5 = self.get_random_block()
            self.pre_held = True
        else:
            if not self.pre_held:
                self.held_tetromino, self.current_tetromino = self.current_tetromino, self.held_tetromino
                self.held_tetromino.row = -3
                self.held_tetromino.col = 3
                while self.held_tetromino.rotation != 0:
                    self.held_tetromino.rotate_cw()
                self.current_tetromino.row = -3
                self.current_tetromino.col = 3
                while self.current_tetromino.rotation != 0:
                    self.current_tetromino.rotate_cw()
                self.pre_held = True
            else:
                self.successful = False
    
    def tetromino_fits(self):
        tiles = self.current_tetromino.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.col) == False:
                return False
        return True
    
    def tetromino_inside(self):
        tiles = self.current_tetromino.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.col) == False:
                return False
        return True
    
    def touching_floor(self):
        tiles = self.current_tetromino.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row+1, tile.col) == False or self.grid.is_inside(tile.row+1, tile.col) == False:
                return True
        return False

    def rotate_cw(self):
        self.successful = True
        self.current_tetromino.rotate_cw()
        if self.tetromino_inside() == False or self.tetromino_fits() == False:
            if self.current_tetromino.id == 1:
                for test, kick in enumerate(self.I_kicks[0][self.current_tetromino.rotation]):
                    self.current_tetromino.move(kick[0], kick[1])
                    if self.tetromino_inside() == False or self.tetromino_fits() == False:
                        self.current_tetromino.move(-kick[0], -kick[1])
                        if test == 3:
                            self.current_tetromino.rotate_ccw()
                            self.successful = False
                    else:
                        break
            else:
                for test, kick in enumerate(self.A_kicks[0][self.current_tetromino.rotation]):
                    self.current_tetromino.move(kick[0], kick[1])
                    if self.tetromino_inside() == False or self.tetromino_fits() == False:
                        self.current_tetromino.move(-kick[0], -kick[1])
                        if test == 3:
                            self.current_tetromino.rotate_ccw()
                            self.successful = False
                    else:
                        break
    
    def rotate_ccw(self):
        self.successful = True
        self.current_tetromino.rotate_ccw()
        if self.tetromino_inside() == False or self.tetromino_fits() == False:
            if self.current_tetromino.id == 1:
                for test, kick in enumerate(self.I_kicks[1][self.current_tetromino.rotation]):
                    self.current_tetromino.move(kick[0], kick[1])
                    if self.tetromino_inside() == False or self.tetromino_fits() == False:
                        self.current_tetromino.move(-kick[0], -kick[1])
                        if test == 3:
                            self.current_tetromino.rotate_cw()
                            self.successful = False
                    else:
                        break
            else:
                for test, kick in enumerate(self.A_kicks[1][self.current_tetromino.rotation]):
                    self.current_tetromino.move(kick[0], kick[1])
                    if self.tetromino_inside() == False or self.tetromino_fits() == False:
                        self.current_tetromino.move(-kick[0], -kick[1])
                        if test == 3:
                            self.current_tetromino.rotate_cw()
                            self.successful = False
                    else:
                        break

    def draw(self, window):
        self.grid.draw(window)
        self.current_tetromino.draw_ghost(window, self.grid)
        self.current_tetromino.draw(window, 251, 120)
        self.held_tetromino.draw_hold(window)
        next_bg = pygame.Rect(600, 150, 150, 450)
        pygame.draw.rect(window, pygame.Color("Black"), next_bg)
        self.next_tetromino1.draw(window, 520, 250)
        self.next_tetromino2.draw(window, 520, 335)
        self.next_tetromino3.draw(window, 520, 420)
        self.next_tetromino4.draw(window, 520, 505)
        self.next_tetromino5.draw(window, 520, 590)