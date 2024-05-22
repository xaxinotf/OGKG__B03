import tkinter as tk
import numpy as np
import itertools


class PolygonApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=800, bg="white")
        self.canvas.pack()
        self.points = []

        self.generate_button = tk.Button(root, text="Generate 10 Random Points", command=self.generate_points)
        self.generate_button.pack(side=tk.LEFT)

        self.num_points_label = tk.Label(root, text="Number of Points:")
        self.num_points_label.pack(side=tk.LEFT)
        self.num_points_entry = tk.Entry(root, width=5)
        self.num_points_entry.pack(side=tk.LEFT)
        self.generate_custom_button = tk.Button(root, text="Generate Custom Points",
                                                command=self.generate_custom_points)
        self.generate_custom_button.pack(side=tk.LEFT)

        self.draw_button = tk.Button(root, text="Draw Polygon", command=self.draw_polygon)
        self.draw_button.pack(side=tk.LEFT)
        self.clear_button = tk.Button(root, text="Clear Points", command=self.clear_points)
        self.clear_button.pack(side=tk.LEFT)

        self.canvas.bind("<Button-1>", self.add_point)

    def generate_points(self):
        self.points = [(np.random.randint(50, 750), np.random.randint(50, 750)) for _ in range(10)]
        self.draw_points()

    def generate_custom_points(self):
        try:
            num_points = int(self.num_points_entry.get())
            self.points = [(np.random.randint(50, 750), np.random.randint(50, 750)) for _ in range(num_points)]
            self.draw_points()
        except ValueError:
            pass

    def add_point(self, event):
        self.points.append((event.x, event.y))
        self.draw_points()

    def clear_points(self):
        self.points = []
        self.canvas.delete("all")

    def draw_points(self):
        self.canvas.delete("all")
        for point in self.points:
            self.canvas.create_oval(point[0] - 2, point[1] - 2, point[0] + 2, point[1] + 2, fill='black')

    def draw_polygon(self):
        if len(self.points) < 3:
            return

        points = np.array(self.points)
        hull = self.smallest_enclosing_polygon(points)

        self.canvas.delete("all")
        self.draw_points()

        for i in range(len(hull)):
            x1, y1 = hull[i]
            x2, y2 = hull[(i + 1) % len(hull)]
            self.canvas.create_line(x1, y1, x2, y2, fill='black')

    def smallest_enclosing_polygon(self, points):
        min_area = float('inf')
        best_hull = None
        for perm in itertools.permutations(points):
            if self.is_simple_polygon(perm):
                area = self.polygon_area(perm)
                if area < min_area:
                    min_area = area
                    best_hull = perm
        return best_hull

    def is_simple_polygon(self, points):
        for i in range(len(points)):
            for j in range(i + 2, len(points)):
                if i == 0 and j == len(points) - 1:
                    continue
                if self.lines_intersect(points[i], points[(i + 1) % len(points)], points[j],
                                        points[(j + 1) % len(points)]):
                    return False
        return True

    def lines_intersect(self, p1, p2, p3, p4):
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

    def polygon_area(self, points):
        n = len(points)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += points[i][0] * points[j][1]
            area -= points[j][0] * points[i][1]
        area = abs(area) / 2.0
        return area


root = tk.Tk()
app = PolygonApp(root)
root.mainloop()
