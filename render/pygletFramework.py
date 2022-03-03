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

from render.pygletDraw import TextLayer, PygletDraw
from render.settings import fwSettings


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


class PygletFramework:

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
		self.screenSize = None
		self.textLine = 30
		self.font = None
		self.fps = 0

		self.setup_keys()

	def __init__(self, window: pyglet.window.Window):
		self.__reset()
		self.world = b2World(gravity=(0, 0), doSleep=True)
		self.destructionListener = fwDestructionListener(test=self)
		self.world.destructionListener = self.destructionListener
		self.window = window

		self.world.warmStarting = self.settings.enableWarmStarting
		self.world.continuousPhysics = self.settings.enableContinuous
		self.world.subStepping = self.settings.enableSubStepping

		# Load the font and record the screen dimensions
		self.font = pyglet.font.load(self.fontname, self.fontsize)
		self.screenSize = b2Vec2(self.window.width, self.window.height)

		self.renderer = PygletDraw(self.window)
		self.renderer.surface = self.window.screen
		# Aaron: everything will be rendered manually

		# self.world.renderer = self.renderer
		self._viewCenter = b2Vec2(0, 0)
		self.groundbody = self.world.CreateBody()


	def run(self):
		"""
		Main loop.
		"""
		self.window.push_handlers(self)
		# self.window.push_handlers(self.renderer)

		if self.settings.hz > 0.0:
			pyglet.clock.schedule_interval(self.display, 1.0 / self.settings.hz)

		# self.window.push_handlers(pyglet.window.event.WindowEventLogger())
		# TODO: figure out why this is required
		self.window._enable_event_queue = False

	def cancel(self):
		pyglet.clock.unschedule(self.display)
		self.window.remove_handlers(self)
		self.window.remove_handlers(self.renderer)

	def SimulationLoop(self, dt):
		"""
		The main simulation loop. Don't override this, override Step instead.
		And be sure to call super(classname, self).Step(settings) at the end
		of your Step function.
		"""
		# Check the input and clear the screen
		self.CheckKeys()
		# self.window.clear()

		# Update the keyboard status
		self.window.push_handlers(self.keys)

		# Create a new batch for drawing
		self.renderer.clear_batch()

		# Step the physics
		self.Step()
		# self.window.invalid = True

	def Step(self):
		"""
		The main physics step.

		Takes care of physics drawing (callbacks are executed after the world.Step() )
		and drawing additional information.
		"""
		self.stepCount += 1
		time_step = 1.0 / self.settings.hz
		self.world.Step(time_step, self.settings.velocityIterations, self.settings.positionIterations)
		self.world.ClearForces()

	def display(self, dt):
		raise NotImplementedError()

	def on_close(self):
		"""
		Callback: user tried to close the window
		"""
		self.cancel()

	def on_key_press(self, key, modifiers):
		self._Keyboard_Event(key, down=True)

	def on_key_release(self, key, modifiers):
		self._Keyboard_Event(key, down=False)

	def on_mouse_press(self, x, y, button, modifiers):
		p = self.ConvertScreenToWorld(x, y)
		self.mouseWorld = p
		if button == pyglet.window.mouse.LEFT:
			if modifiers & pyglet.window.key.MOD_SHIFT:
				self.ShiftMouseDown(p)
			else:
				self.MouseDown(p)
		elif button == pyglet.window.mouse.MIDDLE:
			pass

	def on_mouse_release(self, x, y, button, modifiers):
		"""
		Mouse up
		"""
		p = self.ConvertScreenToWorld(x, y)
		self.mouseWorld = p

		if button == pyglet.window.mouse.LEFT:
			self.MouseUp(p)

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		"""
		Mouse scrollwheel used
		"""
		pass

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		"""
		Mouse moved while clicking
		"""
		p = self.ConvertScreenToWorld(x, y)
		self.mouseWorld = p
		self.MouseMove(p)


	
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
		ratio = float(self.window.width) / self.window.height
		extents = b2Vec2(ratio, 1.0)
		extents *= self.renderer.viewZoom

		lower = self.renderer.viewCenter - extents
		upper = self.renderer.viewCenter + extents

		u = float(x) / self.window.width
		v = float(y) / self.window.height

		p = b2Vec2(
			(1.0 - u) * lower.x + u * upper.x,
			(1.0 - v) * lower.y + v * upper.y)
		return p

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
