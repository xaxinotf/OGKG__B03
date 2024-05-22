import random
import matplotlib.pyplot as plt
import networkx as nx
from scipy.spatial import Delaunay
from matplotlib.widgets import Button, TextBox

# Ініціалізація глобальних змінних
points = []
tri = None
mst = None

# Функція для генерації випадкових точок
def generate_random_points(num_points, x_max, y_max):
    return [(random.uniform(0, x_max), random.uniform(0, y_max)) for _ in range(num_points)]

# Функція для побудови тріангуляції Делоне
def delaunay_triangulation(points):
    return Delaunay(points)

# Функція для створення графа та зважування ребер
def create_graph_from_triangulation(tri):
    G = nx.Graph()
    for simplex in tri.simplices:
        for i in range(3):
            for j in range(i + 1, 3):
                p1, p2 = simplex[i], simplex[j]
                area = triangle_area(tri.points[p1], tri.points[p2], tri.points[simplex[3-i-j]])
                G.add_edge(p1, p2, weight=area)
    return G

# Функція для обчислення площі трикутника
def triangle_area(a, b, c):
    return 0.5 * abs((a[0] - c[0]) * (b[1] - a[1]) - (a[0] - b[0]) * (c[1] - a[1]))

# Функція для знаходження MST
def minimum_spanning_tree(G):
    return nx.minimum_spanning_tree(G, weight='weight')

# Функція для обробки подій миші
def onclick(event):
    if event.inaxes:
        points.append((event.xdata, event.ydata))
        ax.plot(event.xdata, event.ydata, 'o')
        plt.draw()

# Функція для додавання точок вручну
def submit(text):
    try:
        x, y = map(float, text.split(','))
        points.append((x, y))
        ax.plot(x, y, 'o')
        plt.draw()
    except ValueError:
        print("Будь ласка, введіть координати у форматі 'x, y'.")

# Функція для генерації та візуалізації многокутника
def generate_polygon(event):
    global tri, mst
    if len(points) < 3:
        print("Потрібно щонайменше 3 точки для побудови многокутника.")
        return
    tri = delaunay_triangulation(points)
    G = create_graph_from_triangulation(tri)
    mst = minimum_spanning_tree(G)
    plot_mst(points, mst)

# Функція для побудови та візуалізації MST
def plot_mst(points, mst):
    ax.clear()
    x, y = zip(*points)
    ax.plot(x, y, 'o')
    for edge in mst.edges(data=True):
        p1, p2 = edge[0], edge[1]
        ax.plot([points[p1][0], points[p2][0]], [points[p1][1], points[p2][1]], 'r')
    plt.draw()

# Ініціалізація графічного інтерфейсу
fig, ax = plt.subplots()
ax.set_title('Click to add points, or enter coordinates (x, y) and press "Submit"')
cid = fig.canvas.mpl_connect('button_press_event', onclick)

# Кнопка для генерації многокутника
ax_button = plt.axes([0.8, 0.05, 0.1, 0.075])
btn = Button(ax_button, 'Generate')
btn.on_clicked(generate_polygon)

# Поле для введення координат
axbox = plt.axes([0.1, 0.05, 0.65, 0.075])
text_box = TextBox(axbox, 'Enter point (x, y): ')
text_box.on_submit(submit)

plt.show()
