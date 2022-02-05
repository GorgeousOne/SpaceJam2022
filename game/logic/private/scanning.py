from typing import List

import numpy as np

from game.logic.location import Location
from game.logic.scan import Scan

EPSILON = 0.0001

def wrap_to_pi(rad_angle):
	return (rad_angle + np.pi) % (2 * np.pi) - np.pi

def calculate_scan_energy_cost(scan: Scan) -> float:
	return scan.get_radius() * scan.get_angle()


def calculate_scan_results(scan: Scan, scan_center: Location, targets: List[Location]) -> List[Location]:
	return list(filter(lambda loc: is_loc_in_scan(loc, scan, scan_center), targets))


def is_loc_in_scan(loc: Location, scan: Scan, scan_center: Location) -> bool:
	dist_vec = loc.get_position() - scan_center.get_position()

	if np.linalg.norm(dist_vec) > scan.get_radius():
		return False
	angle_to_loc = np.arctan2(dist_vec[1], dist_vec[0])
	rel_angle = wrap_to_pi(angle_to_loc - scan.get_direction())
	return abs(rel_angle) - scan.get_angle() / 2 <= EPSILON
