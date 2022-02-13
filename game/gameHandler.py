import math
from typing import List

from Box2D import b2Vec2, b2World, b2Color

from game.boxContactListener import BoxContactListener
from game.boxRocket import BoxRocket
from game.boxScan import BoxScan
from game.boxSpaceship import BoxSpaceship
from logic import scanning
from logic.location import Location
from logic.pilotAction import PilotAction


class GameHandler:

	def __init__(self, world: b2World, contact_listener: BoxContactListener):
		self.world = world
		self.contact_listener = contact_listener
		self.rocket_speed = 10
		self.tick_energy = 100
		self.colorScanSuccess = b2Color(1, .3, .3)

	def update(self):
		for spaceship in self.contact_listener.spaceships:
			# try:
			action = spaceship.update(self.tick_energy)
			self.handle_pilot_action(spaceship, action)
			# except Exception as e:
			# 	print(str(e.__traceback__))
			# 	continue

	def handle_pilot_action(self, spaceship: BoxSpaceship, action: PilotAction):
		if not action:
			return
		if action.scan_action:
			self.handle_pilot_scan(spaceship, action.scan_action, action)
			return
		if action.move_action:
			self.handle_pilot_move(spaceship, action.move_action)
		if action.shoot_action:
			self.handle_pilot_shoot(spaceship, action.shoot_action)

	def handle_pilot_scan(self, spaceship: BoxSpaceship, scan: dict, action: PilotAction):
		# TODO more better error raising
		energy_cost = scanning.calculate_scan_energy_cost(scan.get("angle"), scan.get("radius"))

		if energy_cost > spaceship.energy:
			raise ValueError("Not enough energy to perform scan.")

		located_rockets = scanning.calculate_located_rockets(
			spaceship.get_location(),
			scan.get("radius"),
			scan.get("direction"),
			scan.get("angle"),
			[other.get_location() for other in self.contact_listener.spaceships if other != spaceship])

		# print(self.spaceships, [other.get_location() for other in self.spaceships if other != spaceship], located_rockets)
		if located_rockets:
			self.contact_listener.add_scan(BoxScan(
				spaceship.get_location().get_position(),
				scan.get("radius"),
				scan.get("direction"),
				scan.get("angle"),
				self.colorScanSuccess))
		else:
			self.contact_listener.add_scan(BoxScan(
				spaceship.get_location().get_position(),
				scan.get("radius"),
				scan.get("direction"),
				scan.get("angle")))

		self.process_scan(spaceship, action, located_rockets)

	def process_scan(self, spaceship: BoxSpaceship, action: PilotAction, located_rockets: List[Location]):
		# try:
		action = spaceship.process_scan(action, located_rockets)
		if not action:
			return

		self.handle_pilot_action(spaceship, action)
		# except Exception as e:
		# 	print(str(e))
		# 	return
		# make sure no second scan is possible after first scan
		action.scan_action = None
		self.handle_pilot_action(spaceship, action)

	def handle_pilot_move(self, spaceship: BoxSpaceship, move: dict):
		# TODO test energy cost
		force = angle2vec(move.get("direction")) * move.get("power")
		spaceship.move(force)

	def handle_pilot_shoot(self, spaceship: BoxSpaceship, shoot: dict):
		direction = angle2vec(shoot.get("angle")) * 30
		self.contact_listener.add_rocket(BoxRocket(self.world, spaceship, direction))


def angle2vec(angle: float) -> b2Vec2:
	return b2Vec2(math.cos(angle), math.sin(angle))
