from logic.location import Location
from logic.pilotAction import PilotAction
from logic.spaceshipPilot import SpaceshipPilot


class AfkPilot(SpaceshipPilot):

	def __init__(self, level_width = 0, spaceship_size = 0):
		super().__init__(level_width, spaceship_size)

	def update(self, current_location: Location, current_health: float, current_energy: float) -> PilotAction:
		pass
