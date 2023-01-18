import pygame
import constants
from load_image_func import load_image


class Blink(pygame.sprite.Sprite):
    def __init__(self, sprite_group, screen):
        super().__init__(sprite_group)
        self.screen = screen
        self.is_blink = False
        self.transperency = 0
        self.start_event = False

        constants.EVENTS["HOLDBLINK"], constants.event_ctr = (
            pygame.USEREVENT + constants.event_ctr,
            constants.event_ctr + 1,
        )

        # Load all pictures of sprite
        self.blinked_image = load_image("blink.png")

        self.image = self.blinked_image  # Variable for storing the selected image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # Set start position of sprite
        self.rect.center = (
            constants.RESOLUTION[0] * 0.5,
            constants.RESOLUTION[1] * 0.5,
        )

        self.image.set_alpha(self.transperency)

    def update(self, *args) -> None:
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and args[0].button == 3:
            self.is_blink = True

        if args and args[0].type == pygame.MOUSEBUTTONUP and args[0].button == 3:
            self.is_blink = False
            self.transperency = 0
            self.image.set_alpha(self.transperency)

        if self.is_blink:
            self.transperency += 25
            self.image.set_alpha(self.transperency)

        if self.transperency == 250:
            self.start_event = True
            pygame.time.set_timer(constants.EVENTS["HOLDBLINK"], 1500)
