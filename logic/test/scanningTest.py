import unittest

import numpy as np

from logic import scanning
from logic.location import Location


class ScanningTest(unittest.TestCase):

	def test_scan_ship_on_circle_edge(self):
		scan_center = Location()
		loc = Location(np.array([2, 0]))
		self.assertTrue(scanning.is_loc_in_scan(loc, scan_center, 2, 0, 2 * np.pi))  # 360° 2m scan

	def test_scan_ship_outside_circle(self):
		scan_center = Location()
		loc = Location(np.array([2.01, 0]))
		self.assertFalse(scanning.is_loc_in_scan(loc, scan_center, 2, 0, 2 * np.pi))

	def test_scan_ship_inside_shifted_circle(self):
		scan_center = Location(np.array([10, 0]))
		loc = Location(np.array([11, 0]))
		self.assertTrue(scanning.is_loc_in_scan(loc, scan_center, 2, 0, 2 * np.pi))

	def test_scan_ship_inside_circle_segment(self):
		scan_center = Location()
		loc = Location(np.array([1, 0]))
		self.assertTrue(scanning.is_loc_in_scan(loc, scan_center, 2, 0, np.pi / 2))  # 90° 2m  scan

	def test_scan_ship_on_circle_segment_edge(self):
		scan_center = Location()
		loc = Location(np.array([1, 1]))
		self.assertTrue(scanning.is_loc_in_scan(loc, scan_center, 2, 0, np.pi / 2))

	def test_scan_ship_outside_circle_segment(self):
		scan_center = Location()
		loc = Location(np.array([0, 1]))
		self.assertFalse(scanning.is_loc_in_scan(loc, scan_center, 2, 0, np.pi / 2))

	def test_scan_ship_inside_rotated_circle_segment(self):
		scan_center = Location()
		loc = Location(np.array([0, 1]))
		self.assertTrue(scanning.is_loc_in_scan(loc, scan_center, 2, np.pi/2, np.pi/2))

	def test_scan_ship_in_positive_direction_with_segment_in_negative_direction(self):
		scan_center = Location()
		loc = Location(np.array([-1, 1]))  # ship towards 135°
		self.assertTrue(scanning.is_loc_in_scan(loc, scan_center, 2, -np.pi, np.pi / 2))  # scan towards -180°

	def test_energy_consumption_full_circle(self):
		pass

	def test_energy_consumption_circle_segment(self):
		pass
