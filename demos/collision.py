#! /usr/bin/python3
# -*- coding: utf-8 -*-


import pyglet
import numpy as np


# gravity
g = 9.798
# feather constants
K1 = 1000 # when ball still moves towards obstacle
K2 = 100 # when ball has bounced off obstacle
# damping
damp = 0


DELTA = 0.01
SPEED = 4


W_WIDTH, W_HEIGHT = 500, 500
window = pyglet.window.Window(W_WIDTH, W_HEIGHT)


class Ball(object):
	def __init__(self, pos_x, pos_y, radius, mass):
		self.pos = np.array([pos_x, pos_y], np.double)
		self.radius = radius
		self.mass = mass
		self.v = np.array([0, 0], np.double)
		self.F = np.array([0, -self.mass * g], np.double)


	def distance(self, obstacle):
		# ignore special cases where the ball hits an edge of the obstacle
		dist1 = np.linalg.norm(obstacle.pos1 - self.pos)
		dist2 = np.linalg.norm(obstacle.pos2 - self.pos)
		if dist1 > obstacle.len or dist2 > obstacle.len:
			return np.Infinity

		# distance of the ball's center from obstacle
		r = (obstacle.dir_vec[0] * (self.pos[0] - obstacle.pos1[0]) + obstacle.dir_vec[1] * (self.pos[1] - obstacle.pos1[1])) / np.sum(np.square(obstacle.dir_vec))
		return np.linalg.norm(obstacle.pos1 + r * obstacle.dir_vec - self.pos)


	def react(self, obstacle):
		dist = self.distance(obstacle)

		# continuous collision detection
		if dist < self.radius:
			
			# make normal point in right direction (towards the ball)
			if np.dot(obstacle.normal, self.pos - obstacle.pos1) < 0:
				obs_normal = obstacle.normal * -1
			else:
				obs_normal = obstacle.normal

			# check whether velocity points in same direction as the normal
			if np.dot(obs_normal, self.v) < 0:
				k = K1
			else:
				k = K2

			self.F = self.F + k * (self.radius - dist) * obs_normal
			

	def move(self, dt):
		a = self.F / self.mass
		self.v = self.v * (1 - damp) + a * dt
		self.pos = self.pos + self.v * dt
		self.F = np.array([0, -self.mass * g], np.double)


	def draw(self):
		draw_circle(self.pos, self.radius)


class Obstacle(object):
	def __init__(self, pos1_x, pos1_y, pos2_x, pos2_y):
		self.pos1 = np.array([pos1_x, pos1_y], np.double)
		self.pos2 = np.array([pos2_x, pos2_y], np.double)
		self.dir_vec = self.pos1 - self.pos2
		self.len = np.linalg.norm(self.dir_vec)

		self.normal = np.array([-self.dir_vec[1], self.dir_vec[0]], np.double)

		# normalize
		self.normal = self.normal / np.linalg.norm(self.normal)


	def draw(self):
		pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (self.pos1[0], self.pos1[1], self.pos2[0], self.pos2[1])))


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
	for b in balls:
		for o in obstacles:
			b.react(o)
		b.move(DELTA * SPEED)


@window.event
def on_draw():
    window.clear()
    for o in balls + obstacles:
    	o.draw()


balls = [
	# pos_x, pos_y, radius, mass
	Ball(W_WIDTH / 8.0, 4 * W_HEIGHT / 5.0, 15, 5)
]
obstacles = [
	# pos1_x, pos1_y, pos2_x, pos2_y
	Obstacle(1, 3 * W_HEIGHT / 4.0, W_WIDTH / 2.0, W_HEIGHT / 2.0),
	Obstacle(W_WIDTH, W_HEIGHT / 2.0, W_WIDTH / 2.0, W_HEIGHT / 4.0)
]

pyglet.clock.schedule_interval(simulate, DELTA)
pyglet.app.run()