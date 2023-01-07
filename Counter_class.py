import pygame
import constants
from load_image_func import load_image


class Counter(pygame.sprite.Sprite):
    font_name = pygame.font.match_font("arial")

    def __init__(self, sprite_group, screen) -> None:
        super().__init__(sprite_group)
        self.screen = screen

        # Load all pictures of sprite
        self.base_image = load_image("counter.png")

        self.image = self.base_image  # Variable for storing the selected image
        self.score = 0
        self.rect = self.image.get_rect()

        # Set start position of sprite
        self.rect.center = (
            constants.RESOLUTION[0] * 0.5,
            constants.RESOLUTION[1] * 0.2,
        )

    def change_score(self, shift):
        self.score += shift
        if self.get_score() < 0:
            self.score = 0

    def get_score(self):
        return self.score

    def update(self, *args, **kwargs) -> None:
        # Creating of textbox for score of counter
        font = pygame.font.Font(self.font_name, 30)
        text_surface = font.render(str(self.get_score()), True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (
            self.rect.centerx,
            self.rect.centery,
        )  # Set position of textbox at the center of counter spriteS
        self.screen.blit(text_surface, text_rect)
