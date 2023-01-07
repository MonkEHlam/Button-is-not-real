import pygame
import constants
from load_image_func import load_image


class Button(pygame.sprite.Sprite):
    def __init__(self, sprite_group, screen, counter, movable_sprites):
        super().__init__(sprite_group)
        self.screen = screen
        self.counter = counter
        self.prevert_sprite_group = movable_sprites

        # Load all pictures of sprite
        self.upped_image = load_image("button.png")
        
        self.image = self.upped_image # Variable for storing the selected image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # Set start position of sprite
        self.rect.center = (
            constants.RESOLUTION[0] * 0.5,
            constants.RESOLUTION[1] * 0.5,
        )

    def update(self, *args) -> None:
        if (
            args
            and args[0].type == pygame.MOUSEBUTTONDOWN
            and self.rect.collidepoint(args[0].pos)
            and not pygame.sprite.spritecollideany(self, self.prevert_sprite_group)
        ):
            self.counter.change_score(1)
