import pyglet


class PygletWindow(pyglet.window.Window):

	def __init__(self, framework):
		super(PygletWindow, self).__init__(config=pyglet.gl.Config(sample_buffers=1, samples=8))
		self.framework = framework
		self._isFirstDraw = True

	def on_close(self):
		"""
		Callback: user tried to close the window
		"""
		if self.framework:
			pyglet.clock.unschedule(self.framework.SimulationLoop)
		super(PygletWindow, self).on_close()


	def on_show(self):
		"""
		Callback: the window was shown.
		"""
		# updates projection on next draw
		self._isFirstDraw = True

	# adds projection update on first draw, doesn't work earlier somehow
	def on_draw(self):
		if self.framework and self._isFirstDraw:
			self.framework.updateProjection()
			self._isFirstDraw = False

	def on_key_press(self, key, modifiers):
		if self.framework:
			self.framework._Keyboard_Event(key, down=True)

	def on_key_release(self, key, modifiers):
		self.framework._Keyboard_Event(key, down=False)

	def on_mouse_press(self, x, y, button, modifiers):
		if not self.framework:
			return

		p = self.framework.ConvertScreenToWorld(x, y)
		self.framework.mouseWorld = p
		if button == pyglet.window.mouse.LEFT:
			if modifiers & pyglet.window.key.MOD_SHIFT:
				self.framework.ShiftMouseDown(p)
			else:
				self.framework.MouseDown(p)
		elif button == pyglet.window.mouse.MIDDLE:
			pass

	def on_mouse_release(self, x, y, button, modifiers):
		"""
		Mouse up
		"""
		if not self.framework:
			return

		p = self.framework.ConvertScreenToWorld(x, y)
		self.framework.mouseWorld = p

		if button == pyglet.window.mouse.LEFT:
			self.framework.MouseUp(p)

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		"""
		Mouse scrollwheel used
		"""
		pass

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		"""
		Mouse moved while clicking
		"""
		if not self.framework:
			return
		p = self.framework.ConvertScreenToWorld(x, y)
		self.framework.mouseWorld = p
		self.framework.MouseMove(p)

