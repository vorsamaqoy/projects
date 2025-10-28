import pygame
import neat
import pickle
import sys
import time

pygame.init()

# Impostazioni schermo
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Paddle Game with NEAT')

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
def draw_info(screen, generation, score, best_fitness):
    font = pygame.font.Font(None, 36)
    generation_text = font.render(f"Generazione: {generation}", True, (255, 255, 255))
    screen.blit(generation_text, (10, 10))
    score_text = font.render(f"Punteggio: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 50))
    fitness_text = font.render(f"Fitness Migliore: {best_fitness:.2f}", True, (255, 255, 255))
    screen.blit(fitness_text, (10, 90))

# Variabile globale per tenere traccia della generazione corrente
current_generation = 0

# Funzione per valutare i genomi
def eval_genomes(genomes, config):
    global current_generation
    current_generation += 1
    print(f"****** Running generation {current_generation} ******")
    
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        paddle = pygame.Rect(screen_width - 700, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)
        ball = pygame.Rect(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, ball_size, ball_size)
        
        score = 0
        best_fitness = 0
        
        # Variabili per penalità
        last_paddle_y = paddle.y
        time_last_moved = time.time()
        penalize_interval = 5  # Intervallo di tempo in secondi per penalizzare
        
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

            # Penalità se il paddle rimane fermo per troppo tempo
            if paddle.y == last_paddle_y:
                if time.time() - time_last_moved > penalize_interval:
                    genome.fitness -= 1  # Penalità per non movimento
            else:
                time_last_moved = time.time()  # Resetta il timer
                last_paddle_y = paddle.y
            
            # Calcola il fitness
            genome.fitness = score
            if genome.fitness > best_fitness:
                best_fitness = genome.fitness
            
            # Verifica se il punteggio ha superato la soglia
            if genome.fitness >= 20:
                print(f"Genoma {genome_id} ha raggiunto il punteggio {genome.fitness}!")
                # Salva il genoma vincente
                with open("best_genome.pkl", "wb") as f:
                    pickle.dump(genome, f)
                # Termina l'addestramento interrompendo il ciclo
                pygame.quit()
                sys.exit()
    
            # Disegna lo sfondo
            screen.fill(black)
            
            # Disegna il paddle e la palla
            pygame.draw.rect(screen, white, paddle)
            pygame.draw.ellipse(screen, white, ball)
            
            # Mostra informazioni
            draw_info(screen, current_generation, score, best_fitness)
            
            # Aggiorna lo schermo
            pygame.display.flip()
            
            # Imposta il frame rate
            clock.tick(240)
        
        print(f"Genoma {genome_id}: Fitness finale {genome.fitness}")

# Funzione principale per eseguire NEAT
def run_neat(config_file):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    try:
        winner = population.run(eval_genomes, 50)  # Numero massimo di generazioni aumentato
    except SystemExit:
        # Il sistema si è fermato perché un genoma ha raggiunto il punteggio desiderato
        print("Addestramento interrotto: un genoma ha raggiunto il punteggio desiderato.")
        return

    # Salvare il genoma migliore se non è già stato salvato
    try:
        with open("best_genome.pkl", "rb") as f:
            pass  # Il file esiste già
    except FileNotFoundError:
        with open("best_genome.pkl", "wb") as f:
            pickle.dump(winner, f)
        print('\nMigliore genoma salvato:\n{!s}'.format(winner))

    print('\nMigliore genoma:\n{!s}'.format(winner))

# Avviare il programma
if __name__ == "__main__":
    config_path = 'config-feedforward.txt'
    run_neat(config_path)
