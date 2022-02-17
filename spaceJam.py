from typing import Tuple

import glooey
import numpy as np
from Box2D import b2Color, b2Vec2

from game.boxBackground import BoxBackground
from game.boxBorder import BoxBorder
from game.boxContactListener import BoxContactListener
from game.boxRocket import BoxRocket
from game.boxSpaceship import BoxSpaceship
from game.gameHandler import GameHandler
from game.pilotHandler import PilotHandler
from gui.pygletFramework import PygletFramework
from logic.pilot.afkPilot import AfkPilot
from logic.pilot.circlePilot import CirclePilot
from logic.spaceshipPilot import SpaceshipPilot


class MyLabel(glooey.Label):
	custom_color = '#babdb6'
	custom_font_size = 10
	custom_alignment = 'center'


class MyTitle(glooey.Label):
	custom_color = '#eeeeec'
	custom_font_size = 12
	custom_alignment = 'center'
	custom_bold = True


class MyButton(glooey.Button):
	Foreground = MyLabel
	custom_alignment = 'fill'

	class Base(glooey.Background):
		custom_color = '#204a87'

	class Over(glooey.Background):
		custom_color = '#3465a4'

	class Down(glooey.Background):
		custom_color = '#729fcff'

	def __init__(self, text, response):
		super().__init__(text)
		self.response = response

	def on_click(self, widget):
		print(self.response)


class SpaceJam(PygletFramework):
	name = "Space Jam"

	def __init__(self):
		super(SpaceJam, self).__init__()

		self.windowSize = 600
		self.window.set_size(self.windowSize, self.windowSize)
		self.window.set_caption("Space Jam")
		self.gameSize = 100
		self.frameCount = 0

		self.contactHandler = BoxContactListener(self.world)
		self.world.contactListener = self.contactHandler

		self.pilotHandler = PilotHandler()
		self.gameHandler = GameHandler(self.world, self.contactHandler)

		self._create_battlefield()
		self.spawn_ship(AfkPilot(self.gameSize), (40, 50))
		self.spawn_ship(CirclePilot(self.gameSize), (75, 50), b2Color(0.26, 0.53, 0.96))

		# gui = glooey.Gui(self.window)
		# vbox = glooey.VBox()
		# vbox.alignment = 'center'
		# title = MyTitle("What...is your favorite color?")
		# vbox.add(title)
		# buttons = [
		# 	MyButton("Blue.", "Right, off you go."),
		# 	MyButton("Blue. No yel--", "Auuuuuuuugh!"),
		# 	MyButton("I don't know that!", "Auuuuuuuugh!"),
		# ]
		# for button in buttons:
		# 	vbox.add(button)
		# gui.add(vbox)

	def Redraw(self):
		self.frameCount += 1

		if self.frameCount % (self.settings.hz // 5) == 0:
			self.gameHandler.update()

		self.contactHandler.remove_bodies()

		# try to keep the amount of layers low :P
		for ship in self.contactHandler.spaceships:
			ship.display(self.renderer, 0)
		for explosion in self.contactHandler.explosions:
			explosion.display(self.renderer, 1)
		for scan in self.contactHandler.scans:
			scan.display(self.renderer, 1)
		for rocket in self.contactHandler.rockets:
			rocket.display(self.renderer, 1)

		self.border.display(self.renderer, 0)
		self.background.display(self.renderer, 2, self.frameCount)

	def _create_battlefield(self):
		self.world.gravity = (0.0, 0.0)
		self.border = BoxBorder(self.world, self.gameSize, 1)
		self.background = BoxBackground(self.gameSize)

		self.setZoom((self.gameSize + 4) / 50)
		self.viewCenter.x = self.gameSize / 2
		self.viewCenter.y = self.gameSize / 2

	def spawn_ship(self, pilot: SpaceshipPilot, pos: Tuple[float, float] = (0, 0), fill: b2Color = b2Color(1, 0.73, 0)):
		self.contactHandler.add_spaceship(BoxSpaceship(self.world, pilot, 60, pos, fill))

	def Keyboard(self, key):
		if key == 32:
			for ship in self.contactHandler.spaceships:
				# heading = ship.get_location().get_direction() * 30
				heading = b2Vec2(np.cos(ship.body.angle), np.sin(ship.body.angle)) * 30
				rocket = BoxRocket(self.world, ship, heading)
				self.contactHandler.add_rocket(rocket)


if __name__ == "__main__":
	SpaceJam().run()
