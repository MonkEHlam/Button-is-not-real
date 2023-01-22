import pygame
import Button_class
import Display_class
import Screwdriver_class
import Blink_class
import constants
import EventManager
from load_image_func import load_image
from AnimatedSprite_class import AnimatedSprite
from random import randint, choice, sample, shuffle

if __name__ == "__main__":
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    trash_group = pygame.sprite.Group()
    group_that_not_draw = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    blink_group = pygame.sprite.Group()
    movable_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode(constants.RESOLUTION)
    clock = pygame.time.Clock()
    button_colors = [i for i in range(10)]
    shuffle(button_colors)

    # Create every base sprites
    display = Display_class.Display(group_that_not_draw, screen)
    blink = Blink_class.Blink(blink_group, screen)
    screwdriver = Screwdriver_class.Screwdriver(movable_sprites, screen, blink)
    button = Button_class.Button(
        all_sprites,
        screen,
        display,
        blink,
        movable_sprites,
        screwdriver,
        button_colors.pop(),
    )
    em = EventManager.EventManager(screen, display, screwdriver, button, blink)
    bg = load_image("bg.png")
    pygame.mixer.Sound("sounds/bg.ogg").play()
    fake_template = load_image("fake_template.png")
    fake_template.set_alpha(0)
    rain = AnimatedSprite(trash_group, load_image("rain.png"), 7, 5, 0, 0)
    pygame.mixer.music.load("sounds/rain.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    words_group = []
    fake_buttons_far = pygame.sprite.Group()
    fake_buttons_close = pygame.sprite.Group()
    running = True

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

    pygame.time.set_timer(constants.EVENTS["DISPLAYTEXTUPDATE"], 20)
    pygame.time.set_timer(constants.EVENTS["RAINUPDATE"], 40)
    pygame.time.set_timer(constants.EVENTS["WORDSPAWN"], 5)
    pygame.time.set_timer(constants.EVENTS["FORSEDBLINK"], 3500)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == constants.EVENTS["DISPLAYTEXTUPDATE"]:
                display.update(event)
            if event.type == constants.EVENTS["RAINUPDATE"]:
                rain.update(event)
            if em.words_spawn and event.type == constants.EVENTS["WORDSPAWN"]:
                surf = pygame.font.Font("fonts/rough.ttf", randint(20, 70)).render(
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
            if (
                em.words_spawn
                and blink.is_blink
                and event.type == constants.EVENTS["HOLDBLINK"]
            ):
                em.words_spawn = False
                words_group.clear()

            if (
                event.type == constants.EVENTS["DELETEFAKES"]
                and fake_buttons_close.sprites()
            ):
                button.set_to_default()
                fake_buttons_far.empty()
                fake_buttons_close.empty()
                fake_template.set_alpha(0)

            all_sprites.update(event)
            fake_buttons_far.update(event)
            fake_buttons_close.update(event)
            movable_sprites.update(event)
            blink_group.update(event)

        if em.spawn_buttons:
            poses = sample(constants.FAKE_BUTTONS_POS, 10)
            button.rect.topleft = poses[-1]
            if poses[-1][1] == constants.FAKE_BUTTONS_POS[0][1]:
                fake_buttons_far.add(button)
            else:
                fake_buttons_close.add(button)
            for i in range(9):
                if poses[i][1] == constants.FAKE_BUTTONS_POS[0][1]:
                    b = Button_class.Button(
                        fake_buttons_far,
                        screen,
                        display,
                        blink,
                        movable_sprites,
                        screwdriver,
                        button_colors[i],
                        True,
                        poses[i],
                    )
                else:
                    b = Button_class.Button(
                        fake_buttons_close,
                        screen,
                        display,
                        blink,
                        movable_sprites,
                        screwdriver,
                        button_colors[i],
                        True,
                        poses[i],
                    )
            em.spawn_buttons = False
            shuffle(button_colors)
            fake_template.set_alpha(255)

        if blink.start_event == True:
            em.start_event(2)
            blink.start_event = False
        if button.start_event == True:
            em.start_event(1)
            button.start_event = False

        em.checker()
        trash_group.draw(screen)
        screen.blit(bg, (0, 0))
        screen.blit(fake_template, (288, 340))

        # updating sprites if there is no new events
        all_sprites.update()
        blink_group.update()
        group_that_not_draw.update()
        movable_sprites.update()

        all_sprites.draw(screen)
        fake_buttons_far.draw(screen)
        fake_buttons_close.draw(screen)
        movable_sprites.draw(screen)
        for word in words_group:
            screen.blit(word[0], word[1])
        blink_group.draw(screen)
        # The development point of ending score
        if display.get_score(1) == 40:
            running = False
        clock.tick(constants.FPS)
        pygame.display.flip()
    pygame.quit()
