import pygame as p
import screeninfo as si
import pytmx as pt

p.init()

SCREEN_WIDTH = si.get_monitors()[0].width
SCREEN_HEIGHT = si.get_monitors()[0].height
FPS = 80
set_tile_scale = 2

class Platform(p.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super(Platform, self).__init__()

        self.image = p.transform.scale(image, (width*set_tile_scale, height*set_tile_scale)).convert_alpha()
        self.rect = self.image.get_rect()
        self.set_coords = (x*set_tile_scale, y*set_tile_scale)



class Game(p.sprite.Sprite):
    def __init__(self):
        self.screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        p.display.set_caption("Платформер")
        self.clock = p.time.Clock()
        self.is_running = False

        self.map = pt.load_pygame("maps/map.tmx")

        self.all_sprites = p.sprite.Group()
        self.all_platforms = p.sprite.Group()

        for layer in self.map:
            for x, y, gid in layer:
                tile = self.map.get_tile_image_by_gid(gid)

                if tile:
                    platform = Platform(
                        tile,
                        x * self.map.tilewidth,
                        y * self.map.tileheight,
                        self.map.tilewidth,
                        self.map.tileheight
                    )

                    self.all_sprites.add(platform)
                    self.all_platforms.add(platform)

        self.run()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        quit()

    def event(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                self.is_running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill("white")

        for platform in self.all_platforms:
            self.screen.blit(platform.image, platform.set_coords)

        p.display.flip()


if __name__ == "__main__":
    game = Game()