import pygame
import random
import sys

pygame.mixer.init()  # Initialize the mixer first
pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Superman the kryptonian")
clock = pygame.time.Clock()

# Load and scale background
bg = pygame.image.load("background.png").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Game images and sizes
BUILDING_W, BUILDING_H = 100, 200
ENEMY_W, ENEMY_H = 50, 50
POWER_W, POWER_H = 40, 40
HERO_W, HERO_H = 60, 50

building_imgs = [
    pygame.transform.scale(pygame.image.load(f).convert_alpha(), (BUILDING_W, BUILDING_H))
    for f in ["building.png", "building1.png", "building3.png"]
]

enemy_img = pygame.transform.scale(pygame.image.load("enemy.jpg").convert_alpha(), (ENEMY_W, ENEMY_H))
power_img = pygame.transform.scale(pygame.image.load("power.png").convert_alpha(), (POWER_W, POWER_H))
hero_img = pygame.transform.scale(pygame.image.load("hero.png").convert_alpha(), (HERO_W, HERO_H))
super_logo = pygame.transform.scale(pygame.image.load("super.png").convert_alpha(), (150, 100))

# Sounds
powerup_sound = pygame.mixer.Sound("powerup.mp3")

# Buttons
start_img = pygame.transform.scale(pygame.image.load("start.png").convert_alpha(), (230, 80))
pause_img = pygame.transform.scale(pygame.image.load("pause.png").convert_alpha(), (40, 40))
resume_img = pygame.transform.scale(pygame.image.load("resume.png").convert_alpha(), (140, 60))
exit_img = pygame.transform.scale(pygame.image.load("exit.png").convert_alpha(), (140, 60))
restart_img = pygame.transform.scale(pygame.image.load("restart.png").convert_alpha(), (120, 50))

# Button rects
start_rect = start_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
pause_rect = pause_img.get_rect(topleft=(10, 10))
resume_rect = resume_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
restart_rect = restart_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
exit_rect = exit_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))

# Font
font = pygame.font.SysFont(None, 48)

def draw_text(text, size, color, x, y):
    f = pygame.font.SysFont(None, size)
    surf = f.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)

def draw_colored_text(text, x, y):
    red = (255, 0, 0)
    blue = (0, 0, 255)
    size = 24
    spacing = 0
    f = pygame.font.SysFont(None, size)
    for i, ch in enumerate(text):
        color = red if i % 2 == 0 else blue
        ch_surf = f.render(ch, True, color)
        ch_rect = ch_surf.get_rect()
        ch_rect.topleft = (x + spacing, y)
        screen.blit(ch_surf, ch_rect)
        spacing += ch_rect.width

def reset_game():
    hero = pygame.Rect(100, HEIGHT // 2, HERO_W, HERO_H)
    return hero, 0, WIDTH, random.choice(building_imgs), 0, 0, 0, [], []

# Game constants
GRAVITY = 0.5
JUMP_STRENGTH = -7
BOOST_STRENGTH = -14
MAX_FALL = 8
BUILDING_SPEED = 4

# Initial state
hero, hero_movement, building_x, current_building, drone_timer, power_timer, score, drones, powers = reset_game()
game_active = False
game_paused = False
game_over = False

# Background music
pygame.mixer.music.load("super.mp3")
pygame.mixer.music.set_volume(100)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_active:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and start_rect.collidepoint(e.pos):
                game_active = True
                game_paused = False
                game_over = False
                pygame.mixer.music.play(-1)
        elif game_over:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if restart_rect.collidepoint(e.pos):
                    hero, hero_movement, building_x, current_building, drone_timer, power_timer, score, drones, powers = reset_game()
                    game_active = True
                    game_paused = False
                    game_over = False
                    pygame.mixer.music.play(-1)
                elif exit_rect.collidepoint(e.pos):
                    pygame.quit()
                    sys.exit()
        elif game_paused:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if resume_rect.collidepoint(e.pos):
                    game_paused = False
                    pygame.mixer.music.unpause()
                elif exit_rect.collidepoint(e.pos):
                    pygame.quit()
                    sys.exit()
        else:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                hero_movement = JUMP_STRENGTH
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and pause_rect.collidepoint(e.pos):
                game_paused = True
                pygame.mixer.music.pause()

    screen.blit(bg, (0, 0))

    if not game_active:
        screen.blit(super_logo, (WIDTH // 2 - 75, HEIGHT // 2 - 250))
        draw_colored_text("Symbol of Hope", WIDTH // 2 - 80, HEIGHT // 2 - 140)
        screen.blit(start_img, start_rect)
    elif game_over:
        draw_text("Game Over", 64, (255, 0, 0), WIDTH // 2, HEIGHT // 2 - 100)
        screen.blit(restart_img, restart_rect)
        screen.blit(exit_img, exit_rect)
    elif game_paused:
        draw_text("Paused", 64, (255, 255, 0), WIDTH // 2, HEIGHT // 2 - 120)
        screen.blit(resume_img, resume_rect)
        screen.blit(exit_img, exit_rect)
    else:
        hero_movement = min(hero_movement + GRAVITY, MAX_FALL)
        hero.y += int(hero_movement)
        screen.blit(hero_img, hero)
        hero_rect = hero

        building_x -= BUILDING_SPEED
        if building_x < -BUILDING_W:
            building_x = WIDTH
            current_building = random.choice(building_imgs)
            score += 1
        building_y = HEIGHT - BUILDING_H
        screen.blit(current_building, (building_x, building_y))
        building_rect = pygame.Rect(building_x, building_y, BUILDING_W, BUILDING_H)

        drone_timer += 1
        if drone_timer > 80:
            drone_timer = 0
            y = random.randint(20, HEIGHT // 2)
            drones.append(pygame.Rect(WIDTH, y, ENEMY_W, ENEMY_H))
        for d in drones[:]:
            d.x -= BUILDING_SPEED + 1
            screen.blit(enemy_img, d)
            if d.right < 0:
                drones.remove(d)

        power_timer += 1
        if power_timer > 300:
            power_timer = 0
            y = random.randint(HEIGHT // 2, HEIGHT - POWER_H - 20)
            powers.append(pygame.Rect(WIDTH, y, POWER_W, POWER_H))
        for p in powers[:]:
            p.x -= BUILDING_SPEED
            screen.blit(power_img, p)
            if hero_rect.colliderect(p):
                hero_movement = BOOST_STRENGTH
                powerup_sound.play()
                powers.remove(p)
            elif p.right < 0:
                powers.remove(p)

        if (hero_rect.colliderect(building_rect)
                or any(hero_rect.colliderect(d) for d in drones)
                or hero.top < 0 or hero.bottom > HEIGHT):
            game_over = True
            pygame.mixer.music.stop()

        screen.blit(pause_img, pause_rect)
        draw_text(str(score), 48, (255, 255, 255), WIDTH // 2, 40)

    pygame.display.update()
    clock.tick(30)
