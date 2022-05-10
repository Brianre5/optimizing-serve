import numpy as np

# Simulation Parameters
PIX2M = 3.0 / 100.0  # factor to convert from pixels to meters
M2PIX = 1.0 / PIX2M  # factor to convert from meters to pixels
SIMULATION_FREQUENCY = 60.0  # Frequency of simulation
SIMULATION_SAMPLE_TIME = 1.0 / SIMULATION_FREQUENCY
DRAW_FREQUENCY = 60.0  # Screen update frequency
MAX_ACCELERATED_FACTOR = 100  # How much faster than realtime the simulation is executed in accelerated mode
DEFAULT_ACCELERATED_FACTOR = MAX_ACCELERATED_FACTOR
MAX_EPISODE_TIME = 2.75  # Time limit of a training episode
RAIO_QUADRIL = 0.166  # m
# Formacoes = [P1, Lib, P2, C, Lev, Opos], o numero da formacao representa a posição do levantador
formation_1 = [(15.4, 2.3), (16.2, 4.5), (16, 7), (10, 4.8), (16.2, 2), (10.5, 8)]
formation_2 = [(15.4, 2.3), (16.2, 4.5), (15.5, 7), (10, 8.2), (10.5, 2), (17.2, 5.4)]
formation_3 = [(16, 2), (16.2, 4.5), (16, 7), (11, 2.3), (10, 4), (17.5, 3)]
formation_4 = [(15.8, 7), (15.5, 2.3), (16.2, 4.7), (11, 7.8), (10, 8.3), (17.2, 1)]
formation_5 = [(15.8, 7), (16, 2.3), (16.2, 4.7), (12, 8.5), (13, 8), (11, 1.5)]
formation_6 = [(15.8, 7), (16.2, 5), (16.1, 2), (11, 0.9), (11.5, 3), (10, 1.8)]


class Params:
    """
    Represents an auxiliary class for storing parameters.
    I know this is bad hack, but we are using Python anyway.
    """
    pass
