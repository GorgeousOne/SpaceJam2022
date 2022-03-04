import numpy as np
import math

def wrap_to_pi(rad_angle):
	return (rad_angle + math.pi) % (2 * math.pi) - math.pi

class Location:

	def __init__(self, position: np.ndarray = np.zeros(2), velocity: np.ndarray = np.zeros(2)):
		"""
		Represents the position and velocity of a spaceship.
		"""
		self._position = position.copy()
		self._velocity = velocity.copy()

	def get_position(self) -> np.ndarray:
		"""
		:return: 2D vector with x and y coordinate of a position
		"""
		return self._position

	def get_velocity(self) -> np.ndarray:
		"""
		:return: 2D vector with x and y coordinate of a velocity
		"""
		return self._velocity

	def __repr__(self):
		return "(pos: " + str(self._position) + ", vel: " + str(self._velocity) + ")"