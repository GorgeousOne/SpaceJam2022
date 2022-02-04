import numpy as np

from logic.location import Location
from logic.scan import Scan


def calculate_scan_energy_cost(scan: Scan) -> float:
	return scan.get_radius() * scan.get_angle()


def is_loc_in_scan(loc: Location, scan: Scan, scan_center: Location) -> bool:
	dist_vec = loc.get_position() - scan_center.get_position()

	if np.linalg.norm(dist_vec) > scan.get_radius():
		return False

	angle_to_loc = np.arctan2(dist_vec[1], dist_vec[0])
	rel_angle = abs(angle_to_loc - scan_center.get_rotation())
	return rel_angle <= scan.get_angle() / 2