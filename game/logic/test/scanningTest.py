import unittest

import numpy as np

from game.logic.location import Location
from game.logic.private import scanning
from game.logic.scan import Scan


class ScanningTest(unittest.TestCase):

	def test_scan_ship_on_circle_edge(self):
		scan = Scan(2, 2*np.pi) # 2m 360° scan
		scan_center = Location(np.zeros(2))

		loc = Location(np.array([2, 0]))
		self.assertTrue(scanning.is_loc_in_scan(loc, scan, scan_center))
		pass

	def test_scan_ship_outside_circle(self):
		scan = Scan(2, 2 * np.pi)
		scan_center = Location(np.zeros(2))

		loc = Location(np.array([2.01, 0]))
		self.assertFalse(scanning.is_loc_in_scan(loc, scan, scan_center))
		pass

	def test_scan_ship_inside_circle_segment(self):
		scan = Scan(2, np.pi / 2) # 2m 90° scan
		scan_center = Location(np.zeros(2))

		loc = Location(np.array([1, 0]))
		self.assertTrue(scanning.is_loc_in_scan(loc, scan, scan_center))
		pass

	def test_scan_ship_on_circle_segment_edge(self):
		scan = Scan(2, np.pi / 2)
		scan_center = Location(np.zeros(2))

		loc = Location(np.array([1, 1]))
		self.assertTrue(scanning.is_loc_in_scan(loc, scan, scan_center))
		pass

	def test_scan_ship_outside_circle_segment(self):
		scan = Scan(2, np.pi / 2)
		scan_center = Location(np.zeros(2))

		loc = Location(np.array([0, 1]))
		self.assertFalse(scanning.is_loc_in_scan(loc, scan, scan_center))
		pass

	def test_energy_consumption_full_circle(self):
		pass

	def test_energy_consumption_circle_segment(self):
		pass
