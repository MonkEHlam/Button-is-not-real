import pygame
import constants
import Display_class
import Screwdriver_class
import Blink_class
import constants
from load_image_func import load_image


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        sprite_group: pygame.sprite.Group,
        display: Display_class.Display,
        blink: Blink_class.Blink,
        prevert_sprites: pygame.sprite.Group,
        screwdriver: Screwdriver_class.Screwdriver,
        color_num: int,
        is_fake=False,
        pos=(),
    ):
        super().__init__(sprite_group)
        self.blink = blink
        self.display = display
        self.prevert_sprite_group = prevert_sprites
        self.screwdriver = screwdriver
        self.is_fake = is_fake
        
        self.no_push = 0
        self.flag = True
        self.is_broken = False
        self.is_touched = False
        self.is_stuck = False
        self.fix_started = False
        self.need_hold_btn = False
        self.start_event = False
        self.start_time = pygame.time.get_ticks()
        self.holding_btn = 0

        # Load all pictures of sprite
        self.upped_image = load_image(f"buttons/btn{color_num}.png")
        self.down_image = load_image(f"buttons/pbtn{color_num}.png")

        self.image = self.upped_image  # Variable for storing the selected image
        self.rect = self.image.get_rect()

        self.s_push = pygame.mixer.Sound("sounds/push.ogg")
        self.s_push.set_volume(0.5)
        self.s_unpush = pygame.mixer.Sound("sounds/unpush.ogg")
        self.s_unpush.set_volume(0.5)

        # Set start position of sprite
        if not pos:
            self.rect.topleft = constants.BUTTON_POS
        else:
            self.rect.topleft = pos

    def set_to_default(self, base=True, s=True):
        """return btn into default settings"""
        self.start_time = pygame.time.get_ticks()
        self.rect.topleft = constants.BUTTON_POS
        self.upped_image.set_alpha(255)
        self.down_image.set_alpha(255)
        self.image = self.upped_image
        self.no_push = 0
        self.holding_btn = 0
        self.flag = True
        self.is_touched = False
        
        if not base:
            self.is_broken = False
            self.is_stuck = False
            self.fix_started = False
        if s:
            self.s_unpush.play()
        

    def update(self, *args) -> None:
        # Next three conditions checking is button was fixed from some event
        if args and args[0].type == constants.EVENTS["FIXINGSTUCKEDBUTTON"]:
            self.set_to_default(False)
            self.display.change_score(1)
            pygame.time.set_timer(constants.EVENTS["SCOREDOWN"], 0)
            pygame.time.set_timer(constants.EVENTS["FIXINGSTUCKEDBUTTON"], 0)
            pygame.event.post(pygame.event.Event(constants.EVENTS["EVENTEND"]))

        if self.need_hold_btn and self.holding_btn > 1000:
            self.need_hold_btn = False
            self.display.set_display_text("PUSH THE BUTTON")
            pygame.event.post(pygame.event.Event(constants.EVENTS["EVENTEND"]))
            print(1)

        # Start fixing button from stucking
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
            and not self.is_broken
            and not self.is_touched
            and not self.blink.is_blink
            and self.rect.collidepoint(args[0].pos)
            and not pygame.sprite.spritecollideany(self, self.prevert_sprite_group)
        ):
            self.is_touched = True
            pygame.time.set_timer(constants.EVENTS["SCOREDOWN"], 0)
            self.rect.y += self.image.get_height() - self.down_image.get_height()
            self.image = self.down_image
            self.s_push.play()
            self.start_time = pygame.time.get_ticks()

        if (
            args
            and args[0].type == pygame.MOUSEBUTTONUP
            and args[0].button == 1
            and self.is_touched
            and not self.is_stuck
            and not self.is_broken
        ):
            self.set_to_default()
            
            if not self.is_fake:
                self.display.change_score(1)
                self.start_event = True
                pygame.event.post(pygame.event.Event(constants.EVENTS["DELETEFAKES"]))
            else:
                pygame.event.post(pygame.event.Event(constants.EVENTS["DELETEFAKES"]))
                self.display.change_score(-3)

        # Count time of holding or not pushing
        if self.is_touched and self.holding_btn > 1500:
            self.no_push = pygame.time.get_ticks() - self.start_time
        elif self.is_touched:
            self.holding_btn = pygame.time.get_ticks() - self.start_time
        else:
            self.no_push = pygame.time.get_ticks() - self.start_time

        # Start punish for not pushing
        if self.no_push > 2100 and self.flag:
            pygame.time.set_timer(constants.EVENTS["SCOREDOWN"], 1000)
            self.flag = False
