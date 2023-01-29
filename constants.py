"""ll pos variables defined because of the graphics"""

EVENTS = {}  # Dictionary {str: int} for storing custom events
event_ctr = 1
RESOLUTION = (1280, 720)  # Resolution of window(1920x1080)
FPS = 60  # Limit of frames per second
GAME_DURATION = 180  # Timer for gameplay in seconds

BUTTON_PUSH_TIMES = 111
BUTTON_POS = (581, 340)
DISPLAY_POS = (305, 20)
SCREWDRIVER_POS = (185, 426)
SCREWS_POS = ((689, 382), (566, 382), (689, 284), (566, 284))
BOOM_POS = (610, 280)
WORDS_POOL = [
    "HASTUR",
    "RUN",
    "CARCOSA",
    "CULT",
    "WELCOME",
    "DELIRIUM",
    "ILUSSIONS",
    "REALITY",
    "ANCIENTS",
]
FAKE_BUTTONS_POS = [(x, y) for x in range(300, 865, 141) for y in (317, 433)]
FAKE_TEMPLATE_POS = (288, 340)
RADIO_POS = (985, 265)
BACKSWAP_POS = (48, 48)

RADIO_MUSIC_LENGTH = 5700
