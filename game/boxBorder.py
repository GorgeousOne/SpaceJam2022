from Box2D import b2World, b2Draw, b2Color


class BoxBorder:

	def __init__(self, world: b2World, size: float, thickness: float):
		self.size = size
		self.thickness = thickness
		self.fill = b2Color(255, 255, 255)
		self.body = world.CreateBody(position=(0, 0))

		self.body.CreateEdgeChain(
			[(0, 0),
			 (0, size),
			 (size, size),
			 (size, 0),
			 (0, 0)]
		)
		self.displayVertices = [
			(0, 0),
			(0 - thickness, 0 - thickness),
			(0, size),
			(0 - thickness, size + thickness),
			(size, size),
			(size + thickness, size + thickness),
			(size, 0),
			(size + thickness, 0 - thickness),
			(0, 0),
			(0 - thickness, 0 - thickness),
		]

	def display(self, renderer: b2Draw):
		# from custom pyglet framework
		renderer.DrawSolidTriangleStrip(self.displayVertices, self.fill)

		