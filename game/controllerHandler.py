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


class ControllerHandler:

	def __init__(self):
		self.controllers = {}
		self.load_user_controllers()

	def load_user_controllers(self):
		args = sys.argv

		if len(args) < 2:
			print("meh")

		for i in range(1, len(args)):
			module = load_module(args[i])

			try:
				controller = module.SpaceshipController()
			except AttributeError:
				raise ValueError("Could not locate class SpaceshipController in script " + args[i])
			self.register_controller(module.__name__, controller)

	def register_controller(self, name, controller):
		self.controllers[name] = controller
		print("register controller", name)
