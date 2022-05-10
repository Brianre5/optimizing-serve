from scipy.integrate import odeint
import numpy as np
import math


# Funcao baseada na EDO da trajetoria em x, y, z e nas velocidades a qualquer momento
def trajetoria(cond_inicial, t):
    g = 9.8
    ks = 0.0006586161
    kd = 0.012381
    mass = 0.27
    x, y, z, vel_x, vel_y, vel_z, wx, wy, wz = cond_inicial
    velocidade = [vel_x, vel_y, vel_z]
    vel_angular = [wx, wy, wz]
    f_spin = np.cross(vel_angular, velocidade)
    dydt = [vel_x, vel_y, vel_z,
            -(kd / mass) * vel_x * math.sqrt(vel_x ** 2 + vel_y ** 2 + vel_z ** 2) + ks / mass * f_spin[0],
            -g - (kd / mass) * vel_y * math.sqrt(vel_x ** 2 + vel_y ** 2 + vel_z ** 2) + ks / mass * f_spin[1],
            -(kd / mass) * vel_z * math.sqrt(vel_x ** 2 + vel_y ** 2 + vel_z ** 2) + ks / mass * f_spin[2],
            wx, wy, wz]
    return dydt


def caminho(y0, tmax, ):
    n_iterations = int(1000*tmax)
    time = np.linspace(0, tmax, n_iterations)
    sol = odeint(trajetoria, y0, time)
    y_rede = 0
    x_final = 0
    z_final = 0
    tempofinal = 0
    vel_angular = 0
    index = n_iterations - 1
    for i in range(n_iterations):
        if abs(sol[i][0] - 9) < 0.01:
            y_rede = sol[i][1]
        if sol[i][1] < 0.10345:
            x_final = sol[i][0]
            z_final = sol[i][2]
            vel_angular = math.sqrt( sol[i][6]**2 + sol[i][7]**2 + sol[i][8]**2)
            tempofinal = time[i]
            index = i
            break
    return [sol, y_rede, x_final, z_final, tempofinal, index, vel_angular]
