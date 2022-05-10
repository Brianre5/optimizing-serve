import pygame
import numpy as np
import simulation
from math import inf
from simulation import simulate, ball1, ball2, enemies
from trajetoria import caminho
from constants import MAX_EPISODE_TIME, Params
from particle_swarm_optimization import ParticleSwarmOptimization
import matplotlib.pyplot as plt
pygame.init()

# Inicialização do pygame
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((800, 740))
pygame.display.set_caption("Simulador de saque")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 20, True)
# Mude a formacao dos recebedores inimigos
formacao = 2  # 1, 2, ..., 6. Posicao do levantador


def save_best_position(positio, qual):
    fil = open("best_position.txt", 'w')
    print(positio)
    for contt in range(9):
        fil.write(str(positio[contt]) + '\n')
    print(qual)
    fil.write(str(qual))
    fil.close()


def plot_results():
    """
    Plots the results of the optimization.
    """
    fig_format = 'png'

    plt.figure()
    plt.plot(quality_history)
    plt.xlabel('Iteratação')
    plt.ylabel('Qualidade')
    plt.title('Convergência da qualidade')
    plt.grid()
    plt.savefig('line_quality_convergence.%s' % fig_format, format=fig_format)
    best_history = []
    best = -inf
    for q in quality_history:
        if q > best:
            best = q
        best_history.append(best)

    plt.figure()
    plt.plot(best_history)
    plt.xlabel('Iteratação')
    plt.ylabel('Melhor qualidade')
    plt.title('Convergência da melhor qualidade')
    plt.grid()
    plt.savefig('line_best_convergence.%s' % fig_format, format=fig_format)
    plt.show()


running = True  # Se o programa esta rodando
accelerated_mode = False  # Se a execução está em modo acelerado(+ rápido que o mundo real)
accelerated_factor = 10
previous_keys = pygame.key.get_pressed()
training = True  # Se as particulas estão treinando (a otimização está ocorrendo)


def write_text():
    text = font.render('Iteração: ' + str(training_iteration), True, (0, 0, 0))
    screen.blit(text, (100, 600))
    text = font.render('Training: ' + str(training), True, (0, 0, 0))
    screen.blit(text, (100, 630))
    text = font.render('Aceleracao: ' + str(accelerated_factor), True, (0, 0, 0))
    screen.blit(text, (100, 660))
    text = font.render('Pressione P para plotar os resultados', True, (0, 0, 0))
    screen.blit(text, (100, 690))


def process_inputs():
    global accelerated_mode, training, accelerated_factor
    if keys[pygame.K_a] and not previous_keys[pygame.K_a]:
        accelerated_mode = not accelerated_mode
    if keys[pygame.K_t] and not previous_keys[pygame.K_t]:
        training = not training
    if keys[pygame.K_UP] and not previous_keys[pygame.K_UP]:
        accelerated_factor += 1
    if keys[pygame.K_DOWN] and not previous_keys[pygame.K_DOWN]:
        accelerated_factor -= 1
    if keys[pygame.K_p] and not previous_keys[pygame.K_p]:
        plot_results()
    accelerated_factor = min(max(1, accelerated_factor), 20)


# Defining PSO hyperparameters
hyperparams = Params()
hyperparams.num_particles = 100
hyperparams.inertia_weight = 0.7
hyperparams.cognitive_parameter = 0.5
hyperparams.social_parameter = 0.7
lower_bound = np.array([-4, 1.9, 0, 5, -3, -12, 0, -15, -15])
upper_bound = np.array([0, 3, 9, 20, 10, 12, 0, 15, 0])
pso = ParticleSwarmOptimization(hyperparams, lower_bound, upper_bound)

# Initializing history
position_history = []  # history of evaluated particle positions
quality_history = []  # history of evaluated qualities

# O primeiro parametro usado vai ser o melhor já achado
f = open("best_position.txt", 'r')
position = pso.get_position_to_evaluate()
for i in range(9):
    stri = f.readline()
    position[i] = float(stri)
f.close()
position = np.array([position[0], position[1], position[2], position[3], position[4], position[5], position[6],
                     position[7], position[8]])
pso.create_1st_particle(position)
[sol, y_rede, x_final, z_final, tempofinal, index, vel_angular] = caminho(position, MAX_EPISODE_TIME)
indice = 0
training_iteration = 1

while running:
    simulate()
    clock.tick(1000)
    num_steps = 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            save_best_position(pso.get_best_position(), pso.get_best_value())
    keys = pygame.key.get_pressed()
    process_inputs()

    if accelerated_mode:
        num_steps = accelerated_factor
    for i in range(num_steps):
        write_text()
        qualidade = simulation.evaluate(sol, y_rede, x_final, z_final, tempofinal, index, vel_angular, formacao)

        # Adicionar essa itecao na historia
        position_history.append(np.array(position))
        quality_history.append(qualidade)

        # Mostrar a trajetória da bola de volei
        ball1(sol[indice][0], sol[indice][1])
        ball2(sol[indice][0], sol[indice][2])
        # Mostrar os recebedores
        enemies(formacao)
        if indice <= index:
            indice += 1
        if indice > index:
            indice = 0
            if training:
                training_iteration += 1
                print(' Qualidade: ' + str(qualidade))
                pso.notify_evaluation(qualidade)
                position = pso.get_position_to_evaluate()
            else:
                print(' Qualidade: ' + str(qualidade))
                position = pso.get_best_position()
            [sol, y_rede, x_final, z_final, tempofinal, index, vel_angular] = caminho(position, MAX_EPISODE_TIME)
            qualidade = 0
    previous_keys = keys
    pygame.display.update()

