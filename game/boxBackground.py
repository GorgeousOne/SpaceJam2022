import math
import random

from Box2D import b2Draw, b2Color, b2Vec2

from gui.backends.pyglet_framework import PygletDraw

STAR_SHAPE = [
	b2Vec2(-1, 0),
	b2Vec2(0, 1),
	b2Vec2(1, 0),
	b2Vec2(0, -1),
]


def _create_star(pos: b2Vec2, size: float):
	return [pos + vec * size for vec in STAR_SHAPE]


class BoxBackground:

	def __init__(self, size: float):
		self.size = size
		self.starsAmount = 100
		self.stars = [{
			"frequency": random.random(),
			"shape": _create_star(b2Vec2(random.random() * size, random.random() * size), random.uniform(0.2, 0.4) * self.size / 100)}
			for i in range(self.starsAmount)
		]

	def display(self, renderer: PygletDraw, layer_index: int, frame_count: int):
		for star in self.stars:
			luminance = 0.5 * math.sin(frame_count / 100 * star["frequency"]) + 0.5
			color = b2Color(luminance, luminance, luminance + 0.1)
			renderer.DrawGradientRect(layer_index, star["shape"], color, color)

		# draw grid:
		unit = 10
		steps = int(math.ceil(self.size / unit))
		for x in range(1, steps):
			renderer.DrawSegment(layer_index, b2Vec2(x * unit, 0), b2Vec2(x * unit, self.size), b2Color(0.1, 0.1, 0.15))

		for y in range(1, steps):
			renderer.DrawSegment(layer_index, b2Vec2(0, y * unit), b2Vec2(self.size, y * unit), b2Color(0.1, 0.1, 0.15))
