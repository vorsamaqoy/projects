import pygame
import random

# Inizializza pygame
pygame.init()

# Dimensioni della finestra
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tennis Game")

# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Velocità iniziale della palla
ball_speed_x = random.choice([-5, 5])
ball_speed_y = random.choice([-5, 5])

# Dimensioni dei paddle e posizioni iniziali
paddle_width, paddle_height = 10, 100
player_x, player_y = 50, height // 2 - paddle_height // 2
ai_x, ai_y = width - 50, height // 2 - paddle_height // 2
ball_x, ball_y = width // 2, height // 2

# Variabili per il punteggio e le abilità dell'IA
player_score = 0
ai_score = 0
ai_reaction_speed = 1  # Inizio con reazione molto bassa
ai_max_reaction_speed = 10  # Velocità massima dell'IA

# Funzione principale di gioco
def game_loop():
    global player_y, ai_y, ball_x, ball_y, ball_speed_x, ball_speed_y
    global ai_reaction_speed, player_score, ai_score
    
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movimento del giocatore
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= 7
        if keys[pygame.K_DOWN] and player_y < height - paddle_height:
            player_y += 7

        # Movimento dell'IA (con reazione variabile)
        if ai_y + paddle_height / 2 < ball_y and ai_y < height - paddle_height:
            ai_y += ai_reaction_speed
        if ai_y + paddle_height / 2 > ball_y and ai_y > 0:
            ai_y -= ai_reaction_speed

        # Aggiorna la posizione della palla
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Collisioni con il bordo superiore e inferiore
        if ball_y <= 0 or ball_y >= height:
            ball_speed_y *= -1

        # Collisione con i paddles
        if (ball_x <= player_x + paddle_width and player_y < ball_y < player_y + paddle_height):
            ball_speed_x *= -1
            # Calcola angolo di rimbalzo basato sulla posizione
            impact_position = (ball_y - player_y) / paddle_height  # Normalizza la posizione di impatto
            ball_speed_y = (impact_position - 0.5) * 15  # Cambia traiettoria in base all'impatto
            randomize_ball_speed()
        elif (ball_x >= ai_x - paddle_width and ai_y < ball_y < ai_y + paddle_height):
            ball_speed_x *= -1
            # Calcola angolo di rimbalzo basato sulla posizione
            impact_position = (ball_y - ai_y) / paddle_height  # Normalizza la posizione di impatto
            ball_speed_y = (impact_position - 0.5) * 15  # Cambia traiettoria in base all'impatto
            randomize_ball_speed()

        # Reset della palla e gestione punti
        if ball_x < 0:  # Punto per l'IA
            ai_score += 1
            ball_x, ball_y = width // 2, height // 2
            ball_speed_x = random.choice([-5, 5])
            ball_speed_y = random.choice([-5, 5])
            # L'IA migliora solo quando perde
            ai_reaction_speed = min(ai_max_reaction_speed, ai_reaction_speed + 1)  # Aumenta la reazione dell'IA

        elif ball_x > width:  # Punto per il giocatore
            player_score += 1
            ball_x, ball_y = width // 2, height // 2
            ball_speed_x = random.choice([-5, 5])
            ball_speed_y = random.choice([-5, 5])
            # Non aumentare la reazione dell'IA quando il giocatore segna

        # Disegna
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (player_x, player_y, paddle_width, paddle_height))
        pygame.draw.rect(screen, WHITE, (ai_x, ai_y, paddle_width, paddle_height))
        pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, 15, 15))

        # Mostra il punteggio
        font = pygame.font.SysFont("Arial", 30)
        score_text = font.render(f"Score: Player {player_score} - AI {ai_score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Funzione per randomizzare la velocità della palla
def randomize_ball_speed():
    global ball_speed_x, ball_speed_y
    if random.random() < 0.5:  # 50% di possibilità di aumentare la velocità
        ball_speed_x *= 1.1
        ball_speed_y *= 1.1

# Avvia il gioco
game_loop()
