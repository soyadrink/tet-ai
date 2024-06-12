import pygame
from game import Game
from colours import Colours
import numpy as np

pygame.init()
score_font = pygame.font.Font(None, 50)
other_font = pygame.font.Font(None, 40)

fps = 60000
game_speed = 50
grav_speed = int(1000 / game_speed)
lock_delay = 0.5 / game_speed

gravity = pygame.USEREVENT

class Tetris:
    def __init__(self, width=800, height=800):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("tetris srs+ lmao")
        self.clock = pygame.time.Clock()
        self.reset()
    
    def reset(self):
        self.game = Game(lock_delay)
        pygame.time.set_timer(gravity, grav_speed)
        self.score_rect = pygame.Rect(250, (self.game.grid.rows+4)*self.game.grid.cell_size, self.game.grid.cols*self.game.grid.cell_size, 2*self.game.grid.cell_size)
        self.next_text = other_font.render("next", True, Colours.white)
        self.hold_text = other_font.render("hold", True, Colours.white)
        self.window.blit(self.hold_text, (90, 110, 150, 100))
        self.window.blit(self.next_text, (630, 110, 150, 450))
        self.frame = 0

    def do_action(self, action):
        reward = 0

        # do nothing
        if np.array_equal(action, [1, 0, 0, 0, 0, 0, 0, 0]):
            pass
        
        # left
        elif np.array_equal(action, [0, 1, 0, 0, 0, 0, 0, 0]):
            self.game.move_left()
            if self.game.successful:
                self.game.reset_autolock()
                if self.game.increment_autolock(0, self.game.touching_floor()):
                    if self.game.touching_floor():
                        reward += self.game.lock_tetromino()
                        self.game.reset_autolock()
                        pygame.time.set_timer(gravity, grav_speed)
                        self.game.reset_autolock_counter()

        # right
        elif np.array_equal(action, [0, 0, 1, 0, 0, 0, 0, 0]):
            self.game.move_right()
            if self.game.successful:
                self.game.reset_autolock()
                if self.game.increment_autolock(0, self.game.touching_floor()):
                    if self.game.touching_floor():
                        reward += self.game.lock_tetromino()
                        self.game.reset_autolock()
                        pygame.time.set_timer(gravity, grav_speed)
                        self.game.reset_autolock_counter()

        # clockwise
        elif np.array_equal(action, [0, 0, 0, 1, 0, 0, 0, 0]):
            was_on_floor = self.game.touching_floor()
            self.game.rotate_cw()
            if self.game.successful:
                self.game.reset_autolock()
                if was_on_floor and not self.game.touching_floor():
                    pygame.time.set_timer(gravity, grav_speed)
                if self.game.increment_autolock(1, self.game.touching_floor()):
                    self.game.move_down()
                    if self.game.touching_floor():
                        reward += self.game.lock_tetromino()
                    self.game.reset_autolock()
                    pygame.time.set_timer(gravity, grav_speed)
                    self.game.reset_autolock_counter()
        
        # countercw
        elif np.array_equal(action, [0, 0, 0, 0, 1, 0, 0, 0]):
            was_on_floor = self.game.touching_floor()
            self.game.rotate_ccw()
            if self.game.successful:
                self.game.reset_autolock()
                if was_on_floor and not self.game.touching_floor():
                    pygame.time.set_timer(gravity, grav_speed)
                if self.game.increment_autolock(1, self.game.touching_floor()):
                    self.game.move_down()
                    if self.game.touching_floor():
                        reward += self.game.lock_tetromino()
                    self.game.reset_autolock()
                    pygame.time.set_timer(gravity, grav_speed)
                    self.game.reset_autolock_counter()

        # soft drop
        elif np.array_equal(action, [0, 0, 0, 0, 0, 1, 0, 0]):
            self.game.move_down()
            if self.game.successful:
                self.game.reset_autolock()
                pygame.time.set_timer(gravity, grav_speed)
                self.game.reset_autolock_counter()

        # hard drop
        elif np.array_equal(action, [0, 0, 0, 0, 0, 0, 1, 0]):
            reward += self.game.hard_drop()
            self.game.reset_autolock()
            pygame.time.set_timer(gravity, grav_speed)
            self.game.reset_autolock_counter()
        
        # hold
        elif np.array_equal(action, [0, 0, 0, 0, 0, 0, 0, 1]):
            self.game.hold_tetromino()
            if self.game.successful:
                self.game.reset_autolock()
                pygame.time.set_timer(gravity, grav_speed)
                self.game.reset_autolock_counter()
        
        return reward

    def play_step(self, action):
        self.frame += 1
        reward = self.game.score / 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == gravity:
                self.game.move_down()
                if self.game.successful:
                    self.game.reset_autolock()
                    self.game.reset_autolock_counter()

        if self.game.touching_floor():
            pygame.time.set_timer(gravity, grav_speed)
            if self.game.check_autolock():
                reward += self.game.lock_tetromino()
                self.game.reset_autolock()
                self.game.reset_autolock_counter()
        
        reward += self.do_action(action)
        reward += 2 - (self.game.get_bumpiness() / 10)
        reward += (10 - self.game.get_height()) / 5
        
        if self.game.game_over:
            reward -= 5
            return reward, self.game.game_over, self.game.score

        pygame.draw.rect(self.window, Colours.black, self.score_rect)
        score_surface = score_font.render(str(self.game.score), True, Colours.white)
        self.window.blit(score_surface, score_surface.get_rect(centerx = self.score_rect.centerx, centery = self.score_rect.centery))
        self.game.draw(self.window)
        pygame.display.update()
        self.clock.tick(fps)
        return reward, self.game.game_over, self.game.score