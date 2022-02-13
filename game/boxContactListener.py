from Box2D import b2ContactListener, b2World, b2Color

from game.boxExplosion import BoxExplosion
from game.boxRocket import BoxRocket
from game.boxScan import BoxScan
from game.boxSpaceship import BoxSpaceship


class BoxContactListener(b2ContactListener):

	def __init__(self, world: b2World):
		b2ContactListener.__init__(self)
		self._world = world
		self.spaceships = set()
		self.rockets = set()
		self.explosions = set()
		self.scans = set()
		self._bodies_to_remove = set()

	def add_rocket(self, rocket: BoxRocket):
		self.rockets.add(rocket)

	def add_spaceship(self, spaceship: BoxSpaceship):
		self.spaceships.add(spaceship)

	def add_scan(self, scan: BoxScan):
		self.scans.add(scan)

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
				self._handle_spaceship_damage(other)
			else:
				return
		self._bodies_to_remove.add(rocket.body)
		self.rockets.discard(rocket)
		self.explosions.add(BoxExplosion(rocket.body.position, 3, 1, rocket.color))

	def _handle_spaceship_damage(self, spaceship):
		spaceship.damage(20)
		if spaceship.health <= 0:
			self._bodies_to_remove.add(spaceship.body)
			self.spaceships.discard(spaceship)
			self.explosions.add(BoxExplosion(spaceship.body.position, 5, 2, b2Color(1, 0, 0)))

	def remove_bodies(self):
		for scan in list(self.scans):
			if scan.is_over():
				self.scans.discard(scan)

		for explosion in list(self.explosions):
			if explosion.is_over():
				self.explosions.discard(explosion)

		for body in self._bodies_to_remove:
			self._world.DestroyBody(body)
		self._bodies_to_remove.clear()

	def EndContact(self, contact):
		pass

	def PreSolve(self, contact, oldManifold):
		pass

	def PostSolve(self, contact, impulse):
		pass
