import math
import random
from typing import List

from location import Location
from pilotAction import PilotAction, ScanAction

from spaceshipPilot import SpaceshipPilot
import spaceshipPilot as pilot


class Batman(SpaceshipPilot):

	def __init__(self):
		super().__init__("#202020")
		self.gameSize = 100
		self.shipSize = 5
		self.speed = 5
		self.speedSlow = 2

		self.rocketSpeed = 5
		self.energyRegen = 10
		self.mid = pilot.create_vec(self.gameSize/2, self.gameSize/2)

		self.doSteerCorner = True
		self.doStayInCorner = True
		self.doSteerCenter = False

		self.corner = None
		self.doScan = False

		self.startScanDir = 0
		self.currentScanDir = 0

		self.scanDist = 30
		cost_factor = 1.0 / (10 * math.pi)
		max_area = (2 * self.energyRegen) / (self.scanDist * self.scanDist * cost_factor)
		self.scanAngle = 0.75 * max_area
		self.scanCount = 0
		self.lastHealth = 0

	def prepare_scan(
			self,
			game_tick: int,
			current_location: Location,
			current_health: float,
			current_energy: float):
		action = None
		if self.doScan:
			action = self.create_scan()
		return action

	def update(
			self, game_tick: int,
			current_location: Location,
			current_health: float,
			current_energy: float,
			located_spaceships: List[Location]) -> PilotAction:
		action = PilotAction()
		pos = current_location.get_position()
		vel = current_location.get_velocity()

		if game_tick == 0:
			self.lastHealth = current_health
			self.decide_corner(action)
			return action

		if game_tick == 3 * 5:
			self.doSteerCorner = False
			self.doScan = True

		if current_health + 19 < self.lastHealth:
			self.flee(action)

		self.lastHealth = current_health

		if self.doSteerCorner:
			self.keep_steering_corner(pos, vel, action)
		elif self.doStayInCorner:
			self.stay_in_corner(pos, vel, action)
		elif self.doSteerCenter:
			self.keep_steering_center(pos, vel, action)

		if located_spaceships:
			self.target(pos, located_spaceships, action)

		return action

	def flee(self, action):
		self.doSteerCorner = True
		self.doStayInCorner = True
		self.doSteerCenter = False
		self.doScan = False
		self.decide_corner(action)

	def target(self, pos, located, action):
		ship = located[0]
		ship_pos = ship.get_position()
		ship_vel = ship.get_velocity()

		dist = pilot.get_vec_length(ship_pos - pos)
		factor = (dist / self.rocketSpeed)
		target = ship_pos + ship_vel * factor
		shoot_dir = target - pos
		action.shoot_rocket(pilot.get_angle_of_vec(shoot_dir))

	def decide_corner(self, action):
		pos = pilot.create_vec(
			random.randint(0, self.gameSize),
			random.randint(0, self.gameSize))

		self.corner = pilot.create_vec(0, 0)
		if pos[0] > self.gameSize/2:
			self.corner[0] = self.gameSize
		if pos[1] > self.gameSize / 2:
			self.corner[1] = self.gameSize
		self.move_towards(self.corner, pos, pilot.create_vec(0, 0), action, self.speed)
		self.startScanDir = pilot.get_angle_of_vec(self.mid - self.corner) - 0.25 * math.pi
		self.currentScanDir = self.startScanDir
		self.scanDist = 30

	def keep_steering_corner(self, pos, vel, action):
		dist = self.corner - pos

		if pilot.get_vec_length(dist) < self.shipSize:
			self.doSteerCorner = False
			self.doScan = True
			action.shoot_rocket(pilot.get_angle_of_vec(self.mid - pos))
			return

		if pilot.get_vec_length(vel) < self.speed:
			self.move_towards(self.corner, pos, vel, action, self.speed)

	def create_scan(self):
		if self.scanCount > math.ceil(0.5 * math.pi / self.scanAngle):
			self.scanCount = 0
			self.currentScanDir = self.startScanDir - 0.5 * self.scanAngle

		self.currentScanDir += self.scanAngle * 0.75
		self.scanCount += 1
		return ScanAction(self.currentScanDir, self.scanDist, self.scanAngle)

	def stay_in_corner(self, pos, vel, action):
		self.doStayInCorner = False
		self.doSteerCenter = True

		dist = self.corner - pos

		if pilot.get_vec_length(dist) > 2 * self.shipSize:
			self.move_towards(self.corner, pos, vel, action, self.speed)

		if pilot.get_angle_between_vecs(dist, vel) > math.pi/2:
			action.move_spaceship_with_vec(-vel)

	def keep_steering_center(self, pos, vel, action):
		dist = self.mid - pos

		if pilot.get_vec_length(dist) < self.shipSize:
			self.flee(action)
			return

		if pilot.get_vec_length(vel) < self.speedSlow:
			self.move_towards(self.mid, pos, vel, action, self.speedSlow)

	def move_towards(self, point, pos, vel, action, speed):
		new_vel = pilot.clip_vec(point - pos, speed)
		new_vel = pilot.clip_vec(new_vel - vel, speed)
		action.move_spaceship_with_vec(new_vel)
