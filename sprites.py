import pygame
from settings import *

# --- プレイヤークラス (Player Class) ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 25))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 10))
        self.speed = PLAYER_SPEED

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self, all_sprites, bullets):
        if len(bullets) < PLAYER_BULLET_LIMIT:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

# --- プレイヤーの弾クラス (Player Bullet Class) ---
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_y = BULLET_SPEED

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# --- インベーダークラス (Invader Class) ---
class Invader(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(INVADER_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))

# --- インベーダーの弾クラス (InvaderBullet Class) ---
class InvaderBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_y = INVADER_BULLET_SPEED

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
