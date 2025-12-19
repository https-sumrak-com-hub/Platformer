import pygame as p
import screeninfo as si
import pytmx as pt
from PIL import Image

from txt.main import scr_w

p.init()
p.mixer.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

FPS = 80
set_tile_scale = 2

def li(file, width, height):
    image = p.image.load(file).convert_alpha()
    image = p.transform.scale(image, (width, height))
    return image

def load_anims(location):
    animations = {
        "r": [],
        "l": []
    }

    tile_size = (int(location[-12:-5].split(" x ")[0]), int(location[-12:-5].split(" x ")[1]))

    with Image.open(location) as img:
        count_images =  img.width // tile_size[0]

        spritesheet = li(location, img.width, img.height)

    for i in range(count_images):
        x = i * tile_size[0]
        y = 0
        rect = p.Rect(x, y, tile_size[0], tile_size[1])
        animations["r"].append(p.transform.scale(spritesheet.subsurface(rect), (tile_size[0] * set_tile_scale, tile_size[1] * set_tile_scale)))

    animations["l"].append(p.transform.flip(image, True, False) for image in animations["r"])

    return animations

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


class Player(p.sprite.Sprite):
    def __init__(self, screen):
        super(Player, self).__init__()
        self.screen = screen
        self.move_que = True

        self.anims = load_anims("sprites/Sprite Pack 3/2 - Twiggy/Back_Turned (32 x 32).png")

        self.image = li("maps/Tiles/Assets/Assets.png", 50, 50)



        self.rect = self.image.get_rect()
        self.rect.center = (200, 100)

        self.velocity_x = 0
        self.velocity_y = 0
        self.jump_que = False

        self.vel_def = 6
        self.vel_fast = 12
        self.gravity = 2

        self.collides = {
            "bridge": [46, 47, 48],
            "ladder": [43, 44],
            "thorns": [45]
        }

    def gravity_checker(self, platforms, vector):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if vector == "x":
                    if self.velocity_x > 0:
                        self.rect.right = platform.rect.left
                    else:
                        self.rect.left = platform.rect.right
                    self.velocity_x = 0

                elif vector == "y":
                    if self.velocity_y > 0:
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        self.jump_que = True
                    else:
                        self.rect.top = platform.rect.bottom
                        self.velocity_y = 0


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

                if collide.id in self.collides["thorns"]:
                    self.move_que = False
                    self.dead_anim()


    def move(self):
        keys = p.key.get_pressed()

        if self.move_que:
            if keys[p.K_d] or keys[p.K_a] or keys[p.K_SPACE] or keys[p.K_LSHIFT]:
                if keys[p.K_SPACE] and self.jump_que:
                    self.velocity_y -= 30
                    self.jump_que = False

                if keys[p.K_LSHIFT]:
                    self.velocity_y = self.vel_def

                if keys[p.K_d]:
                    self.velocity_x = self.vel_def

                elif keys[p.K_a]:
                    self.velocity_x = -self.vel_def

                else:
                    self.velocity_x *= 0.2

            else:
                self.velocity_x *= 0.2

        self.velocity_y += self.gravity

    def dead_anim(self):
        dead_text = Image.open("dead_text.png").convert("RGBA")
        datas = dead_text.getdata()
        new_data = []

        dead_sound = p.music.mixer.load("dead_sound.mp3")
        dead_background = li("dead.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        p.music.mixer.play(dead_sound)
        self.screen.blit(dead_background, (0, 0))

        rect = dead_text.get_rect()
        rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        for i in range(256):
            for item in datas:
                # Изменить альфа (прозрачность) на 128 (50% прозрачности, 0=прозр., 255=непрозр.)
                new_data.append((*item[:3], i))

            self.screen.blit(dead_text, rect)

    def update(self, map_layers):
        self.collide_checker(map_layers["collides"])
        self.move()
        self.rect.x += self.velocity_x
        self.gravity_checker(map_layers["platform"], "x")
        self.rect.y += self.velocity_y
        self.gravity_checker(map_layers["platform"], "y")


    def draw(self, camX, camY):
        self.screen.blit(self.image, (self.rect.x - camX, self.rect.y - camY))



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

        self.map_pixel_width = self.map.width * self.map.tilewidth * set_tile_scale
        self.map_pixel_height = self.map.height * self.map.tileheight * set_tile_scale

        self.camX = 0
        self.camY = 0

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
                if layer_name == "collides":
                    print(gid)
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

            if event.type == p.KEYDOWN:
                if event.key == p.K_d:
                    self.camX += 15

                if event.key == p.K_a:
                    self.camX -= 15

    def update(self):
        self.event()

        self.camX = max(0, min(self.pers.rect.x - SCREEN_WIDTH / 2, self.map_pixel_width - SCREEN_WIDTH))
        self.camY = max(0, min(self.pers.rect.y - SCREEN_HEIGHT / 2, self.map_pixel_height - SCREEN_HEIGHT))

        self.pers.update(self.map_layers)
        self.draw()

        self.keys = p.key.get_pressed()


    def draw(self):
        self.screen.fill("white")
        for layer_names in self.map_layers:
            for platform in self.map_layers[layer_names]:
                self.screen.blit(platform.image,
                                 (platform.set_coords_x - self.camX,
                                  platform.set_coords_y - self.camY))

        self.pers.draw(self.camX, self.camY)


        p.display.flip()


if __name__ == "__main__":
    game = Game()