import pygame
import constants
from load_image_func import load_image


class Button(pygame.sprite.Sprite):
    def __init__(
        self, sprite_group, screen, display, blink, prevert_sprites, screwdriver
    ):
        super().__init__(sprite_group)
        self.blink = blink
        self.screen = screen
        self.display = display
        self.prevert_sprite_group = prevert_sprites
        self.screwdriver = screwdriver

        self.is_touched = False
        self.is_stuck = False
        self.need_hold_btn = False
        self.start_event = False
        self.fix_started = False
        self.dont_push = False

        constants.EVENTS["FIXINGSTUCKEDBUTTON"], constants.event_ctr = (
            pygame.USEREVENT + constants.event_ctr,
            constants.event_ctr + 1,
        )
        # Load all pictures of sprite
        self.upped_image = load_image("base_btn.png")
        self.down_image = load_image("pushed_btn.png")

        self.image = self.upped_image  # Variable for storing the selected image
        self.rect = self.image.get_rect()

        # Set start position of sprite
        self.rect.x, self.rect.y = constants.BUTTON_POS

    def update(self, *args) -> None:
        if args and args[0].type == constants.EVENTS["FIXINGSTUCKEDBUTTON"]:
            self.image = self.upped_image
            self.rect.y = constants.BUTTON_POS[1]
            self.is_stuck = False
            self.is_touched = False
            self.screwdriver.fixing = False
            self.display.change_score(1)
            pygame.time.set_timer(constants.EVENTS["FIXINGSTUCKEDBUTTON"], 0)

        if args and args[0].type == constants.EVENTS["WAITFORBTN"]:
            if self.need_hold_btn == True:
                self.need_hold_btn = False
                self.is_touched = False
                self.image = self.upped_image
                self.rect.y = constants.BUTTON_POS[1]

            self.dont_push = False
            self.display.set_display_text("PUSH THE BUTTON")
            pygame.time.set_timer(constants.EVENTS["WAITFORBTN"], 0)
            self.fix_started = False

        if (
            not self.fix_started
            and self.is_stuck
            and pygame.sprite.spritecollideany(self, self.prevert_sprite_group)
            and not self.screwdriver.is_grab
        ):
            pygame.time.set_timer(constants.EVENTS["FIXINGSTUCKEDBUTTON"], 1500)
            self.fix_started = True
            pygame.time.set_timer(constants.EVENTS["SCREWDRIVERANIMUPDATE"], 70)

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
            self.rect.y = constants.BUTTON_POS[1] + (
                self.upped_image.get_height() - self.down_image.get_height()
            )

        if (
            args
            and args[0].type == pygame.MOUSEBUTTONUP
            and args[0].button == 1
            and self.is_touched
            and not self.is_stuck
        ):
            self.image = self.upped_image
            self.rect.y = constants.BUTTON_POS[1]
            self.is_touched = False
            self.display.change_score(1)
            self.start_event = True
