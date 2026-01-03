import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
from matplotlib.lines import Line2D

COLOR_MAP = {
    "residential": "#4C72B0",
    "kitchen": "#DD8452",
    "sanitary": "#55A868",
    "common": "#8172B2"
}

LABEL_MAP = {
    "residential": "Residential",
    "kitchen": "Kitchen",
    "sanitary": "Sanitary",
    "common": "Common space"
}


def plot_layout(area, containers, title="Container layout", grid_step=0.5):
    fig, ax = plt.subplots()

    # rysowanie Area - na razie tylko prostokąt
    xs = [p[0] for p in area.polygon]
    ys = [p[1] for p in area.polygon]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    width = max_x - min_x
    height = max_y - min_y

    area_rect = Rectangle(
        (min_x, min_y),
        width,
        height,
        fill=False,
        edgecolor="black",
        linewidth=2
    )
    ax.add_patch(area_rect)

    # siatka pod spodem
    grid_color = "#dddddd"
    grid_alpha = 0.35

    x = min_x
    while x <= max_x:
        line = Line2D([x, x], [min_y, max_y],
                      color=grid_color, linewidth=0.8, alpha=grid_alpha)
        line.set_clip_path(area_rect)
        ax.add_line(line)
        x += grid_step

    y = min_y
    while y <= max_y:
        line = Line2D([min_x, max_x], [y, y],
                      color=grid_color, linewidth=0.8, alpha=grid_alpha)
        line.set_clip_path(area_rect)
        ax.add_line(line)
        y += grid_step

    # rysowanie kontenerów
    for c in containers:
        poly = Polygon(
            c.polygon(),
            closed=True,
            facecolor=COLOR_MAP[c.type.value],
            edgecolor="black",
            alpha=0.85
        )
        ax.add_patch(poly)

    """ #adds numbers on the containers
        cx, cy = c.center()
        ax.text(
            cx, cy, str(c.id), 
            color='white', 
            weight='bold', 
            ha='center', 
            va='center', 
            fontsize=8
        )
    """
    #legenda
    legend_elements = [
        Rectangle((0, 0), 1, 1,
                  facecolor=COLOR_MAP[key],
                  edgecolor="black",
                  label=LABEL_MAP[key])
        for key in COLOR_MAP
    ]

    ax.legend(
        handles=legend_elements,
        loc="lower left",
        bbox_to_anchor=(1.02, 1),
        frameon=False,
        title="Container types"
    )

    ax.set_aspect("equal")
    ax.set_xlim(min_x - 0.5, max_x + 0.5)
    ax.set_ylim(min_y - 0.5, max_y + 0.5)
    ax.set_title(title)

    ax.axis("off")

    plt.show()
