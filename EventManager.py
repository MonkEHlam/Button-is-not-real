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
        
        self.whisp = pygame.mixer.Sound("sounds/start_word_whisp.ogg")
        
        self.smth_started = False
        self.btn_missed = False
        self.hold_started = False
        self.blink_ctr = 0
        self.words_spawn = False
        self.spawn_buttons = False
        self.need_hold_btn = False
        self.dont_push = False

        self.blink_event_chanse = [i for i in range(5)]
        self.btn_event_chanse = [i for i in range(3)]

    def start_event(self, evtype: int):
        if not self.smth_started:
            if evtype == 1:
                if choice(self.btn_event_chanse) == max(self.btn_event_chanse):
                    list_of_events = [
                        self.button_stuck,
                        self.hold_btn,
                        self.dont_push_btn,
                        self.words
                    ]
                    choice(list_of_events)()
            if evtype == 2:
                if choice(self.blink_event_chanse) == max(self.blink_event_chanse):
                    list_of_events = [self.move_screwdriver, self.fake_buttons, self.miss_btn]
                    choice(list_of_events)()

    def end_event(self):
        pygame.event.post(pygame.event.Event(constants.EVENTS["EVENTEND"]))

    def checker(self, *args):
        """Check all conditions of events"""
        if self.dont_push and self.btn.is_touched:
            self.turn_down_score(-3)
            self.display.set_display_text("PUSH THE BUTTON")
            self.dont_push = False
            self.end_event()

        if args and args[0].type == constants.EVENTS["WAITFORBTN"] and self.dont_push:
            self.dont_push = False
            self.display.set_display_text("PUSH THE BUTTON")
            pygame.time.set_timer(constants.EVENTS["WAITFORBTN"], 0)
            self.end_event()

        if self.need_hold_btn and not self.hold_started and self.btn.is_touched:
            print(1)
            self.btn.need_hold_btn = True
            self.hold_started = True
            self.need_hold_btn = False
        
        if self.hold_started and not self.btn.is_touched:
            self.smth_started = False
            self.hold_started = False
            self.turn_down_score(-3)
            self.btn.need_hold_btn = False
            print(2)
            self.display.set_display_text("PUSH THE BUTTON")
        
        if self.btn_missed and self.blink.holding_blink > 1500:
            self.btn.set_to_default(False, False)
            self.btn_missed = False
            self.smth_started = False
            self.btn.is_broken = False
        
    def turn_down_score(self, shift: int):
        self.display.change_score(shift)

    # all of functions next is functions of events
    def dont_push_btn(self):
        self.display.set_display_text("DON'T PUSH THE BUTTON")
        self.dont_push = True
        pygame.time.set_timer(constants.EVENTS["WAITFORBTN"], 1500)
        self.smth_started = True

    def words(self):
        self.words_spawn = True
        
        self.whisp.set_volume(1)
        self.whisp.play()
        pygame.time.set_timer(
            constants.EVENTS["WHISPERS"], int(self.whisp.get_length() * 1000)
        )

    def fake_buttons(self):
        self.spawn_buttons = True
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

    def button_stuck(self):
        self.btn.is_stuck = True
        self.smth_started = True

    def hold_btn(self):
        self.display.set_display_text("HOLD THE BUTTON")
        self.need_hold_btn = True
        self.smth_started = True
    
    def miss_btn(self):
        self.btn_missed = True
        self.smth_started = True
        self.btn.is_broken = True
        self.btn.image.set_alpha(0)
