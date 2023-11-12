import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configurar la ventana
WIDTH, HEIGHT = 700, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Basquetbolito')

# Cargar el icono
icon = pygame.image.load('balon.png')

# Establecer el icono de la ventana
pygame.display.set_icon(icon)

# Configurar la bola
BALL_RADIUS = 12
ball = pygame.Rect(random.randint(0, WIDTH - BALL_RADIUS * 6), 0, BALL_RADIUS * 6, BALL_RADIUS * 6)
BASE_BALL_VELOCITY = 4
BALL_VELOCITY = 4
BALL_VELOCITY_MULTIPLIERS = {
    5: 1.3,
    10: 1.5,
    20: 1.7,
    25: 2.0
}

# Configurar la canasta
BASKET_WIDTH, BASKET_HEIGHT = 100, 50
basket = pygame.Rect(WIDTH // 2 - BASKET_WIDTH // 2, HEIGHT - BASKET_HEIGHT * 2, BASKET_WIDTH, BASKET_HEIGHT)
BASKET_VELOCITY = 8

# Configurar el puntaje
score = 0
best_score = 0
font = pygame.font.Font(None, 36)

paused = False

button_width, button_height = 120, 60
resume_button = pygame.Rect(WIDTH // 2 - button_width - 10, HEIGHT // 2 - button_height // 2, button_width,
                            button_height)
quit_button = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 2 - button_height // 2, button_width, button_height)

# Bucle principal del juego
running = True
while running:

    # Cargar y redimensionar la imagen de fondo
    background_image = pygame.image.load('cancha.jpg')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    # Dibujar la imagen de fondo
    win.blit(background_image, (0, 0))

    # Cargar y redimensionar la imagen de la bola
    ball_image = pygame.image.load('balon.png')
    ball_image = pygame.transform.scale(ball_image, (BALL_RADIUS * 6, BALL_RADIUS * 6))
    # Dibujar la imagen de la bola
    win.blit(ball_image, (ball.x, ball.y))

    basket_image = pygame.image.load('canasta.png')
    basket_image = pygame.transform.scale(basket_image, (BASKET_WIDTH, BASKET_HEIGHT))
    # Dibujar la imagen de la canasta
    win.blit(basket_image, (basket.x, basket.y))

    score_text = font.render(f"Puntuación: {score}", True, (255, 128, 0))
    best_score_text = font.render(f"Mejor Puntuación: {best_score}", True, (255, 128, 0))
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))
    win.blit(best_score_text, (WIDTH // 2 - best_score_text.get_width() // 2, 50))

    # Manejar eventos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if paused:
                if resume_button.collidepoint(pygame.mouse.get_pos()):
                    paused = False
                elif quit_button.collidepoint(pygame.mouse.get_pos()):
                    running = False

    if not paused:
        for score_threshold, multiplier in BALL_VELOCITY_MULTIPLIERS.items():
            if score >= score_threshold and BALL_VELOCITY != BASE_BALL_VELOCITY * multiplier:
                BALL_VELOCITY = BASE_BALL_VELOCITY * multiplier

        # Mover la bola
        ball.y += BALL_VELOCITY

        # Mover la canasta
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket.left > 0:
            basket.x -= BASKET_VELOCITY
        if keys[pygame.K_RIGHT] and basket.right < WIDTH:
            basket.x += BASKET_VELOCITY

        basket.y = HEIGHT - BASKET_HEIGHT * 2

        # Comprobar si la bola ha caído en la canasta o fuera de ella
        if ball.bottom >= basket.top:
            if basket.left <= ball.centerx <= basket.right:
                score += 1
                if score > best_score:
                    best_score += 1
                ball.center = (random.randint(0, WIDTH - BALL_RADIUS * 2), BALL_RADIUS)
            else:
                score = 0
                ball.center = (random.randint(0, WIDTH - BALL_RADIUS * 2), BALL_RADIUS)
                BALL_VELOCITY = BASE_BALL_VELOCITY
                paused = True

    else:
        pygame.draw.rect(win, (245, 152, 66), resume_button)
        pygame.draw.rect(win, (245, 152, 66), quit_button)
        # Crear las superficies de texto
        lost_text = font.render("¡Has perdido!", True, (255, 255, 255))
        resume_text = font.render("Reintentar", True, (255, 255, 255))
        quit_text = font.render("Salir", True, (255, 255, 255))
        # Dibujar el texto en los botones
        win.blit(lost_text, (WIDTH // 2 - lost_text.get_width() // 2, HEIGHT // 2 - 80))
        win.blit(resume_text, (resume_button.x + (resume_button.width - resume_text.get_width()) // 2,
                               resume_button.y + (resume_button.height - resume_text.get_height()) // 2))
        win.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width()) // 2,
                             quit_button.y + (quit_button.height - quit_text.get_height()) // 2))

        # Manejar eventos del mouse durante la pausa
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.collidepoint(mouse_x, mouse_y):
                    paused = False
                    # Si se presiona el botón de reintentar, restablecer la posición de la bola
                    ball.center = (random.randint(0, WIDTH - BALL_RADIUS * 2), BALL_RADIUS)
                elif quit_button.collidepoint(mouse_x, mouse_y):
                    running = False
                    paused = False

    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
