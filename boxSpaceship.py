from typing import Tuple

from Box2D import (b2World, b2_pi, b2PolygonShape, b2FixtureDef)


class BoxSpaceship:

	def __init__(self, world: b2World, pos: Tuple[float, float] = (0, 0)):
		shape = b2PolygonShape(vertices=[
			(-1, -1),
			(-1, 1),
			(1, 1),
			(1, -1)
		])

		self.body = world.CreateDynamicBody(
			position=pos,
			angle=b2_pi,
			linearDamping=0,
			shapes=[shape],
			shapeFixture=b2FixtureDef(density=2.0),
			fixedRotation=True
		)
		pass
