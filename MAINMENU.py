import pygame as p
from screeninfo import get_monitors
import main

p.init()

scr_w = get_monitors()[0].width
scr_h = get_monitors()[0].height


b_w = scr_w - scr_w // 2
b_h = 100

avg_b_x = scr_w // 4

fps = 500

fonts_name = "Gotfridus"

font = p.font.Font(f"{fonts_name}.otf", 27)

def load(file, width, height):
    image = p.image.load(f"images/{file}.png").convert_alpha()
    image = p.transform.scale(image, (width, height))
    return image

def txt(text, text_font=font, color="black"):
    return text_font.render(str(text), True, color)

class Button:
    def __init__(self, file, text, x, y, width, height, text_font=font, func=None):
        self.func = func
        self.image_idle = load(file, width, height)
        self.image_choosed = load(f"{file}_choosed", width, height)
        self.image = self.image_idle
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.is_pressed = False

        self.text = txt(text, text_font)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def update(self):
        mouse_pos = p.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.image_choosed
        else:
            self.image = self.image_idle

    def is_clicked(self, event):
        if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                self.func()
        elif event.type == p.MOUSEBUTTONUP and event.button == 1:
            self.is_pressed = False


class Menu:
    def __init__(self):
        self.screen = p.display.set_mode((scr_w, scr_h))
        p.display.set_caption("Game")
        p.display.set_icon(p.Surface.convert(load("game_icon", 50, 50)))
        self.clock = p.time.Clock()

        self.Smode = None
        self.Mmode = None
        self.actual_modes = ["main_menu", f"{self.Mmode}", f"{self.Smode}"]
        self.modes = {
            self.actual_modes[0]: {
                "images": {
                    "background": load("cobblestone", scr_w, scr_h)
                },

                "buttons":  [
                                Button("lenta", "Play", avg_b_x, scr_h // 4 * 2.5, b_w, b_h, font, func=lambda: self.Play()),

                                Button("lenta", "Settings", avg_b_x, scr_h // 4 * 3, b_w, b_h, font, func=lambda: self.settings("None")),

                                Button("lenta", "Quit", avg_b_x, scr_h // 4 * 3.5, b_w, b_h, font, func=lambda: self.quit())
                            ]
            },

            "Msettings": {
                "images": {
                    "background": load("S_background", scr_w, scr_h)
                },

                "buttons": [
                    Button("lenta", "Change window's size", avg_b_x, scr_h // 4, b_w, b_h, font, func=lambda: self.settings("size()")),
                    Button("lenta", "Volume", avg_b_x, scr_h // 4 * 1.5, b_w, b_h, font, func=lambda: self.settings("volume()")),
                    Button("lenta", "Keys", avg_b_x, scr_h // 4 * 2, b_w, b_h, font, func=lambda: self.settings("keys()"))
                           ]
            },

            "Ssize": {
                "images": {
                    "background": load("S_background", scr_w, scr_h)
                },

                "buttons": [
                    Button("lenta", "YOURE IN SIZE", avg_b_x, scr_h // 4, b_w, b_h, font, func=lambda: None)
                ]
            },

            "Svolume": {
                "images": {
                    "background": load("S_background", scr_w, scr_h)
                },

                "buttons": [
                    Button("lenta", "YOURE IN VOLUME", avg_b_x, scr_h // 4, b_w, b_h, font, func=lambda: None)
                ]
            },

            "Skeys": {
                "images": {
                    "background": load("S_background", scr_w, scr_h)
                },

                "buttons": [
                    Button("lenta", "YOURE IN KEYS", avg_b_x, scr_h // 4, b_w, b_h, font, func=lambda: None)
                ]
            }

        }

        self.mode = self.actual_modes[0]
        self.run()

    def run(self):
        while True:
            self.update()
            self.draw("None")
            self.event()
            self.clock.tick(fps)

    def event(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                quit()

            for button in self.modes[self.mode]["buttons"]:
                button.is_clicked(event)

            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    if self.actual_modes.index(self.mode) > 0:
                        self.mode = self.actual_modes[self.actual_modes.index(self.mode) - 1]

    def update(self):
        self.actual_modes = ["main_menu", f"{self.Mmode}", f"{self.Smode}"]
        for button in self.modes[self.mode]["buttons"]:
            button.update()

    def Play(self):
        self.Mmode = "Mgame"
        main.Game()

    def start(self):
        pass

    def settings(self, function):
        self.mode = "Msettings"

        def size():
            self.Smode = "Ssize"
            self.mode = self.Smode

        def volume():
            self.Smode = "Svolume"
            self.actual_modes = ["main_menu", "settings", f"{self.Smode}"]
            self.mode = self.Smode

        def keys():
            self.Smode = "Skeys"
            self.actual_modes = ["main_menu", "settings", f"{self.Smode}"]
            self.mode = self.Smode

        exec(function)

    def quit(self):
        quit()

    def draw(self, new_draw):
        self.screen.blit(self.modes[self.mode]["images"]["background"], (0, 0))

        for button in self.modes[self.mode]["buttons"]:
            button.draw(self.screen)

        exec(new_draw)

        p.display.flip()


if __name__ == "__main__":
    Menu()