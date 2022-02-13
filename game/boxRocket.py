import numpy as np

from Box2D import b2World, b2FixtureDef, b2CircleShape, b2Vec2, b2Color, b2Draw

from game.boxSpaceship import BoxSpaceship


class BoxRocket:

	def __init__(self,
	             world: b2World,
	             shooter: BoxSpaceship,
	             heading: b2Vec2,
	             radius: float = .75):
		self.shooter = shooter
		self.world = world
		self.radius = radius
		self.color = b2Color(shooter.color)

		self.shadowVerts = []
		self.shadowColor = b2Color(self.color)
		self.shadowColor.a = .5

		self._create_shadow(self.radius * 5)

		self.shape = b2CircleShape
		self.body = self.world.CreateDynamicBody(
			userData=self,  # adds a reference on the body to the rocket object
			allowSleep=True,
			position=shooter.get_location().get_position(),
			angle=np.arctan2(heading.y, heading.x),
			linearVelocity=heading,
			fixtures=b2FixtureDef(
				shape=b2CircleShape(radius=radius),
				isSensor=True,
				# restitution=.5,  # bounciness between 0 and 1
			)
		)

	def _create_shadow(self, length):
		self.shadowVerts = [
			b2Vec2(0, self.radius),
			b2Vec2(0, -self.radius),
			b2Vec2(-length, self.radius),
			b2Vec2(-length, -self.radius)
		]

	def display(self, renderer: b2Draw):
		transparent = b2Color()
		transparent.a = 0
		renderer.DrawGradientRect(self._get_shadow_verts_translated(), self.shadowColor, transparent)
		renderer.DrawSolidCircle(self.body.GetWorldPoint(b2Vec2()), self.radius, b2Vec2(), self.color)

	def _get_shadow_verts_translated(self):
		return [self.body.GetWorldPoint(v) for v in self.shadowVerts]
