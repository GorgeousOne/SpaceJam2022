import numpy as np


class Location:

	def __init__(self, position: np.ndarray = np.zeros(2), rotation: float = 0, velocity: np.ndarray = np.zeros(2)):
		self._position = position.copy()
		self._rotation = rotation
		self._velocity = velocity.copy()

	def get_position(self) -> np.ndarray:
		return self._position

	def get_rotation(self) -> float:
		return self._rotation

	def get_velocity(self) -> np.ndarray:
		return self._velocity