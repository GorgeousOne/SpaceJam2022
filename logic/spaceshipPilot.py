from typing import List

from logic.location import Location
from logic.pilotAction import PilotAction


class SpaceshipPilot:

	def __init__(self, game_width, spaceship_size, ship_color: str= "#FFFFFF"):
		self.gameWidth = game_width
		self.spaceshipSize = spaceship_size
		self.shipColor = ship_color

	def update(self, game_tick: int, current_location: Location, current_health: float, current_energy: float) -> PilotAction:
		raise NotImplementedError()

	def process_scan(self, current_action: PilotAction, located_rockets: List[Location]) -> PilotAction:
		raise NotImplementedError()

	# def prepare_scan(self, game_tick: int, current_location: Location, current_health: float, current_energy: float) -> PilotAction:
	# 	raise NotImplementedError()
	#
	# def update(self, game_tick: int, current_location: Location, current_health: float, current_energy: float, located_rockets: List[numpy.ndarray]) -> PilotAction:
	# 	raise NotImplementedError()

