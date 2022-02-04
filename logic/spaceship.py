from typing import List

from logic.location import Location
from logic.spaceAction import SpaceAction

class Spaceship:

	def update(self, position: Location, velocity: float) -> SpaceAction:
		"""
		Function that gets repeatedly called by the game every x ms, when your rocket has recharged energy
		:param position: current location of the rocket
		:param velocity: current velocity of the rocket
		:return: actions your rocket wants to perform this update. If the action contains a scan,
		the function process_scan will be called immediately afterwards with the results
		"""
		pass

	def process_scan(self, located_rockets: List[Location]):
		pass
