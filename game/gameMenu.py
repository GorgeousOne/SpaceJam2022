import glooey
import pyglet

from game.boxBackground import BoxBackground
from gui.pygletDraw import PygletDraw
from gui.pygletWindow import PygletWindow


class MenuLabel(glooey.Label):
	custom_font_name = "Segoe UI"
	custom_color = '#babdb6'
	custom_font_size = 10


class ListTitle(glooey.Label):
	custom_color = '#eeeeec'
	custom_font_size = 12
	custom_alignment = 'center'
	custom_bold = True


class ListButton(glooey.Button):
	Foreground = MenuLabel
	custom_alignment = 'fill'

	class Base(glooey.Background):
		custom_color = '#204a87'

	class Over(glooey.Background):
		custom_color = '#3465a4'

	class Down(glooey.Background):
		custom_color = '#729fcff'

	def __init__(self, text: str, col_index: int, callback):
		super().__init__(text)
		self.colIndex = col_index
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

	def __init__(self, window: PygletWindow, renderer: PygletDraw, game_size: int, background: BoxBackground):
		self.window = window
		self.renderer = renderer
		self.gameSize = game_size

		self.background = background
		self.setup_gui()
		self.frameCount = 0

	def setup_gui(self):
		self.gui = MenuGui(self.window, self.background)
		self.root = glooey.VBox()
		self.root.alignment = 'center'

		buttons = [
			ListButton("🤖 Afk Bote", 1, None),
			ListButton("Circle Bot", 2, None),
			ListButton("I don't know that!", 3, None),
		]

		self.pilot_table = glooey.Grid(num_cols=2, num_rows=len(buttons) + 1)
		self.root.add(self.pilot_table)

		self.pilot_table[0, 0] = ListTitle("Available Pilots")
		self.pilot_table[0, 1] = ListTitle("Selected Pilots")

		for i in range(len(buttons)):
			self.pilot_table[i + 1, 0] = buttons[i]
		self.gui.add(self.root)

	def run(self):
		self.background.set_size(self.window.width)
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

	def select_pilot(self, button: ListButton):
		pass

	def deselect_pilot(self, button: ListButton):
		pass

	def find_pilot_scripts(self, path):
		pass
