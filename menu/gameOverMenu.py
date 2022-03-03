import glooey
from pyglet import gl

from menu.menuWidget import MenuGui, Title, CustomButton
from render.pygletWindow import PygletWindow


class GameOverMenu:

	def __init__(self, window: PygletWindow, return_callback):
		self.window = window
		self.returnCallback = return_callback
		self._setup_gui()

	def _setup_gui(self):
		self.gui = MenuGui(self.window)

		root = glooey.VBox()
		root.set_default_cell_size(1)
		root.set_cell_padding(40)
		root.set_bottom_padding(60)
		root.set_alignment("center")

		self.resultTitle = Title("", font_size=24)
		root.add(self.resultTitle)

		self.readyButton = CustomButton("Return", lambda widget: self.returnCallback())
		self.readyButton.set_size_hint(200, 0)
		self.readyButton.set_alignment("center")
		self.readyButton.get_foreground().set_alignment("center")

		root.add(self.readyButton)
		self.gui.add(root)
		self.gui.hide()

	def set_winner(self, winner: str):
		self.resultTitle.set_text(winner + " won!")

	def unhide(self):
		self.gui.unhide()

	def hide(self):
		self.resultTitle.set_text("It's a tie...")
		self.gui.hide()

	def display(self):
		gl.glPushMatrix()
		gl.glLoadIdentity()
		self.gui.display()
		gl.glPopMatrix()
