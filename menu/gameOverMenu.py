import glooey
import pyglet
from pyglet import gl

from game.boxBackground import BoxBackground
from menu.menuWidget import MenuGui, Title, CustomButton
from render.pygletDraw import PygletDraw
from render.pygletWindow import PygletWindow


class GameOverMenu:

	def __init__(self, window: PygletWindow, return_callback):
		self.window = window
		self.returnCallback = return_callback

		self.pilotClasses = {}
		self._setup_gui()

	def _setup_gui(self):
		self.gui = MenuGui(self.window)
		root = glooey.VBox()
		root.set_default_cell_size(1)
		root.set_cell_padding(20)
		root.set_top_padding(20)
		root.set_alignment("top")

		self.gameTitle = Title("", font_size=24)
		self.gameTitle.set_padding(20)
		root.add(self.gameTitle)

		self.readyButton = CustomButton("Proceed", lambda widget: self.returnCallback())
		self.readyButton.set_size_hint(200, 0)
		self.readyButton.set_alignment("center")
		self.readyButton.get_foreground().set_alignment("center")

		root.add(self.readyButton)
		self.gui.add(root)
		self.window.remove_handlers(self.gui)

	def set_winner(self, winner: str):
		self.gameTitle.set_text(winner + " won!")

	def start(self):
		self.window.push_handlers(self.gui)

	def stop(self):
		self.window.remove_handlers(self.gui)
		self.gameTitle.set_text("It's a tie...")

	def display(self):
		gl.glPushMatrix()
		gl.glLoadIdentity()
		self.gui.display()
		pyglet.gl.glPopMatrix()
