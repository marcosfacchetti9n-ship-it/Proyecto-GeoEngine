from __future__ import annotations

from dataclasses import dataclass, field

from geoengine.algebra.vector import Vector3D


@dataclass(slots=True)
class Particle:
    position: Vector3D
    velocity: Vector3D
    mass: float = 1.0
    radius: float = 0.35
    restitution: float = 0.92
    color: str = "#ff6b6b"
    force_accumulator: Vector3D = field(default_factory=Vector3D.zero)

    def __post_init__(self) -> None:
        if self.mass <= 0:
            raise ValueError("La masa debe ser positiva.")
        if self.radius <= 0:
            raise ValueError("El radio debe ser positivo.")

    @property
    def acceleration(self) -> Vector3D:
        return self.force_accumulator / self.mass

    def apply_force(self, force: Vector3D) -> None:
        self.force_accumulator = self.force_accumulator + force

    def apply_impulse(self, impulse: Vector3D) -> None:
        self.velocity = self.velocity + impulse / self.mass

    def integrate(self, dt: float) -> None:
        self.velocity = self.velocity + self.acceleration * dt
        self.position = self.position + self.velocity * dt
        self.force_accumulator = Vector3D.zero()

    def kinetic_energy(self) -> float:
        return 0.5 * self.mass * self.velocity.norm_squared()

    def momentum(self) -> Vector3D:
        return self.velocity * self.mass
