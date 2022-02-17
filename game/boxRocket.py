import numpy as np

from Box2D import b2World, b2FixtureDef, b2CircleShape, b2Vec2, b2Color

from game.boxSpaceship import BoxSpaceship
from gui.pygletDraw import PygletDraw


class BoxRocket:

	def __init__(self,
	             world: b2World,
	             shooter: BoxSpaceship,
	             heading: b2Vec2,
	             radius: float = 1.0):
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
			b2Vec2(0, -self.radius),
			b2Vec2(0, self.radius),
			b2Vec2(-length, self.radius),
			b2Vec2(-length, -self.radius)
		]

	def display(self, renderer: PygletDraw, layer_index: int):
		# makes shadow look funny when grabbing and redirecting a rocket xD
		self.body.angle = np.arctan2(self.body.linearVelocity.y, self.body.linearVelocity.x)

		transparent = b2Color(self.color)
		transparent.a = 0
		renderer.DrawGradientRect(layer_index, self._get_shadow_verts_translated(), self.shadowColor, transparent)
		renderer.DrawSolidCircle(layer_index, self.body.GetWorldPoint(b2Vec2()), self.radius, b2Vec2(), self.color)

	def _get_shadow_verts_translated(self):
		return [self.body.GetWorldPoint(v) for v in self.shadowVerts]
