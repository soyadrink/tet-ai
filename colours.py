import pygame

class Colours:
    grey30 = pygame.Color("grey30")
    cyan = pygame.Color("cyan")
    blue = pygame.Color("blue")
    orange = pygame.Color("orange")
    yellow = pygame.Color("yellow")
    green = pygame.Color("green")
    purple = pygame.Color("purple")
    red = pygame.Color("red")
    black = pygame.Color("black")
    white = pygame.Color("white")

    @classmethod
    def get_cell_colours(cls):
        return [cls.grey30, cls.cyan, cls.blue, cls.orange, cls.yellow, cls.green, cls.purple, cls.red, cls.black, cls.white]