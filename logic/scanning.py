import math
from typing import List

import numpy as np

from location import Location

EPSILON = 0.0001


def wrap_to_pi(rad_angle):
	return (rad_angle + math.pi) % (2 * math.pi) - math.pi


def calc_scanned_area(distance: float, angle: float) -> float:
	return distance * distance * angle / 2


def calc_located_spaceships(scan_center: Location, direction: float, distance: float, angle: float, targets: List[Location]) -> List[Location]:
	return list(filter(lambda loc: is_loc_in_scan(loc, scan_center, direction, distance, angle), targets))


def is_loc_in_scan(loc: Location, scan_center: Location, direction: float, radius: float, angle: float) -> bool:
	dist_vec = loc.get_position() - scan_center.get_position()

	if np.linalg.norm(dist_vec) > radius:
		return False
	angle_towards_loc = math.atan2(dist_vec[1], dist_vec[0])
	rel_angle = wrap_to_pi(angle_towards_loc - direction)
	return abs(rel_angle) - angle / 2 <= EPSILON
