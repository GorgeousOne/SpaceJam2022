import numpy as np
import copy
from Box2D import b2World, b2FixtureDef, b2CircleShape, b2Vec2, b2Color

from game.boxSpaceship import BoxSpaceship


class BoxRocket:

	def __init__(self,
	             world: b2World,
	             shooter: BoxSpaceship,
	             radius: float = .75):
		self.shooter = shooter
		self.world = world
		self.radius = radius
		self.color = b2Color(shooter.fill)

		self.shadowVerts = []
		self.shadowColor = b2Color(self.color)
		self.shadowColor.a = .5

		self._create_shadow(self.radius * 5)

		self.shape = b2CircleShape
		self.body = self.world.CreateDynamicBody(
			userData=self,  # adds a reference on the body to the rocket object
			allowSleep=True,
			position=shooter.get_location().get_position(),
			angle=shooter.get_location().get_rotation(),
			linearVelocity=shooter.get_location().get_direction() * 30,
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

	def display(self, renderer):
		transparent = b2Color()
		transparent.a = 0
		renderer.DrawGradientRect(self._get_shadow_verts_translated(), self.shadowColor, transparent)
		renderer.DrawSolidCircle(self.body.GetWorldPoint(b2Vec2()), self.radius, b2Vec2(), self.color)

	def _get_shadow_verts_translated(self):
		return [self.body.GetWorldPoint(v) for v in self.shadowVerts]
