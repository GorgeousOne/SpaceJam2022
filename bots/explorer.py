from location import Location
from pilotAction import PilotAction
from spaceshipPilot import SpaceshipPilot


class Explorer(SpaceshipPilot):

	def __init__(self, game_width=0, spaceship_size=0):
		super().__init__(game_width, spaceship_size, "#FF4000")
		self.speed = 2

	def prepare_scan(
			self,
			game_tick: int,
			current_location: Location,
			current_health: float,
			current_energy: float):

		return None

	def update(
			self, game_tick: int,
			current_location: Location,
			current_health: float,
			current_energy: float,
			located_spaceships) -> PilotAction:
		action = PilotAction()
		return action
