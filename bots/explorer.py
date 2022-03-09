import math
import random
from typing import List

from location import Location
from pilotAction import PilotAction, ScanAction
from spaceshipPilot import SpaceshipPilot

import spaceshipPilot as pilot


def steer_to(point, pos, vel, max_speed, action):
	dist = point - pos
	acc = pilot.clip_vec(dist, max_speed) - vel
	action.move_spaceship_with_vec(acc)


class Explorer(SpaceshipPilot):

	def __init__(self):
		super().__init__("#FF4000")
		self.gameWidth = 100
		self.speed = 2
		self.scanDir = random.random() * 2 * math.pi
		self.scanDist = self.gameWidth / 3
		self.scanAngle = math.pi / 8
		self.angleInc = 5 * math.pi / 8
		self.scanInterval = 1

		self.last_sight = 0
		self.last_target = None

	def prepare_scan(
			self,
			game_tick: int,
			current_location: Location,
			current_health: float,
			current_energy: float):

		if game_tick % self.scanInterval == 0:
			# print(pilot.calc_scan_energy_cost(self.scanDist, self.scanAngle))
			if self.last_sight > 0:
				scan = ScanAction(self.scanDir, self.scanDist, self.scanAngle / 2)
			else:
				self.scanDir += self.angleInc
				scan = ScanAction(self.scanDir, self.scanDist, self.scanAngle)

			return scan

	def update(
			self, game_tick: int,
			current_location: Location,
			current_health: float,
			current_energy: float,
			located_spaceships: List[Location]) -> PilotAction:

		action = PilotAction()
		self.last_sight = max(0, self.last_sight - 1)

		if game_tick % self.scanInterval == 0:
			self.target(current_location, located_spaceships, action)

		if self.last_sight == 0 and game_tick % 15 == 0:
			pos = current_location.get_position()
			vel = current_location.get_velocity()
			steer_to(self.create_rnd_point(), pos, vel, self.speed, action)
			# self.nextMoveTick += self.scanInterval

		return action

	def target(self, current_location, located_spaceships, action):
		if not located_spaceships:
			return
		pos = current_location.get_position()
		vel = current_location.get_velocity()
		target_loc = located_spaceships[0]
		self.last_target = target_loc.get_position() + target_loc.get_velocity()
		self.last_sight = 5
		direction = self.last_target - pos
		distance = pilot.get_vec_length(direction)

		self.scanDir = pilot.get_angle_of_vec(direction)
		steer_to(self.last_target, pos, vel, 1, action)

		rocket_speed = 5
		shoot_dir = target_loc.get_position() + (distance / rocket_speed) * target_loc.get_velocity() - pos
		action.shoot_rocket(pilot.get_angle_of_vec(shoot_dir))

	def create_rnd_point(self):
		return pilot.create_vec(
			random.random() * self.gameWidth,
			random.random() * self.gameWidth)
