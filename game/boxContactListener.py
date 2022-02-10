from Box2D import b2ContactListener, b2World

from game.boxRocket import BoxRocket
from game.boxSpaceship import BoxSpaceship


class BoxContactListener(b2ContactListener):

	def __init__(self, world: b2World):
		b2ContactListener.__init__(self)
		self._world = world
		self._rockets = set()
		self._bodies_to_remove = set()

	def add_rocket(self, rocket: BoxRocket):
		self._rockets.add(rocket)

	def BeginContact(self, contact):
		body_a = contact.fixtureA.body
		body_b = contact.fixtureB.body

		if isinstance(body_a.userData, BoxRocket):
			self._handle_rocket_impact(body_a.userData, body_b.userData)
		if isinstance(body_b.userData, BoxRocket):
			self._handle_rocket_impact(body_b.userData, body_a.userData)

	def _handle_rocket_impact(self, rocket: BoxRocket, other):
		# prevents rockets from destroying other rockets of same spaceship
		if isinstance(other, BoxRocket) and other.shooter == rocket.shooter:
			return
		if isinstance(other, BoxSpaceship):
			# prevents rockets from damaging own spaceship
			if rocket.shooter != other:
				other.damage(20)
			else:
				return
		self._bodies_to_remove.add(rocket.body)
		self._rockets.discard(rocket)

	def remove_bodies(self):
		for body in self._bodies_to_remove:
			self._world.DestroyBody(body)
		self._bodies_to_remove.clear()

	def EndContact(self, contact):
		pass

	def PreSolve(self, contact, oldManifold):
		pass

	def PostSolve(self, contact, impulse):
		pass
