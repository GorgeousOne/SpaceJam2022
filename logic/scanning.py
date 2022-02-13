from typing import List

import numpy as np

from logic.location import Location

EPSILON = 0.0001

def wrap_to_pi(rad_angle):
	return (rad_angle + np.pi) % (2 * np.pi) - np.pi

def calculate_scan_energy_cost(direction: float, radius: float) -> float:
	return radius * direction


def calculate_located_rockets(direction: float, angle: float, radius: float, scan_center: Location, targets: List[Location]) -> List[Location]:
	return list(filter(lambda loc: is_loc_in_scan(loc, direction, angle, radius, scan_center), targets))


def is_loc_in_scan(loc: Location, direction: float, angle: float, radius: float, scan_center: Location) -> bool:
	dist_vec = loc.get_position() - scan_center.get_position()

	if np.linalg.norm(dist_vec) > radius:
		return False
	angle_towards_loc = np.arctan2(dist_vec[1], dist_vec[0])
	rel_angle = wrap_to_pi(angle_towards_loc - direction)
	return abs(rel_angle) - angle / 2 <= EPSILON
