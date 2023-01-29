import pygame
import Button_class
import Display_class
import Screwdriver_class
import Blink_class
import constants
import EventManager
import Radio_class
import Start_button
import Timer
import sys
from load_image_func import load_image
from AnimatedSprite_class import AnimatedSprite
from random import randint, choice, sample, shuffle


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
flags_of_display = pygame.SCALED | pygame.FULLSCREEN

def termianate():
    """Stop programm"""
    pygame.quit()
    sys.exit()


def start_screen(clock):
    """Welcome Window"""

    screen = pygame.display.set_mode(constants.RESOLUTION, flags_of_display)
    group = pygame.sprite.Group()
    btn = Start_button.Button(group, screen)
    text_surface = pygame.font.Font("fonts/dialog.ttf", 30).render(
        "Press space to skip", True, (90, 90, 90)
    )
    text_rect = text_surface.get_rect()
    text_rect.bottomright = (constants.RESOLUTION[0] - 10, constants.RESOLUTION[1])
    text_surface2 = pygame.font.Font("fonts/dialog.ttf", 30).render(
        "Press ESC to exit", True, (90, 90, 90)
    )
    text_rect2 = text_surface2.get_rect()
    text_rect2.bottomleft = (10, constants.RESOLUTION[1])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3 and btn.ready:
                    return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    termianate()
            btn.update(event)
        screen.fill("white")
        group.draw(screen)
        btn.update()
        screen.blit(text_surface, text_rect)
        screen.blit(text_surface2, text_rect2)
        pygame.display.flip()
        clock.tick_busy_loop(constants.FPS)


if __name__ == "__main__":
    constants.EVENTS["DISPLAYTEXTUPDATE"], constants.event_ctr = (
        pygame.USEREVENT + constants.event_ctr,
        constants.event_ctr + 1,
    )

    # Create all groups and objects
    clock = pygame.time.Clock()
    start_screen(clock)
    trash_group = pygame.sprite.Group() # For backsprites
    group_that_not_draw = pygame.sprite.Group() # For self blit sprites
    all_sprites = pygame.sprite.Group() # For sprites? that never move
    blink_group = pygame.sprite.Group() # For blink, that draw last
    fake_buttons_far = pygame.sprite.Group() 
    fake_buttons_close = pygame.sprite.Group()
    pervert_sprites = pygame.sprite.Group() # For sprites, what can move and pervert other sprite action
    screen = pygame.display.set_mode(constants.RESOLUTION, flags_of_display)
    
    button_colors = [i for i in range(10)] # Need for random color of btn
    shuffle(button_colors)

    # Create every base sprites
    timer = Timer.Timer()
    display = Display_class.Display(group_that_not_draw, screen, timer)
    radio = Radio_class.Radio(all_sprites)
    blink = Blink_class.Blink(blink_group)
    screwdriver = Screwdriver_class.Screwdriver(pervert_sprites, blink)
    button = Button_class.Button(
        all_sprites,
        display,
        blink,
        pervert_sprites,
        screwdriver,
        button_colors.pop(),
    )
    em = EventManager.EventManager(display, screwdriver, button, blink, timer)
    bg = load_image("bg.png")
    rain = AnimatedSprite(trash_group, load_image("rain.png"), 7, 5, 0, 0)
    fake_template = load_image("fake_template.png")
    fake_template.set_alpha(0)

    # Create sounds
    whispers = pygame.mixer.Sound("sounds/peak_word_whisp.ogg")
    s_rain = pygame.mixer.Sound("sounds/rain.ogg")
    s_rain.set_volume(0.05)
    s_rain.play(-1)
    s_bg = pygame.mixer.Sound("sounds/bg.ogg")
    s_bg.play(-1)
    s_bg.set_volume(0.5)
    words_group = []

    running = True
    # Add all custom events into dict for easy geting from above
    constants.EVENTS["DISPLAYTEXTUPDATE"], constants.event_ctr = (
        pygame.USEREVENT + constants.event_ctr,
        constants.event_ctr + 1,
    )
    constants.EVENTS["RAINUPDATE"], constants.event_ctr = (
        pygame.USEREVENT + constants.event_ctr,
        constants.event_ctr + 1,
    )
    constants.EVENTS["SCREWDRIVERANIMUPDATE"], constants.event_ctr = (
        pygame.USEREVENT + constants.event_ctr,
        constants.event_ctr + 1,
    )
    constants.EVENTS["WORDSPAWN"], constants.event_ctr = (
        pygame.USEREVENT + constants.event_ctr,
        constants.event_ctr + 1,
    )
    constants.EVENTS["FIXINGSTUCKEDBUTTON"], constants.event_ctr = (
        pygame.USEREVENT + constants.event_ctr,
        constants.event_ctr + 1,
    )
    constants.EVENTS["WAITFORBTN"], constants.event_ctr = (
        pygame.USEREVENT + constants.event_ctr,
        constants.event_ctr + 1,
    )
    constants.EVENTS["HOLDBLINK"], constants.event_ctr = (
        pygame.USEREVENT + constants.event_ctr,
        constants.event_ctr + 1,
    )
    constants.EVENTS["DELETEFAKES"], constants.event_ctr = (
        pygame.USEREVENT + constants.event_ctr,
        constants.event_ctr + 1,
    )
    constants.EVENTS["FORSEDBLINK"], constants.event_ctr = (
        pygame.USEREVENT + constants.event_ctr,
        constants.event_ctr + 1,
    )
    constants.EVENTS["EVENTEND"], constants.event_ctr = (
        pygame.USEREVENT + constants.event_ctr,
        constants.event_ctr + 1,
    )
    constants.EVENTS["WHISPERS"], constants.event_ctr = (
        pygame.USEREVENT + constants.event_ctr,
        constants.event_ctr + 1,
    )
    constants.EVENTS["SCOREDOWN"], constants.event_ctr = (
        pygame.USEREVENT + constants.event_ctr,
        constants.event_ctr + 1,
    )
    constants.EVENTS["NEWEVENTS"], constants.event_ctr = (
        pygame.USEREVENT + constants.event_ctr,
        constants.event_ctr + 1,
    )
    constants.EVENTS["RADIOCRACK"], constants.event_ctr = (
        pygame.USEREVENT + constants.event_ctr,
        constants.event_ctr + 1,
    )
    pygame.time.set_timer(constants.EVENTS["NEWEVENTS"], 50000)
    pygame.time.set_timer(constants.EVENTS["DISPLAYTEXTUPDATE"], 20)
    pygame.time.set_timer(constants.EVENTS["RAINUPDATE"], 40)
    pygame.time.set_timer(constants.EVENTS["WORDSPAWN"], 5)

    while running:
        clock.tick_busy_loop(constants.FPS)
        timer.change_time()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    termianate() 
            if event.type == constants.EVENTS["RAINUPDATE"]:
                rain.update(event)
            if event.type == constants.EVENTS["EVENTEND"]:
                em.smth_started = False
                if em.hold_started:
                    em.hold_started = False
            if em.words_spawn and event.type == constants.EVENTS["WORDSPAWN"]:
                surf = pygame.font.Font("fonts/rough.ttf", randint(20, 100)).render(
                    choice(constants.WORDS_POOL),
                    True,
                    (randint(0, 100), randint(0, 100), randint(0, 100)),
                )
                rectforsurf = surf.get_rect()
                rectforsurf.center = (
                    randint(0, constants.RESOLUTION[0]),
                    randint(0, constants.RESOLUTION[0]),
                )
                words_group.append((surf, rectforsurf))

            if event.type == constants.EVENTS["WHISPERS"]:
                whispers.play(-1)
                pygame.time.set_timer(constants.EVENTS["WHISPERS"], 0)

            if em.words_spawn and blink.holding_blink >= 1600:
                em.words_spawn = False
                words_group.clear()
                em.smth_started = False
                em.whisp.stop()
                whispers.stop()

            if (
                event.type == constants.EVENTS["DELETEFAKES"]
                and fake_buttons_close.sprites()
            ):
                button.set_to_default()
                fake_buttons_far.empty()
                fake_buttons_close.empty()
                fake_template.set_alpha(0)
                blink.no_blink = 5001
                em.smth_started = False
            
            # Update with event 
            em.checker(event)
            group_that_not_draw.update(event)
            all_sprites.update(event)
            fake_buttons_far.update(event)
            fake_buttons_close.update(event)
            pervert_sprites.update(event)
            blink_group.update(event)

        if em.spawn_buttons:
            poses = sample(constants.FAKE_BUTTONS_POS, 10)
            # set pos for main button
            button.rect.topleft = poses[-1]
            if poses[-1][1] == constants.FAKE_BUTTONS_POS[0][1]:
                fake_buttons_far.add(button)
            else:
                fake_buttons_close.add(button)
            # creating fake buttons
            for i in range(9):
                if poses[i][1] == constants.FAKE_BUTTONS_POS[0][1]:
                    b = Button_class.Button(
                        fake_buttons_far,
                        display,
                        blink,
                        pervert_sprites,
                        screwdriver,
                        button_colors[i],
                        True,
                        poses[i],
                    )
                else:
                    b = Button_class.Button(
                        fake_buttons_close,
                        display,
                        blink,
                        pervert_sprites,
                        screwdriver,
                        button_colors[i],
                        True,
                        poses[i],
                    )
            em.spawn_buttons = False
            shuffle(button_colors)
            fake_template.set_alpha(255)

        if not em.words_spawn:
            em.whisp.stop()
            whispers.stop()

        # Check is it time to start new event
        if blink.start_event == True:
            em.start_event(2)
            blink.start_event = False

        if button.start_event == True:
            em.start_event(1)
            button.start_event = False

        
        trash_group.draw(screen)
        screen.blit(bg, (0, 0))
        screen.blit(fake_template, (288, 340))

        # Updating sprites if there is no new events
        em.checker()
        all_sprites.update()
        blink_group.update()
        group_that_not_draw.update()
        pervert_sprites.update()

        # Draw sprites
        all_sprites.draw(screen)
        fake_buttons_far.draw(screen)
        fake_buttons_close.draw(screen)
        pervert_sprites.draw(screen)
        for word in words_group:
            screen.blit(word[0], word[1])
        
        blink_group.draw(screen)

        # Check is game over
        if display.get_score(1) == constants.BUTTON_PUSH_TIMES:
            termianate()
        if timer.get_display_time() == "0":
            termianate()
        pygame.display.flip()
