import datetime
import math

from Box2D import b2Color, b2Vec2

from gui.backends.pyglet_framework import PygletDraw


class BoxScan:

	def __init__(self, pos: b2Vec2, radius: float, direction: float, angle: float, color: b2Color = b2Color(0.8, 0.8, 1), duration: float = 0.5):
		self.pos = b2Vec2(pos)
		self.radius = radius
		self.angleStart = direction - angle / 2
		self.angleEnd = direction + angle / 2
		self.duration = datetime.timedelta(seconds=duration)
		self.color = b2Color(color)
		self.start = datetime.datetime.now()
		pass

	def is_over(self):
		dt = datetime.datetime.now() - self.start
		return dt > self.duration

	def display(self, renderer: PygletDraw, layer_index: int):
		dt = datetime.datetime.now() - self.start
		if dt > self.duration:
			return
		fade = 1 - math.pow(dt / self.duration, 3)
		color_mid = b2Color(self.color)
		color_mid.a = 0.05 * fade
		color_out = b2Color(self.color)
		color_out.a = 0.2 * fade

		renderer.DrawGradientArc(layer_index, self.pos, self.radius, self.angleStart, self.angleEnd, color_mid, color_out)
