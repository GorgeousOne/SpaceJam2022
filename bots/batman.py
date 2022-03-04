import math
import random
from typing import List

import numpy as np

from logic.location import Location
from logic.pilotAction import PilotAction
from logic.spaceshipPilot import SpaceshipPilot


class Batman(SpaceshipPilot):

	def __init__(self, game_width = 0, spaceship_size = 0):
		super().__init__(game_width, spaceship_size, "#060606")
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
			located_spaceships) -> PilotAction:
		action = PilotAction()
		if game_tick % 10 == 0:
			action.shoot_rocket(self.angle)
		return action
