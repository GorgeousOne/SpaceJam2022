#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.box2d.org
# Python version Copyright (c) 2010 kne / sirkne at gmail dot com
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software. If you use this software
# in a product, an acknowledgment in the product documentation would be
# appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
# misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

# Plainly altered by Aaron

"""
Global Keys:
    Space  - shoot projectile
    Z/X    - zoom
    Escape - quit

Other keys can be set by the individual test.

Mouse:
    Left click  - select/drag body (creates mouse joint)
    Right click - pan
    Shift+Left  - drag to create a directional projectile
    Scroll      - zoom

You can easily add your own tests based on test_empty.
"""
import string

import pyglet
from Box2D import (b2Vec2, b2World, b2AABB, b2QueryCallback, b2_dynamicBody, b2DestructionListener, b2Joint, b2Fixture)
from pyglet import gl

from gui.pygletDraw import grText, PygletDraw
from gui.pygletWindow import PygletWindow
from gui.settings import fwSettings


class fwDestructionListener(b2DestructionListener):
	"""
	The destruction listener callback:
	"SayGoodbye" is called when a joint or shape is deleted.
	"""

	def __init__(self, test, **kwargs):
		super(fwDestructionListener, self).__init__(**kwargs)
		self.test = test

	def SayGoodbye(self, obj):
		# removes reference to destroyed mouse grabbing joint
		if isinstance(obj, b2Joint):
			if self.test.mouseJoint == obj:
				self.test.mouseJoint = None
			else:
				self.test.JointDestroyed(obj)
		elif isinstance(obj, b2Fixture):
			self.test.FixtureDestroyed(obj)


class fwQueryCallback(b2QueryCallback):

	def __init__(self, p):
		super(fwQueryCallback, self).__init__()
		self.point = p
		self.fixture = None

	def ReportFixture(self, fixture):
		body = fixture.body
		if body.type == b2_dynamicBody:
			inside = fixture.TestPoint(self.point)
			if inside:
				self.fixture = fixture
				# We found the object, so stop the query
				return False
		# Continue the query
		return True


class Keys(object):
	pass


class PygletFramework():

	def setup_keys(self):
		key = pyglet.window.key
		self.keys = key.KeyStateHandler()
		# Only basic keys are mapped for now: K_[a-z0-9], K_F[1-12] and
		# K_COMMA.

		if hasattr(string, 'ascii_uppercase'):
			uppercase = string.ascii_uppercase
		else:
			uppercase = string.uppercase

		for letter in uppercase:
			setattr(Keys, 'K_' + letter.lower(), getattr(key, letter))
		for i in range(10):
			setattr(Keys, 'K_%d' % i, getattr(key, '_%d' % i))
		for i in range(1, 13):
			setattr(Keys, 'K_F%d' % i, getattr(key, 'F%d' % i))

		Keys.K_LEFT = key.LEFT
		Keys.K_RIGHT = key.RIGHT
		Keys.K_UP = key.UP
		Keys.K_DOWN = key.DOWN
		Keys.K_HOME = key.HOME
		Keys.K_PAGEUP = key.PAGEUP
		Keys.K_PAGEDOWN = key.PAGEDOWN
		Keys.K_COMMA = key.COMMA

	def __reset(self):

		self.world = None
		self.mouseJoint = None
		self.settings = fwSettings
		self.mouseWorld = None
		self.stepCount = 0
		self.renderer = None

		# Screen/rendering-related
		self._viewZoom = 10.0
		self._viewCenter = None
		self._viewOffset = None
		self.screenSize = None
		self.rMouseDown = False
		self.textLine = 30
		self.font = None
		self.fps = 0

		# Window-related
		self.fontname = "Calibri"
		self.fontsize = 10
		self.font = None
		self.textGroup = None

		# Screen-related
		self._viewZoom = 1.0
		self._viewCenter = None
		self.screenSize = None
		self.textLine = 30
		self.font = None
		self.fps = 0

		self.setup_keys()

	def __init__(self):
		# super(PygletFramework, self).__init__()

		self.__reset()
		self.world = b2World(gravity=(0, 0), doSleep=True)
		self.destructionListener = fwDestructionListener(test=self)
		self.world.destructionListener = self.destructionListener

		print('Initializing Pyglet framework...')
		self.window = PygletWindow(self)

		# Initialize the text display group
		self.textGroup = grText(self.window)

		# Load the font and record the screen dimensions
		self.font = pyglet.font.load(self.fontname, self.fontsize)
		self.screenSize = b2Vec2(self.window.width, self.window.height)

		self.renderer = PygletDraw(self)
		self.renderer.surface = self.window.screen
		# Aaron: everything will be rendered manually

		self.world.renderer = self.renderer
		self._viewCenter = b2Vec2(0, 0)
		self.groundbody = self.world.CreateBody()

	def setCenter(self, value):
		"""
		Updates the view offset based on the center of the screen.

		Tells the debug draw to update its values also.
		"""
		self._viewCenter = b2Vec2(*value)
		self.updateProjection()

	def setZoom(self, zoom):
		self._viewZoom = zoom
		self.updateProjection()

	viewZoom = property(lambda self: self._viewZoom, setZoom,
	                    doc='Zoom factor for the display')
	viewCenter = property(lambda self: self._viewCenter, setCenter,
	                      doc='Screen center in camera coordinates')

	def updateProjection(self):
		"""
		Recalculates the necessary projection.
		"""
		gl.glViewport(0, 0, self.window.width, self.window.height)

		gl.glMatrixMode(gl.GL_PROJECTION)
		gl.glLoadIdentity()

		ratio = float(self.window.width) / self.window.height

		extents = b2Vec2(ratio * 25.0, 25.0)
		extents *= self._viewZoom

		lower = self._viewCenter - extents
		upper = self._viewCenter + extents

		# L/R/B/T
		gl.gluOrtho2D(lower.x, upper.x, lower.y, upper.y)

		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glLoadIdentity()

	def run(self):
		"""
		Main loop.
		"""
		if self.settings.hz > 0.0:
			pyglet.clock.schedule_interval(self.SimulationLoop, 1.0 / self.settings.hz)

		# self.window.push_handlers(pyglet.window.event.WindowEventLogger())
		# TODO: figure out why this is required
		self.window._enable_event_queue = False
		pyglet.app.run()
		self.world.contactListener = None
		self.world.destructionListener = None
		self.world.renderer = None

	def SimulationLoop(self, dt):
		"""
		The main simulation loop. Don't override this, override Step instead.
		And be sure to call super(classname, self).Step(settings) at the end
		of your Step function.
		"""
		# Check the input and clear the screen
		self.CheckKeys()
		self.window.clear()

		# Update the keyboard status
		self.window.push_handlers(self.keys)

		# Create a new batch for drawing
		# self.renderer.batch = pyglet.graphics.Batch()
		self.renderer.clear_layers()

		# Reset the text position
		self.textLine = 15

		# Draw the title of the test at the top
		# self.Print(self.name)

		# Step the physics
		self.Step(self.settings)
		self.window.invalid = True

		self.fps = pyglet.clock.get_fps()

	def Step(self, settings):
		"""
		The main physics step.

		Takes care of physics drawing (callbacks are executed after the world.Step() )
		and drawing additional information.
		"""

		self.stepCount += 1
		if settings.hz > 0.0:
			timeStep = 1.0 / settings.hz
		else:
			timeStep = 0.0

		# Set the other settings that aren't contained in the flags
		self.world.warmStarting = settings.enableWarmStarting
		self.world.continuousPhysics = settings.enableContinuous
		self.world.subStepping = settings.enableSubStepping

		self.world.Step(timeStep, settings.velocityIterations, settings.positionIterations)
		self.world.ClearForces()

		self.Redraw()
		self.renderer.StartDraw()


	def Redraw(self):
		raise NotImplementedError()

	def _Keyboard_Event(self, key, down=True):
		"""
		Internal keyboard event, don't override this.

		Checks for the initial keydown of the basic testbed keys. Passes the unused
		ones onto the test via the Keyboard() function.
		"""
		if down:
			if key == pyglet.window.key.ESCAPE:
				self.window.on_close()
			else:
				# Inform the test of the key press
				self.Keyboard(key)
		else:
			self.KeyboardUp(key)

	def Keyboard(self, key):
		"""
		Callback indicating 'key' has been pressed down.
		"""
		pass

	def KeyboardUp(self, key):
		"""
		Callback indicating 'key' has been released.
		"""
		pass

	def CheckKeys(self):
		"""
		Check the keys that are evaluated on every main loop iteration.
		I.e., they aren't just evaluated when first pressed down
		"""
		pass

	def ShiftMouseDown(self, p):
		"""
		Indicates that there was a left click at point p (world coordinates)
		with the left shift key being held down.
		"""
		pass

	def MouseDown(self, p):
		"""
		Indicates that there was a left click at point p (world coordinates)
		"""
		if self.mouseJoint is not None:
			return

		# Create a mouse joint on the selected body (assuming it's dynamic)
		# Make a small box.
		aabb = b2AABB(lowerBound=p - (0.001, 0.001),
		              upperBound=p + (0.001, 0.001))

		# Query the world for overlapping shapes.
		query = fwQueryCallback(p)
		self.world.QueryAABB(query, aabb)

		if query.fixture:
			body = query.fixture.body
			# A body was selected, create the mouse joint
			self.mouseJoint = self.world.CreateMouseJoint(
				bodyA=self.groundbody,
				bodyB=body,
				target=p,
				maxForce=1000.0 * body.mass)
			body.awake = True

	def MouseUp(self, p):
		"""
		Left mouse button up.
		"""
		if self.mouseJoint:
			self.world.DestroyJoint(self.mouseJoint)
			self.mouseJoint = None

	def MouseMove(self, p):
		"""
		Mouse moved to point p, in world coordinates.
		"""
		self.mouseWorld = p
		if self.mouseJoint:
			self.mouseJoint.target = p

	def ConvertScreenToWorld(self, x, y):
		"""
		Takes screen (x, y) and returns
		world coordinate b2Vec2(x,y).
		"""
		u = float(x) / self.window.width
		v = float(y) / self.window.height

		ratio = float(self.window.width) / self.window.height
		extents = b2Vec2(ratio * 25.0, 25.0)
		extents *= self._viewZoom

		lower = self._viewCenter - extents
		upper = self._viewCenter + extents

		p = b2Vec2(
			(1.0 - u) * lower.x + u * upper.x,
			(1.0 - v) * lower.y + v * upper.y)

		return p

	def DrawStringAt(self, x, y, str, color=(229, 153, 153, 255)):
		"""
		Draw some text, str, at screen coordinates (x, y).
		"""
		pyglet.text.Label(str, font_name=self.fontname,
		                  font_size=self.fontsize, x=x, y=self.window.height - y,
		                  color=color, batch=self.renderer.batch, group=self.textGroup)

	def Print(self, str, color=(229, 153, 153, 255)):
		"""
		Draw some text, str, at screen coordinates (x, y).
		"""
		pyglet.text.Label(str, font_name=self.fontname,
		                  font_size=self.fontsize, x=5, y=self.window.height -
		                                                  self.textLine, color=color, batch=self.renderer.batch,
		                  group=self.textGroup)
		self.textLine += 15

	def Keyboard(self, key):
		"""
		Callback indicating 'key' has been pressed down.
		"""
		pass

	def KeyboardUp(self, key):
		"""
		Callback indicating 'key' has been released.
		See Keyboard() for key information
		"""
		pass

	def FixtureDestroyed(self, fixture):
		"""
		Callback indicating 'fixture' has been destroyed.
		"""
		pass

	def JointDestroyed(self, joint):
		"""
		Callback indicating 'joint' has been destroyed.
		"""
		pass
