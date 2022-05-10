import numpy as np
import random
from math import inf


class Particle:
    def __init__(self, lower_bound, upper_bound):

        self.x = np.random.uniform(lower_bound, upper_bound)
        delta = lower_bound - upper_bound
        self.v = np.random.uniform(-delta, delta)
        self.best = -inf
        self.best_position = self.x


class ParticleSwarmOptimization:
    def __init__(self, hyperparams, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.best_global = -inf
        self.best_position = None
        self.num_particles = hyperparams.num_particles
        self.inertia_weight = hyperparams.inertia_weight
        self.cognitive_parameter = hyperparams.cognitive_parameter
        self.social_parameter = hyperparams.social_parameter
        self.counter = 0
        self.particles = []
        for i in range(self.num_particles):
            self.particles.append(Particle(lower_bound, upper_bound))

    def get_best_position(self):
        return self.best_position

    def create_1st_particle(self, position):
        self.particles[0].x = position
        self.particles[0].best_position = self.particles[0].x

    def get_best_value(self):
        return self.best_global

    def get_position_to_evaluate(self):
        contador = self.counter % self.num_particles
        self.particles[contador].x = self.particles[contador].x + self.particles[contador].v

        for i in range(len(self.lower_bound)):
            if self.particles[contador].x[i] < self.lower_bound[i]:
                self.particles[contador].x[i] = self.lower_bound[i]
            if self.particles[contador].x[i] > self.upper_bound[i]:
                self.particles[contador].x[i] = self.upper_bound[i]
        self.counter += 1
        return self.particles[contador].x

    def advance_generation(self):
        w = self.inertia_weight
        iteration = self.cognitive_parameter
        globa = self.social_parameter
        for particle in self.particles:

            rp = random.uniform(0.0, 1.0)
            rg = random.uniform(0.0, 1.0)
            particle.v = (w * particle.v) + (iteration * rp * (particle.best_position - particle.x)) + \
                         (globa * rg * (self.best_position - particle.x))
            delta = self.upper_bound - self.lower_bound
            for i in range(len(self.lower_bound)):
                if particle.v[i] > delta[i]:
                    particle.v[i] = delta[i]
                if particle.v[i] < -delta[i]:
                    particle.v[i] = -delta[i]

    def notify_evaluation(self, value):
        contador = (self.counter - 1) % self.num_particles
        if value > self.particles[contador].best:
            self.particles[contador].best = value
            self.particles[contador].best_position = self.particles[contador].x
        if value > self.best_global:
            self.best_global = value
            self.best_position = self.particles[contador].x

        if self.counter % self.num_particles == 0:
            self.advance_generation()
