
# screen constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# obj constants
WIDTH_KEY = 50
HEIGHT_KEY = 50
POS_Y_SKEY = 500
POS_Y_KEY = 0 - HEIGHT_KEY
POS_X_KEY = 300

# other constants
DELAY = 100

# colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0,77)
green = (53,255,101)
strong_green = (0, 184, 43)
blue = (0, 66, 255)
grey = (128, 128, 128)
yellow = (255, 240, 80)
magenta = (255, 119, 168)
cyan = (41, 173, 255)
orange = (255, 163, 0)

#map
# beat_map = [(1, 1, HEIGHT_KEY, False), (1000, 4, 200, True),(3000, 2, 400, True),
#             (9000, 1, HEIGHT_KEY, False),(9000, 2, HEIGHT_KEY, False), (11000, 3, HEIGHT_KEY, False),(11500, 4, HEIGHT_KEY, False),
#             (12000, 4, HEIGHT_KEY, False),(12500, 3, HEIGHT_KEY, False),(13000, 2, HEIGHT_KEY, False),(13500, 1, 400, True),
#             (15000, 2, HEIGHT_KEY, False),(15500, 3, HEIGHT_KEY, False),(16000, 2, HEIGHT_KEY, False),(16500, 4, HEIGHT_KEY, False),
#             (17000, 1, 300, True)
#             ]

# variables
score = 0
velocity = 1
acceleration = 0.001
bonus = 0.4

#time screen variables
time_screen=1
ts_width = POS_X_KEY + 100-80
ts_height = 20
ts_pos_y =(HEIGHT_KEY+POS_Y_SKEY)-20
ts_pos_x = 40
divider=256.25

#text variables
color_text = white
size_font=50