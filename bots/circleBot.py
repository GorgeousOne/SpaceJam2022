import math
from typing import List

import numpy as np

from logic import spaceshipPilot as pilot
from logic.location import Location
from logic.pilotAction import PilotAction
from logic.spaceshipPilot import SpaceshipPilot


class CircleBot(SpaceshipPilot):

	def __init__(self, game_width=0, spaceship_size=0):
		super().__init__(game_width, spaceship_size, "#2D82F0")
		self.center = np.array([self.gameWidth / 2, self.gameWidth / 2])
		self.speed = 3
		self.radius = 30
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
			located_spaceships) -> PilotAction:
		action = PilotAction()
		pos = current_location.get_position()

		if game_tick == 0:
			self.startAngle = pilot.get_angle_of_vec(pos - self.center)

		angle = self.startAngle + game_tick * self.angleStep
		target = self.center + np.array([np.cos(angle), np.sin(angle)]) * self.radius
		vel = current_location.get_velocity()
		acc = target - (pos + vel)
		power = np.linalg.norm(acc)

		if power > self.speed:
			acc = acc * self.speed / power
		action.move_spaceship_with_vec(acc)

		if game_tick % 5 == 0:
			center_dir = pilot.get_angle_of_vec(self.center - pos)
			action.shoot_rocket(center_dir - math.pi / 2)

		return action
