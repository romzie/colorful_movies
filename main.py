import imageio
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

filename = "/media/shared/Aquaman.2018..MULTi.1080p.HDLight.x264.AC3-TOXIC.mkv"
filename = "/media/shared/Mad Max Fury Road 2015.mkv"
method = "mean_pixel_wide"

width = 1 if method == "mean_pixel_wide" else 640
height = 360
fps = 1

reader = imageio.get_reader(filename, size=(width, height), fps=fps)

def frame_wise(reader):
    """Process each frame globally (35min/360p)"""
    mean_colors = []
    square_mean_colors = []
    median_colors = []
    for i, im in tqdm(enumerate(reader)):
        mean = np.mean(np.array(im), axis=0)
        mean_colors.append(tuple(np.mean(mean, axis=0)))
        
        square = np.square(np.array(im), dtype=np.float64)
        mean = np.mean(square, axis=0)
        mean = np.mean(mean, axis=0)
        square_mean_colors.append(tuple(np.sqrt(mean)))

        median = np.median(np.array(im), axis=0)
        median_colors.append(tuple(np.median(median, axis=0)))
    methods = ['mean', 'square_mean', 'median']
    return [mean_colors, square_mean_colors, median_colors], methods

def mean_pixel_wide(reader):
    """Reduce frame to X pixel wide (15min/360p)"""
    mean_colors = []
    colors = []
    for i, im in tqdm(enumerate(reader)):
        colors.append(np.array(im).astype(np.uint8))
        mean = np.mean(np.array(im), axis=0)
        for ind in range(mean.shape[0]):
            mean_colors.append(tuple(mean[ind]))
    return [mean_colors, colors], ['mean_pixel_wide', 'pixel_wide']

colors_arr, method_used_arr = eval(method)(reader)
for colors, method_used in zip(colors_arr, method_used_arr):
    colors = np.array(colors)
    if method_used == 'pixel_wide':
        np_colors = colors.reshape((colors.shape[0], colors.shape[1], 3)).astype(np.uint8)
        result = np.transpose(np_colors, axes=[1,0,2])
    else:
        np_colors = colors.reshape((1, len(colors), 3)).astype(np.uint8)
        result = np.vstack([np_colors] * (len(colors) // 3))
    image_name = '{}_{}_{}_{}_{}.png'.format(os.path.basename(filename), method_used, fps, width, height)
    matplotlib.image.imsave(image_name, result)
