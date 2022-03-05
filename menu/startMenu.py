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
		self.pilotClasses = {}
		self.max_label_width = 220  # manually evaluated
		self._setup_watchdog()

		self.doPilotUpdate = False
		super().__init__(window)

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
		# path = "."
		patterns = ["*.py"]
		ignore_patterns = None
		ignore_directories = True
		case_sensitive = True
		event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
		event_handler.on_created = self._signal_update
		event_handler.on_deleted = self._signal_update
		event_handler.on_modified = self._signal_update
		event_handler.on_moved = self._signal_update
		self.observer = Observer()
		self.observer.schedule(event_handler, ".", recursive=False)
		self.observer.start()

	def get_selected_pilot_classes(self):
		selected_pilots = []
		for elem in self.selectedPilotsBox.get_elems():
			if isinstance(elem, CustomButton):
				selected_pilots.append(self.pilotClasses[elem.get_foreground().get_text()])
		return selected_pilots

	def _add_available_pilot(self, pilot_class):
		name = pilot_class.__name__
		name = name[0:16] if len(name) > 16 else name

		# name = self.trim_string(pilot_class.__name__, self.max_label_width, MenuLabel.custom_font_name, MenuLabel.custom_font_size)
		self.pilotClasses[name] = pilot_class
		self.availablePilotsBox.add_elem(CustomButton(name, self._select_pilot))

	def trim_string(self, string: str, max_width: int, font_name: str, font_size: int = 10):
		substring = string
		while len(substring) > 0:
			print("string", substring)
			label = pyglet.text.Label(substring, font_name=font_name, font_size=font_size)
			if label.content_width > max_width:
				substring = substring[:-1]
			else:
				return substring
		return ""

	def _select_pilot(self, button: CustomButton):
		if len(self.selectedPilotsBox) >= 8:
			return
		text = button.get_foreground().get_text()
		self.selectedPilotsBox.add_elem(CustomButton(text, self._deselect_pilot))

		if len(self.selectedPilotsBox) > 1:
			self.readyBtn.get_foreground().set_text("Ready!")
			self.readyBtn.enable()

	def _deselect_pilot(self, button: CustomButton):
		self.selectedPilotsBox.remove_elem(button)

		if len(self.selectedPilotsBox) < 2:
			self.readyBtn.get_foreground().set_text("Not Ready")
			self.readyBtn.disable()

	def _reset_pilots(self):
		self.pilotClasses.clear()
		self.availablePilotsBox.clear()
		self.selectedPilotsBox.clear()
		self._load_default_pilots()
		self._load_user_pilots()

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
		for importer, mod_name, is_pkg in pkgutil.iter_modules([pkg_path]):
			if is_pkg:
				continue
			try:
				pilot_class = fileLoad.load_class_by_module_name(mod_name + ".py")
			except ValueError as e:
				print(str(e))
				continue

			if hasattr(pilot_class, "prepare_scan") and hasattr(pilot_class, "update"):
				# pass
				self._add_available_pilot(pilot_class)
			else:
				print("Class \"" + pilot_class.__name__ + "\" is missing prepare_scan() function or update() function.")

	def unhide(self):
		super().unhide()
		self._reset_pilots()

	def hide(self):
		super().hide()

	def display(self):
		if self.doPilotUpdate:
			self._reset_pilots()
			self.doPilotUpdate = False
		super().display()

	def _signal_update(self, event):
		self.doPilotUpdate = True
