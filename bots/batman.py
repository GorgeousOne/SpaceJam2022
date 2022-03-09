import math
import random
from typing import List

from location import Location
from pilotAction import PilotAction
from spaceshipPilot import SpaceshipPilot


class Batman(SpaceshipPilot):

	def __init__(self):
		super().__init__("#0A0A0A")
		self.gameTick = 0
		self.angle = random.random() * math.pi * 2
		self.isStart = True

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
			located_spaceships: List[Location]) -> PilotAction:
		action = PilotAction()
		if game_tick % 10 == 0:
			action.shoot_rocket(self.angle)
		return action
