import numpy as np
import string

def read_point_tuple(point_str: str) -> np.ndarray:
	split = point_str.split(",")
	return np.array([float(elem) for elem in split])


def read_svg_path_points(path: str):
	lines = path.split()
	points = []
	current_point = np.array([.0, .0])
	is_relative = False

	for line in lines:
		if len(line) == 1:
			is_relative = line in string.ascii_lowercase
			continue

		point = read_point_tuple(line)
		if is_relative:
			current_point += point
		else:
			current_point = point
		points.append(current_point.copy())
	return points


def point2string(point, decimal_places):
	return "(" + ",".join(("%." + str(decimal_places) + "f") % point[i] for i in range(point.size)) + ")"


if __name__ == '__main__':
	# extracted xml path string of inkscape file
	# d = "m 0,0 2.57444,-6.215241 6.2151305,-2.574437 -2.619551,-11.120134 -12.8233995,-8.4144 -15.504791,-2.11032 -12.57475,2.668931 4.75085,8.724339 4.25454,1.595071 -1.63794,5.783839 -10.53321,3.129362 2e-5,17.065979 10.53319,3.129363 1.63794,5.783836 -4.25454,1.595078 -4.75085,8.724338 12.57475,2.668928 L -6.65338,28.324207 6.1700195,19.909813 30.889983,18.102457 48.905238,11.788921 62.101322,0 48.905238,-11.788922 30.889983,-18.102461 6.1700195,-19.909811 8.7896805,-8.789678 15.004916,-6.215241 17.579357,0 15.004916,6.215241 8.7896805,8.789678 2.57444,6.215241 Z"
	d = "m -27.36611,-11.662352 -10.53321,3.129362 2e-5,17.065979 10.53319,3.129363 L 6.1693798,19.909813 30.889344,18.102457 48.904599,11.788921 62.100683,0 48.904599,-11.788922 30.889344,-18.102461 6.1693798,-19.909811 Z"
	points = read_svg_path_points(d)

	print(",\n".join([point2string(point * 0.05, 2) for point in points]))
	print("for visualization copy and paste result to e.g. https://www.desmos.com/calculator")
