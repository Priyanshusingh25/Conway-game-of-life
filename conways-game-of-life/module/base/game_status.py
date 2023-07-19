from enum import Enum


class GameStatus(Enum):
    STARTING = 0
    RUNNING = 1
    PAUSED = 2
    CLOSED = 3
