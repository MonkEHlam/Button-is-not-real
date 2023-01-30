import pygame
import constants
from load_image_func import load_image


class Button(pygame.sprite.Sprite):
    def __init__(self, group, screen):
        super().__init__(group)
        self.ready = False
        self.screen = screen
        self.is_touched = False
        self.words = [
            "Hey!",
            "Wonna get some easy money?",
            "See this button?",
            "Push it by left mouse button",
            "Nicly done!",
            "You are ready to work!",
            "Push it a couple more times and click left mouse button to start",
        ]
        self.word_num = 0
        self.text_on = "Hey"

        self.f = pygame.font.Font("fonts/dialog.ttf", 30)

        self.upped_image = load_image("buttons/sbtn.png")
        self.down_image = load_image("buttons/spbtn.png")

        self.image = self.upped_image  # Variable for storing the selected image
        self.rect = self.image.get_rect()

        self.s_push = pygame.mixer.Sound("sounds/push.ogg")
        self.s_push.set_volume(0.5)
        self.s_unpush = pygame.mixer.Sound("sounds/unpush.ogg")
        self.s_unpush.set_volume(0.5)

        # Set start position of sprite
        self.rect.topleft = constants.BUTTON_POS

        pygame.time.set_timer(constants.EVENTS["DISPLAYTEXTUPDATE"], 1500)

    def update(self, *args) -> None:
        if args and args[0].type == constants.EVENTS["DISPLAYTEXTUPDATE"]:
            self.word_num += 1
            if self.word_num == 3:
                self.text_on = self.words[self.word_num]
                pygame.time.set_timer(constants.EVENTS["DISPLAYTEXTUPDATE"], 0)
            elif self.word_num == 7:
                self.ready = True
            else:
                if self.word_num < 7:
                    self.text_on = self.words[self.word_num]
                    pygame.time.set_timer(constants.EVENTS["DISPLAYTEXTUPDATE"], 1500)

        if self.word_num >= 3:
            if (
                args
                and args[0].type == pygame.MOUSEBUTTONDOWN
                and args[0].button == 1
                and self.rect.collidepoint(args[0].pos)
            ):
                self.is_touched = True
                self.rect.y += self.image.get_height() - self.down_image.get_height()
                self.image = self.down_image
                self.s_push.play()

            if (
                args
                and args[0].type == pygame.MOUSEBUTTONUP
                and args[0].button == 1
                and self.is_touched
            ):
                self.rect.topleft = constants.BUTTON_POS
                self.image = self.upped_image
                self.s_unpush.play()
                self.is_touched = False
                if self.word_num == 3:
                    pygame.event.post(
                        pygame.event.Event(constants.EVENTS["DISPLAYTEXTUPDATE"])
                    )

        # Create text
        text_surface = self.f.render(self.text_on, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        # Set position of textbox
        text_rect.center = (
            constants.RESOLUTION[0] * 0.5,
            constants.RESOLUTION[1] * 0.3,
        )
        self.screen.blit(text_surface, text_rect)
