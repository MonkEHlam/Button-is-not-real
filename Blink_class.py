import pygame
import constants
from load_image_func import load_image


class Blink(pygame.sprite.Sprite):
    def __init__(self, sprite_group):
        super().__init__(sprite_group)
        self.is_blink = False
        self.transperency = 0
        self.start_event = False
        self.holding_blink = 0
        self.forced = False
        self.no_blink = 0
        self.start_time = 0

        # Load all pictures of sprite
        self.blinked_image = load_image("blink.png")

        self.image = self.blinked_image  # Variable for storing the selected image

        self.rect = self.image.get_rect()

        # Set start position of sprite
        self.rect.center = (
            constants.RESOLUTION[0] * 0.5,
            constants.RESOLUTION[1] * 0.5,
        )

        self.image.set_alpha(self.transperency)

    def set_to_default(self):
        self.is_blink = False
        self.transperency = 0
        self.start_event = False
        self.holding_blink = 0
        self.forced = False
        self.no_blink = 0
        self.start_time = pygame.time.get_ticks()
        self.image.set_alpha(self.transperency)

    def update(self, *args) -> None:
        # Forced blink
        if self.no_blink > 5500:
            self.forced = True
            self.start_time = pygame.time.get_ticks()

        if args and args[0].type == pygame.MOUSEBUTTONDOWN and args[0].button == 3:
            self.is_blink = True
            self.start_time = pygame.time.get_ticks()

        if args and args[0].type == pygame.MOUSEBUTTONUP and args[0].button == 3:
            self.set_to_default()

        if self.forced:
            if self.holding_blink < 100:
                self.is_blink = True
            else:
                self.set_to_default()

        if self.is_blink:
            self.transperency += 15
            self.image.set_alpha(self.transperency)

        # Full blink is cause of event
        if self.transperency == 255:
            self.start_event = True

        # Count time of holding or not blinking
        if self.is_blink and self.transperency >= 255:
            self.holding_blink = pygame.time.get_ticks() - self.start_time
        else:
            self.no_blink = pygame.time.get_ticks() - self.start_time
