import importlib.util
import os
import sys


class SpaceshipHandler:

	def __init__(self):
		self.controllers = {}
		self.load_user_controllers()

	def load_user_controllers(self):
		args = sys.argv

		if len(args) < 2:
			print("meh")

		for i in range(1, len(args)):
			path = os.path.abspath(args[i])

			if not os.path.isfile(path):
				raise ValueError("Could not find script " + path)

			module_name = path.split(os.path.sep)[-1].split(".")[0]
			spec = importlib.util.spec_from_file_location(module_name, path)
			module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(module)

			try:
				controller = module.SpaceshipController()
			except AttributeError:
				raise ValueError("Could not locate class SpaceshipController in script " + path)

			print("registered controller", controller)


def my_import(name):
	components = name.split('.')
	mod = __import__(components[0])
	for comp in components[1:]:
		mod = getattr(mod, comp)
	return mod
