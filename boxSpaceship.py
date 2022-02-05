from typing import Tuple

from Box2D import (b2World, b2_pi, b2PolygonShape, b2FixtureDef, b2Draw, b2Color)


class BoxSpaceship:

	def __init__(self, world: b2World, pos: Tuple[float, float] = (0, 0)):
		self.fill = b2Color(255, 255, 255)
		self.shape = b2PolygonShape(vertices=[
			(-1, -1),
			(-1, 1),
			(1, 1),
			(1, -1)
		])
		self.body = world.CreateDynamicBody(
			position=pos,
			angle=b2_pi,
			linearDamping=0,
			shapes=[self.shape],
			shapeFixture=b2FixtureDef(density=2.0),
			fixedRotation=True
		)

	def display(self, renderer: b2Draw):
		vertices = []

		for v in self.shape.vertices:
			vertices.append(self.body.GetWorldPoint(v))
		renderer.DrawSolidPolygon(vertices, self.fill)