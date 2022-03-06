import math
from typing import List

import numpy as np

from logic.location import Location
from logic.pilotAction import PilotAction, ScanAction

PI = math.pi


class SpaceshipPilot:

	def __init__(self, game_width, spaceship_size, ship_color: str = "#FFFFFF"):
		self.gameWidth = game_width
		self.spaceshipSize = spaceship_size
		self.shipColor = ship_color

	def prepare_scan(
			self,
			game_tick: int,
			current_location: Location,
			current_health: float,
			current_energy: float) -> ScanAction:
		"""
		A function called every time unit (round). *Can* be used to tell the framework scan for other spaceships.
		If a scan detects other spaceships their locations will be passed to the update-function as "located_spaceships" parameter.
		:param game_tick: number of rounds passed since that start of the simulation
		:param current_location: position and velocity of the spaceship in this moment
		:param current_health: amount of health the spaceship has left (spaceship explodes if health drops to zero)
		:param current_energy: amount of energy the ship has currently to perform actions (a portion is restored each round)
		:return: a scan action or None
		"""
		raise NotImplementedError()

	def update(
			self, game_tick: int,
			current_location: Location,
			current_health: float,
			current_energy: float,
			located_spaceships: List[np.ndarray]) -> PilotAction:
		"""
		This function is called after "prepare_scan". Implement your logic here
		:param located_spaceships: list of 2D vectors as the positions of all spaceships located with a scan
		:return: a pilot action to move the spaceship or shoot a rocket
		"""
		raise NotImplementedError()


def create_vec(x: float, y: float) -> np.ndarray:
	"""
	Creates a 2D vector with an x- and y-coordinate.
	The the coordinates can be accessed with the square bracket operator (vec[n]) with 0 for x and 1 for y
	"""
	return np.array([x, y], dtype=float)

def get_vec_length(vec: np.ndarray):
	"""
	Returns the length of the vector
	"""
	return np.linalg.norm(vec)

def get_norm_vec(vec: np.ndarray) -> np.ndarray:
	"""
	Returns the normal vector of the vector.
	"""
	return vec / np.linalg.norm(vec)

def create_vec_from_angle(angle: float):
	"""
	Returns a normalized vector pointing in the direction of the angle
	"""
	return np.array([np.cos[angle], np.sin(angle)])

def get_angle_of_vec(vec: np.ndarray) -> float:
	"""
	Returns the angle of the vector (-pi to +pi)
	"""
	return np.arctan2(vec[1], vec[0])

def get_angle_between_vecs(vec1: np.ndarray, vec2: np.ndarray) -> float:
	v1_u = get_norm_vec(vec1)
	v2_u = get_norm_vec(vec2)
	return math.acos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))