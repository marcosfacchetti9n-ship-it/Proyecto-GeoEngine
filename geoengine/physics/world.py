from __future__ import annotations

from dataclasses import dataclass
import math

from geoengine.algebra.vector import Vector3D
from geoengine.physics.particle import Particle


@dataclass(slots=True, frozen=True)
class SimulationSnapshot:
    total_energy: float
    total_momentum: Vector3D
    particle_count: int


class World:
    def __init__(
        self,
        gravity: Vector3D | None = None,
        floor_y: float = -2.8,
        bounds_x: tuple[float, float] = (-4.5, 4.5),
    ) -> None:
        self.gravity = gravity if gravity is not None else Vector3D(0.0, -9.81, 0.0)
        self.floor_y = floor_y
        self.bounds_x = bounds_x
        self.particles: list[Particle] = []

    def add_particle(self, particle: Particle) -> None:
        self.particles.append(particle)

    def step(self, dt: float) -> None:
        for particle in self.particles:
            particle.apply_force(self.gravity * particle.mass)
            particle.integrate(dt)
            self._resolve_floor_collision(particle)
            self._resolve_wall_collision(particle)
        self.resolve_collisions()

    def snapshot(self) -> SimulationSnapshot:
        return SimulationSnapshot(
            total_energy=sum(particle.kinetic_energy() for particle in self.particles),
            total_momentum=self.total_momentum(),
            particle_count=len(self.particles),
        )

    def total_momentum(self) -> Vector3D:
        momentum = Vector3D.zero()
        for particle in self.particles:
            momentum = momentum + particle.momentum()
        return momentum

    def resolve_collisions(self) -> None:
        for index, first in enumerate(self.particles):
            for second in self.particles[index + 1 :]:
                self._resolve_pair(first, second)

    def _resolve_floor_collision(self, particle: Particle) -> None:
        if particle.position.y - particle.radius >= self.floor_y:
            return
        particle.position = Vector3D(particle.position.x, self.floor_y + particle.radius, particle.position.z)
        if particle.velocity.y < 0:
            particle.velocity = Vector3D(
                particle.velocity.x * 0.98,
                -particle.velocity.y * particle.restitution,
                particle.velocity.z * 0.98,
            )

    def _resolve_wall_collision(self, particle: Particle) -> None:
        left, right = self.bounds_x
        if particle.position.x - particle.radius < left:
            particle.position = Vector3D(left + particle.radius, particle.position.y, particle.position.z)
            particle.velocity = Vector3D(abs(particle.velocity.x) * particle.restitution, particle.velocity.y, particle.velocity.z)
        if particle.position.x + particle.radius > right:
            particle.position = Vector3D(right - particle.radius, particle.position.y, particle.position.z)
            particle.velocity = Vector3D(-abs(particle.velocity.x) * particle.restitution, particle.velocity.y, particle.velocity.z)

    def _resolve_pair(self, first: Particle, second: Particle) -> None:
        offset = second.position - first.position
        distance_sq = offset.norm_squared()
        min_distance = first.radius + second.radius
        if distance_sq >= min_distance**2:
            return

        if math.isclose(distance_sq, 0.0):
            normal = Vector3D.unit_x()
            distance = min_distance
        else:
            distance = math.sqrt(distance_sq)
            normal = offset / distance

        overlap = min_distance - distance
        correction = normal * (overlap / 2.0 + 1e-3)
        first.position = first.position - correction
        second.position = second.position + correction

        relative_velocity = second.velocity - first.velocity
        speed_along_normal = relative_velocity.dot(normal)
        if speed_along_normal > 0:
            return

        restitution = min(first.restitution, second.restitution)
        impulse_scale = -(1.0 + restitution) * speed_along_normal
        impulse_scale /= (1.0 / first.mass) + (1.0 / second.mass)
        impulse = normal * impulse_scale
        first.apply_impulse(-impulse)
        second.apply_impulse(impulse)
