import io
import click
import numpy as np
import skimage
from skimage import filters, data, io
from skimage.transform import resize
import vpype as vp
from shapely.geometry import LineString


@click.command('scribbletrace')
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    '--width', '-w', default=40
)
@vp.generator
def scribbletrace(filename, width, scribbletype):

    img = io.imread(filename, as_gray=True)

    output_width = width
    quantificationlevels = 4

    scale_factor = round(img.shape[0]/output_width)

    img = resize(img, (round(img.shape[0]/scale_factor),
                       round(img.shape[1]/scale_factor)), anti_aliasing=True)
    img_orig = img

    img_dy = skimage.filters.sobel_h(img, mask=img < 255)
    img_dx = skimage.filters.sobel_v(img, mask=img < 255)

    img = 1-img
    img = np.round(np.multiply(img, quantificationlevels - 1)) + 1

    randomness_vertex = 0.1  
    randomness_position = 0.5


    randomness_length = 1
    lc = vp.LineCollection()

    def rotate_origin(xy, radians):
        x, y = xy
        xx = x * np.cos(radians) + y * np.sin(radians)
        yy = -x * np.sin(radians) + y * np.cos(radians)
        return xx, yy

    def pixplot():
        for n in range(val):
            vert_x = np.multiply(np.array([-0.5, 0.5]), np.maximum(grad_mag*0.1, 1))

            vert_x = np.multiply(vert_x, np.random.uniform(1-randomness_length, 1+randomness_length, 1))
            vert_y = np.array([0, 0])

            vert_y = vert_y + np.random.uniform(-randomness_vertex, randomness_vertex, 2)
            vert_x = vert_x + np.random.uniform(-randomness_vertex, randomness_vertex, 2)
            # rotate line by gradient direction so that line is perpendicular to gradients
            p1 = rotate_origin([vert_x[0], vert_y[0]], alpha)
            p2 = rotate_origin([vert_x[1], vert_y[1]], alpha)

            vert_x = np.array([p1[0], p2[0]]) + c + \
                np.random.uniform(-randomness_position, +randomness_position)
            vert_y = np.array([p1[1], p2[1]]) + r + \
                np.random.uniform(-randomness_position, +randomness_position)
            lc.append(LineString(
                [(vert_x[0], vert_y[0]), (vert_x[1], vert_y[1])]))

    height, width = img.shape
    for c in range(width):
        for r in range(height):
            val = int(img[r, c])
            grad_direction = np.array([img_dx[r, c], img_dy[r, c]])
            alpha = np.arctan2(grad_direction[0], grad_direction[1])
            grad_mag = grad_direction[0]*grad_direction[0] + \
                grad_direction[1]*grad_direction[1]
            pixplot()
    return lc


scribbletrace.help_group = "Plugins"
