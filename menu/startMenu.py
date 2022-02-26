import os
import pkgutil

import glooey
from pyglet import gl
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

import bots.afkBot
import bots.circleBot
import bots.batman

from menu.menuWidget import CustomButton, ScrollList, MenuGui, Title
from render.pygletWindow import PygletWindow
from util import fileLoad


class StartMenu:

	def __init__(self, window: PygletWindow, game_start_callback):
		self.window = window
		self.gameStartCallback = game_start_callback

		self.availablePilotsCount = 0
		self.selectedPilotsCount = 0

		self.pilotClasses = {}
		self._setup_gui()

		# manually evaluated
		self.max_label_width = 140
		self._load_default_pilots()
		self._load_user_pilots()
		# self._setup_watchdog()

	def _setup_gui(self):
		self.gui = MenuGui(self.window)

		root = glooey.VBox()
		root.set_default_cell_size(1)
		root.set_cell_padding(20)
		root.set_padding(20)
		root.set_alignment("top")

		game_title = Title("Space Jam", font_size=24)
		game_title.set_padding(20)
		root.add(game_title)

		table_container = glooey.HBox()
		table_container.set_cell_padding(40)
		root.add(table_container)

		self.availablePilotsBox = ScrollList("Available")
		self.selectedPilotsBox = ScrollList("Selected")
		table_container.add(self.availablePilotsBox)
		table_container.add(self.selectedPilotsBox)

		self.readyButton = CustomButton("Not Ready", lambda widget: self.gameStartCallback())
		self.readyButton.set_size_hint(200, 0)
		self.readyButton.set_alignment("center")
		self.readyButton.get_foreground().set_alignment("center")

		self.readyButton.disable()
		root.add(self.readyButton)
		self.gui.add(root)
		self.gui.hide()

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

	def unhide(self):
		self.gui.unhide()

	def hide(self):
		self.gui.hide()

	def display(self):
		gl.glPushMatrix()
		gl.glLoadIdentity()
		self.gui.display()
		gl.glPopMatrix()

	def _add_available_pilot(self, pilot_class):
		name = self.trim_string(pilot_class.__name__, self.max_label_width, MenuLabel.custom_font_name, MenuLabel.custom_font_size)
		self.pilotClasses[name] = pilot_class
		self.availablePilotsBox.add_elem(CustomButton(name, self._select_pilot))
		self.availablePilotsCount += 1

	def trim_string(self, string: str, max_width: int, font_name: str, font__size: int = 10):
		substring = string
		while len(substring) > 0:
			label = pyglet.text.Label(substring)
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
			self.readyButton.get_foreground().set_text("Ready!")
			self.readyButton.enable()

	def _deselect_pilot(self, button: CustomButton):
		self.selectedPilotsBox.remove_elem(button)
		self.selectedPilotsCount -= 1

		if self.selectedPilotsCount < 2:
			self.readyButton.get_foreground().set_text("Not Ready")
			self.readyButton.disable()

	def _load_default_pilots(self):
		self._add_available_pilot(bots.afkBot.AfkBot)
		self._add_available_pilot(bots.circleBot.CircleBot)
		self._add_available_pilot(bots.batman.Batman)

	# can't get it to work with pyinstaller
	# pkg_path = fileLoad.resource_path(pilots.__name__)
	# for importer, modname, ispkg in pkgutil.iter_modules([pkg_path]):
	# 	pilot_class_path = pilots.__name__ + os.path.sep + modname + ".py"
	# 	self._add_available_pilot(fileLoad.load_class_by_module_name(pilot_class_path))

	def _load_user_pilots(self):
		pkg_path = os.path.abspath("../game")
		for importer, modname, ispkg in pkgutil.iter_modules([pkg_path]):
			if ispkg:
				continue
			try:
				pilot_class = fileLoad.load_class_by_module_name(modname + ".py")
			except ValueError as e:
				print(str(e))
				continue

			if hasattr(pilot_class, "update") and hasattr(pilot_class, "process_scan"):
				self._add_available_pilot(pilot_class)
			else:
				print("Class", pilot_class.__name__, "is missing update() function or process_scan() function.")

	# watchdog functions
	def on_created(self, event):
		print(f"hey, {event.src_path} has been created!")

	def on_deleted(self, event):
		print(f"Someone deleted {event.src_path}!")

	def on_modified(self, event):
		print(f"{event.src_path} has been modified")

	def on_moved(self, event):
		print(f"someone moved {event.src_path} to {event.dest_path}")
