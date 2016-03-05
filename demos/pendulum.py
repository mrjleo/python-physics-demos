#! /usr/bin/python3
# -*- coding: utf-8 -*-


import pyglet


# feather constant
k = 5.0
# mass
m = 2.0
omega_sqr = k/m
# damping
damp = 0.001
# initial values
y = 2.5
v = -omega_sqr * y


DELTA = 0.01


SCALE = 40
W_WIDTH, W_HEIGHT = 200, 500
window = pyglet.window.Window(W_WIDTH, W_HEIGHT)


def simulate(dt):
	global y, v

	v = v * (1 - damp) - omega_sqr * y * DELTA
	y = y + v * DELTA


@window.event
def on_draw():
	window.clear()

	x_pos = W_WIDTH / 2.0
	y_pos = W_HEIGHT / 2.0 + y * SCALE

	pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (x_pos, W_HEIGHT, x_pos, y_pos)))
	pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x_pos - 10, y_pos - 10, x_pos - 10, y_pos + 10, x_pos + 10, y_pos + 10, x_pos + 10, y_pos - 10)))


pyglet.clock.schedule_interval(simulate, DELTA)
pyglet.app.run()