import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configurar la ventana
WIDTH, HEIGHT = 600, 750
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Basquetbolito')

# Cargar el icono
icon = pygame.image.load('balon.png')

# Establecer el icono de la ventana
pygame.display.set_icon(icon)

# Configurar la bola
BALL_RADIUS = 12
BALL_VELOCITY = 4
balls = []  # Lista para almacenar las bolas

# Configurar la canasta
BASKET_WIDTH, BASKET_HEIGHT = 100, 50
basket = pygame.Rect(WIDTH // 2 - BASKET_WIDTH // 2, HEIGHT - BASKET_HEIGHT * 4, BASKET_WIDTH, BASKET_HEIGHT)
BASKET_VELOCITY = 6

# Configurar el puntaje
score = 0
best_score = 0
font = pygame.font.Font(None, 36)

paused = False

button_width, button_height = 120, 60
resume_button = pygame.Rect(WIDTH // 2 - button_width - 10, HEIGHT // 2 - button_height // 2, button_width,
                            button_height)
quit_button = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 2 - button_height // 2, button_width, button_height)

# Inicializar la velocidad del balón y de la canasta
ball_velocity = BALL_VELOCITY
basket_velocity = BASKET_VELOCITY

# Función para crear una nueva bola
def crear_nueva_bola():
    new_ball = pygame.Rect(random.randint(0, WIDTH - BALL_RADIUS * 6), 0, BALL_RADIUS * 6, BALL_RADIUS * 6)
    balls.append(new_ball)

# Bucle principal del juego
running = True
while running:

    # Cargar y redimensionar la imagen de fondo
    background_image = pygame.image.load('cancha.jpg')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    # Dibujar la imagen de fondo
    win.blit(background_image, (0, 0))

    for ball in balls:
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
            elif event.key == pygame.K_LEFT:
                basket.x -= basket_velocity
            elif event.key == pygame.K_RIGHT:
                basket.x += basket_velocity

    if not paused:
        for ball in balls:
            # Mover la bola con la velocidad actual
            ball.y += ball_velocity

        # Comprobar si la bola ha caído en la canasta o fuera de ella
        for ball in balls:
            if ball.bottom >= basket.top:
                if basket.left <= ball.centerx <= basket.right:
                    score += 1
                    if score > best_score:
                        best_score += 1
                    print(f"¡Punto! Tu puntuación es ahora {score}.")
                    balls.remove(ball)
                    if score >= 7:
                        # Aumentar la velocidad de la canasta y el balón
                        basket_velocity += 2  # Ajusta la velocidad de la canasta como desees
                        ball_velocity += 2  # Ajusta la velocidad del balón como desees

        # Eliminar bolas que han salido de la pantalla
        balls = [ball for ball in balls if ball.y < HEIGHT]

        # Crear nuevas bolas si no hay suficientes en la pantalla
        while len(balls) < 3:  # Puedes ajustar este número según tus preferencias
            crear_nueva_bola()

    else:
        pygame.draw.rect(win, (245, 152, 66), resume_button)
        pygame.draw.rect(win, (245, 152, 66), quit_button)
        # Crear las superficies de texto
        resume_text = font.render("Reanudar", True, (255, 255, 255))
        quit_text = font.render("Cerrar", True, (255, 255, 255))
        # Dibujar el texto en los botones
        win.blit(resume_text, (resume_button.x + (resume_button.width - resume_text.get_width()) // 2,
                               resume_button.y + (resume_button.height - resume_text.get_height()) // 2))
        win.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width()) // 2,
                             quit_button.y + (quit_button.height - quit_text.get_height()) // 2))

    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
