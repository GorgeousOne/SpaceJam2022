import math
import random

import numpy as np

from location import Location
from pilotAction import PilotAction
from spaceshipPilot import SpaceshipPilot


class TestDummy(SpaceshipPilot):

	def __init__(self, game_width = 0, spaceship_size = 0):
		super().__init__(game_width, spaceship_size, "#808080")
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
		return None

def vec_angle(vec: np.ndarray):
	return math.atan2(vec[1], vec[0])