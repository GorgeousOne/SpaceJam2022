import random
import math
from Box2D import b2Draw, b2Color, b2Vec2

STAR_SHAPE = [
	b2Vec2(-0.5, -0.5),
	b2Vec2(-0.5, 0.5),
	b2Vec2(0.5, 0.5),
	b2Vec2(0.5, -0.5),
]


def _create_rect(pos: b2Vec2, size: float):
	return [pos + vec * size for vec in STAR_SHAPE]


class BoxBackground:

	def __init__(self, size: float):
		self.size = size
		self.starsAmount = 100
		self.stars = [{
			"frequency": random.random(),
			"shape": _create_rect(b2Vec2(random.random()*size, random.random()*size), random.uniform(0.6,1) * self.size/200)}
			for i in range(self.starsAmount)
		]

	def display(self, renderer: b2Draw, frame_count):
		for star in self.stars:
			luminance = (0.5 * math.sin(frame_count/100 * star["frequency"]) + 0.5)
			color = b2Color(luminance, luminance, luminance + 0.1)
			renderer.DrawGradientRect(star["shape"], color, color)

