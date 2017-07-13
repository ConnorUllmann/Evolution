from random import randint

class Color:

    @staticmethod
    def random():
        return (randint(0, 255), randint(0, 255), randint(0, 255))

    @staticmethod
    def invert(color):
        return (255 - color[0], 255 - color[1], 255 - color[2])

    @staticmethod
    def multiply(color, multiplicant):
        return (color[0] * multiplicant, color[1] * multiplicant, color[2] * multiplicant)

    @staticmethod
    def lerp(A, B, t):
        return ((B[0] - A[0]) * t + A[0], (B[1] - A[1]) * t + A[1], (B[2] - A[2]) * t + A[2])

    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    white = (255, 255, 255)
    black = (0, 0, 0)
    cyan = (0, 255, 255)
    yellow = (255, 255, 0)
    orange = (255, 128, 0)
    teal = (0, 255, 128)
    magenta = (255, 0, 255)

    light_red = (255, 128, 128)
    light_green = (128, 255, 128)
    light_blue = (128, 128, 255)
    light_cyan = (128, 255, 255)
    light_yellow = (255, 255, 128)
    light_magenta = (255, 128, 255)

    dark_red = (128, 0, 0)
    dark_green = (0, 128, 0)
    dark_blue = (0, 0, 128)
    dark_cyan = (0, 128, 128)
    dark_yellow = (128, 128, 0)
    dark_magenta = (128, 0, 128)

    light_grey = light_gray = (192, 192, 192)
    medium_grey = medium_gray = (128, 128, 128)
    dark_grey = dark_gray = (64, 64, 64)

    all = (
        white, red, green, blue, white, cyan, yellow, orange, teal, magenta,
        light_red, light_green, light_blue, light_cyan, light_yellow, light_magenta,
        dark_red, dark_green, dark_blue, dark_cyan, dark_yellow, dark_magenta,
        light_grey, medium_grey, dark_grey, black
    )