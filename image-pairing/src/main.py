from argparse import ArgumentParser
from os import listdir, path, mkdir
from cv2 import imread, imwrite, resize, INTER_AREA, hconcat
from data_manipulation import DataFrame, find_time_lapses
from split_results import train_test_split
from shutil import rmtree


def read_images_from_directory(input_directory):
    sub_directories = sorted(listdir(input_directory), key=len)
    images = []
    for image_sub_directory in sub_directories:
        current_directory_path = path.join(
            input_directory, image_sub_directory)
        current_image_list = sorted(listdir(current_directory_path), key=len)
        images.append([imread(path.join(current_directory_path, image))
                       for image in current_image_list])

    return images


def resize_images(images):
    # minimum_shape = min([image.shape[0:2]
    #                      for image_group in images for image in image_group])
    new_shape = (256, 256)
    resized_images = [[resize(image, new_shape, interpolation=INTER_AREA)
                       for image in image_group] for image_group in images]
    return resized_images


def save_results(images, input_directory, output_directory, data_frame,
                 train_test_ratio, range_mode, range_start, range_end):
    sub_directories = sorted(listdir(input_directory), key=len)
    resulting_data = []
    for index in range(len(sub_directories)):
        pairs = [[0, -1]]
        current_patient_ID = ""
        image_index = 0
        if data_frame:
            current_row = data_frame.access_row_by_index(index)
            current_patient_ID = current_row[0]
            pairs = find_time_lapses(
                current_row[1:],
                range_start, range_end, range_mode)
        for pair in pairs:
            result_image = hconcat(
                [images[index][pair[0]], images[index][pair[1]]])
            if data_frame:
                resulting_data.append([f"{current_patient_ID}-{image_index}.jpg", result_image])
            else:
                resulting_data.append([f"{image_index}.jpg", result_image])
            image_index += 1
    
    (train_data, test_data) = train_test_split(
        resulting_data, train_test_ratio)
    train_directory = path.join(output_directory, "train")
    test_directory = path.join(output_directory, "test")

    write_data(train_directory, train_data)
    write_data(test_directory, test_data)


def write_data(directory, data):
    create_directory(directory, delete_content=True)
    for element in data:
        imwrite(path.join(directory, element[0]), element[1])


def create_directory(directory, delete_content=False):
    if path.isdir(directory) and delete_content:
        rmtree(directory)
    if not path.isdir(directory):
        mkdir(directory)


parser = ArgumentParser()
parser.add_argument("-i", "--input", help="Input directory", required=True)
parser.add_argument("-o", "--output", help="Output directory", required=True)
parser.add_argument("-r", "--ratio", help="Train test ratio",
                    required=False, default=0.0)
parser.add_argument("-d", "--data", help="Data file in CSV format",
                    required=False)
parser.add_argument("-m", "--mode", help="How the range will be used (M for months, Y for years...)",
                    required=False, default="M")
parser.add_argument("-s", "--start", help="Start of the range to form image pairs",
                    required=False, default=0)
parser.add_argument("-e", "--end", help="End of the range to form image pairs",
                    required=False, default=12)

parsed_arguments = vars(parser.parse_args())
input_directory = str(parsed_arguments["input"])
output_directory = str(parsed_arguments["output"])
train_test_ratio = float(parsed_arguments["ratio"])
date_range_mode = str(parsed_arguments["mode"])
date_rage_start = float(parsed_arguments["start"])
date_rage_end = float(parsed_arguments["end"])



data_frame = ""
if parsed_arguments["data"]:
    data_frame = DataFrame(str(parsed_arguments["data"]))

create_directory(output_directory, delete_content=False)

images = read_images_from_directory(input_directory)
resized_images = resize_images(images)

save_results(resized_images, input_directory,
             output_directory, data_frame, train_test_ratio,
             date_range_mode, date_rage_start, date_rage_end)
