import pygame as p
import pytmx

p.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 80


class Game:
    def __init__(self):
        self.screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        p.display.set_caption("Платформер")
        self.clock = p.time.Clock()
        self.is_running = False

        self.map = pytmx.load_pygame("maps/map.tmx")

        self.run()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        p.quit()
        quit()

    def event(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                self.is_running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill("white")
        for layer in self.map:
            for x, y, gid in layer:
                tile = self.map.get_tile_image_by_gid(gid)

                if tile:
                    self.screen.blit(tile, (x * self.map.tilewidth, y * self.map.tileheight))
        
        p.display.flip()


if __name__ == "__main__":
    game = Game()