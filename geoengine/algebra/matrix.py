from __future__ import annotations

from dataclasses import dataclass
import math

from geoengine.algebra.vector import Vector3D


@dataclass(slots=True, frozen=True)
class Matrix3x3:
    data: tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]

    def __init__(self, data: list[list[float]] | tuple[tuple[float, float, float], ...]) -> None:
        if len(data) != 3 or any(len(row) != 3 for row in data):
            raise ValueError("Matrix3x3 requiere una estructura de 3x3.")
        normalized = tuple(tuple(float(value) for value in row) for row in data)
        object.__setattr__(self, "data", normalized)

    def __repr__(self) -> str:
        return f"Matrix3x3({self.data!r})"

    def __mul__(self, other: Matrix3x3 | Vector3D | float) -> Matrix3x3 | Vector3D:
        if isinstance(other, Vector3D):
            values = other.to_tuple()
            return Vector3D(
                sum(self.data[0][column] * values[column] for column in range(3)),
                sum(self.data[1][column] * values[column] for column in range(3)),
                sum(self.data[2][column] * values[column] for column in range(3)),
            )

        if isinstance(other, Matrix3x3):
            rows = []
            for row in range(3):
                rows.append(
                    [
                        sum(self.data[row][k] * other.data[k][column] for k in range(3))
                        for column in range(3)
                    ]
                )
            return Matrix3x3(rows)

        if isinstance(other, (int, float)):
            return Matrix3x3([[value * other for value in row] for row in self.data])

        return NotImplemented

    def __rmul__(self, scalar: float) -> Matrix3x3:
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return self * scalar

    def transpose(self) -> Matrix3x3:
        return Matrix3x3([[self.data[column][row] for column in range(3)] for row in range(3)])

    def determinant(self) -> float:
        a, b, c = self.data[0]
        d, e, f = self.data[1]
        g, h, i = self.data[2]
        return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)

    def inverse(self) -> Matrix3x3:
        det = self.determinant()
        if math.isclose(det, 0.0):
            raise ValueError("La matriz no es invertible.")
        a, b, c = self.data[0]
        d, e, f = self.data[1]
        g, h, i = self.data[2]
        cofactors = [
            [e * i - f * h, -(d * i - f * g), d * h - e * g],
            [-(b * i - c * h), a * i - c * g, -(a * h - b * g)],
            [b * f - c * e, -(a * f - c * d), a * e - b * d],
        ]
        return (1.0 / det) * Matrix3x3(cofactors).transpose()

    def apply_to_points(self, points: list[Vector3D]) -> list[Vector3D]:
        return [self * point for point in points]

    @staticmethod
    def identity() -> Matrix3x3:
        return Matrix3x3(((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)))

    @staticmethod
    def scale(sx: float, sy: float, sz: float) -> Matrix3x3:
        return Matrix3x3(((sx, 0.0, 0.0), (0.0, sy, 0.0), (0.0, 0.0, sz)))

    @staticmethod
    def shear_xy(kx: float, ky: float) -> Matrix3x3:
        return Matrix3x3(((1.0, kx, 0.0), (ky, 1.0, 0.0), (0.0, 0.0, 1.0)))

    @staticmethod
    def rotation_x(angle_rad: float) -> Matrix3x3:
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        return Matrix3x3(((1.0, 0.0, 0.0), (0.0, c, -s), (0.0, s, c)))

    @staticmethod
    def rotation_y(angle_rad: float) -> Matrix3x3:
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        return Matrix3x3(((c, 0.0, s), (0.0, 1.0, 0.0), (-s, 0.0, c)))

    @staticmethod
    def rotation_z(angle_rad: float) -> Matrix3x3:
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        return Matrix3x3(((c, -s, 0.0), (s, c, 0.0), (0.0, 0.0, 1.0)))

    @staticmethod
    def from_euler(rx: float, ry: float, rz: float) -> Matrix3x3:
        return Matrix3x3.rotation_z(rz) * Matrix3x3.rotation_y(ry) * Matrix3x3.rotation_x(rx)
