from cv2 import imread, split, merge, imwrite
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from math import atan2, pi, radians, sin, cos
from imutils import rotate
from argparse import ArgumentParser
from os import getcwd, path, mkdir
from json import load


def rotate_point(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
    qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
    return int(qx), int(qy)


def rotate_crop_show(p1, p2, l, path):
    gs = gridspec.GridSpec(2, 2)
    plt.figure()

    # vector que une los dos puntos
    v = (p2[0] - p1[0], p2[1] - p1[1])
    if (v[0] < 0):
        v = (p1[0] - p2[0], p1[1] - p2[1])

    # ángulo que forma ese vector con la horizontal
    ang = atan2(v[1], v[0])  # atan2(deltaY, deltaX)

    img = imread(path)
    plt.subplot(gs[0, 0])
    showImage(img)

    c = (p1[0], p1[1])
    w = img.shape[1]  # ancho de la imagen
    l = round(w * 0.37)

    bounding_rect = img[4: l,
                        4: l, :]
    plt.subplot(gs[0, 1])
    showImage(bounding_rect)

    # rotamos el ángulo inverso
    rot_img = rotate(bounding_rect, ang*180/pi)

    plt.subplot(gs[1, 0])
    showImage(rot_img)

    h = rot_img.shape[0]  # alto de la imagen
    w = rot_img.shape[1]  # ancho de la imagen
    c = (rotate_point([int(w/2), int(h/2)], c, radians(-ang*180/pi)))
    print(c)

    l = int(min(h, w) * 0.7)
    half_length = int(l/2)

    crop_img = rot_img[c[1] - half_length: c[1] + half_length,
                       c[0] - half_length: c[0] + half_length, :]
    # mostrar
    plt.subplot(gs[1, 1])
    showImage(crop_img)
    plt.show()


def rotate_crop(p1, p2, bouding_rect_side, final_window_side, path):
    v = (p2[0] - p1[0], p2[1] - p1[1])
    if (v[0] < 0):
        v = (p1[0] - p2[0], p1[1] - p2[1])

    ang = atan2(v[1], v[0])  # atan2(deltaY, deltaX)

    image = imread(path)

    c = (p1[0], p1[1])
    w = image.shape[1]
    length = round(w * bouding_rect_side)

    bounding_rect = image[0: length, 0: length, :]

    rotated_image = rotate(bounding_rect, ang*180/pi)

    h = rotated_image.shape[0]
    w = rotated_image.shape[1]
    c = (rotate_point([int(w/2), int(h/2)], c, radians(-ang*180/pi)))

    length = int(min(h, w) * final_window_side)
    half_length = int(length/2)
    cropped_image = rotated_image[c[1] - half_length: c[1] + half_length,
                                  c[0] - half_length: c[0] + half_length, :]
    return cropped_image


def showImage(img):
    b, g, r = split(img)
    frame_rgb = merge((r, g, b))
    plt.imshow(frame_rgb)


def parse_click(click_data):
    return [click_data["x"], click_data["y"]]


def save_image(image, image_path, output_directory):
    current_directory_name = path.split(path.dirname(image_path))[1]
    current_directory_path = path.join(
        output_directory, current_directory_name)
    if not path.isdir(current_directory_path):
        mkdir(current_directory_path)
    image_name = path.split(path.splitext(image_path)[0])[1]
    image_name += ".jpg"
    current_image_path = path.join(current_directory_path, image_name)
    imwrite(current_image_path, image)


# Argument Parsing
parser = ArgumentParser()
parser.add_argument(
    "-s", "--size", help="Side size of the final square window", required=True)
parser.add_argument(
    "-b", "--bounding", help="Side size of the initial bounding rect", required=True)
parser.add_argument("-o", "--output", help="Output directory", required=True)

parser.add_argument("clicks data", default=getcwd(),
                    help="Json file with the clicks data from the files")
parsed_arguments = vars(parser.parse_args())
file_path = parsed_arguments["clicks data"]
# square_size = int(parsed_arguments["size"]) if parsed_arguments["size"] else 425
square_size = float(parsed_arguments["size"])
bounding_rect_size = float(parsed_arguments["bounding"])
output_directory = str(parsed_arguments["output"])
if not path.isdir(output_directory):
    mkdir(output_directory)
file = open(file_path)
data_read = load(file)

for image_info in data_read:
    first_click = parse_click(image_info[0])
    second_click = parse_click(image_info[1])
    image_path = image_info[-1]
    # rotate_crop_show(first_click, second_click, square_size, image_path)
    resulting_image = rotate_crop(
        first_click, second_click, square_size, bounding_rect_size, image_path)
    save_image(resulting_image, image_path, output_directory)

file.close()

# rotate_crop_show((309, 298), (22, 265), 350,
#                   "C:\\Users\\usuario\\Downloads\\GCL\\22\\1.tif")
# rotate_crop_show((312,302), (23,285), 425, "C:\\Users\\usuario\\Downloads\\GCL\\107\\1.tif")
# rotate_crop_show((303, 296), (573, 263), 350,
#                   "C:\\Users\\usuario\\Downloads\\GCL\\10\\1g.tif")
# rotate_crop_show((235, 228), (459, 185), 350,
#                   "C:\\Users\\usuario\\Downloads\\GCL\\448\\2.jpg")
