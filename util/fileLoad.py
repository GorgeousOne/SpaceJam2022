import importlib.util
import os
import sys


def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)


def load_external_module(rel_path: str):
	abs_path = os.path.abspath(rel_path)

	if not os.path.isfile(abs_path):
		raise ValueError("Could not find module " + abs_path)

	module_name = abs_path.split(os.path.sep)[-1].split(".")[0]
	spec = importlib.util.spec_from_file_location(module_name, abs_path)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


def load_class_by_module_name(module_path):
	module = load_external_module(module_path)
	class_name = module.__name__.split("/")[-1]
	class_name = class_name[0].upper() + class_name[1:]
	try:
		return getattr(module, class_name)
	except AttributeError:
		raise ValueError("Could not find a class \"" + class_name + "\" in module \"" + module_path + "\".")
