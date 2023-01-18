import pygame
import constants
from load_image_func import load_image


class Display(pygame.sprite.Sprite):
    def __init__(self, sprite_group, screen: pygame.Surface) -> None:
        super().__init__(sprite_group)
        self.screen = screen
        self.font = pygame.font.Font("fonts/digital.ttf", 36)
        # Load all pictures of sprite
        self.base_image = load_image("display.png")

        self.image = self.base_image  # Variable for storing the selected image
        self.score = 0
        self.display_text = "PUSH THE BUTTON"
        self.display_text_on_screen = ""
        self.text_number = 0

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = constants.DISPLAY_POS

    def change_score(self, shift):
        self.score += shift
        if self.get_score(1) < 0:
            self.score = 0

    def get_score(self, is_int=0) -> str:
        if is_int:
            return self.score
        score = int(self.score)
        if score < 10:
            return "00" + str(score)
        if score < 100:
            return "0" + str(score)
        return str(score)

    def set_display_text(self, text):
        self.display_text = text
        self.display_text_on_screen = ""
        self.text_number = 0

    def update_display_text(self):
        self.display_text_on_screen += self.display_text[self.text_number]
        self.text_number += 1

    def get_display_text(self) -> str:
        return self.display_text_on_screen

    def update(self, *args, **kwargs) -> None:
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        # Update counter of pushes
        counter_surface = self.font.render(self.get_score(), True, (113, 130, 139))
        counter_rect = counter_surface.get_rect()

        # Set position of counter's textbox
        counter_rect.top = self.rect.y + 20
        counter_rect.centerx = self.rect.centerx

        self.screen.blit(counter_surface, counter_rect)

        # Update display text
        if args and self.display_text != self.display_text_on_screen:
            self.update_display_text()
        text_surface = self.font.render(self.get_display_text(), True, (113, 130, 139))
        text_rect = text_surface.get_rect()
        # Set position of text's textbox
        text_rect.center = self.rect.center
        self.screen.blit(text_surface, text_rect)