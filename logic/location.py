import numpy as np


class Location:

	def __init__(self, position: np.ndarray, rotation: float):
		self._position = position
		self._rotation = rotation

	def get_position(self) -> np.ndarray:
		return self._position

	def get_rotation(self) -> float:
		return self._rotation
