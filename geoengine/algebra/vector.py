from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(slots=True, frozen=True)
class Vector3D:
    x: float
    y: float
    z: float

    def __repr__(self) -> str:
        return f"Vector3D({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector3D):
            return False
        return (
            math.isclose(self.x, other.x, abs_tol=1e-9)
            and math.isclose(self.y, other.y, abs_tol=1e-9)
            and math.isclose(self.z, other.z, abs_tol=1e-9)
        )

    def __add__(self, other: Vector3D) -> Vector3D:
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3D) -> Vector3D:
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> Vector3D:
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float) -> Vector3D:
        return self * scalar

    def __truediv__(self, scalar: float) -> Vector3D:
        if math.isclose(scalar, 0.0):
            raise ValueError("No se puede dividir un vector por cero.")
        return Vector3D(self.x / scalar, self.y / scalar, self.z / scalar)

    def __neg__(self) -> Vector3D:
        return Vector3D(-self.x, -self.y, -self.z)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def to_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def norm(self) -> float:
        return math.sqrt(self.norm_squared())

    def norm_squared(self) -> float:
        return self.x**2 + self.y**2 + self.z**2

    def normalized(self) -> Vector3D:
        magnitude = self.norm()
        if math.isclose(magnitude, 0.0):
            raise ValueError("No se puede normalizar el vector nulo.")
        return self / magnitude

    def dot(self, other: Vector3D) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector3D) -> Vector3D:
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def distance_to(self, other: Vector3D) -> float:
        return (self - other).norm()

    def angle_to(self, other: Vector3D) -> float:
        denominator = self.norm() * other.norm()
        if math.isclose(denominator, 0.0):
            raise ValueError("No se puede calcular un angulo con el vector nulo.")
        cosine = max(-1.0, min(1.0, self.dot(other) / denominator))
        return math.acos(cosine)

    def lerp(self, other: Vector3D, t: float) -> Vector3D:
        return self + (other - self) * t

    @staticmethod
    def zero() -> Vector3D:
        return Vector3D(0.0, 0.0, 0.0)

    @staticmethod
    def unit_x() -> Vector3D:
        return Vector3D(1.0, 0.0, 0.0)

    @staticmethod
    def unit_y() -> Vector3D:
        return Vector3D(0.0, 1.0, 0.0)

    @staticmethod
    def unit_z() -> Vector3D:
        return Vector3D(0.0, 0.0, 1.0)
