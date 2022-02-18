import importlib.util
import os
import sys


def load_module(rel_path: str):
	abs_path = os.path.abspath(rel_path)

	if not os.path.isfile(abs_path):
		raise ValueError("Could not find script " + abs_path)

	module_name = abs_path.split(os.path.sep)[-1].split(".")[0]
	spec = importlib.util.spec_from_file_location(module_name, abs_path)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


def load_pilot_class(module_path):
	module = load_module(module_path)
	class_name = module.__name__
	class_name = class_name[0].upper() + class_name[1:]
	try:
		return getattr(module, class_name)
	except AttributeError:
		raise ValueError("Could not locate class " + class_name + " in script " + module_path)


class PilotHandler:

	def __init__(self, game_handler, game_size, spaceship_size):
		self.gameHandler = game_handler
		self.gameSize = game_size
		self.spaceshipSize = spaceship_size

	def add_cmd_line_pilots(self):
		args = sys.argv

		if len(args) < 2:
			print("no pilot scripts passed in cmd line arguments")
		for i in range(1, len(args)):
			self.gameHandler.spawn_spaceship(load_pilot_class(args[i])(self.gameSize, self.spaceshipSize))


	# def load_user_pilots(self):
	# 	args = sys.argv
	#
	# 	if len(args) < 2:
	# 		print("no user scripts loaded from cmd line arguments")
	#
	# 	for i in range(1, len(args)):
	# 		module = load_module(args[i])
	#
	# 		try:
	# 			pilot = module.SpaceshipPilot()
	# 		except AttributeError:
	# 			raise ValueError("Could not locate class SpaceshipPilot in script " + args[i])
	# 		self.gameHandler.register_pilot(module.__name__, pilot)

	# def register_pilot(self, name, pilot):
	# 	self.pilots[name] = pilot
	# 	print("register pilot", name)
