#! /usr/bin/python3
# -*- coding: utf-8 -*-


import pyglet
import numpy as np


# gravitational constant
G = 6.67384e-11


DELTA = 0.01


W_WIDTH, W_HEIGHT = 500, 500
window = pyglet.window.Window(W_WIDTH, W_HEIGHT)


class Planet(object):
	def __init__(self, pos_x, pos_y, radius, mass, v_x, v_y):
		self.pos = np.array([pos_x, pos_y], np.double)
		self.radius = radius
		self.mass = mass
		self.v = np.array([v_x, v_y], np.double)
		self.F = np.array([0, 0], np.double)


	# F = G * m * M / r^2 * e_r
	def calc_force(self, other_planet):
		link = other_planet.pos - self.pos
		dist = np.linalg.norm(link)

		return G * self.mass * other_planet.mass / dist ** 3 * link


	def react(self, other_planet):
		self.F = self.F + self.calc_force(other_planet)


	def move(self, dt):
		a = self.F / self.mass

		self.v = self.v + a * dt
		self.pos = self.pos + self.v * dt

		self.F = np.array([0, 0], np.double)


# https://sites.google.com/site/swinesmallpygletexamples/immediate-circle
def draw_circle(pos, radius):
    iterations = int(2 * radius * np.pi)
    s = np.sin(2 * np.pi / iterations)
    c = np.cos(2 * np.pi / iterations)

    dx, dy = radius, 0

    pyglet.gl.glBegin(pyglet.gl.GL_TRIANGLE_FAN)
    pyglet.gl.glVertex2f(pos[0], pos[1])
    for i in range(iterations + 1):
        pyglet.gl.glVertex2f(pos[0] + dx, pos[1] + dy)
        dx, dy = (dx * c - dy * s), (dy * c + dx * s)
    pyglet.gl.glEnd()


def simulate(dt):
	for p1 in planets:
		for p2 in planets:
			if p1 != p2:
				p1.react(p2)
	
	for p in planets:
		p.move(DELTA)


@window.event
def on_draw():
    window.clear()
    for p in planets:
    	draw_circle(p.pos, p.radius)


planets = [
	# pos_x, pos_y, radius, mass, v_x, v_y
	Planet(W_WIDTH / 2.0, W_HEIGHT / 2.0, 40, 2e16, 0, 0),
	Planet(W_WIDTH / 3.0, W_HEIGHT / 2.0, 20, 2e10, 0, 150),
	Planet(W_WIDTH / 4.0, W_HEIGHT / 2.0, 10, 1e8, 0, -100)
]


pyglet.clock.schedule_interval(simulate, DELTA)
pyglet.app.run()