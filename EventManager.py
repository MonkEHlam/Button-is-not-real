import pygame
import constants
from random import choice, randrange


class EventManager:
    def __init__(self, screen, display, screwdriver, button, blink) -> None:
        self.screen = screen
        self.display = display
        self.screwdriver = screwdriver
        self.btn = button
        self.blink = blink

        self.blink_ctr = 0
        self.words_spawn = False
        self.spawn_buttons = False
        self.need_hold_btn = False

        self.blink_event_chanse = [i for i in range(4)]
        self.btn_event_chanse = [i for i in range(3)]

    def start_event(self, evtype: int):
        if evtype == 1:
            if choice(self.btn_event_chanse) == max(self.btn_event_chanse):
                list_of_events = [
                    self.button_stuck,
                    self.hold_btn,
                    self.dont_push_btn,
                    self.words,
                ]
                choice(list_of_events)()
        if evtype == 2:
            if choice(self.blink_event_chanse) == max(self.blink_event_chanse):
                list_of_events = [self.move_screwdriver, self.fake_buttons]
                choice(list_of_events)()

    def move_screwdriver(self):
        self.screwdriver.image = pygame.transform.rotate(
            self.screwdriver.image, randrange(-180, 180)
        )
        self.screwdriver.rect = self.screwdriver.image.get_rect()
        self.screwdriver.image.set_alpha(60)
        self.screwdriver.rect.bottomright = (
            randrange(constants.RESOLUTION[0]),
            randrange(338, constants.RESOLUTION[1]),
        )
        print(self.screwdriver.rect.topleft)

    def button_stuck(self):
        if not self.need_hold_btn:
            self.btn.is_stuck = True

    def hold_btn(self):
        self.display.set_display_text("HOLD THE BUTTON")
        self.need_hold_btn = True

    def checker(self):
        if self.need_hold_btn and self.btn.is_touched:
            self.need_hold_btn = False
            self.btn.need_hold_btn = True
            pygame.time.set_timer(constants.EVENTS["WAITFORBTN"], 1200)
            self.btn.fix_started = True

        if (
            self.btn.need_hold_btn
            and self.btn.is_touched == False
            and self.btn.fix_started == True
        ):
            self.turn_down_score(-3)
            pygame.time.set_timer(constants.EVENTS["WAITFORBTN"], 0)
            self.btn.need_hold_btn = False
            self.btn.fix_started = False
            self.display.set_display_text("PUSH THE BUTTON")

        if self.btn.dont_push and self.btn.is_touched:
            self.turn_down_score(-3)
            pygame.time.set_timer(constants.EVENTS["WAITFORBTN"], 0)
            self.btn.dont_push = False
            self.display.set_display_text("PUSH THE BUTTON")

    def turn_down_score(self, shift: int):
        self.display.change_score(shift)

    def dont_push_btn(self):
        self.display.set_display_text("DON'T PUSH THE BUTTON")
        self.btn.dont_push = True
        pygame.time.set_timer(constants.EVENTS["WAITFORBTN"], 2000)

    def words(self):
        self.words_spawn = True

    def fake_buttons(self):
        self.spawn_buttons = True
        self.btn.fakes = True