#! /usr/bin/python3
# -*- coding: utf-8 -*-


import pyglet
import math


# gravity
g = 9.798
# lengths
l1, l2 = 100, 80
# masses
m1, m2 = 2, 1
# initial values
th1, th2 = math.pi / 2, math.pi
om1, om2 = 0, 0
# damping
damp = 0.001
trail = []


SHOW_TRAIL = True
DELTA = 0.01
SPEED = 10


W_WIDTH, W_HEIGHT = 400, 400
window = pyglet.window.Window(W_WIDTH, W_HEIGHT)


def simulate(dt):
	global th1, th2, om1, om2

	delta = th2 - th1
	m = m1 + m2

	om1_add = (m2 * l1 * om1 ** 2 * math.sin(delta) * math.cos(delta) + m2 * g * math.sin(th2) * math.cos(delta) + m2 * l2 * om2 ** 2 * math.sin(delta) - m * g * math.sin(th1)) / (m * l1 - m2 * l1 * math.cos(delta) ** 2)
	om2_add = (-m2 * l2 * om2 ** 2 * math.sin(delta) * math.cos(delta) + m * (g * math.sin(th1) * math.cos(delta) - l1 * om1 ** 2 * math.sin(delta) - g * math.sin(th2))) / (m * l2 - m2 * l2 * math.cos(delta) ** 2)

	om1 = om1 * (1 - damp) + om1_add * DELTA * SPEED
	om2 = om2 * (1 - damp) + om2_add * DELTA * SPEED

	th1 = th1 + om1 * DELTA * SPEED
	th2 = th2 + om2 * DELTA * SPEED


@window.event
def on_draw():
	global trail
	window.clear()

	if SHOW_TRAIL:
		pyglet.graphics.draw(int(len(trail) / 2), pyglet.gl.GL_POINTS, ('v2f', trail))

	anchor_x = W_WIDTH / 2.0
	anchor_y = W_HEIGHT / 2.0

	pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (anchor_x - 2, anchor_y - 2, anchor_x - 2, anchor_y + 2, anchor_x + 2, anchor_y + 2, anchor_x + 2, anchor_y - 2)))

	pt1_x = anchor_x + math.sin(th1) * l1
	pt1_y = anchor_y - math.cos(th1) * l1

	pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (anchor_x, anchor_y, pt1_x, pt1_y)))
	pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (pt1_x - 2, pt1_y - 2, pt1_x - 2, pt1_y + 2, pt1_x + 2, pt1_y + 2, pt1_x + 2, pt1_y - 2)))

	pt2_x = pt1_x + math.sin(th2) * l2
	pt2_y = pt1_y - math.cos(th2) * l2

	pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (pt1_x, pt1_y, pt2_x, pt2_y)))
	pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (pt2_x - 2, pt2_y - 2, pt2_x - 2, pt2_y + 2, pt2_x + 2, pt2_y + 2, pt2_x + 2, pt2_y - 2)))

	if SHOW_TRAIL:
		trail.append(pt2_x)
		trail.append(pt2_y)


pyglet.clock.schedule_interval(simulate, DELTA)
pyglet.app.run()