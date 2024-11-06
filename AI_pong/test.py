import pygame
import neat
import pickle
import sys

pygame.init()

# Impostazioni schermo
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Paddle Game with Trained Model')

# Colori
white = (255, 255, 255)
black = (0, 0, 0)

# Paddle
paddle_width = 8
paddle_height = 80
paddle_speed = 10

# Palla
ball_size = 15
ball_speed_x = 10
ball_speed_y = 10

# Clock
clock = pygame.time.Clock()

# Funzione per gestire il movimento della palla
def move_ball(ball, paddle):
    global ball_speed_x, ball_speed_y
    
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Collisione con il bordo superiore e inferiore
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
        
    if ball.right >= screen_width:
        ball_speed_x *= -1

    # Collisione con il paddle
    if ball.colliderect(paddle):
        ball_speed_x *= -1

    # Se la palla tocca il lato sinistro dello schermo, il gioco termina
    if ball.left <= 0:
        return True  # Gioco finito

    return False  # Gioco continua

# Funzione per visualizzare informazioni
def draw_info(screen, score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Punteggio: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

# Funzione per giocare con il modello allenato
def play_with_trained_model(config_file, genome_file):
    # Carica il genoma migliore
    with open(genome_file, "rb") as f:
        genome = pickle.load(f)

    # Carica la configurazione
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )

    # Crea la rete neurale dal genoma
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    paddle = pygame.Rect(screen_width - 700, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)
    ball = pygame.Rect(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, ball_size, ball_size)
    
    score = 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        # Movimento della palla
        game_over = move_ball(ball, paddle)
        if game_over:
            break

        # Input per la rete neurale
        output = net.activate((paddle.y, ball.y, abs(paddle.y - ball.y)))
        
        # Decidere il movimento del paddle in base all'output della rete neurale
        if output[0] > 0.5 and paddle.bottom < screen_height:
            paddle.y += paddle_speed
        elif output[0] <= 0.5 and paddle.top > 0:
            paddle.y -= paddle_speed
        
        # Limita il paddle ai bordi dello schermo
        if paddle.top < 0:
            paddle.top = 0
        if paddle.bottom > screen_height:
            paddle.bottom = screen_height

        # Incrementa il punteggio se la palla tocca il paddle
        if ball.colliderect(paddle):
            score += 1

        # Disegna lo sfondo
        screen.fill(black)
        
        # Disegna il paddle e la palla
        pygame.draw.rect(screen, white, paddle)
        pygame.draw.ellipse(screen, white, ball)
        
        # Mostra informazioni
        draw_info(screen, score)
        
        # Aggiorna lo schermo
        pygame.display.flip()
        
        # Imposta il frame rate
        clock.tick(240)
    
    print(f"Il modello ha terminato la partita con un punteggio di {score}.")

# Avviare il programma
if __name__ == "__main__":
    config_path = 'config-feedforward.txt'  # Assicurati che il percorso sia corretto
    genome_path = 'best_genome.pkl'  # Il file salvato in precedenza
    play_with_trained_model(config_path, genome_path)
