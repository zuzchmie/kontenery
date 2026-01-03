import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

COLOR_MAP = {
    "residential": "#4C72B0", # Blue
    "kitchen": "#DD8452",     # Orange
    "sanitary": "#55A868",    # Green
    "common": "#8172B2"       # Purple
}

def plot_layout(area, containers, title="Layout", grid_step=0.5, global_angle=0):
    fig, ax = plt.subplots()
    area_patch = Polygon(area.polygon, closed=True, fill=False, edgecolor="black", linewidth=2)
    ax.add_patch(area_patch)
    for c in containers:
        # Get color based on the type
        # We use .value because c.type is an Enum member
        c_type_str = c.type.value 
        color = COLOR_MAP.get(c_type_str, "#808080")
        
        # Get the rotated coordinates from the container
        poly_coords = c.polygon(global_angle)
        
        # Create and add the polygon patch
        container_patch = Polygon(
            poly_coords, 
            closed=True, 
            facecolor=color, 
            edgecolor="black", 
            alpha=0.8,
            label=c_type_str # Useful for automatic legends
        )
        ax.add_patch(container_patch)

    # 3. Final plot styling
    ax.set_aspect("equal")
    xs, ys = zip(*area.polygon)
    ax.set_xlim(min(xs) - 1, max(xs) + 1)
    ax.set_ylim(min(ys) - 1, max(ys) + 1)
    ax.axis("off")
    plt.savefig("layout.png")