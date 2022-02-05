from Box2D import b2World, b2Draw, b2Color


class BoxBorder:

	def __init__(self, world: b2World, size: float, thickness: float):
		self.size = size
		self.thickness = thickness
		self.body = world.CreateBody(position=(0, 0))
		self.fill = b2Color(255, 255, 255)

		extent = size/2
		self.body.CreateEdgeChain(
			[(-extent, -extent),
			 (-extent, extent),
			 (extent, extent),
			 (extent, -extent),
			 (-extent, -extent)]
		)
		self.displayVertices = [
			(-extent, -extent),
			(-extent - thickness, -extent - thickness),
			(-extent, extent),
			(-extent - thickness, extent + thickness),
			(extent, extent),
			(extent + thickness, extent + thickness),
			(extent, -extent),
			(extent + thickness, -extent - thickness),
			(-extent, -extent),
			(-extent - thickness, -extent - thickness),
		]

	def display(self, renderer: b2Draw):
		# from custom pyglet framework
		renderer.DrawSolidTriangleStrip(self.displayVertices, self.fill)

		