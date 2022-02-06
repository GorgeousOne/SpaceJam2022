from typing import Tuple

import numpy as np
from Box2D import (b2World, b2PolygonShape, b2FixtureDef, b2Draw, b2Color)

from logic.location import Location


class BoxSpaceship:

	def __init__(self, world: b2World, pos: Tuple[float, float] = (0, 0), color: b2Color = b2Color(1., 1., 1.)):
		self.fill = b2Color(color)
		self.shape = b2PolygonShape(vertices=[
			(2.618, 0),
			(0, -1),
			(-1, 0),
			(0, 1),
		])
		self.body = world.CreateDynamicBody(
			position=pos,
			# angle=b2_pi,
			linearDamping=0,
			shapes=[self.shape],
			shapeFixture=b2FixtureDef(density=2.0),
			# fixedRotation=True # fixes angular velocity to one value
		)
	# self.body.linearVelocity += b2Vec2(20, 1)
	# self.body.angularVelocity += np.pi

	def get_location(self):
		pos = self.body.position
		vel = self.body.linearVelocity
		return Location(np.array([pos.x, pos.y]), self.body.angle, np.array([vel.x, vel.y]))

	def display(self, renderer: b2Draw):
		vertices = []

		for v in self.shape.vertices:
			vertices.append(self.body.GetWorldPoint(v))
		renderer.DrawSolidPolygon(vertices, self.fill)
