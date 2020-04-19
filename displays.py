import numpy as np
import PIL.Image as Image
from PIL.ImageDraw import Draw
from tqdm import tqdm


def build_final_product(barcode, display):
    """Converts barcode into another view if needed"""
    if display == 'circle':
        return rectangle_to_vinyle(barcode)

    elif display == 'barcode':
        return Image.fromarray(barcode)


def rectangle_to_vinyle(np_img):
    """Convert lines into circles, from left=in to right=out (7min/img)"""
    min_radius = np_img.shape[1] // 2
    max_radius = np_img.shape[1] + min_radius
    side_length = max_radius * 2

    pil_circle = Image.new('RGB', (side_length, side_length), color='white')
    drawer = Draw(pil_circle, mode='RGB')

    degree_step = 180.0 / np_img.shape[0]
    #angle is 0 at 3 o'clock, increasing clockwise
    get_angle = lambda x: 270 - x * degree_step

    for i, col in tqdm(enumerate(np.transpose(np_img, axes=[1,0,2])), total=np_img.shape[1]):
        x0 = side_length // 2 - min_radius - i
        x1 = side_length // 2 + min_radius + i

        for j, pixel in enumerate(col):
            drawer.arc([x0, x0, x1, x1], get_angle(j+1), get_angle(j), tuple(pixel), 2)
            drawer.arc([x0, x0, x1, x1], get_angle(-j), get_angle(-j-1), tuple(pixel), 2)

    return pil_circle
