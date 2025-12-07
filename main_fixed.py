import pygame as p
import pytmx as pt

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
FPS = 80
set_tile_scale = 1

class Platform(p.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__()

        self.image = p.transform.scale(image, (width*set_tile_scale, height*set_tile_scale))
        self.rect = self.image.get_rect()

        # Исходные координаты тайла с учётом масштаба
        self.set_coords_x = x * set_tile_scale
        self.set_coords_y = y * set_tile_scale

        # rect должен совпадать с реальным положением платформы
        self.rect.x = self.set_coords_x
        self.rect.y = self.set_coords_y

    def update_rect(self):
        """Обновляем hitbox после движения камеры"""
        self.rect.x = self.set_coords_x
        self.rect.y = self.set_coords_y


class Player(p.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen

        self.image = p.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 100)

        # Скорости
        self.velocity_x = 0
        self.velocity_y = 0

        self.gravity = 2
        self.is_jumping = False

    def move(self):
        keys = p.key.get_pressed()

        # Горизонтальное движение
        self.velocity_x = 0
        if keys[p.K_d]:
             self.velocity_x = 5
        elif keys[p.K_a]:
            self.velocity_x = -5

        # Прыжок
        if keys[p.K_w] and not self.is_jumping:
            self.velocity_y = -20
            self.is_jumping = True

        # Гравитация (она должна работать всегда)
        self.velocity_y += self.gravity

        # Двигаем сначала по X
        self.rect.x += self.velocity_x

    def apply_gravity(self):
        # Двигаем по Y отдельно
        self.rect.y += self.velocity_y

    def check_collisions(self, platforms):
        """Нормальная обработка коллизий со всеми платформами"""
        for platform in platforms:

            if self.rect.colliderect(platform.rect):

                # --- Вертикальные столкновения ---
                if self.velocity_y > 0:  # падение
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.is_jumping = False  # Можно снова прыгать

                elif self.velocity_y < 0:  # удар головой
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

                # --- Горизонтальные столкновения ---
                if self.velocity_x > 0:  # идём вправо
                    self.rect.right = platform.rect.left
                elif self.velocity_x < 0:  # идём влево
                    self.rect.left = platform.rect.right

    def update(self, platforms):
        self.move()
        self.apply_gravity()
        self.check_collisions(platforms)

    def draw(self):
        self.screen.blit(self.image, self.rect)


class Game:
    def __init__(self):
        self.screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.pers = Player(self.screen)

        p.display.set_caption("Платформер")
        self.clock = p.time.Clock()
        self.is_running = False

        self.map = pt.load_pygame("maps/map.tmx")

        self.all_platforms = p.sprite.Group()

        # Загружаем платформы
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
                    self.all_platforms.add(platform)

        self.cam_speed = 10
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

        keys = p.key.get_pressed()

        # Двигаем камеру — по сути, двигаем платформы
        if keys[p.K_d]:
            for platform in self.all_platforms:
                platform.set_coords_x -= self.cam_speed
                platform.update_rect()

        if keys[p.K_a]:
            for platform in self.all_platforms:
                platform.set_coords_x += self.cam_speed
                platform.update_rect()

    def update(self):
        self.pers.update(self.all_platforms)

    def draw(self):
        self.screen.fill("white")

        for platform in self.all_platforms:
            self.screen.blit(platform.image, (platform.set_coords_x, platform.set_coords_y))

        self.pers.draw()
        p.display.flip()

Game()