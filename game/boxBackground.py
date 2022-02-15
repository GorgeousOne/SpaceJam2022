import numpy as np
import random
import math
from Box2D import b2World, b2Draw, b2Color, b2Vec2


class BoxBackground:

	def __init__(self, world: b2World, size: float, thickness: float):
		self.size = size
		self.thickness = thickness
		self.starsAmount = 100
		self.stars = [{"magnitude": random.uniform(0.6,1), "frequency": random.random(), "position": {"x": random.random()*size, "y":random.random()*size} } for i in range(self.starsAmount) ]
		self.fill = b2Color(255, 255, 255)


	def display(self, renderer: b2Draw, frameCount):
		# from custom pyglet framework
		for star in self.stars:
			luminance = (0.5 * math.sin(frameCount/100 * star["frequency"]) + 0.5)
			color = b2Color(luminance, luminance, luminance + 0.1)
			renderer.DrawPoint([star["position"]["x"], star["position"]["y"]], (self.size/10) * star["magnitude"], color)
		
