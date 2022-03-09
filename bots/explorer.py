import math
import random

from location import Location
from pilotAction import PilotAction, ScanAction
from spaceshipPilot import SpaceshipPilot

import spaceshipPilot as pilot

class Explorer(SpaceshipPilot):

	def __init__(self, game_width=0, spaceship_size=0):
		super().__init__(game_width, spaceship_size, "#FF4000")
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
				self.scanInterval = 2
				scan = ScanAction(self.scanDir, self.scanDist, self.scanAngle * 1.5)
			else:
				self.scanInterval = 1
				self.scanDir += self.angleInc
				scan = ScanAction(self.scanDir, self.scanDist, self.scanAngle)

			return scan

	def update(
			self, game_tick: int,
			current_location: Location,
			current_health: float,
			current_energy: float,
			located_spaceships) -> PilotAction:

		action = PilotAction()
		self.last_sight = max(0, self.last_sight - 1)

		if game_tick % self.scanInterval == 0:
			self.target(current_location, located_spaceships, action)

		if self.last_sight == 0 and game_tick % 15 == 0:
			pos = current_location.get_position()
			vel = current_location.get_velocity()
			self.steer_to(self.create_rnd_point(), pos, vel, self.speed, action)
			# self.nextMoveTick += self.scanInterval

		return action

	def target(self, current_location, located_spaceships, action):
		if not  located_spaceships:
			return
		pos = current_location.get_position()
		vel = current_location.get_velocity()
		self.last_target = located_spaceships[0]
		self.last_sight = 5
		direction = self.last_target - pos
		self.scanDir = pilot.get_angle_of_vec(direction)
		self.steer_to(self.last_target, pos, vel, 1, action)
		action.shoot_rocket(self.scanDir)

	def steer_to(self, point, pos, vel, max_speed, action):
		dist = point - pos
		acc = pilot.clip_vec(dist, max_speed) - vel
		action.move_spaceship_with_vec(acc)

	def create_rnd_point(self):
		return pilot.create_vec(
			random.random() * self.gameWidth,
			random.random() * self.gameWidth)
