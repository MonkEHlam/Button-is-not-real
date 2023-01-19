import pygame
import constants
from load_image_func import load_image


class Button(pygame.sprite.Sprite):
    def __init__(
        self, sprite_group, screen, display, blink, prevert_sprites, screwdriver, is_fake=False, pos=()
    ):
        super().__init__(sprite_group)
        self.blink = blink
        self.screen = screen
        self.display = display
        self.prevert_sprite_group = prevert_sprites
        self.screwdriver = screwdriver
        self.is_fake = is_fake

        self.is_touched = False
        self.is_stuck = False
        self.need_hold_btn = False
        self.start_event = False
        self.fix_started = False
        self.dont_push = False
        
        # Load all pictures of sprite
        self.upped_image = load_image("base_btn.png")
        self.down_image = load_image("pushed_btn.png")

        self.image = self.upped_image  # Variable for storing the selected image
        self.rect = self.image.get_rect()

        # Set start position of sprite
        if not pos:
            self.rect.topleft = constants.BUTTON_POS
        else:
            self.rect.topleft = pos

    def set_to_default(self):
        self.rect.topleft = constants.BUTTON_POS
        self.image = self.upped_image
        self.is_touched = False
        self.is_stuck = False
        self.need_hold_btn = False
        self.start_event = False
        self.fix_started = False
        self.dont_push = False
        self.fakes = False

        if self.rect.topleft == constants.BUTTON_POS:
            print(1)
        

    def update(self, *args) -> None:
        if args and args[0].type == constants.EVENTS["FIXINGSTUCKEDBUTTON"]:
            self.set_to_default()
            self.display.change_score(1)
            pygame.time.set_timer(constants.EVENTS["FIXINGSTUCKEDBUTTON"], 0)

        if args and args[0].type == constants.EVENTS["WAITFORBTN"]:
            self.set_to_default()
            self.display.set_display_text("PUSH THE BUTTON")
            pygame.time.set_timer(constants.EVENTS["WAITFORBTN"], 0)

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
            self.rect.y += (
                self.image.get_height() - self.down_image.get_height()
            )
            self.image = self.down_image

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
            if not self.is_fake:
                self.display.change_score(1)
                self.start_event = True
            else:
                pygame.event.post(pygame.event.Event(constants.EVENTS["DELETEFAKES"]))
                self.display.change_score(-3)
