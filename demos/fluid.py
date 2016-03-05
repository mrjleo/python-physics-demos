#! /usr/bin/python3
# -*- coding: utf-8 -*-


import pyglet
import numpy as np
import itertools as it


# gravity
g = 5


DROP_RADIUS = 5
SCALE = 30
PARTICLE_SPACING = 0.4
FIXED_PARTICLE_SPACING = 0.1
PARTICLE_MASS = 10.0
DELTA = 0.01


WIDTH = 4 * DROP_RADIUS
HEIGHT = WIDTH
window = pyglet.window.Window(WIDTH * SCALE, HEIGHT * SCALE)


DROP_RADIUS_SQR = DROP_RADIUS ** 2
center = np.array([WIDTH / 2.0, HEIGHT], np.double)
def test_coord(c):
	link = c - center
	return np.dot(link, link) < DROP_RADIUS_SQR


# create drop particles (particles within radius)
part_pos_x = np.arange(center[0] - DROP_RADIUS, center[0] + DROP_RADIUS, PARTICLE_SPACING)
part_pos_y = np.arange(center[1] - DROP_RADIUS, center[1], PARTICLE_SPACING)
part_pos = np.asarray([c for c in it.product(part_pos_x, part_pos_y) if test_coord(c)], np.double)


# create fixed particles (top edge)
fix_part_pos_x = np.arange(0, WIDTH, FIXED_PARTICLE_SPACING)
fix_part_pos_y = np.array([center[1] - FIXED_PARTICLE_SPACING], np.double)
fix_part_pos = np.asarray([c for c in it.product(fix_part_pos_x, fix_part_pos_y)], np.double)


# initialize
part_v = np.zeros_like(part_pos, np.double)
init_f = np.array([0, -g * PARTICLE_MASS], np.double)


def simulate(dt):
	global part_pos, part_v

	def calc_force(p, particles, amp=1.0):
		link = particles - p

		# use squared distances to avoid roots
		dist = np.sum(link ** 2, axis=1).reshape(-1, 1)

		# prevent particles from reacting to themselves by using a zero (0.63246) of the function
		dist[dist == 0] = 0.63246

		# simplified Lennard-Jones potential
		return 20.0 * link / dist ** 2 - 8.0 * link / dist ** 3 * amp

	# particles react to the fixed particles (amplified) and each other
	part_forces = np.asarray([np.sum(calc_force(p, part_pos), axis=0) for p in part_pos], np.double) + np.asarray([np.sum(calc_force(p, fix_part_pos, 1.75), axis=0) for p in part_pos], np.double) + init_f

	part_a = part_forces / PARTICLE_MASS
	part_v = part_v + part_a * DELTA
	part_pos = part_pos + part_v * DELTA


@window.event
def on_draw():
	window.clear()

	# fixed particles
	[pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ('v2d', c * SCALE)) for c in fix_part_pos]

	# particles
	[pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ('v2d', c * SCALE)) for c in part_pos]


pyglet.clock.schedule_interval(simulate, DELTA)
pyglet.app.run()