import math
import random
from typing import List

import numpy as np

from logic.location import Location
from logic.pilotAction import PilotAction
from logic.spaceshipPilot import SpaceshipPilot


class TestBot(SpaceshipPilot):

	def __init__(self, game_width=0, spaceship_size=0):
		super().__init__(game_width, spaceship_size, "#99FF00")
		self.angle = random.random() * math.pi * 2
		self.isStart = True

	def update(self, game_tick: int, current_location: Location, current_health: float, current_energy: float) -> PilotAction:
		action = PilotAction()
		if game_tick == 0:
			action.move_spaceship(0, 1)
		elif game_tick % 5 == 0:
			print(current_location.get_position(), "speed", current_location.get_velocity())
		return action

	def process_scan(self, current_action: PilotAction, located_rockets: List[Location]) -> PilotAction:
		pass


def vec_angle(vec: np.ndarray):
	return math.atan2(vec[1], vec[0])
