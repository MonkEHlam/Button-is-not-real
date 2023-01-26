import constants
import pygame
import math


class Timer:
    def __init__(self) -> None:
        self.start_time = pygame.time.get_ticks()
        self.current_time = 0
        self.display_time = math.ceil(
            (constants.GAME_DURATION * 1000 - self.current_time) / 1000 / 60
        )

    def change_time(self):
        self.current_time = pygame.time.get_ticks() - self.start_time
        self.display_time = math.ceil(
            (constants.GAME_DURATION * 1000 - self.current_time) / 1000 / 60
        )

    def get_display_time(self) -> str:
        """return str num of remainig minutes round to top"""
        return str(self.display_time)
