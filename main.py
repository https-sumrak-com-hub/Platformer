import pygame as p
import screeninfo as si
import pytmx as pt

p.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

FPS = 80
set_tile_scale = 2

def li(file, width, height):
    image = p.image.load(file).convert_alpha()
    image = p.transform.scale(image, (width, height))
    return image

class Platform(p.sprite.Sprite):
    def __init__(self, image, x, y, width, height, layer_name, id):
        super(Platform, self).__init__()
        self.layer = layer_name
        self.id = id

        self.height = height
        self.image = p.transform.scale(image, (width * set_tile_scale, height * set_tile_scale)).convert_alpha()
        self.rect = self.image.get_rect()

        self.set_coords_x = x * set_tile_scale
        self.set_coords_y = y * set_tile_scale

        self.rect.x = self.set_coords_x
        self.rect.y = self.set_coords_y

    def update(self):
        self.rect.x = self.set_coords_x
        self.rect.y = self.set_coords_y


class Player(p.sprite.Sprite):
    def __init__(self, screen):
        super(Player, self).__init__()
        self.screen = screen

        self.image = li("maps/Tiles/Assets/Assets.png", 25, 25)

        self.rect = self.image.get_rect()
        self.rect.center = (200, 100)  # Начальное положение персонажа

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_jumping = False

        self.vel_def = 2
        self.vel_fast = 6
        self.gravity = 2
        # self.map_width, self.map_height = map_width * set_tile_scale, map_height * set_tile_scale

        self.collides = {
            "bridge": [46, 47, 48],
            "ladder": [43, 44, 45]
        }

    def gravity_checker(self, platforms):
        for platform in platforms:

            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False

            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0

                # КОЛЛИЗИИ ПО X
            if platform.rect.collidepoint(self.rect.midright):
                self.rect.right = platform.rect.left

            if platform.rect.collidepoint(self.rect.midleft):
                self.rect.left = platform.rect.right

            # if self.rect.colliderect(platform.rect):
            #     if platform.rect.y > self.rect.y:
            #         self.velocity_x = -1
            #     if self.velocity_y > 0:
            #         self.rect.bottom = platform.rect.top
            #         self.velocity_y = 0
            #     if self.velocity_y < 0:
            #         self.rect.top = platform.rect.bottom
            #         self.velocity_y = self.gravity
            # if platform.rect.collidepoint(self.rect.midright):
            #     self.rect.right = platform.rect.left
            #
            # if platform.rect.collidepoint(self.rect.midleft):
            #     self.rect.left = platform.rect.right

    def collide_checker(self, collides):
        keys = p.key.get_pressed()

        for collide in collides:
            if self.rect.colliderect(collide.rect):
                if collide.id in self.collides["bridge"]:
                    if self.velocity_y > 0:
                        self.rect.bottom = collide.rect.top
                        self.velocity_y = 0
                    if self.velocity_y < 0:
                        self.rect.top = collide.rect.bottom
                        self.velocity_y = self.gravity

                if collide.id in self.collides["ladder"]:
                    if keys[p.K_w]:
                        self.velocity_y = self.vel_def
                    if keys[p.K_s]:
                        self.velocity_y = -self.vel_def

    def move(self):
        keys = p.key.get_pressed()

        if keys[p.K_d]:
            self.velocity_x = self.vel_def

        elif keys[p.K_a]:
            self.velocity_x = -self.vel_def

        elif keys[p.K_SPACE]:
            self.velocity_y = -self.vel_def

        elif keys[p.K_LSHIFT]:
            self.velocity_y = self.vel_def

        else:
            smoothless = 0.4
            time = p.time.get_ticks() + 50
            if p.time.get_ticks() < time:
                if self.velocity_x > 0:
                    self.velocity_x -= smoothless
                elif self.velocity_x < 0:
                    self.velocity_x += smoothless
                if self.velocity_y > 0:
                    self.velocity_y -= smoothless
                elif self.velocity_y < 0:
                    self.velocity_y += smoothless


        self.velocity_y += self.gravity
        self.rect.x += self.velocity_x


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


    def update(self, map_layers):
        self.move()
        self.rect.y += self.velocity_y
        self.gravity_checker(map_layers["platform"])
        # self.collide_checker(map_layers["collides"])

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

        self.map_layers = {
                            "platform": self.layer_loader("platform"),
                            "collides": self.layer_loader("collides"),
                            "decorations": self.layer_loader("decorations")
                          }



        self.cam_speed = self.pers.vel_def
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2

        self.run()

    def layer_loader(self, layer_name):
        platforms = p.sprite.Group()
        for x, y, gid in self.map.get_layer_by_name(layer_name):
            tile = self.map.get_tile_image_by_gid(gid)

            if tile:
                platform = Platform(
                    tile,
                    x * self.map.tilewidth,
                    y * self.map.tileheight,
                    self.map.tilewidth,
                    self.map.tileheight,
                    layer_name,
                    gid
                )

                platforms.add(platform)

        return platforms


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

        if self.keys[p.K_d] or self.keys[p.K_a]:
            for layer_name in self.map_layers:
                for platform in self.map_layers[layer_name]:
                    if self.keys[p.K_d]:
                        platform.set_coords_x -= self.cam_speed
                    if self.keys[p.K_a]:
                        platform.set_coords_x += self.cam_speed
                    platform.update()

    def update(self):
        self.event()
        self.draw()
        self.pers.update(self.map_layers)
        self.keys = p.key.get_pressed()


    def draw(self):
        self.screen.fill("white")
        for layer_names in self.map_layers:
            for platform in self.map_layers[layer_names]:
                self.screen.blit(platform.image, (platform.set_coords_x, platform.set_coords_y))

        self.pers.draw()


        p.display.flip()


if __name__ == "__main__":
    game = Game()