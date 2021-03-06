import datetime
import math

from Box2D import b2Color, b2Vec2

from render.pygletDraw import PygletDraw


class BoxExplosion:

	def __init__(self, pos: b2Vec2, radius: float, duration: float = 1, color: b2Color = b2Color(1, 1, 1)):
		self.pos = b2Vec2(pos)
		self.radius = radius
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
		scale = 1 - math.pow(1 - (dt / self.duration), 3)
		color_mid = b2Color(self.color)
		color_out = b2Color(self.color)
		color_mid.a = 0.2 * (1 - scale)
		color_out.a = (1 - scale)
		renderer.DrawGradientCirc(layer_index, self.pos, self.radius * scale, color_mid, color_out)

