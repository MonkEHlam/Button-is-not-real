import pygame
import constants
from load_image_func import load_image


class Button(pygame.sprite.Sprite):
    
    def __init__(self, sprite_group, screen, counter):
        super().__init__(sprite_group)
        self.screen = screen
        self.counter = counter

        self.image = load_image('button.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (constants.RESOLUTION[0] * 0.5, constants.RESOLUTION[1] * 0.5)
    
    def update(self, *args) -> None:
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.counter.change_score(1)