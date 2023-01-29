import pygame
import constants
from random import choice, randrange
import Button_class
import Display_class
import Screwdriver_class
import Blink_class
import constants


class EventManager:
    def __init__(
        self,
        display: Display_class.Display,
        screwdriver: Screwdriver_class.Screwdriver,
        button: Button_class.Button,
        blink: Blink_class.Blink,
    ) -> None:
        self.display = display
        self.screwdriver = screwdriver
        self.btn = button
        self.blink = blink

        self.smth_started = False
        self.blink_ctr = 0
        self.words_spawn = False
        self.spawn_buttons = False
        self.need_hold_btn = False

        self.blink_event_chanse = [i for i in range(3)]
        self.btn_event_chanse = [i for i in range(3)]

    def start_event(self, evtype: int):
        if not self.smth_started:
            if evtype == 1:
                if choice(self.btn_event_chanse) == max(self.btn_event_chanse):
                    list_of_events = [
                        self.button_stuck,
                        self.hold_btn,
                        self.dont_push_btn,
                        self.words,
                    ]
                    choice(list_of_events)()
                    self.smth_started = True
            if evtype == 2:
                if choice(self.blink_event_chanse) == max(self.blink_event_chanse):
                    list_of_events = [self.move_screwdriver, self.fake_buttons]
                    choice(list_of_events)()
                    self.smth_started = True

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
        self.smth_started = False

    def button_stuck(self):
        if not self.need_hold_btn:
            self.btn.is_stuck = True

    def hold_btn(self):
        self.display.set_display_text("HOLD THE BUTTON")
        self.need_hold_btn = True

    def checker(self):
        if self.need_hold_btn and not self.btn.is_touched:
            self.btn.need_hold_btn = True
            self.btn.hold_started = True
            self.need_hold_btn = False

        # print(self.btn.need_hold_btn, 0 < self.btn.holding_btn < 1000, not self.btn.is_touched, self.btn.hold_started)
        if (
            self.btn.need_hold_btn
            and 0 < self.btn.holding_btn < 1000
            and not self.btn.is_touched
            and self.btn.hold_started
        ):
            self.turn_down_score(-3)
            self.btn.set_to_default()
            self.display.set_display_text("PUSH THE BUTTON")
            self.btn.need_hold_btn = False

        if self.btn.dont_push and self.btn.is_touched:
            self.turn_down_score(-3)
            pygame.time.set_timer(constants.EVENTS["WAITFORBTN"], 0)
            self.btn.dont_push = False
            self.display.set_display_text("PUSH THE BUTTON")
            self.smth_started = False

    def turn_down_score(self, shift: int):
        self.display.change_score(shift)

    def dont_push_btn(self):
        self.display.set_display_text("DON'T PUSH THE BUTTON")
        self.btn.dont_push = True
        pygame.time.set_timer(constants.EVENTS["WAITFORBTN"], 2000)

    def words(self):
        self.words_spawn = True
        whisp = pygame.mixer.Sound("sounds/start_word_whisp.ogg")
        whisp.set_volume(1)
        whisp.play()
        pygame.time.set_timer(
            constants.EVENTS["WHISPERS"], int(whisp.get_length() * 1000)
        )

    def fake_buttons(self):
        if not self.btn.is_stuck and self.btn.dont_push:
            self.spawn_buttons = True
            self.btn.fakes = True
