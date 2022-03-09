import math
from math import cos, sin, pi

from typing import List

import numpy as np

from location import Location
from pilotAction import PilotAction, ScanAction

class SpaceshipPilot:

	def __init__(self, game_width, spaceship_size, ship_color: str = "#FFFFFF"):
		"""
		Abstract class for piloting a spaceship.
		:param game_width: width and height of the game field
		:param spaceship_size: maximum size of the spaceship
		:param ship_color: hex string for the ship color
		"""
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
		This function is called after "prepare_scan". Implement your logic here.
		:param located_spaceships: list of 2D vectors as the positions of all spaceships located with a scan
		:return: a pilot action to move the spaceship or shoot a rocket
		"""
		raise NotImplementedError()

def calc_scan_energy_cost(distance: float, angle: float) -> float:
	"""
	Calculates the energy cost of a scan
	"""
	cost_factor = 1.0 / (10 * math.pi)
	return distance * distance * angle / 2 * cost_factor

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
	return vec / get_vec_length(vec)

def clip_vec(vec: np.ndarray, max_length: float) -> np.ndarray:
	"""
	Returns a vector that has a limited length
	"""
	if get_vec_length(vec) > max_length:
		return get_norm_vec(vec) * max_length
	return np.copy(vec)


def create_vec_from_angle(theta: float) -> np.ndarray:
	"""
	Returns a normalized vector pointing in the direction of the angle
	"""
	return np.array([np.cos[theta], np.sin(theta)])

def get_angle_of_vec(vec: np.ndarray) -> float:
	"""
	Returns the angle of the vector (-pi to +pi)
	"""
	return math.atan2(vec[1], vec[0])

def get_point_dist(point1: np.ndarray, point2: np.ndarray):
	return get_vec_length(point2 - point1)

def get_angle_between_vecs(vec1: np.ndarray, vec2: np.ndarray) -> float:
	v1_u = get_norm_vec(vec1)
	v2_u = get_norm_vec(vec2)
	return math.acos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def rotate_vec(vec: np.ndarray, theta: float):
	"""
	Returns a copy of a 2D-vector rotated by the angle theta (counter clockwise)
	"""
	rotation = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
	return rotation.dot(vec)