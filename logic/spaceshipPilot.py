from typing import List

from logic.location import Location
from logic.pilotAction import PilotAction


class SpaceshipPilot:

	def __init__(self, level_width, spaceship_size):
		self.level_width = level_width
		self.spaceship_size = spaceship_size

	def update(self, current_location: Location, current_health: float, current_energy: float) -> PilotAction:
		raise NotImplementedError()

	def process_scan(self, current_action: PilotAction, located_rockets: List[Location]) -> PilotAction:
		raise NotImplementedError()