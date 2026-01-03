import random
from container import Container, ContainerType, CONTAINER_SIZES
from area import Area
from plot_layouts import plot_layout

TYPE_WEIGHTS = {
    ContainerType.RESIDENTIAL: 0.5,
    ContainerType.KITCHEN: 0.2,
    ContainerType.SANITARY: 0.2,
    ContainerType.COMMON: 0.1
}


def rects_overlap(c1, c2):
    return not (
        c1.x + c1.width <= c2.x or
        c2.x + c2.width <= c1.x or
        c1.y + c1.height <= c2.y or
        c2.y + c2.height <= c1.y
    )


def generate_weighted_layout(area, spacing=0.1, step=0.1):
    xs = [p[0] for p in area.polygon]
    ys = [p[1] for p in area.polygon]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    containers = []
    cid = 1

    y = min_y + spacing
    while y <= max_y - spacing:
        x = min_x + spacing
        row_max_h = 0 # najwyszy container
        
        while x <= max_x - spacing:
            ctype = random.choices(list(TYPE_WEIGHTS.keys()), weights=list(TYPE_WEIGHTS.values()))[0]
            w, h = CONTAINER_SIZES[ctype.value]

            # odwrócenie container na 50%
            if random.random() > 0.5:
                w, h = h, w

            #sprawdzanie granic Area
            if x + w <= max_x - spacing and y + h <= max_y - spacing:
                new_c = Container(cid, ctype, x, y, w, h)

                #nakladanie sie
                if not any(rects_overlap(existing, new_c) for existing in containers):
                    containers.append(new_c)
                    cid += 1
                    x += w + spacing
                    row_max_h = max(row_max_h, h)
                    continue
            # przesuwanie minimalnie jeeli się nie zmieściło
            x += step
        y += (row_max_h + spacing) if row_max_h > 0 else step

    return containers

area = Area.rectangular(2, 2)
containers = generate_weighted_layout(area, spacing=0.1)
plot_layout(area, containers, "Containter layout")

