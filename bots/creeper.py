import numpy as np

import spaceshipPilot as pilot
from location import Location
from pilotAction import PilotAction
from spaceshipPilot import SpaceshipPilot


class Creeper(SpaceshipPilot):

	def __init__(self, game_width=0, spaceship_size=0):
		super().__init__(game_width, spaceship_size, "#1B8F1D")
		self.speed = 3
		self.xCoord = None
		self.fliesLeft = None
		self.facing = None
		self.didReachWall = False
		self.patrolsUp = True

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
		vel = current_location.get_velocity()

		if game_tick == 0:
			self.decide_side(pos, action)
			return action

		if not self.didReachWall:
			did_reach_wall = self.check_wall_reach(pos)
			if did_reach_wall:
				self.didReachWall = True
			else:
				self.correct_trajectory(vel, action)

		if not self.didReachWall:
			return action

		self.patrol(pos, vel, action)

		if game_tick % 6 == 0:
			action.shoot_rocket(self.facing)

		return action

	def decide_side(self, pos, action):
		if pos[0] < self.gameWidth / 2:
			self.xCoord = self.spaceshipSize
			self.fliesLeft = True
			self.facing = 0
		else:
			self.xCoord = self.gameWidth - self.spaceshipSize
			self.fliesLeft = False
			self.facing = np.pi
		action.move_spaceship_with_vec(pilot.create_vec(5, 0) * (-1 if self.fliesLeft else 1))

	def check_wall_reach(self, pos):
		if self.fliesLeft:
			if pos[0] < self.xCoord:
				return True
		else:
			if pos[0] > self.xCoord:
				return True
		return False

	def correct_trajectory(self, vel, action):
		if pilot.get_vec_length(vel) < 5:
			goal_velocity = pilot.create_vec(5, 0) * (-1 if self.fliesLeft else 1)
			action.move_spaceship_with_vec(goal_velocity - vel)

	def patrol(self, pos, vel, action):
		patrol_speed = 2
		if self.patrolsUp:
			if pos[1] > self.gameWidth - self.spaceshipSize:
				self.patrolsUp = not self.patrolsUp
				return
			goal_vel = pilot.create_vec(0, patrol_speed)
			impulse = goal_vel - vel
			if pilot.get_vec_length(goal_vel - vel) > 0.1:
				action.move_spaceship_with_vec(impulse)
		else:
			if pos[1] < self.spaceshipSize:
				self.patrolsUp = not self.patrolsUp
				return
			goal_vel = pilot.create_vec(0, -patrol_speed)
			impulse = goal_vel - vel
			if pilot.get_vec_length(goal_vel - vel) > 0.1:
				action.move_spaceship_with_vec(impulse)

