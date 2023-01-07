import pygame
import constants
from load_image_func import load_image


class Screwdriver(pygame.sprite.Sprite):
    def __init__(self, sprite_group, screen):
        super().__init__(sprite_group)
        self.screen = screen

        # Load all pictures of sprite
        self.base_image = load_image("screwdriver.png")

        self.image = self.base_image  # Variable for storing the selected image
        self.is_grab = False
        self.rect = self.image.get_rect()

        # Set start position of sprite
        self.rect.center = (
            constants.RESOLUTION[0] * 0.2,
            constants.RESOLUTION[1] * 0.2,
        )

    def update(self, *args) -> None:
        # Check is screwdriver is picked up
        if (
            args
            and args[0].type == pygame.MOUSEBUTTONDOWN
            and self.rect.collidepoint(args[0].pos)
        ):
            self.is_grab = True
        # Check is screwdriver is drop up
        if args and args[0].type == pygame.MOUSEBUTTONUP:
            self.is_grab = False
        # Moving scerdriver if it is picked up
        if self.is_grab:
            self.rect.center = pygame.mouse.get_pos()
