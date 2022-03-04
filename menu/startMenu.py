import os
import pkgutil

import glooey
import pyglet
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from bots import afkBot, circleBot, batman, testBot
from menu.gameMenu import GameMenu

from menu.menuWidget import CustomButton, ScrollList, Title, MenuLabel
from render.pygletWindow import PygletWindow
from util import fileLoad


class StartGameMenu(GameMenu):

	def __init__(self, window: PygletWindow, game_start_callback):
		self.gameStartCallback = game_start_callback
		self.availablePilotsCount = 0
		self.selectedPilotsCount = 0
		self.pilotClasses = {}

		super().__init__(window)

		# manually evaluated
		self.max_label_width = 220
		self._load_default_pilots()
		self._load_user_pilots()
		# self._setup_watchdog()

	def _setup_gui(self):
		super()._setup_gui()

		container = glooey.VBox()
		container.set_default_cell_size(1)
		container.set_cell_padding(20)
		container.set_padding(20)
		container.set_alignment("top")

		game_title = Title("Space Jam", font_size=24)
		game_title.set_padding(20)
		container.add(game_title)

		table_container = glooey.HBox()
		table_container.set_cell_padding(40)
		container.add(table_container)

		self.availablePilotsBox = ScrollList("Available")
		self.selectedPilotsBox = ScrollList("Selected")
		table_container.add(self.availablePilotsBox)
		table_container.add(self.selectedPilotsBox)

		self.readyBtn = CustomButton("Not Ready", lambda widget: self.gameStartCallback())
		self.readyBtn.set_size_hint(200, 0)
		self.readyBtn.set_alignment("center")
		self.readyBtn.get_foreground().set_alignment("center")

		self.readyBtn.disable()
		container.add(self.readyBtn)
		self.root.add(container)

	def _setup_watchdog(self):
		patterns = ["*.py"]
		ignore_patterns = None
		ignore_directories = True
		case_sensitive = True
		my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
		my_event_handler.on_created = self.on_created
		my_event_handler.on_deleted = self.on_deleted
		my_event_handler.on_modified = self.on_modified
		my_event_handler.on_moved = self.on_moved

		path = "../game"
		self.my_observer = Observer()
		self.my_observer.schedule(my_event_handler, path, recursive=False)
		self.my_observer.start()

	def get_selected_pilot_classes(self):
		selected_pilots = []
		for elem in self.selectedPilotsBox.get_elems():
			if isinstance(elem, CustomButton):
				selected_pilots.append(self.pilotClasses[elem.get_foreground().get_text()])
		return selected_pilots

	def _add_available_pilot(self, pilot_class):
		name = self.trim_string(pilot_class.__name__, self.max_label_width, MenuLabel.custom_font_name, MenuLabel.custom_font_size)
		self.pilotClasses[name] = pilot_class
		self.availablePilotsBox.add_elem(CustomButton(name, self._select_pilot))
		self.availablePilotsCount += 1

	def trim_string(self, string: str, max_width: int, font_name: str, font_size: int = 10):
		substring = string
		while len(substring) > 0:
			label = pyglet.text.Label(substring, font_name=font_name, font_size=font_size)
			if label.content_width > max_width:
				substring = substring[:-1]
			else:
				return substring
		return ""

	def _select_pilot(self, button: CustomButton):
		if self.selectedPilotsCount >= 8:
			return
		text = button.get_foreground().get_text()
		self.selectedPilotsBox.add_elem(CustomButton(text, self._deselect_pilot))
		self.selectedPilotsCount += 1

		if self.selectedPilotsCount > 1:
			self.readyBtn.get_foreground().set_text("Ready!")
			self.readyBtn.enable()

	def _deselect_pilot(self, button: CustomButton):
		self.selectedPilotsBox.remove_elem(button)
		self.selectedPilotsCount -= 1

		if self.selectedPilotsCount < 2:
			self.readyBtn.get_foreground().set_text("Not Ready")
			self.readyBtn.disable()

	def _load_default_pilots(self):
		self._add_available_pilot(afkBot.AfkBot)
		self._add_available_pilot(circleBot.CircleBot)
		self._add_available_pilot(testBot.TestBot)
		self._add_available_pilot(batman.Batman)

	# can't get it to work with pyinstaller
	# pkg_path = fileLoad.resource_path(pilots.__name__)
	# for importer, modname, ispkg in pkgutil.iter_modules([pkg_path]):
	# 	pilot_class_path = pilots.__name__ + os.path.sep + modname + ".py"
	# 	self._add_available_pilot(fileLoad.load_class_by_module_name(pilot_class_path))

	def _load_user_pilots(self):
		pkg_path = os.path.abspath(".")
		for importer, modname, ispkg in pkgutil.iter_modules([pkg_path]):
			if ispkg:
				continue
			try:
				pilot_class = fileLoad.load_class_by_module_name(modname + ".py")
			except ValueError as e:
				print(str(e))
				continue

			if hasattr(pilot_class, "prepare_scan") and hasattr(pilot_class, "update"):
				self._add_available_pilot(pilot_class)
			else:
				print("Class", pilot_class.__name__, "is missing prepare_scan() function or update() function.")

	# watchdog functions
	def on_created(self, event):
		print(f"hey, {event.src_path} has been created!")

	def on_deleted(self, event):
		print(f"Someone deleted {event.src_path}!")

	def on_modified(self, event):
		print(f"{event.src_path} has been modified")

	def on_moved(self, event):
		print(f"someone moved {event.src_path} to {event.dest_path}")
