from typing import List

from game import timeLimit
from game.boxSpaceship import BoxSpaceship
from logic.location import Location
from logic.pilotAction import PilotAction
from logic import scanning


class GameHandler:

	def __init__(self):
		self.spaceships = set()
		pass

	def update(self):
		for spaceship in self.spaceships:
			try:
				action = timeLimit.execute_limited(spaceship.update, 0.1, 0.01)
				self.handle_pilot_action(spaceship, action)
			except timeLimit.TimeoutException as e:
				print(str(e))
				continue
			except Exception as e:
				print(e.__traceback__)
				continue

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
			scan.get("direction"),
			scan.get("angle"),
			scan.get("radius"),
			spaceship.get_location(),
			[other.get_location() for other in self.spaceships if other != spaceship])
		self.process_scan(spaceship, action, located_rockets)


	def process_scan(self, spaceship: BoxSpaceship, action: PilotAction, located_rockets: List[Location]):
		try:
			action = timeLimit.execute_limited(spaceship.update, 0.1, 0.01)
			self.handle_pilot_action(spaceship, action)
		except timeLimit.TimeoutException as e:
			print(str(e))
			return
		except Exception as e:
			print(e.__traceback__)
			return
		# make sure no second scan is possible after first scan
		action.scan_action = None
		self.handle_pilot_action(spaceship, action)

	def handle_pilot_move(self, spaceship: BoxSpaceship, move: dict):
		pass

	def handle_pilot_shoot(self, spaceship: BoxSpaceship, shoot: dict):
		pass
