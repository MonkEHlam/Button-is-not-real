import pygame
import constants
from load_image_func import load_image


class Button(pygame.sprite.Sprite):
    def __init__(self, sprite_group, screen, counter, blink, prevert_sprites):
        super().__init__(sprite_group)
        self.blink = blink
        self.screen = screen
        self.counter = counter
        self.prevert_sprite_group = prevert_sprites
        self.is_touched = False

        # Load all pictures of sprite
        self.upped_image = load_image("button_up.png")
        self.down_image = load_image("button_down.png", -1)

        self.image = self.upped_image  # Variable for storing the selected image
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
            and args[0].button == 1
            and not self.blink.is_blink
            and self.rect.collidepoint(args[0].pos)
            and not pygame.sprite.spritecollideany(self, self.prevert_sprite_group)
        ):
            self.is_touched = True
            self.image = self.down_image
        
        if (
            args
            and args[0].type == pygame.MOUSEBUTTONUP
            and args[0].button == 1
            and self.is_touched
        ):
            self.image = self.upped_image
            self.is_touched = False
            self.counter.change_score(1)

