from tetromino import Tetromino
from position import Position

class I(Tetromino):
    def __init__(self):
        super().__init__(id=1)
        self.cells = {
            0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],
            1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],
            2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
            3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]
        }
        self.move(-3, 3)

class J(Tetromino):
    def __init__(self):
        super().__init__(id=2)
        self.cells = {
            0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],
            3: [Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]
        }
        self.move(-3, 3)

class L(Tetromino):
    def __init__(self):
        super().__init__(id=3)
        self.cells = {
            0: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
			1: [Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],
			2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0)],
			3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)]
        }
        self.move(-3, 3)

class O(Tetromino):
    def __init__(self):
        super().__init__(id=4)
        self.cells = {
            0: [Position(0, 1), Position(0, 2), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(1, 2)],
            2: [Position(0, 1), Position(0, 2), Position(1, 1), Position(1, 2)],
            3: [Position(0, 1), Position(0, 2), Position(1, 1), Position(1, 2)],
        }
        self.move(-3, 3)

class S(Tetromino):
    def __init__(self):
        super().__init__(id=5)
        self.cells = {
            0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
            2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
            3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(-3, 3)

class T(Tetromino):
    def __init__(self):
        super().__init__(id=6)
        self.cells = {
            0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(-3, 3)

class Z(Tetromino):
    def __init__(self):
        super().__init__(id=7)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
            1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]
        }
        self.move(-3, 3)

class X(Tetromino):
    def __init__(self):
        super().__init__(id=8)
        self.cells = {
            0: [Position(0, 0), Position(0, 0), Position(0, 0), Position(0, 0)],
            1: [Position(0, 0), Position(0, 0), Position(0, 0), Position(0, 0)],
            2: [Position(0, 0), Position(0, 0), Position(0, 0), Position(0, 0)],
            3: [Position(0, 0), Position(0, 0), Position(0, 0), Position(0, 0)]
        }
        self.move(-3, 3)