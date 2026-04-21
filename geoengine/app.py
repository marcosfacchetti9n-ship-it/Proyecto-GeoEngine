from __future__ import annotations

import math
import tkinter as tk
from tkinter import ttk

from geoengine.algebra.matrix import Matrix3x3
from geoengine.algebra.vector import Vector3D
from geoengine.rendering.projection import Projector
from geoengine.scenes import CUBE_EDGES, CUBE_VERTICES, build_demo_world


class TransformPanel(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=16)
        self.canvas = tk.Canvas(self, width=760, height=620, bg="#08111f", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        controls = ttk.Frame(self, padding=(18, 0, 0, 0))
        controls.grid(row=0, column=1, sticky="ns")

        self.rotation_x = tk.DoubleVar(value=24.0)
        self.rotation_y = tk.DoubleVar(value=32.0)
        self.rotation_z = tk.DoubleVar(value=4.0)
        self.scale = tk.DoubleVar(value=1.0)
        self.shear = tk.DoubleVar(value=0.15)
        self.auto_rotate = tk.BooleanVar(value=True)
        self._time = 0.0

        self._add_slider(controls, "Rotacion X", self.rotation_x, -180, 180)
        self._add_slider(controls, "Rotacion Y", self.rotation_y, -180, 180)
        self._add_slider(controls, "Rotacion Z", self.rotation_z, -180, 180)
        self._add_slider(controls, "Escala", self.scale, 0.4, 1.8)
        self._add_slider(controls, "Shear XY", self.shear, -0.8, 0.8)
        ttk.Checkbutton(controls, text="Rotacion automatica", variable=self.auto_rotate).pack(anchor="w", pady=(12, 18))

        ttk.Label(controls, text="Matriz activa", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.matrix_text = tk.Text(controls, width=28, height=10, bg="#111827", fg="#dbeafe", relief="flat", font=("Consolas", 10))
        self.matrix_text.pack(fill="x", pady=(8, 12))

        ttk.Label(
            controls,
            text="Esta escena resume algebra lineal visual: rotaciones 3D, escala, shear y proyeccion en perspectiva.",
            wraplength=230,
            justify="left",
        ).pack(anchor="w")

        self.after(16, self.animate)

    def _add_slider(self, parent: ttk.Frame, label: str, variable: tk.DoubleVar, start: float, end: float) -> None:
        ttk.Label(parent, text=label).pack(anchor="w")
        ttk.Scale(parent, from_=start, to=end, variable=variable, orient="horizontal", length=240).pack(anchor="w", pady=(0, 12))

    def _current_matrix(self) -> Matrix3x3:
        rotation = Matrix3x3.from_euler(
            math.radians(self.rotation_x.get()),
            math.radians(self.rotation_y.get()),
            math.radians(self.rotation_z.get()),
        )
        return rotation * Matrix3x3.shear_xy(self.shear.get(), self.shear.get() * 0.35) * Matrix3x3.scale(
            self.scale.get(),
            self.scale.get(),
            self.scale.get(),
        )

    def _draw_axis(self, projector: Projector, matrix: Matrix3x3, axis: Vector3D, label: str, color: str) -> None:
        start = projector.project(Vector3D.zero())
        end = projector.project(matrix * axis * 1.6)
        self.canvas.create_line(*start, *end, fill=color, width=3, arrow=tk.LAST)
        self.canvas.create_text(end[0] + 14, end[1], text=label, fill=color, font=("Segoe UI", 11, "bold"))

    def draw(self) -> None:
        self.canvas.delete("all")
        projector = Projector(width=760, height=620)
        matrix = self._current_matrix()
        transformed_vertices = matrix.apply_to_points(CUBE_VERTICES)

        self.canvas.create_text(18, 18, anchor="nw", fill="#dbeafe", font=("Segoe UI", 16, "bold"), text="Linear Transform Sandbox")
        self.canvas.create_text(18, 46, anchor="nw", fill="#93c5fd", font=("Segoe UI", 10), text="Cubo transformado + base canonica + vector proyectado.")

        for start_index, end_index in CUBE_EDGES:
            start = projector.project(transformed_vertices[start_index])
            end = projector.project(transformed_vertices[end_index])
            self.canvas.create_line(*start, *end, fill="#7dd3fc", width=2)

        self._draw_axis(projector, matrix, Vector3D.unit_x(), "e1", "#f97316")
        self._draw_axis(projector, matrix, Vector3D.unit_y(), "e2", "#22c55e")
        self._draw_axis(projector, matrix, Vector3D.unit_z(), "e3", "#a78bfa")

        vector_tip = projector.project(matrix * Vector3D(0.9, 1.2, 0.7))
        origin = projector.project(Vector3D.zero())
        self.canvas.create_line(*origin, *vector_tip, fill="#facc15", width=4, arrow=tk.LAST)
        self.canvas.create_text(vector_tip[0] + 16, vector_tip[1] - 8, text="v", fill="#fde68a", font=("Segoe UI", 11, "bold"))

        self.matrix_text.delete("1.0", tk.END)
        for row in matrix.data:
            self.matrix_text.insert(tk.END, "[" + "  ".join(f"{value: .3f}" for value in row) + "]\n")

    def animate(self) -> None:
        if self.auto_rotate.get():
            self._time += 0.025
            self.rotation_y.set((self.rotation_y.get() + 0.7) % 360)
            self.rotation_x.set(20 + math.sin(self._time * 0.8) * 18)
            self.rotation_z.set(math.cos(self._time * 0.45) * 18)
        self.draw()
        self.after(16, self.animate)


class PhysicsPanel(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=16)
        self.canvas = tk.Canvas(self, width=760, height=620, bg="#0f172a", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        controls = ttk.Frame(self, padding=(18, 0, 0, 0))
        controls.grid(row=0, column=1, sticky="ns")

        self.world = build_demo_world()
        self.running = tk.BooleanVar(value=True)
        self.energy_var = tk.StringVar()
        self.momentum_var = tk.StringVar()

        ttk.Checkbutton(controls, text="Simulacion en marcha", variable=self.running).pack(anchor="w", pady=(0, 14))
        ttk.Button(controls, text="Reiniciar escena", command=self._reset_world).pack(anchor="w", pady=(0, 18))
        ttk.Label(controls, textvariable=self.energy_var, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))
        ttk.Label(controls, textvariable=self.momentum_var, wraplength=230, justify="left").pack(anchor="w", pady=(0, 18))
        ttk.Label(
            controls,
            text="Choques resueltos por impulso con masas distintas, gravedad y limites laterales.",
            wraplength=230,
            justify="left",
        ).pack(anchor="w")

        self.after(16, self.animate)

    def _reset_world(self) -> None:
        self.world = build_demo_world()

    def _world_to_canvas(self, point: Vector3D) -> tuple[float, float]:
        scale = 72
        return (760 / 2 + point.x * scale, 620 - 110 - point.y * scale)

    def _draw_background(self) -> None:
        floor_y = self._world_to_canvas(Vector3D(0.0, self.world.floor_y, 0.0))[1]
        for x in range(0, 760, 48):
            self.canvas.create_line(x, 0, x, 620, fill="#13233f")
        for y in range(0, 620, 48):
            self.canvas.create_line(0, y, 760, y, fill="#13233f")
        self.canvas.create_rectangle(0, floor_y, 760, 620, fill="#1e293b", outline="")
        self.canvas.create_line(0, floor_y, 760, floor_y, fill="#94a3b8", width=3)

    def _draw_particles(self) -> None:
        scale = 72
        for particle in self.world.particles:
            x, y = self._world_to_canvas(particle.position)
            radius = particle.radius * scale
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=particle.color, outline="")
            self.canvas.create_text(x, y, fill="#020617", font=("Segoe UI", 10, "bold"), text=f"m={particle.mass:.1f}")

    def animate(self) -> None:
        if self.running.get():
            self.world.step(1 / 60)
        self.canvas.delete("all")
        self._draw_background()
        self._draw_particles()
        self.canvas.create_text(18, 18, anchor="nw", fill="#e2e8f0", font=("Segoe UI", 16, "bold"), text="Particle Dynamics Sandbox")
        self.canvas.create_text(18, 46, anchor="nw", fill="#93c5fd", font=("Segoe UI", 10), text="Rebote contra piso y paredes, energia y momento lineal.")

        snapshot = self.world.snapshot()
        self.energy_var.set(f"Energia cinetica total: {snapshot.total_energy:.3f}")
        self.momentum_var.set(
            f"Momento lineal total: ({snapshot.total_momentum.x:.3f}, {snapshot.total_momentum.y:.3f}, {snapshot.total_momentum.z:.3f})"
        )
        self.after(16, self.animate)


class GeoEngineApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("GeoEngine | Linear Algebra + Physics Sandbox")
        self.root.geometry("1120x720")
        self.root.configure(bg="#e5eef9")
        self._configure_style()

        hero = ttk.Frame(self.root, padding=(18, 14))
        hero.pack(fill="x")
        ttk.Label(hero, text="GeoEngine", style="Hero.TLabel").pack(anchor="w")
        ttk.Label(
            hero,
            text="Interactive geometry and physics sandbox built to showcase mathematical intuition in software.",
            style="Subhero.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        notebook.add(TransformPanel(notebook), text="Transformations")
        notebook.add(PhysicsPanel(notebook), text="Physics")

    def _configure_style(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#e5eef9")
        style.configure("TNotebook", background="#e5eef9", borderwidth=0)
        style.configure("TNotebook.Tab", padding=(16, 8), font=("Segoe UI", 10, "bold"))
        style.configure("TLabel", background="#e5eef9", foreground="#0f172a", font=("Segoe UI", 10))
        style.configure("Hero.TLabel", background="#e5eef9", foreground="#0f172a", font=("Segoe UI", 24, "bold"))
        style.configure("Subhero.TLabel", background="#e5eef9", foreground="#334155", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("TCheckbutton", background="#e5eef9", font=("Segoe UI", 10))

    def run(self) -> None:
        self.root.mainloop()


def launch_app() -> None:
    GeoEngineApp().run()
