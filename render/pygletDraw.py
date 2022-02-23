import math

import pyglet
from Box2D import b2Draw, b2Color, b2Vec2
from pyglet import gl


class grBlended(pyglet.graphics.Group):
	"""
	This pyglet rendering group enables blending.
	"""

	def set_state(self):
		gl.glEnable(gl.GL_BLEND)
		gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

	def unset_state(self):
		gl.glDisable(gl.GL_BLEND)


class grPointSize(pyglet.graphics.Group):
	"""
	This pyglet rendering group sets a specific point size.
	"""

	def __init__(self, size=4.0):
		super(grPointSize, self).__init__()
		self.size = size

	def set_state(self):
		gl.glPointSize(self.size)

	def unset_state(self):
		gl.glPointSize(1.0)


class TextLayer(pyglet.graphics.OrderedGroup):
	"""
	This pyglet rendering group sets the proper projection for
	displaying text when used.
	"""
	window = None

	def __init__(self, order, window, pos: b2Vec2=None):
		super().__init__(order)
		self.window = window
		self.pos = pos

	def set_state(self):
		gl.glMatrixMode(gl.GL_PROJECTION)
		gl.glPushMatrix()
		gl.glLoadIdentity()
		gl.gluOrtho2D(0, self.window.width, 0, self.window.height)

		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glPushMatrix()
		gl.glLoadIdentity()
		if self.pos:
			gl.glTranslatef(self.pos.x % 1.0, self.pos.y % 1.0, 0)

	def unset_state(self):
		gl.glPopMatrix()
		gl.glMatrixMode(gl.GL_PROJECTION)
		gl.glPopMatrix()
		gl.glMatrixMode(gl.GL_MODELVIEW)


class PygletDraw(b2Draw):
	"""
	This debug draw class accepts callbacks from Box2D (which specifies what to draw)
	and handles all of the rendering.

	If you are writing your own game, you likely will not want to use debug drawing.
	Debug drawing, as its name implies, is for debugging.
	"""
	blended = grBlended()
	circle_segments = 16
	surface = None
	circle_cache_tf = {}  # triangle fan (inside)
	circle_cache_ll = {}  # line loop (border)

	def __init__(self, window: pyglet.window.Window):
		super(PygletDraw, self).__init__()
		self.window = window
		self.batch = pyglet.graphics.Batch()
		self.layers = {}

		self._viewZoom = 10.0
		self._viewCenter = b2Vec2(300, 300)
		self._viewOffset = b2Vec2(0, 0)

	# self._isFirstDraw = False

	def setCenter(self, value):
		"""
		Updates the view offset based on the center of the screen.

		Tells the debug draw to update its values also.
		"""
		self._viewCenter = b2Vec2(*value)

	# self.updateProjection()

	def setZoom(self, zoom):
		self._viewZoom = zoom

	# self.updateProjection()

	viewZoom = property(lambda self: self._viewZoom, setZoom,
	                    doc='Zoom factor for the display')
	viewCenter = property(lambda self: self._viewCenter, setCenter,
	                      doc='Screen center in camera coordinates')

	def updateProjection(self):
		"""
		Recalculates the necessary projection.
		"""
		raise ValueError("Function should not be called if model view matrix is handled manually")
		gl.glViewport(0, 0, self.window.width, self.window.height)
		gl.glMatrixMode(gl.GL_PROJECTION)
		gl.glLoadIdentity()

		ratio = float(self.window.width) / self.window.height

		extents = b2Vec2(ratio, 1.0)
		extents *= self._viewZoom

		lower = self._viewCenter - extents
		upper = self._viewCenter + extents

		# L/R/B/T
		gl.gluOrtho2D(lower.x, upper.x, lower.y, upper.y)

		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glLoadIdentity()

	def on_show(self):
		"""
		Callback: the window was shown.
		"""
		pass

	def clear_batch(self):
		self.batch = pyglet.graphics.Batch()

	def get_or_create_layer(self, layer_index, is_text: bool = False) -> pyglet.graphics.OrderedGroup:
		if layer_index not in self.layers.keys():
			if is_text:
				self.layers[layer_index] = TextLayer(layer_index, self.window)
			else:
				self.layers[layer_index] = pyglet.graphics.OrderedGroup(layer_index)

		return self.layers[layer_index]

	def StartDraw(self):
		# if self._isFirstDraw:
		#     self.updateProjection()
		#     self._isFirstDraw = False
		self.batch.draw()

	def EndDraw(self):
		self.batch = pyglet.graphics.Batch()
		pass

	def vertex_array(self, vertices):
		out = []
		for v in vertices:
			out.extend(v)
		return len(vertices), out

	def triangle_fan(self, vertices):
		"""
		in: vertices arranged for gl_triangle_fan ((x,y),(x,y)...)
		out: vertices arranged for gl_triangles (x,y,x,y,x,y...)
		"""
		out = []
		for i in range(1, len(vertices) - 1):
			# 0,1,2  0,2,3  0,3,4 ...
			out.extend(vertices[0])
			out.extend(vertices[i])
			out.extend(vertices[i + 1])
		return len(out) // 2, out

	def triangle_strip(self, vertices):
		"""
		in: vertices arranged for gl_triangle_fan ((x,y),(x,y)...)
		out: vertices arranged for gl_triangles (x,y,x,y,x,y...)
		"""
		out = []
		for i in range(len(vertices) - 2):
			# 0,1,2  1,2,3  2,3,4 ...
			out.extend(vertices[i])
			out.extend(vertices[i + 1])
			out.extend(vertices[i + 2])
		return len(out) // 2, out

	def line_loop(self, vertices):
		"""
		in: vertices arranged for gl_line_loop ((x,y),(x,y)...)
		out: vertices arranged for gl_lines (x,y,x,y,x,y...)
		"""
		out = []
		for i in range(len(vertices) - 1):
			# 0,1  1,2  2,3 ... len-1,len  len,0
			out.extend(vertices[i])
			out.extend(vertices[i + 1])

		out.extend(vertices[len(vertices) - 1])
		out.extend(vertices[0])

		return len(out) // 2, out

	def _getLLCircleVertices(self, radius, points):
		"""
		Get the line loop-style vertices for a given circle.
		Drawn as lines.

		"Line Loop" is used as that's how the C++ code draws the
		vertices, with lines going around the circumference of the
		circle (GL_LINE_LOOP).

		This returns 'points' amount of lines approximating the
		border of a circle.

		(x1, y1, x2, y2, x3, y3, ...)
		"""
		ret = []
		step = 2 * math.pi / points
		n = 0
		for i in range(points):
			ret.append((math.cos(n) * radius, math.sin(n) * radius))
			n += step
			ret.append((math.cos(n) * radius, math.sin(n) * radius))
		return ret

	def _getTFCircleVertices(self, radius, points):
		"""
		Get the triangle fan-style vertices for a given circle.
		Drawn as triangles.

		"Triangle Fan" is used as that's how the C++ code draws the
		vertices, with triangles originating at the center of the
		circle, extending around to approximate a filled circle
		(GL_TRIANGLE_FAN).

		This returns 'points' amount of lines approximating the
		circle.

		(a1, b1, c1, a2, b2, c2, ...)
		"""
		ret = []
		step = 2 * math.pi / points
		n = 0
		for i in range(points):
			ret.append((0.0, 0.0))
			ret.append((math.cos(n) * radius, math.sin(n) * radius))
			n += step
			ret.append((math.cos(n) * radius, math.sin(n) * radius))
		return ret

	def getCircleVertices(self, center, radius, points):
		"""
		Returns the triangles that approximate the circle and
		the lines that border the circles edges, given
		(center, radius, points).

		Caches the calculated LL/TF vertices, but recalculates
		based on the center passed in.

		TODO: Currently, there's only one point amount,
		so the circle cache ignores it when storing. Could cause
		some confusion if you're using multiple point counts as
		only the first stored point-count for that radius will
		show up.
		TODO: What does the previous TODO mean?

		Returns: (tf_vertices, ll_vertices)
		"""
		if radius not in self.circle_cache_tf:
			self.circle_cache_tf[
				radius] = self._getTFCircleVertices(radius, points)
			self.circle_cache_ll[
				radius] = self._getLLCircleVertices(radius, points)

		ret_tf, ret_ll = [], []

		for x, y in self.circle_cache_tf[radius]:
			ret_tf.extend((x + center[0], y + center[1]))
		for x, y in self.circle_cache_ll[radius]:
			ret_ll.extend((x + center[0], y + center[1]))
		return ret_tf, ret_ll

	def getArcVertices(self, center, radius, angle_start, angle_end):
		angle = angle_end - angle_start
		fan = []
		fan.append((center[0], center[1]))
		for i in range(self.circle_segments):
			current_angle = angle_start + i / (self.circle_segments + 1) * angle
			fan.append((
				center[0] + math.cos(current_angle) * radius,
				center[1] + math.sin(current_angle) * radius))
		return self.triangle_fan(fan)

	def c4f_arr(self, color: b2Color):
		return [color.r, color.g, color.b, getattr(color, "a", 1.0)]

	def DrawCircle(self, layer_index, center, radius, color):
		"""
		Draw an unfilled circle given center, radius and color.
		"""
		layer = self.get_or_create_layer(layer_index)
		unused, ll_vertices = self.getCircleVertices(
			center, radius, self.circle_segments)
		ll_count = len(ll_vertices) // 2

		self.batch.add(ll_count, gl.GL_LINES, layer,
		               ('v2f', ll_vertices),
		               ('c4f', [color.r, color.g, color.b, 1.0] * ll_count))

	def DrawSolidCircle(self, layer_index, center, radius, color):
		"""
		Draw an filled circle given center, radius, axis (of orientation) and color.
		"""
		layer = self.get_or_create_layer(layer_index)
		tf_vertices, ll_vertices = self.getCircleVertices(
			center, radius, self.circle_segments)
		tf_count, ll_count = len(tf_vertices) // 2, len(ll_vertices) // 2

		self.batch.add(tf_count, gl.GL_TRIANGLES, layer,
		               ('v2f', tf_vertices),
		               ('c4f', self.c4f_arr(color) * tf_count))

	def DrawPolygon(self, layer_index, vertices, color):
		"""
		Draw a wireframe polygon given the world vertices (tuples) with the specified color.
		"""
		layer = self.get_or_create_layer(layer_index)
		if len(vertices) == 2:
			p1, p2 = vertices
			self.batch.add(2, gl.GL_LINES, layer,
			               ('v2f', (p1[0], p1[1], p2[0], p2[1])),
			               ('c3f', [color.r, color.g, color.b] * 2))
		else:
			ll_count, ll_vertices = self.line_loop(vertices)

			self.batch.add(ll_count, gl.GL_LINES, layer,
			               ('v2f', ll_vertices),
			               ('c4f', [color.r, color.g, color.b, 1.0] * (ll_count)))

	def DrawSolidPolygon(self, layer_index, vertices, color):
		"""
		Draw a filled polygon given the world vertices (tuples) with the specified color.
		"""
		layer = self.get_or_create_layer(layer_index)
		if len(vertices) == 2:
			p1, p2 = vertices
			self.batch.add(2, gl.GL_LINES, layer,
			               ('v2f', (p1[0], p1[1], p2[0], p2[1])),
			               ('c3f', [color.r, color.g, color.b] * 2))
		else:
			tf_count, tf_vertices = self.triangle_fan(vertices)
			if tf_count == 0:
				return

			self.batch.add(tf_count, gl.GL_TRIANGLES, layer,
			               ('v2f', tf_vertices),
			               ('c4f', [color.r, color.g, color.b, 1.0] * (tf_count)))

	def DrawSolidTriangleStrip(self, layer_index, vertices, color):
		layer = self.get_or_create_layer(layer_index)
		ts_count, ts_vertices = self.triangle_strip(vertices)

		self.batch.add(ts_count, gl.GL_TRIANGLES, layer,
		               ('v2f', ts_vertices),
		               ('c4f', [color.r, color.g, color.b, 1.0] * (ts_count)))

	def DrawIndexedTriangles(self, layer_index, vertices, indices, color):
		layer = self.get_or_create_layer(layer_index)
		count, vertex_arr = self.vertex_array(vertices)
		self.batch.add_indexed(count, gl.GL_TRIANGLES, layer,
		                       indices,
		                       ('v2f', vertex_arr),
		                       ('c4f', self.c4f_arr(color) * count))

	def DrawGradientRect(self, layer_index, vertices, color1, color2):
		"""
		Draw a rectangle fading from one color to another
		"""
		layer = self.get_or_create_layer(layer_index)
		count, vertices = self.vertex_array(vertices)
		self.batch.add_indexed(4, gl.GL_TRIANGLES, layer,
		                       [0, 1, 2, 0, 2, 3],
		                       ('v2f', vertices),
		                       ('c4f', self.c4f_arr(color1) * 2 + self.c4f_arr(color2) * 2))

	def DrawGradientCirc(self, layer_index, center, radius, color_mid, color_out):
		"""
		Draw a circle fading from a center color color to a border color
		"""
		layer = self.get_or_create_layer(layer_index)
		tf_vertices, unused = self.getCircleVertices(center, radius, self.circle_segments)
		tf_count = len(tf_vertices) // 2
		tri_color = self.c4f_arr(color_mid) + self.c4f_arr(color_out) * 2

		self.batch.add(tf_count, gl.GL_TRIANGLES, layer,
		               ('v2f', tf_vertices),
		               ('c4f', tri_color * (tf_count // 3)))

	def DrawGradientArc(self, layer_index, center, radius, angle_start, angle_end, color_mid, color_out):
		layer = self.get_or_create_layer(layer_index)
		tf_count, tf_vertices = self.getArcVertices(center, radius, angle_start, angle_end)
		tri_color = self.c4f_arr(color_mid) + self.c4f_arr(color_out) * 2

		self.batch.add(tf_count, gl.GL_TRIANGLES, layer,
		               ('v2f', tf_vertices),
		               ('c4f', tri_color * (tf_count // 3)))

	def DrawSegment(self, layer_index, p1, p2, color):
		"""
		Draw the line segment from p1-p2 with the specified color.
		"""
		layer = self.get_or_create_layer(layer_index)
		self.batch.add(2, gl.GL_LINES, layer,
		               ('v2f', (p1[0], p1[1], p2[0], p2[1])),
		               ('c3f', [color.r, color.g, color.b] * 2))

	def DrawXForm(self, layer_index, xf):
		"""
		Draw the transform xf on the screen
		"""
		layer = self.get_or_create_layer(layer_index)
		p1 = xf.position
		k_axisScale = 0.4
		p2 = p1 + k_axisScale * xf.R.x_axis
		p3 = p1 + k_axisScale * xf.R.y_axis

		self.batch.add(3, gl.GL_LINES, layer,
		               ('v2f', (p1[0], p1[1], p2[0], p2[
			               1], p1[0], p1[1], p3[0], p3[1])),
		               ('c3f', [1.0, 0.0, 0.0] * 2 + [0.0, 1.0, 0.0] * 2))

	def DrawPoint(self, layer_index, p, size, color):
		"""
		Draw a single point at point p given a point size and color.
		"""
		self.batch.add(1, gl.GL_POINTS, grPointSize(size),
		               ('v2f', (p[0], p[1])),
		               ('c3f', [color.r, color.g, color.b]))

	def DrawAABB(self, layer_index, aabb, color):
		"""
		Draw a wireframe around the AABB with the given color.
		"""
		layer = self.get_or_create_layer(layer_index)
		self.batch.add(8, gl.GL_LINES, layer,
		               ('v2f', (aabb.lowerBound.x, aabb.lowerBound.y,
		                        aabb.upperBound.x, aabb.lowerBound.y,
		                        aabb.upperBound.x, aabb.lowerBound.y,
		                        aabb.upperBound.x, aabb.upperBound.y,
		                        aabb.upperBound.x, aabb.upperBound.y,
		                        aabb.lowerBound.x, aabb.upperBound.y,
		                        aabb.lowerBound.x, aabb.upperBound.y,
		                        aabb.lowerBound.x, aabb.lowerBound.y)),
		               ('c3f', [color.r, color.g, color.b] * 8))

	def DrawText(self, layer_index, text: str, pos: b2Vec2, font_name: str, font_size: int):
		layer = self.get_or_create_layer(layer_index, is_text= True)
		pos = self.to_screen(pos)
		layer.pos = pos
		pyglet.text.Label(text,
		                  font_name=font_name,
		                  font_size=font_size,
		                  x=pos.x, y=pos.y,
		                  anchor_x='center',
		                  anchor_y='center',
		                  batch=self.batch,
		                  group=layer)

	def to_screen(self, point):
		"""
		Takes screen (x, y) and returns
		world coordinate b2Vec2(x,y).
		"""
		ratio = float(self.window.width) / self.window.height
		extents = b2Vec2(ratio, 1.0)
		extents *= self.viewZoom

		lower = self._viewCenter - extents
		upper = self._viewCenter + extents

		u = float(point.x - lower.x) / (upper.x - lower.x)
		v = float(point.y - lower.y) / (upper.y - lower.y)

		return b2Vec2(
			u * self.window.width,
			v * self.window.height)
