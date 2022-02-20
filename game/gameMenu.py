import os
import sys

import glooey
import pyglet

from game.boxBackground import BoxBackground
from gui.pygletDraw import PygletDraw
from gui.pygletWindow import PygletWindow


def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)


class MenuLabel(glooey.Label):
	custom_font_name = "GravityBold8"
	custom_color = '#DDDDDD'
	custom_font_size = 12
	custom_padding = 10


class List(glooey.VBox):
	custom_cell_padding = 10
	custom_default_cell_size = 10


class ListTitle(glooey.Label):
	custom_font_name = "GravityBold8"
	custom_color = '#eeeeec'
	custom_font_size = 12
	custom_alignment = 'center'
	custom_bold = True


class ListButton(glooey.Button):
	Foreground = MenuLabel
	custom_alignment = 'fill'

	class Base(glooey.Background):
		custom_color = '#1940ff'

	class Over(glooey.Background):
		custom_color = '#3859FF'

	class Down(glooey.Background):
		custom_color = '#5773FF'

	def __init__(self, text: str, callback):
		super().__init__(text)
		self.callback = callback

	def on_click(self, widget):
		if self.callback:
			self.callback(self)


class MenuGui(glooey.Gui):

	def __init__(self, window: pyglet.window.Window, background: BoxBackground):
		super().__init__(window, clear_before_draw=False)
		self.background = background

	def display(self):
		super().on_draw()

	def on_draw(self):
		"""
		Disables auto drawing
		"""
		pass


class GameMenu:

	def __init__(self, window: PygletWindow, window_size: int, renderer: PygletDraw, game_size: int, background: BoxBackground):
		# https://jotson.itch.io/gravity-pixel-font
		font_path = resource_path(os.path.sep.join(["res", "GravityBold8.ttf"]))
		pyglet.font.add_file(font_path)

		self.window = window
		self.windowSize = window_size
		self.renderer = renderer
		self.gameSize = game_size

		self.background = background
		self.frameCount = 0

		self.availablePilotsCount = 0
		self.selectedPilotsCount = 0
		self.setup_gui()

	def setup_gui(self):
		self.gui = MenuGui(self.window, self.background)
		self.root = glooey.VBox()
		self.root.top_padding = 100
		self.root.alignment = "top"

		self.pilotTable = glooey.HBox()
		self.pilotTable.cell_padding = 80
		self.root.add(self.pilotTable)

		self.availablePilotsBox = List()
		self.selectedPilotsBox = List()

		self.availablePilotsBox.add(ListTitle("Available"))
		self.selectedPilotsBox.add(ListTitle("Selected"))

		self.pilotTable.add(self.availablePilotsBox)
		self.pilotTable.add(self.selectedPilotsBox)

		buttons = [
			"Afk Bot",
			"Circle Bot",
			"User Script",
		]

		for i in range(len(buttons)):
			self._add_available_pilot(buttons[i])

		self.gui.add(self.root)

	def run(self):
		self.background.set_size(self.windowSize)
		pyglet.clock.schedule_interval(self.display, 1.0 / 30)
		pass

	def cancel(self):
		pyglet.clock.unschedule(self.display)

	def display(self, dt):
		self.window.clear()
		self.background.display(self.renderer, 0, self.frameCount)
		self.renderer.StartDraw()
		self.gui.display()
		self.frameCount += 1

	def _add_available_pilot(self, name: str):
		self.availablePilotsBox.add(ListButton(name, self._select_pilot))
		self.availablePilotsCount += 1

	def _select_pilot(self, button: ListButton):
		if self.selectedPilotsCount >= 10:
			return
		text = button.get_foreground().get_text()
		self.selectedPilotsBox.add(ListButton(text, self._deselect_pilot))
		self.selectedPilotsCount += 1

	def _deselect_pilot(self, button: ListButton):
		self.selectedPilotsBox.remove(button)
		self.selectedPilotsCount -= 1

	def find_pilot_scripts(self, path):
		pass
