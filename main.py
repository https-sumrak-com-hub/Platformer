import pygame as p
import screeninfo as si
import pytmx as pt

p.init()

SCREEN_WIDTH = si.get_monitors()[0].width
SCREEN_HEIGHT = si.get_monitors()[0].height
FPS = 80
set_tile_scale = 2

def li(file, width, height):
    image = p.image.load(file).convert_alpha()
    image = p.transform.scale(image, (width, height))
    return image

class Platform(p.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super(Platform, self).__init__()

        self.image = p.transform.scale(image, (width*set_tile_scale, height*set_tile_scale)).convert_alpha()
        self.rect = self.image.get_rect()
        self.set_coords_x = x*set_tile_scale
        self.set_coords_y = y*set_tile_scale


class Player(p.sprite.Sprite):
    def __init__(self, screen):
        super(Player, self).__init__()
        self.screen = screen
        self.keys = p.key.get_pressed()

        self.image = li("maps/Tiles/Assets/Assets.png", 50, 50)


        self.rect = self.image.get_rect()
        self.rect.center = (200, 100)  # Начальное положение персонажа

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        # self.map_width, self.map_height = map_width * set_tile_scale, map_height * set_tile_scale

    def ENSTEIN(self, platforms):
        print(self.rect)
        for platform in platforms:
            if platform.rect.collidepoint(self.rect[0] + 25, self.rect[1] + 25):
                self.rect = (self.rect[0], 100)
                self.velocity_y = 10

            elif platform.rect.collidepoint(self.rect[1] - 50, 100):
                self.rect = (self.rect[0], 100)
                self.velocity_y = 0

            else:
                self.velocity_y = -10

    def move(self):
        if self.keys[p.K_d]:
            self.velocity_x = 10

        elif self.keys[p.K_a]:
            self.velocity_x = -10

        elif self.keys[p.K_w]:
            self.velocity_y = -10

        elif self.keys[p.K_s]:
            self.velocity_y = 10

        else:
            self.velocity_x = 0
            self.velocity_y = 0

        self.velocity_y += self.gravity
        self.rect = (self.rect[0] + self.velocity_x, self.rect[1] + self.velocity_y)

    # match a:
        #     case p.K_d:
        #         self.velocity_x = 10
        #     case p.K_a:
        #         self.velocity_x = -10
        #     case None:
        #         self.velocity_x = 0
        # print(self.velocity_x)

    # new_x = self.rect.x + self.velocity_x
    # if 0 <= new_x <= self.map_width - self.rect.width:
    #     self.rect.x = new_x


    def update(self, platforms):
        self.ENSTEIN(platforms)
        self.keys = p.key.get_pressed()
        self.move()

    def draw(self):
        self.screen.blit(self.image, self.rect)

class Game(p.sprite.Sprite):
    def __init__(self):
        self.screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.pers = Player(self.screen)

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
        self.pers.update(self.all_sprites)
        self.keys = p.key.get_pressed()


    def draw(self):
        self.screen.fill("white")

        for platform in self.all_platforms:
            self.screen.blit(platform.image, (platform.set_coords_x, platform.set_coords_y))

        self.pers.draw()

        p.display.flip()


if __name__ == "__main__":
    game = Game()