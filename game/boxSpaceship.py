from typing import Tuple, List

import numpy as np
from Box2D import (b2World, b2PolygonShape, b2FixtureDef, b2Draw, b2Color, b2Body, b2Vec2)

from logic.location import Location
from logic.pilotAction import PilotAction
from logic.spaceshipPilot import SpaceshipPilot


class BoxSpaceship:

	def __init__(self, world: b2World, pilot: SpaceshipPilot, health: int, pos: Tuple[float, float] = (0, 0), color: b2Color = b2Color(1., 1., 1.)):
		self.pilot = pilot
		self.health = health
		self.energy = 0

		self.color = b2Color(color)
		self.shape = b2PolygonShape(vertices=[
			(2.618, 0),
			(0, -1),
			(-1, 0),
			(0, 1),
		])
		self.body = world.CreateDynamicBody(
			userData=self,  # adds a reference on the body to the spaceship object
			position=pos,
			linearDamping=0,
			shapes=[self.shape],
			shapeFixture=b2FixtureDef(
				restitution = 0.2, # bounciness between 0 and 1
				# density= 1.0
			),
			fixedRotation=True # fixes angular velocity to one value
		)

	def update(self, new_energy) -> PilotAction:
		self.energy = new_energy
		return self.pilot.update(self.get_location(), self.health, self.energy)

	def process_scan(self, current_action: PilotAction, located_rockets: List[Location]) -> PilotAction:
		return self.pilot.process_scan(current_action, located_rockets)

	def move(self, impulse: b2Vec2):
		# self.body.angle = np.arctan2(impulse.y, impulse.x)
		self.body.linearVelocity += impulse
		if self.body.linearVelocity.y != 0 or self.body.linearVelocity.x != 0:
			self.body.angle = np.arctan2(self.body.linearVelocity.y, self.body.linearVelocity.x)

	def damage(self, amount: int):
		self.health -= amount
		if self.health <= 0:
			self.color = b2Color(255, 0, 0)

	def get_location(self):
		pos = self.body.position
		vel = self.body.linearVelocity
		return Location(np.array([pos.x, pos.y]), self.body.angle, np.array([vel.x, vel.y]))

	def display(self, renderer: b2Draw):
		# self.body.angle = np.arctan2(self.body.linearVelocity.y, self.body.linearVelocity.x)
		vertices = []

		for v in self.shape.vertices:
			vertices.append(self.body.GetWorldPoint(v))
		renderer.DrawSolidPolygon(vertices, self.color)
