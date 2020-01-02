#core
import sys

#dependencies
try:
    import pyglet
except:
    raise Exception("incorrect dependencies installed or are missing")

#files
import read_chunks

#marching squares algorithm for generating contour data
#TODO:
#linear interpolation
#line assembly and smoothing
def marching_squares(heightmap):
    data = []

    for y in range(len(heightmap) - 1):
        current_row = []

        for x in range(len(heightmap[0])- 1):
            current_element = []

            #find height values of 2x2 matrix in clockwise order
            case = (
                heightmap[y]    [x]    ,
                heightmap[y]    [x + 1],
                heightmap[y + 1][x + 1],
                heightmap[y + 1][x]
            )

            #return true if height thresholdq is met
            bitmap = list(map(lambda e: e == heightmap[y][x], case))

            #convert point differences to locations for drawing
            if bitmap[0] != bitmap[1]: current_element.append("top")
            if bitmap[1] != bitmap[2]: current_element.append("right")
            if bitmap[2] != bitmap[3]: current_element.append("bottom")
            if bitmap[3] != bitmap[0]: current_element.append("left")

            current_row.append(current_element)

        data.append(current_row)

    return data



#draw map using pyglet
def draw(data, scale = 20):

    #dict for translating strings to xy vaules
    translate = {
        "left": (-1, 0),
        "top": (0, 1),
        "right": (1, 0),
        "bottom": (0, -1),
    }

    #create canvas
    window = pyglet.window.Window(
        scale * 2 * len(data[0]),
        scale * 2 * len(data)
    )

    def draw_line(x1, x2, y1, y2):
        pyglet.graphics.draw(
            2, pyglet.gl.GL_LINES,
            ('v2i', (
                x1 * scale,
                y1 * scale,
                x2 * scale,
                y2 * scale)
            ))

    #for debugging only
    def draw_grid():
        for i in range(len(data[0])):
            draw_line(*[arg * 2 for arg in [i, i, 0, scale * len(data)]])

        for i in range(len(data)):
            draw_line(*[arg * 2 for arg in [0, scale * len(data[0]), i, i]])

    #window event loop here
    @window.event
    def on_draw():
        window.clear()

        #TODO: clean this shit up lol
        y = 0
        for row in data:
            x = 0
            for element in row:
                if element:
                    #translate string to tuple with co-ords
                    start = translate[element[0]]
                    end = translate[element[1]]

                    #position in list + tuple inside square + 1
                    draw_line(
                        x * 2  + start[0] + 1,
                        x * 2  + end[0]   + 1,
                        y * -2 + start[1] - 1 + len(data) * 2,
                        y * -2 + end[1]   - 1 + len(data) * 2
                    )

                x += 1

            y += 1

    pyglet.app.run()



if __name__ == "__main__":
    try:
        world = sys.argv[1]
    except:
        raise Exception("No world specified")

    try:
        args = sys.argv[2:6]
        args = [int(x) for x in args]
    except:
        args = [0, 0, 0, 0]

    heightmap = read_chunks.generate_heightmap(world, *args)
    data = marching_squares(heightmap)
    draw(data, 20)

    pass
