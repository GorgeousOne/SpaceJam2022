import math
from typing import List

import numpy as np

from logic.location import Location
from logic.pilotAction import PilotAction
from logic.spaceshipPilot import SpaceshipPilot


class CirclePilot(SpaceshipPilot):

	def __init__(self, game_width=0, spaceship_size=0):
		super().__init__(game_width, spaceship_size)
		self.center = np.array([self.gameWidth / 2, self.gameWidth / 2])
		self.updateCount = 0
		self.speed = 5
		self.radius = 30
		self.angleStep = self.speed / self.radius

		self.startAngle = 0

	def update(self, current_location: Location, current_health: float, current_energy: float) -> PilotAction:
		self.updateCount += 1

		action = PilotAction()
		pos = current_location.get_position()

		if self.updateCount == 1:
			self.startAngle = vec_angle(pos - self.center)

		angle = self.startAngle + self.updateCount * self.angleStep
		target = self.center + np.array([np.cos(angle), np.sin(angle)]) * self.radius
		vel = current_location.get_velocity()
		impulse = target - (pos + vel)
		action.move_spaceship(vec_angle(impulse), np.linalg.norm(impulse))

		if self.updateCount % 5 == 0:
			center_dir = vec_angle(self.center - pos)
			action.shoot_rocket(center_dir - math.pi/2)
			action.scan_area(50, center_dir, math.pi / 8)
		return action

	def process_scan(self, current_action: PilotAction, located_rockets: List[Location]) -> PilotAction:
		return current_action


def vec_angle(vec: np.ndarray):
	return math.atan2(vec[1], vec[0])

def norm_vec(vec: np.ndarray):
	"""
	Returns the normal vector of the vector.
	"""
	return vec / np.linalg.norm(vec)


def angle_between(v1: np.ndarray, v2: np.ndarray):
	v1_u = norm_vec(v1)
	v2_u = norm_vec(v2)
	return math.acos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
