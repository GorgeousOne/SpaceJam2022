from typing import List

import numpy as np

from logic.location import Location
from logic.pilotAction import PilotAction
from logic.spaceshipPilot import SpaceshipPilot


class CirclePilot(SpaceshipPilot):

	def __init__(self, level_width=0, spaceship_size=0):
		super().__init__(level_width, spaceship_size)
		self.centerVec = np.array([self.level_width / 2, self.level_width / 2])

	def update(self, current_location: Location, current_health: float, current_energy: float) -> PilotAction:
		action = PilotAction()
		pos_vec = current_location.get_position()
		dist_vec = self.centerVec - pos_vec

		dist = np.linalg.norm(dist_vec)
		angle_to_mid = np.arctan2(dist_vec[1], dist_vec[0])

		action.move_spaceship(angle_to_mid + np.pi/4, np.power(self.level_width - dist, 2))
		action.shoot_rocket(angle_to_mid + np.pi)
		return action

	def process_scan(self, current_action: PilotAction, located_rockets: List[Location]) -> PilotAction:
		pass


def norm_vec(vector):
	""" Returns the normal vector of the vector.  """
	return vector / np.linalg.norm(vector)


def angle_between(v1: np.ndarray, v2: np.ndarray):
	v1_u = norm_vec(v1)
	v2_u = norm_vec(v2)
	return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
