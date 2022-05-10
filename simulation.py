import pygame
from constants import M2PIX, MAX_EPISODE_TIME, formation_3, formation_1, formation_2, formation_4, RAIO_QUADRIL,\
    formation_5, formation_6
import math
import numpy as np

screen = pygame.display.set_mode((800, 740))
ball1Img = pygame.image.load('volleyball.png')
ball2Img = pygame.image.load('volleyball.png')


def simulate():
    screen.fill((255, 255, 255))
    # Quadra de cima(eixo xy)
    pygame.draw.line(screen, (0, 0, 0), (100, 200), (700, 200), 3)
    pygame.draw.line(screen, (0, 0, 0), (400, 200), (400, 152), 1)
    pygame.draw.line(screen, (0, 0, 0), (400, 152.4), (400, 119), 3)
    # Quadra de baixo(eixo xz)
    pygame.draw.line(screen, (0, 0, 0), (100, 250), (700, 250), 3)
    pygame.draw.line(screen, (0, 0, 0), (100, 550), (700, 550), 3)
    pygame.draw.line(screen, (0, 0, 0), (100, 250), (100, 550), 3)
    pygame.draw.line(screen, (0, 0, 0), (700, 250), (700, 550), 3)
    pygame.draw.line(screen, (0, 0, 0), (400, 550), (400, 250), 2)
    pygame.draw.line(screen, (0, 0, 0), (300, 550), (300, 250), 1)
    pygame.draw.line(screen, (0, 0, 0), (500, 550), (500, 250), 1)


def enemies(formacao):
    posicao = 0
    if formacao == 1:
        posicao = formation_1
    if formacao == 2:
        posicao = formation_2
    if formacao == 3:
        posicao = formation_3
    if formacao == 4:
        posicao = formation_4
    if formacao == 5:
        posicao = formation_5
    if formacao == 6:
        posicao = formation_6

    for i in range(3):
        formation = posicao[i]
        x = formation[0]
        y = formation[1]
        xp = 100 + x * M2PIX
        yp = 250 + y * M2PIX
        pygame.draw.circle(screen, (255, 0, 0), (xp, yp), 100*RAIO_QUADRIL, 3)
    for i in range(3):
        formation = posicao[i+3]
        x = formation[0]
        y = formation[1]
        xp = 100 + x * M2PIX
        yp = 250 + y * M2PIX
        pygame.draw.circle(screen, (0, 255, 0), (xp, yp), 100 * RAIO_QUADRIL, 3)


def ball1(x, y):
    xp = 100 - 8 + x * M2PIX
    yp = 200 - 8 - y * M2PIX
    screen.blit(ball1Img, (xp, yp))


def ball2(x, y):
    xp = 100 - 8 + x * M2PIX
    yp = 250 - 8 + y * M2PIX
    if np.greater(y, -1) & np.less(y, 10):
        screen.blit(ball2Img, (xp, yp))
    pygame.draw.line(screen, (255, 0, 0), (0, 250 - 8 + -1 * M2PIX), (800, 250 - 8 + -1 * M2PIX), 1)
    pygame.draw.line(screen, (255, 0, 0), (0, 250 - 8 + 10 * M2PIX), (800, 250 - 8 + 10 * M2PIX), 1)


def distancia(formacao,xf,yf):
    posicao = 0
    if formacao == 1:
        posicao = formation_1
    if formacao == 2:
        posicao = formation_2
    if formacao == 3:
        posicao = formation_3
    if formacao == 4:
        posicao = formation_4
    if formacao == 5:
        posicao = formation_5
    if formacao == 6:
        posicao = formation_6
    dist = 10000000
    for i in range(6):
        jogador = posicao[i]
        new_d = math.sqrt((xf-jogador[0])**2 + (yf-jogador[1])**2)
        if new_d < dist:
            dist = new_d
    return dist


def evaluate(sol, y_rede, x_final, z_final, tempofinal, index, vel_angular, formacao):
    pv = 28
    pd = 45
    pt = 60
    pw = 0.1
    dist = 0
    erro = -20
    # 5 cm from ball diameter
    dentro = True
    if y_rede <= 2.43 + 0.05:
        erro += 200
        dentro = False

    if index > int(MAX_EPISODE_TIME*1000) - 3:
        erro += 100

    if z_final + 0.051725 < 0 or z_final - 0.051725 > 9:
        erro += 150 + 15 * min(abs(z_final - 0), abs(z_final - 9))
        dentro = False
    if x_final - 0.051725 < 9 or x_final - 0.051725 > 18:
        erro += 150 + 15 * min(abs(x_final - 9), abs(x_final - 18))
        dentro = False
    # Se a bola for dentro calculamos a distancia da bola aos jogadores
    if dentro:
        dist = distancia(formacao, x_final, z_final)

    v_final = math.sqrt( (sol[index][3]) ** 2 + (sol[index][4]) ** 2 + (sol[index][5]) ** 2 )
    reward = pv * v_final - pt * tempofinal + pd * dist + pw * vel_angular - erro
    return reward
