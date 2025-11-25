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
        self.set_coords_x = x*set_tile_scale
        self.set_coords_y = y*set_tile_scale



class Game(p.sprite.Sprite):
    def __init__(self):
        self.screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        p.display.set_caption("Платформер")
        self.clock = p.time.Clock()
        self.is_running = False

        self.keys = p.key.get_pressed()

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

        self.cam_speed = 10
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2

        self.run()




    def run(self):
        self.is_running = True
        while self.is_running:
            self.update()
            self.clock.tick(FPS)
        quit()

    def event(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                self.is_running = False

        if self.keys[p.K_d]:
            for platform in self.all_platforms:
                platform.set_coords_x -= self.cam_speed
        if self.keys[p.K_a]:
            for platform in self.all_platforms:
                platform.set_coords_x += self.cam_speed

    def update(self):
        self.event()
        self.draw()
        self.keys = p.key.get_pressed()


    def draw(self):
        self.screen.fill("white")

        for platform in self.all_platforms:
            self.screen.blit(platform.image, (platform.set_coords_x, platform.set_coords_y))

        p.display.flip()


if __name__ == "__main__":
    game = Game()