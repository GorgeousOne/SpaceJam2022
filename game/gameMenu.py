import os
import pkgutil

import glooey
import pyglet
from pyglet import gl
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

import pilots.afkPilot
import pilots.circlePilot

from game.boxBackground import BoxBackground
from gui.pygletDraw import PygletDraw
from gui.pygletWindow import PygletWindow
from util import fileLoad


class MenuLabel(glooey.Label):
	custom_font_name = "GravityBold8"
	custom_color = '#DDDDDD'
	custom_font_size = 12
	custom_padding = 10


class ListBox(glooey.ScrollBox):
	custom_alignment = 'center'
	custom_height_hint = 360

	class VBar(glooey.VScrollBar):
		custom_scale_grip = True

	def __init__(self):
		super().__init__()
		self.table = glooey.VBox()
		self.table.set_cell_padding(10)
		self.table.set_default_cell_size(1)
		self.add(self.table)

	def add_elem(self, elem: glooey.Widget):
		self.table.add(elem)

	def remove_elem(self, elem: glooey.Widget):
		self.table.remove(elem)

	def get_elems(self):
		return self.table.get_children()

class Title(glooey.Label):
	custom_font_name = "GravityBold8"
	custom_font_size = 12
	custom_color = '#eeeeec'
	custom_alignment = 'center'


class CustomButton(glooey.Button):
	Foreground = MenuLabel
	custom_alignment = 'fill'

	class Base(glooey.Background):
		custom_color = '#1940ff'

	class Over(glooey.Background):
		custom_color = '#3859FF'

	class Down(glooey.Background):
		custom_color = '#5773FF'

	class Off(glooey.Background):
		custom_color = "#696969"

	def __init__(self, text: str, callback):
		super().__init__(text)
		self.callback = callback

	def on_click(self, widget):
		if self.callback:
			self.callback(self)


class MenuGui(glooey.Gui):

	def __init__(self, window: pyglet.window.Window):
		super().__init__(window, clear_before_draw=False)

	def display(self):
		super().on_draw()

	def on_draw(self):
		"""
		Disables auto drawing
		"""
		pass


class GameMenu:

	def __init__(self, window: PygletWindow, game_matrixf, background: BoxBackground, game_start_callback):
		# https://jotson.itch.io/gravity-pixel-font
		font_path = fileLoad.resource_path(os.path.sep.join(["res", "GravityBold8.ttf"]))
		pyglet.font.add_file(font_path)

		self.window = window
		self.gameMatrixF = game_matrixf
		self.background = background
		self.gameStartCallback = game_start_callback

		self.renderer = PygletDraw(self.window)
		self.frameCount = 0
		self.availablePilotsCount = 0
		self.selectedPilotsCount = 0

		self.pilotClasses = {}
		self._setup_gui()
		self._setup_watchdog()

	def get_selected_pilot_classes(self):
		selected_pilots = []
		for elem in self.selectedPilotsBox.get_elems():
			if isinstance(elem, CustomButton):
				selected_pilots.append(self.pilotClasses[elem.get_foreground().get_text()])
		return selected_pilots


	def _setup_gui(self):
		self.gui = MenuGui(self.window)
		root = glooey.VBox()
		root.set_default_cell_size(1)
		root.set_cell_padding(40)
		root.set_top_padding(40)
		root.set_alignment("top")

		gameTitle = Title("Space Jam", font_size=24)
		root.add(gameTitle)

		tableContainer = glooey.HBox()
		tableContainer.set_cell_padding(40)
		root.add(tableContainer)

		self.availablePilotsBox = ListBox()
		self.selectedPilotsBox = ListBox()
		self.availablePilotsBox.add_elem(Title("Available"))
		self.selectedPilotsBox.add_elem(Title("Selected"))
		tableContainer.add(self.availablePilotsBox)
		tableContainer.add(self.selectedPilotsBox)

		self._load_default_pilots()
		self._load_user_pilots()

		self.readyButton = CustomButton("Not Ready", lambda widget: self.gameStartCallback())
		self.readyButton.set_size_hint(200, 0)
		self.readyButton.set_alignment("center")
		self.readyButton.get_foreground().set_alignment("center")

		self.readyButton.disable()
		root.add(self.readyButton)

		self.gui.add(root)

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

		path = "."
		self.my_observer = Observer()
		self.my_observer.schedule(my_event_handler, path, recursive=False)
		self.my_observer.start()

	def run(self):
		pyglet.clock.schedule_interval(self.display, 1.0 / 30)

	def cancel(self):
		pyglet.clock.unschedule(self.display)
		self.my_observer.stop()
		self.my_observer.join()

	def display(self, dt):
		self.window.clear()

		gl.glPushMatrix()
		gl.glLoadMatrixf(self.gameMatrixF)
		self.background.display(self.renderer, 0, self.frameCount)
		self.renderer.StartDraw()
		pyglet.gl.glPopMatrix()

		self.gui.display()
		self.frameCount += 1

	def _add_available_pilot(self, pilot_class):
		name = pilot_class.__name__
		self.pilotClasses[name] = pilot_class
		self.availablePilotsBox.add_elem(CustomButton(name, self._select_pilot))
		self.availablePilotsCount += 1

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
		self._add_available_pilot(pilots.afkPilot.AfkPilot)
		self._add_available_pilot(pilots.circlePilot.CirclePilot)
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