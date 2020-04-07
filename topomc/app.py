import sys

# files
from common import yaml_open
import heightmap as hm
import marching_squares
import draw
import vectorize
import logging

try:
    from matplotlib import pyplot
    from scipy.ndimage import gaussian_filter1d
    import anvil
except ImportError as e:
    logging.critical("Main: Dependencies not installed")
    raise e

version = sys.version_info
if version.major == 2:
    logging.critical("Main: Unsupported Python version")
    sys.exit()
if version.major == 3 and version.minor < 7:
    logging.critical("Main: Unsupported Python version")
    sys.exit()

logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s', level=10)

def run(args):
    try:
        bounding_points = (x1, z1, x2, z2) = [int(x) for x in args[1:5]]
    except ValueError:
        logging.critical("App: no co-ordinates for world specified")
        return 1
    if x1 > x2 or z1 > z2:
        logging.critical("App: Invalid co-ordinates")
        return 1

    total_bound_chunks = (x2+1 - x1) * (z2+1 - z1)

    try:
        world = args[5]
    except IndexError:
        logging.info("No world found, using default")
        world = yaml_open.get("world")

    try:
        contour_interval = int(args[6])
    except IndexError:
        logging.info("None or invalid contour interval found, using default")
        contour_interval = yaml_open.get("contour_interval")

    contour_offset = yaml_open.get("contour_offset")

    heightmap = hm.Heightmap(world, *bounding_points)

    if not isinstance(contour_interval, int) \
    or not isinstance(contour_offset, int):
        logging.critical("App: Contour interval/offset must be an integer")

    marching_squares.square_march(heightmap, contour_interval)

    topodata = vectorize.Topodata(heightmap)
    scale = yaml_open.get("window_scale")
    smooth = yaml_open.get("smoothen")
    smoothness = yaml_open.get("smoothness")
    index = yaml_open.get("index")
    save_loc = yaml_open.get("pdf_save_location")
    if smooth and not smoothness:
        logging.critical("App: smoothness can not be zero if smoothing is enabled")
        sys.exit()
    if save_loc:
        if not save_loc.endswith(".pdf"):
            if save_loc.endswith("/"):
                save_loc = save_loc + "map.pdf"
            else:
                save_loc = save_loc + ".pdf"
    draw.draw(topodata, scale, smooth, smoothness, index, save_loc)
