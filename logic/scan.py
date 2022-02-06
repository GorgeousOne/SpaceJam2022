import numpy as np
from logic import wrap_to_pi

class Scan:
	def __init__(self, radius: float, direction: float, angle: float):
		"""
		:param radius: distance to scan in meters
		:param direction: direction to scan towards as angle between -PI and PI
		:param angle: size of the scan as angle of a circular segment between 0 and 2 PI
		"""
		if angle < 0:
			raise ValueError("Scan cannot be lower 0")
		elif angle > 2 * np.pi:
			raise ValueError("Scan cannot be greater 2*pi")
		self._direction = wrap_to_pi(direction)
		self._radius = radius
		self._angle = angle

	def get_radius(self) -> float:
		return self._radius

	def get_direction(self) -> float:
		return self._direction

	def get_angle(self) -> float:
		return self._angle

	def calculate_energy_cost(self) -> float:
		return self._radius * self._angle
