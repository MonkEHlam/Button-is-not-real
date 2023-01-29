import pygame
import constants
from random import randrange, randint
import Button_class
import Display_class
import Screwdriver_class
import Blink_class
import Timer
import constants


class EventManager:
    def __init__(
        self,
        display: Display_class.Display,
        screwdriver: Screwdriver_class.Screwdriver,
        button: Button_class.Button,
        blink: Blink_class.Blink,
        timer: Timer.Timer
    ) -> None:
        self.display = display
        self.screwdriver = screwdriver
        self.btn = button
        self.blink = blink
        self.timer = timer
        
        self.whisp = pygame.mixer.Sound("sounds/start_word_whisp.ogg")
        
        self.smth_started = False
        self.btn_missed = False
        self.hold_started = False
        self.blink_ctr = 0
        self.words_spawn = False
        self.spawn_buttons = False
        self.need_hold_btn = False
        self.dont_push = False

        self.reserv_btn_events_list = [[self.words, 4, True, 4, 0],]
        self.reserv_blink_events_list = [[self.fake_buttons, 2, True, 5, 0]]
        self.btn_events_list = [
                        # [name of event, ordinal num, is callable, freqency, ctr for freqency]
                        [self.button_stuck, 1, False, 5, 0],
                        [self.hold_btn, 2, True, 2, 0],
                        [self.dont_push_btn, 3, True, 2, 0],
                        [self.radio_crack, 5, False, 8, 0],
                        [self.back_swap, 6, True, 20, 0]
                    ]
        self.blink_events_list = [[self.move_screwdriver, 1, True, 1, 0], [self.miss_btn, 2, False, 3, 0]]
        
        self.blink_event_chanse = len(self.blink_events_list) * 2
        self.btn_event_chanse = len(self.btn_events_list) * 3

    def start_event(self, evtype: int):
        if not self.smth_started:
            if evtype == 1:
                num = randint(1, self.btn_event_chanse)
                for event in self.btn_events_list:
                    if event[1] == num:
                        if event[2]:
                            event[2] = False
                            event[0]()
                            return None
                    if event[2] == False and event[3] != event[4]:
                        event[4] += 1
                    if event[2] == False and event[3] == event[4]:
                        event[4] = 0
                        event[2] = True
            if evtype == 2:
                for event in self.blink_events_list:
                    num = randint(1, self.blink_event_chanse)
                    if event[1] == num:
                        if event[2]:
                            event[2] = False
                            event[0]()
                            return None
                    if event[2] == False and event[3] != event[4]:
                        event[4] += 1
                    if event[2] == False and event[3] == event[4]:
                        event[4] = 0
                        event[2] = True

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
        
        if args and args[0].type == constants.EVENTS["NEWEVENTS"]:
            if self.timer.get_display_time() == "3":
                self.btn_events_list.append(self.reserv_btn_events_list.pop(0))
                self.blink_events_list.append(self.reserv_blink_events_list.pop(0))
                self.blink_event_chanse = len(self.blink_events_list) * 2
                self.btn_event_chanse = len(self.btn_events_list) * 3
            
            if self.timer.get_display_time == "2":
                self.btn_events_list.append(self.reserv_btn_events_list.pop(0))
                self.blink_event_chanse = len(self.blink_events_list) * 2
                self.btn_event_chanse = len(self.btn_events_list) * 3

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

    def radio_crack(self):
        pygame.event.post(pygame.event.Event(constants.EVENTS["RADIOCRACK"]))
    
    def back_swap(self):
        pygame.event.post(pygame.event.Event(constants.EVENTS["BACKSWAP"]))