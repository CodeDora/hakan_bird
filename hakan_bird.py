import pygame
import sys
import random  # gerekli kütüphaneler

pygame.init()
pygame.mixer.init()

# Ekran boyutlarının ayarlayabilirsin
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hakan Bird")

# Arkaplan resmi değiştirme kısmı
background_image = pygame.image.load('arkaplan.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ses dosyaları
jump_sound_1 = pygame.mixer.Sound('ses1.mp3')
jump_sound_2 = pygame.mixer.Sound('ses2.mp3')

# Yeni ses dosyası 3 skora geldiğinde çalacak dosya
new_sound = pygame.mixer.Sound('ses3.mp3')

# Kuş özellikleri
bird_image = pygame.transform.scale(pygame.image.load('hakan_bird.png'), (50, 50))
bird_rect = bird_image.get_rect()
bird_rect.topleft = (100, HEIGHT // 2)
bird_speed = 5
jump_strength = 9
gravity = 0.5
bird_velocity = 0

# Engeller hakkında bilgi
obstacle_width = 50
obstacle_gap = 150
obstacle_speed = 5
obstacle_list = []

# Skor
score = 0
font = pygame.font.SysFont(None, 36)

# 'ses3.mp3' çalındı mı kontrolü
new_sound_playing = False

def play_random_jump_sound():
    # Rastgele bir ses dosyasını seçerek çal ve başlatılan ekranı sesi bekle
    random_jump_sound = random.choice([jump_sound_1, jump_sound_2])
    random_jump_sound.play()

def draw_bird():
    screen.blit(bird_image, bird_rect.topleft)

def draw_obstacle(x, gap_y):
    pygame.draw.rect(screen, BLACK, (x, 0, obstacle_width, gap_y))
    pygame.draw.rect(screen, BLACK, (x, gap_y + obstacle_gap, obstacle_width, HEIGHT - gap_y - obstacle_gap))

def display_score(score):
    score_text = font.render(f"Skor: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def reset_game(): #resetle
    global bird_rect, obstacle_list, score, bird_velocity
    bird_rect.topleft = (100, HEIGHT // 2)
    obstacle_list = []
    score = 0
    bird_velocity = 0

def game_over(): # bitiş
    blur_surface = pygame.Surface((WIDTH, HEIGHT))
    blur_surface.set_alpha(128)
    screen.blit(blur_surface, (0, 0))

    over_text = font.render("Oyun Bitti", True, BLACK)
    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - over_text.get_height() // 2 - 30))

    restart_text = font.render("Yeniden Başlamak için SPACE tuşuna basın", True, BLACK)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 - restart_text.get_height() // 2 + 30))

    pygame.display.update()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting_for_key = False
                reset_game()

# Ana oyun döngüsü
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            bird_velocity = -jump_strength
            play_random_jump_sound()

    # Kuşun hareketi
    bird_velocity += gravity
    bird_rect.y += bird_velocity

    # Engellerin hareketi
    for obstacle in obstacle_list:
        obstacle[0] -= obstacle_speed

    # Yeni engel ekleme
    if not obstacle_list or obstacle_list[-1][0] < WIDTH - WIDTH // 3:
        gap_y = random.randint(50, HEIGHT - obstacle_gap - 50)
        obstacle_list.append([WIDTH, gap_y])

    # Çarpışma kontrolü
    if bird_rect.y > HEIGHT or bird_rect.y < 0:
        game_over()

    for obstacle in obstacle_list:
        if (
            bird_rect.colliderect(pygame.Rect(obstacle[0], 0, obstacle_width, obstacle[1])) or
            bird_rect.colliderect(pygame.Rect(obstacle[0], obstacle[1] + obstacle_gap, obstacle_width, HEIGHT - obstacle[1] - obstacle_gap))
        ):
            game_over()

    # Skor kontrolü
    if obstacle_list and obstacle_list[0][0] < bird_rect.x:
        score += 1
        if score == 3 and not new_sound_playing:  # Skor 3 oldu ve yeni ses dosyası çalınmadıysa
            new_sound.play()  # Yeni ses dosyasını çal
            new_sound_playing = True  # Yeni ses dosyasının çaldığını işaretle
        elif score > 3:
            new_sound_playing = False  # Skor 3'ten büyükse ve yeni ses dosyası çalındıysa, diğer ses dosyalarına izin ver
        obstacle_list.pop(0)

    # Ekranı temizle
    screen.blit(background_image, (0, 0))

    # Engelleri çiz
    for obstacle in obstacle_list:
        draw_obstacle(obstacle[0], obstacle[1])

    # Kuşu çiz
    draw_bird()
     # Skoru göster
    display_score(score)
    # Ekranı güncelle
    pygame.display.update()
    # FPS ayarı
    pygame.time.Clock().tick(30)
