from os import path
from PIL import Image, ImageStat
import numpy as np


def get_image_matrix(filename, folder=None):
    # Open image and return the image and a numpy array (shape(h,w,3))
    if folder is None:
        folder = path.dirname(__file__)
    im = Image.open(path.join(folder, filename))
    return im, np.asarray(im)


def find_possible_tile_sizes(size, min_square=5):
    # find square lengths that divide the image in equally sized mosaic pieces
    height, width = size
    possible_tile_sizes = []
    for square_length in range(min_square, min(height, width)//2):
        if height % square_length == 0 and width % square_length == 0:
            possible_tile_sizes.append(square_length)
    return possible_tile_sizes


def get_closest(target, array):
    # get closest target number from a list of numbers
    array = np.asarray(array)
    idx = (np.abs(array - target)).argmin()
    return array[idx]


class Mosaic:
    def __init__(self, filename, tile_size):
        self.image, self.nparray = get_image_matrix(filename)
        possible_tile_sizes = find_possible_tile_sizes(self.image.size)
        if tile_size in possible_tile_sizes:
            self.tile_size = tile_size
        else:
            self.tile_size = get_closest(tile_size, possible_tile_sizes)

    def split(self):
        self.tiles = []
        for pos_y in range(0, self.image.size[1] - 1, self.tile_size):
            for pos_x in range(0, self.image.size[0] - 1, self.tile_size):
                tile_area = (pos_x, pos_y, pos_x + self.tile_size, pos_y + self.tile_size)
                tile_image = self.image.crop(tile_area)
                position = (pos_x, pos_y)
                tile = Tile(tile_image, position)
                self.tiles.append(tile)

    def build_mosaic(self):
        # rebuild image with modified tiles
        self.image = Image.new('RGB', self.image.size)
        for tile in self.tiles:
            tile.replace_tile()
            self.image.paste(tile.image, box=tile.position)

    def show(self):
        self.image.show()

    def save(self):
        self.image.save(path.join(path.dirname(__file__), f'mosaic_{self.tile_size}.jpg'))


class Tile:
    def __init__(self, image, position):
        self.image = image
        self.nparray = np.asarray(image)
        self.position = position  # Position of the tile in the mosaic

    # Get average color value of the tile
    def get_avg_color(self):
        # reds = np.dot(self.nparray, np.array((1, 0, 0)))
        # greens = np.dot(self.nparray, np.array((0, 1, 0)))
        # blues = np.dot(self.nparray, np.array((0, 0, 1)))
        # red = np.average(reds)
        # green = np.average(greens)
        # blue = np.average(blues)
        # return (int(red), int(green), int(blue))

        # mean = ImageStat.Stat(self.image).mean
        # return int(mean[0]), int(mean[1]), int(mean[2])

        return tuple(ImageStat.Stat(self.image).median)

    # For now replaces the tile with a blank image of its average color

    def replace_tile(self):
        self.image = Image.new('RGB', self.image.size, color=self.get_avg_color())
        self.nparray = np.asarray(self.image)

    def __repr__(self):
        return f'Tile at {self.position}, width: {self.image.size[0]}'


def main():
    mosaic = Mosaic('xlgddaexman21.jpg', 12)
    mosaic.split()
    mosaic.build_mosaic()
    mosaic.show()
    # stats = ImageStat.Stat(mosaic.image)
    # print(stats.median)
    # print(stats.mean)
    # print(stats.stddev)
    # print(stats.var)


if __name__ == '__main__':
    main()
