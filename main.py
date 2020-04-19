import imageio
import os
from tqdm import tqdm
import argparse

from methods import build_barcode
from displays import build_final_product


def main(args):
    wide_methods = ['x_wide', 'x_mean_wide']
    width = 1 if args.method in wide_methods else 640
    height = 360

    reader = imageio.get_reader(args.video_file, size=(width, height), fps=args.fps)
    nb_frames = (int(reader.get_meta_data()['duration']) + 1) * args.fps

    if args.method in wide_methods:
        height = nb_frames * width // 3
        reader = imageio.get_reader(args.video_file, size=(width, height), fps=args.fps)

    print('Number of frames to process:', nb_frames)

    barcode = build_barcode(reader, nb_frames, args.method, wide_methods)

    pil_result = build_final_product(barcode, args.display)

    image_name = '{}_{}_{}_{}_{}.png'.format(os.path.basename(args.video_file), args.fps, args.method, width, height)
    pil_result.save(os.path.join(args.out_folder, image_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--video_file', type=str, required=True)
    parser.add_argument('--out_folder', type=str, required=True)
    parser.add_argument('--method', type=str, default='x_wide', help='mean, square_mean, median, x_wide, x_mean_wide')
    parser.add_argument('--display', type=str, default='circle', help='barcode or circle')
    parser.add_argument('--fps', type=float, default=1, help='how many frames to process per sec')

    args = parser.parse_args()

    if args.display not in ['barcode', 'circle']:
        raise ValueError('Incorrect display style: {}'.format(args.display))
    elif args.method not in ['mean', 'square_mean', 'median', 'x_wide', 'x_mean_wide']:
        raise ValueError('Incorrect method: {}'.format(args.method))

    os.makedirs(args.out_folder, exist_ok=True)

    main(args)

