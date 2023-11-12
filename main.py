import pygame
import sys
import random
import pickle

# Inicializar Pygame
pygame.init()
SCORES_FILE = "top_scores.pkl"
top_scores = []
try:
    with open(SCORES_FILE, "rb") as file:
        top_scores = pickle.load(file)
except (FileNotFoundError, EOFError):
    top_scores = []

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


def display_top_scores(top_scores):
    font = pygame.font.Font(None, 24)
    y_position = 10  # Posición inicial en y para mostrar el top 5

    for i, (name, score) in enumerate(top_scores, 1):
        text = font.render(f"{i}. {name}: {score}", True, (255, 255, 255))
        win.blit(text, (WIDTH - text.get_width() - 10, y_position))
        y_position += text.get_height() + 5


def get_player_name():
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)

    # Configuración de la ventana emergente
    popup_width, popup_height = WIDTH // 2, HEIGHT // 4
    popup_rect = pygame.Rect(WIDTH // 4, HEIGHT // 3, popup_width, popup_height)

    input_box = pygame.Rect(0, 0, popup_width - 20, 32)
    input_box.center = popup_rect.center

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if popup_rect.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        win.fill((255, 255, 255))

        # Dibujamos la ventana emergente
        pygame.draw.rect(win, (255, 255, 255), popup_rect)  # Cambiamos el color de fondo
        pygame.draw.rect(win, (169, 169, 169), popup_rect, 2)

        # Dibujamos el texto "Ingresa tu nombre" centrado
        prompt_text = font.render("Ingresa tu nombre", True, (0, 0, 0))
        text_x = popup_rect.centerx - prompt_text.get_width() // 2
        win.blit(prompt_text, (text_x, popup_rect.top + 10))

        # Centramos el campo de texto
        input_box.centerx = popup_rect.centerx  # Ajustamos el centro en el eje X
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        win.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(win, color, input_box, 2)
        pygame.display.flip()
        pygame.time.wait(30)


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
                    best_score = score

                ball.center = (random.randint(0, WIDTH - BALL_RADIUS * 2), BALL_RADIUS)
            else:
                if score > 0:  # Verificar si se hizo al menos una canasta antes de perder
                    print(f"¡Has perdido! Tu puntuación final fue {score}.")
                    # Verificar si el puntaje pertenece al top 5
                    if len(top_scores) < 5 or score > top_scores[-1][1]:
                        player_name = get_player_name()
                        top_scores.append((player_name, score))
                        top_scores.sort(key=lambda x: x[1], reverse=True)
                        top_scores = top_scores[:5]

                        with open(SCORES_FILE, "wb") as file:
                            pickle.dump(top_scores, file)

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

    display_top_scores(top_scores)
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
