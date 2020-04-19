import numpy as np
from tqdm import tqdm

def build_barcode(reader, nb_frames, method, wide_methods):
    """"""
    colors = []
    for i, im in tqdm(enumerate(reader), total=nb_frames):
        if i> 300: break

        if method == 'mean':
            mean = np.mean(np.array(im), axis=0)
            colors.append(tuple(np.mean(mean, axis=0)))

        elif method == 'square_mean':
            square = np.square(np.array(im), dtype=np.float64)
            mean = np.mean(square, axis=0)
            mean = np.mean(mean, axis=0)
            colors.append(tuple(np.sqrt(mean)))

        elif method == 'median':
            median = np.median(np.array(im), axis=0)
            colors.append(tuple(np.median(median, axis=0)))

        elif method == 'x_wide':
            for ind in range(im.shape[1]):
                colors.append(np.array(im[:,ind,:]).astype(np.uint8))

        elif method == 'x_mean_wide':
            mean = np.mean(np.array(im), axis=0)
            for ind in range(mean.shape[0]):
                colors.append(tuple(mean[ind]))

    colors = np.array(colors)

    if method in wide_methods:
        np_colors = colors.reshape((colors.shape[0], colors.shape[1], 3)).astype(np.uint8)
        barcode = np.transpose(np_colors, axes=[1,0,2])

    else:
        np_colors = colors.reshape((1, len(colors), 3)).astype(np.uint8)
        barcode = np.vstack([np_colors] * (len(colors) // 3))

    return barcode
