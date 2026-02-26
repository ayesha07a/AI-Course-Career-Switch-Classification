# task1
import math
import random
ALPHA = 1000
BETA = 2
GAMMA = 1


block_info = [("ALU", 5, 5), ("Cache", 7, 4), ("CtrlUnit", 4, 4), ("RegFile", 6, 6), ("Decoder", 5, 3), ("FloatUnit", 5, 5)]
wires = [(3, 0), (2, 0), (0, 1), (3, 5), (1, 4), (4, 5)]

layouts_task1 = {
    "P1": [(9, 3), (12, 15), (13, 16), (1, 13), (4, 15), (9, 6)],
    "P2": [(8, 0), (7, 12), (4, 11), (1, 13), (14, 10), (9, 11)],
    "P3": [(6, 5), (12, 9), (9, 7), (8, 6), (2, 7), (3, 1)],
    "P4": [(3, 11), (11, 12), (14, 11), (6, 10), (3, 11), (3, 0)],
    "P5": [(10, 12), (8, 16), (10, 4), (13, 6), (6, 0), (3, 7)],
    "P6": [(0, 2), (0, 0), (14, 12), (4, 5), (12, 4), (3, 10)]
}

def midpoint(x, y, w, h):
    return x + w / 2.0, y + h / 2.0

def distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx * dx + dy * dy)

def check_overlap(design):
    count = 0
    for i in range(len(design)):
        x1, y1 = design[i]
        w1, h1 = block_info[i][1], block_info[i][2]
        for j in range(i + 1, len(design)):
            x2, y2 = design[j]
            w2, h2 = block_info[j][1], block_info[j][2]
            if not (x1 + w1 <= x2 or x1 >= x2 + w2 or y1 + h1 <= y2 or y1 >= y2 + h2):
                count += 1
    return count

def total_wire_length(design):
    acc = 0.0
    for i, j in wires:
        x1, y1 = design[i]
        x2, y2 = design[j]
        w1, h1 = block_info[i][1], block_info[i][2]
        w2, h2 = block_info[j][1], block_info[j][2]
        c1 = midpoint(x1, y1, w1, h1)
        c2 = midpoint(x2, y2, w2, h2)
        acc += distance(c1, c2)
    return acc

def bounding_area(design):
    min_x, min_y = 9999, 9999
    max_x, max_y = -1, -1
    for i in range(len(design)):
        x, y = design[i]
        w, h = block_info[i][1], block_info[i][2]
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x + w)
        max_y = max(max_y, y + h)
    return (max_x - min_x) * (max_y - min_y)

def score_layout(design):
    ov = check_overlap(design)
    wl = total_wire_length(design)
    area = bounding_area(design)
    fitness = - (ALPHA * ov + BETA * wl + GAMMA * area)
    return ov, wl, area, fitness


for key in sorted(layouts_task1.keys()):
    ov, wl, ar, fit = score_layout(layouts_task1[key])
    print(f"\n{key} → {', '.join(str(pos) for pos in layouts_task1[key])}")
    print(f"Pairwise block overlap count = {ov}")
    print(f"Total wiring distance (center-to-center) of the specified connected pairs = {round(wl, 2)}")
    print(f"Total bounding box area = {ar}")
    print(f"Total fitness value = - ({ALPHA} * {ov}) - ({BETA} * {round(wl, 2)}) - ({GAMMA} * {ar}) = {round(fit, 2)}")
    print(f"Fitness for generation 1 chromosome {key[-1]} = {round(fit, 2)}")


# task2
blocks = block_info  
connections = wires

def get_center(x, y, w, h):
    return x + w / 2.0, y + h / 2.0

def dist(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def overlap_check(layout):
    count = 0
    for i in range(len(layout)):
        x1, y1 = layout[i]
        w1, h1 = blocks[i][1], blocks[i][2]
        for j in range(i + 1, len(layout)):
            x2, y2 = layout[j]
            w2, h2 = blocks[j][1], blocks[j][2]
            if not (x1 + w1 <= x2 or x1 >= x2 + w2 or y1 + h1 <= y2 or y1 >= y2 + h2):
                count += 1
    return count

def total_wires(layout):
    total = 0.0
    for a, b in connections:
        x1, y1 = layout[a]
        x2, y2 = layout[b]
        w1, h1 = blocks[a][1], blocks[a][2]
        w2, h2 = blocks[b][1], blocks[b][2]
        c1 = get_center(x1, y1, w1, h1)
        c2 = get_center(x2, y2, w2, h2)
        total += dist(c1, c2)
    return total

def bound_area(layout):
    x_min, y_min = 9999, 9999
    x_max, y_max = -1, -1
    for i in range(len(layout)):
        x, y = layout[i]
        w, h = blocks[i][1], blocks[i][2]
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        x_max = max(x_max, x + w)
        y_max = max(y_max, y + h)
    return (x_max - x_min) * (y_max - y_min)

def fitness_score(layout):
    ov = overlap_check(layout)
    wires = total_wires(layout)
    area = bound_area(layout)
    score = - (ALPHA * ov + BETA * wires + GAMMA * area)
    return ov, wires, area, score

def two_point_crossover(p1, p2):
    i = random.randint(0, 4)
    j = random.randint(i + 1, 5)
    child1 = p1[:i] + p2[i:j] + p1[j:]
    child2 = p2[:i] + p1[i:j] + p2[j:]
    return child1, child2



parent1 = layouts_task1["P1"]
parent2 = layouts_task1["P2"]
child1, child2 = two_point_crossover(parent1, parent2)


child_list = [child1, child2]
child_names = ["First Child", "Second Child"]

for index in range(2):
    layout = child_list[index]
    ov = overlap_check(layout)
    wl = total_wires(layout)
    ar = bound_area(layout)
    fit = - (ALPHA * ov + BETA * wl + GAMMA * ar)

    print(f"\n{child_names[index]} Result:")
    print("  Pairwise block overlap count        :", ov)
    print("  Total Wire Length    :", round(wl, 2))
    print("  Bounding Box Area    :", ar)
    print(f"  Total fitness value     : - ({ALPHA} * {ov}) - ({BETA} * {round(wl, 2)}) - ({GAMMA} * {ar})")
    print("  Final Fitness Score  :", round(fit, 2))

    