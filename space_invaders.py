import pygame
import random
import time
from pygame import mixer

# Inizializzazione di Pygame
pygame.init()
pygame.mixer.init()

# Costanti del gioco
LARGHEZZA = 800
ALTEZZA = 600
FPS = 60
NEON_COLOR = (0, 255, 255)
PLAYER_SPEED = 5
BULLET_SPEED = 7
ALIEN_SPEED = 3

# Variabili globali
score = 0
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
aliens = pygame.sprite.Group()
player = None

# Creazione della finestra
screen = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Space Invaders - Futuristic Edition")

# Caricamento delle immagini
player_img = pygame.image.load("player.png").convert()
player_img.set_colorkey((255, 255, 255))  # Rimuove il colore bianco
player_img = pygame.transform.scale(player_img, (64, 64))

alien_img = pygame.image.load("alien.png")
alien_img = pygame.transform.scale(alien_img, (48, 48))

# Font per il testo
FONT = pygame.font.SysFont('arial', 30)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGHEZZA // 2
        self.rect.bottom = ALTEZZA - 10
        self.speedx = 0
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -PLAYER_SPEED
        if keystate[pygame.K_RIGHT]:
            self.speedx = PLAYER_SPEED
        self.rect.x += self.speedx
        
        if self.rect.right > LARGHEZZA:
            self.rect.right = LARGHEZZA
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            sparo_sound.play()

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = alien_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(LARGHEZZA - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, ALIEN_SPEED + 1)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > ALTEZZA:
            return True
        return False

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 16))
        self.image.fill(NEON_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -BULLET_SPEED

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Caricamento dei suoni
sparo_sound = pygame.mixer.Sound("sparo.mp3")
death_sound = pygame.mixer.Sound("death.mp3")
start_sound = pygame.mixer.Sound("start.mp3")

def spawn_alien():
    if len(aliens) < 5:  # Limita il numero di alieni sullo schermo
        if random.random() < 0.03:  # 3% di probabilità di spawn per frame
            alien = Alien()
            aliens.add(alien)
            all_sprites.add(alien)

def draw_text(text, size, x, y, color=NEON_COLOR):
    font = pygame.font.SysFont('arial', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def init_game():
    global all_sprites, bullets, aliens, player, score
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    score = 0
    start_sound.play()

def show_game_over():
    global score
    draw_text("GAME OVER", 64, LARGHEZZA // 2, ALTEZZA // 4)
    draw_text(f"Punteggio finale: {score}", 30, LARGHEZZA // 2, ALTEZZA // 2)
    draw_text("Premi P per giocare di nuovo", 30, LARGHEZZA // 2, ALTEZZA * 3/4)
    pygame.display.flip()

def main():
    global score
    running = True
    game_over = True
    clock = pygame.time.Clock()

    while running:
        if game_over:
            show_game_over()
            waiting = True
            while waiting:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting = False
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_p:
                            init_game()
                            game_over = False
                            waiting = False

        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        if not game_over:
            spawn_alien()
            all_sprites.update()
            
            for alien in aliens:
                if alien.update():
                    alien.kill()
                    score -= 10

            hits = pygame.sprite.groupcollide(aliens, bullets, True, True)
            for hit in hits:
                score += 20

            if pygame.sprite.spritecollide(player, aliens, False):
                death_sound.play()
                game_over = True

            screen.fill((0, 0, 0))
            all_sprites.draw(screen)
            draw_text(f"Punteggio: {score}", 30, LARGHEZZA // 2, 10)
            pygame.draw.rect(screen, NEON_COLOR, (0, 0, LARGHEZZA, ALTEZZA), 2)
            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()