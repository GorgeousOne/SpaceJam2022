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


class PilotHandler:

	def __init__(self):
		self.pilots = {}
		self.load_user_pilots()

	def load_user_pilots(self):
		args = sys.argv

		if len(args) < 2:
			print("no user scripts loaded from cmd line arguments")

		for i in range(1, len(args)):
			module = load_module(args[i])

			try:
				pilot = module.SpaceshipPilot()
			except AttributeError:
				raise ValueError("Could not locate class SpaceshipPilot in script " + args[i])
			self.register_pilot(module.__name__, pilot)

	def register_pilot(self, name, pilot):
		self.pilots[name] = pilot
		print("register pilot", name)
