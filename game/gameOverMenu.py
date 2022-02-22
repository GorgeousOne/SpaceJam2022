import glooey
import pyglet
from pyglet import gl

from game.boxBackground import BoxBackground
from render.pygletDraw import PygletDraw
from render.pygletWindow import PygletWindow


class MenuLabel(glooey.Label):
	custom_font_name = "GravityBold8"
	custom_color = '#DDDDDD'
	custom_font_size = 12
	custom_padding = 10


class Title(glooey.Label):
	custom_font_name = "GravityBold8"
	custom_font_size = 12
	custom_color = '#eeeeec'
	custom_alignment = 'center'


class VScrollBox(glooey.ScrollBox):
	class VBar(glooey.VScrollBar):
		pass


class ScrollList(glooey.VBox):
	custom_alignment = 'top'
	custom_default_cell_size = 1
	custom_cell_padding = 15

	def __init__(self, name):
		super().__init__()
		self.header = Title(name)
		self.table = VScrollBox()

		self.table.set_height_hint(360)
		self.tableContents = glooey.VBox()
		self.tableContents.set_cell_padding(10)
		self.tableContents.set_default_cell_size(1)

		self.add(self.header)
		self.add(self.table)
		self.table.add(self.tableContents)

	def add_elem(self, elem: glooey.Widget):
		self.tableContents.add(elem)

	def remove_elem(self, elem: glooey.Widget):
		self.tableContents.remove(elem)

	def get_elems(self):
		return self.tableContents.get_children()


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

	def __init__(self, window: PygletWindow, background: BoxBackground, game_start_callback):
		self.window = window
		self.background = background
		self.gameStartCallback = game_start_callback

		self.renderer = PygletDraw(self.window)
		self.frameCount = 0
		self.availablePilotsCount = 0
		self.selectedPilotsCount = 0

		self.pilotClasses = {}
		self._setup_gui()

	def _setup_gui(self):
		self.gui = MenuGui(self.window)
		root = glooey.VBox()
		root.set_default_cell_size(1)
		root.set_cell_padding(20)
		root.set_top_padding(20)
		root.set_alignment("top")

		gameTitle = Title("Bot won the game", font_size=24)
		gameTitle.set_padding(20)
		root.add(gameTitle)

		self.readyButton = CustomButton("Not Ready", lambda widget: self.gameStartCallback())
		self.readyButton.set_size_hint(200, 0)
		self.readyButton.set_alignment("center")
		self.readyButton.get_foreground().set_alignment("center")

		root.add(self.readyButton)

		self.gui.add(root)

	def run(self, fps):
		pyglet.clock.schedule_interval(self.display, 1.0 / fps)

	def cancel(self):
		pyglet.clock.unschedule(self.display)

	def display(self, dt):
		self.window.clear()
		self.background.display(self.renderer, 0, self.frameCount)
		self.renderer.StartDraw()

		gl.glPushMatrix()
		gl.glLoadIdentity()
		self.gui.display()
		pyglet.gl.glPopMatrix()
		self.frameCount += 1
