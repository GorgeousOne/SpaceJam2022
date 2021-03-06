import math
from typing import List

import numpy as np

import spaceshipPilot as pilot
from location import Location
from pilotAction import PilotAction
from spaceshipPilot import SpaceshipPilot


class Orbiter(SpaceshipPilot):

	def __init__(self):
		super().__init__("#2D82F0")
		self.gameWidth = 100
		self.center = np.array([self.gameWidth / 2, self.gameWidth / 2])
		self.speed = 3
		self.radius = 20
		self.angleStep = self.speed / self.radius
		self.startAngle = 0

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
		pos = current_location.get_position()

		if game_tick == 0:
			self.startAngle = pilot.get_angle_of_vec(pos - self.center)

		angle = self.startAngle + game_tick * self.angleStep
		target = self.center + np.array([np.cos(angle), np.sin(angle)]) * self.radius

		vel = current_location.get_velocity()
		direction = pilot.clip_vec(target - pos, self.speed)
		action.move_spaceship_with_vec(direction - vel)

		if game_tick % 10 == 0:
			center_dir = pilot.get_angle_of_vec(self.center - pos)
			action.shoot_rocket(center_dir - math.pi / 2)
		return action
