import pygame
import sys
import random
from settings import *
from sprites import *

# --- テキスト描画関数 (Function to draw text) ---
def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.Font(pygame.font.match_font(FONT_NAME), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        # 新しいゲームを開始
        self.score = 0
        self.game_over = False
        self.win = False
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.invaders = pygame.sprite.Group()
        self.invader_bullets = pygame.sprite.Group()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.invader_speed_x = INVADER_START_SPEED_X
        for row in range(5):
            for col in range(10):
                invader = Invader(50 + col * 60, 50 + row * 40)
                self.invaders.add(invader)
                self.all_sprites.add(invader)

        self.run()

    def run(self):
        # ゲームループ
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            if not self.game_over and not self.win:
                self.update()
            self.draw()

    def update(self):
        # ゲームループ - 更新
        self.all_sprites.update()
        self.update_invaders()

        # 当たり判定
        hits = pygame.sprite.groupcollide(self.bullets, self.invaders, True, True)
        if hits:
            self.score += len(hits) * SCORE_PER_INVADER

        if pygame.sprite.spritecollide(self.player, self.invader_bullets, True):
            self.player.kill()
            self.game_over = True

        if not self.invaders:
            self.win = True

    def update_invaders(self):
        # インベーダーの移動ロジック
        if self.invaders:
            edge_hit = False
            for invader in self.invaders:
                if invader.rect.right >= SCREEN_WIDTH or invader.rect.left <= 0:
                    edge_hit = True
                    break

            if edge_hit:
                self.invader_speed_x *= -1
                for inv in self.invaders:
                    inv.rect.y += INVADER_DROP_SPEED

            for invader in self.invaders:
                invader.rect.x += self.invader_speed_x

        # インベーダーの発射
        if self.invaders and random.random() < INVADER_FIRE_RATE:
            shooter = random.choice(self.invaders.sprites())
            invader_bullet = InvaderBullet(shooter.rect.centerx, shooter.rect.bottom)
            self.all_sprites.add(invader_bullet)
            self.invader_bullets.add(invader_bullet)

    def events(self):
        # ゲームループ - イベント
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if not self.game_over and not self.win:
                    if event.key == pygame.K_SPACE:
                        self.player.shoot(self.all_sprites, self.bullets)
                else:
                    if self.playing:
                        self.playing = False
                    self.running = False

    def draw(self):
        # ゲームループ - 描画
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        draw_text(self.screen, f"Score: {self.score}", 22, SCREEN_WIDTH / 2, 10)

        if self.game_over:
            draw_text(self.screen, "GAME OVER", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
            draw_text(self.screen, "Press any key to quit", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        if self.win:
            draw_text(self.screen, "YOU WIN!", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
            draw_text(self.screen, f"Final Score: {self.score}", 28, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        pygame.display.flip()

def main():
    g = Game()
    while g.running:
        g.new()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
