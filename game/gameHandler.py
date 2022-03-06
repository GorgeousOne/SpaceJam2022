import math
import random

import numpy as np
from Box2D import b2Vec2, b2World, b2Color

from game.boxContactListener import BoxContactListener
from game.boxRocket import BoxRocket
from game.boxScan import BoxScan
from game.boxSpaceship import BoxSpaceship
from logic import scanning
from logic.pilotAction import PilotAction, ScanAction
from logic.spaceshipPilot import SpaceshipPilot
from util import colorParse


class GameHandler:

	def __init__(self, world: b2World, contact_handler: BoxContactListener, game_size: int, ticks_per_second: int):
		self.world = world
		self.contactHandler = contact_handler
		self.gameSize = game_size
		self.ticksPerSecond = ticks_per_second

		self.spaceshipHealth = 100
		self.spaceshipMaxEnergy = 100

		self.maxSpaceshipSpeedPerTick = 5
		self.energyPerTick = 10

		self.timePenaltyStart = 15 * self.ticksPerSecond
		self.timPenaltyDmg = 1

		self.rocketSpeed = 25
		self.scanSuccessColor = b2Color(1, .2, .2)
		self.scanFailColor = b2Color(1, 1, 1)
		self.spaceshipSpawnRange = self.gameSize * 0.4
		self.gameTick = 0

		self.rocketCost = 50
		self.accCostPerMeterSecondSq = 1
		self.scanCostPerMeterSq = 1

	def reset(self):
		self.gameTick = 0

	def spawn_spaceship(self, pilot: SpaceshipPilot):
		angle = random.uniform(-math.pi, math.pi)
		distance = self.spaceshipSpawnRange * math.acos(random.uniform(0, 1)) / math.pi
		pos = b2Vec2(
			self.gameSize / 2 + math.cos(angle) * distance,
			self.gameSize / 2 + math.sin(angle) * distance)

		ship_color = colorParse.rgb_to_b2color(colorParse.hex_to_rgb(pilot.shipColor))
		self.contactHandler.add_spaceship(BoxSpaceship(
			self.world,
			pilot,
			self.spaceshipHealth,
			self.spaceshipMaxEnergy,
			ship_color,
			pos,
			random.uniform(-math.pi, math.pi)))

	def update(self):
		if self.gameTick > self.timePenaltyStart:
			for spaceship in list(self.contactHandler.spaceships):
				self.contactHandler.damage_spaceship(spaceship, self.timPenaltyDmg)

		for spaceship in self.contactHandler.spaceships:
			spaceship.add_energy(self.energyPerTick)
			scan = spaceship.prepare_scan(self.gameTick, self.ticksPerSecond)
			located_spaceships = []

			if scan:
				located_spaceships = self.handle_pilot_scan(spaceship, scan)

			action = spaceship.update(self.gameTick, self.ticksPerSecond, located_spaceships)
			self.handle_pilot_action(spaceship, action)
		self.gameTick += 1

	def handle_pilot_action(self, spaceship: BoxSpaceship, action: PilotAction):
		if not action:
			return
		if action.acceleration is not None:
			self.handle_pilot_move(spaceship, action.acceleration)
		if action.shootAngle is not None:
			self.handle_pilot_shoot(spaceship, action.shootAngle)

	def handle_pilot_scan(self, spaceship: BoxSpaceship, scan: ScanAction):
		energy_cost = scanning.calc_scan_energy_cost(scan.angle, scan.distance)

		if energy_cost > spaceship.energy:
			return []
		# raise ValueError("Not enough energy to perform scan.")
		spaceship.use_energy(energy_cost)

		located_rockets = scanning.calc_located_spaceships(
			spaceship.get_location(self.ticksPerSecond),
			scan.direction,
			scan.distance,
			scan.angle,
			[other.get_location().position for other in self.contactHandler.spaceships if other != spaceship])

		if located_rockets:
			self.contactHandler.add_scan(BoxScan(
				spaceship.get_location(self.ticksPerSecond).get_position(),
				scan.direction,
				scan.distance,
				scan.angle,
				self.scanSuccessColor if located_rockets else self.scanFailColor))
		return located_rockets

	def handle_pilot_move(self, spaceship: BoxSpaceship, acceleration: np.ndarray):
		power = min(self.maxSpaceshipSpeedPerTick, np.linalg.norm(acceleration))
		energy_cost = power * self.accCostPerMeterSecondSq

		if energy_cost > spaceship.energy:
			return
		spaceship.use_energy(energy_cost)
		try:
			b2acc = b2Vec2(acceleration[0], acceleration[1])
			spaceship.move(b2acc, self.maxSpaceshipSpeedPerTick, self.ticksPerSecond)
		except TypeError as e:
			print("Could not move spaceship with: " + str(acceleration) + ". Is this really a float vector?")

	def handle_pilot_shoot(self, spaceship: BoxSpaceship, shoot_angle: float):
		if self.rocketCost > spaceship.energy:
			return
		spaceship.use_energy(self.rocketCost)
		direction = angle_to_b2vec(shoot_angle) * self.rocketSpeed
		self.contactHandler.add_rocket(BoxRocket(self.world, spaceship, direction))


def angle_to_b2vec(angle: float) -> b2Vec2:
	return b2Vec2(math.cos(angle), math.sin(angle))
